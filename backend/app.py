from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, and_
from datetime import datetime, timedelta, date
from apscheduler.schedulers.background import BackgroundScheduler
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Set up logging for anomaly detection
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置CORS，允许前端访问后端并携带凭证
CORS(app, supports_credentials=True, origins=['http://localhost:8080'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    poops = db.Column(db.Integer, default=0)
    monthly_poops = db.Column(db.Integer, default=0)  # 新增：记录每月排便数
    is_flagged = db.Column(db.Boolean, default=False)  # 标记异常用户
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PoopRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_suspicious = db.Column(db.Boolean, default=False)  # 标记可疑记录
    ip_address = db.Column(db.String(45))  # 记录IP地址用于异常检测
    
    user = db.relationship('User', backref=db.backref('poop_records', lazy=True))

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_count = db.Column(db.Integer, default=0)
    record_count = db.Column(db.Integer, default=0)  # 记录次数
    
    user = db.relationship('User', backref=db.backref('daily_stats', lazy=True))
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='_user_date_uc'),)

# 异常检测函数
def detect_anomalies(user_id, poop_count, ip_address):
    """
    检测异常行为并返回是否可疑及原因
    """
    today = date.today()
    current_time = datetime.utcnow()
    
    # 检查今日总数是否超过合理范围
    today_records = PoopRecord.query.filter(
        PoopRecord.user_id == user_id,
        func.date(PoopRecord.timestamp) == today
    ).all()
    
    today_total = sum([record.count for record in today_records])
    
    # 异常检测规则
    anomalies = []
    
    # 1. 单日超过8次明显异常
    if today_total + poop_count > 8:
        anomalies.append("单日记录超过8次，可能异常")
    
    # 2. 单次记录超过3次
    if poop_count > 3:
        anomalies.append("单次记录超过3次，不合理")
    
    # 3. 5分钟内记录超过2次
    five_minutes_ago = current_time - timedelta(minutes=5)
    recent_records = PoopRecord.query.filter(
        PoopRecord.user_id == user_id,
        PoopRecord.timestamp >= five_minutes_ago
    ).all()
    recent_count = sum([record.count for record in recent_records])
    
    if recent_count + poop_count > 2:
        anomalies.append("5分钟内记录超过2次")
    
    # 4. 1小时内记录超过4次
    one_hour_ago = current_time - timedelta(hours=1)
    hourly_records = PoopRecord.query.filter(
        PoopRecord.user_id == user_id,
        PoopRecord.timestamp >= one_hour_ago
    ).all()
    hourly_count = sum([record.count for record in hourly_records])
    
    if hourly_count + poop_count > 4:
        anomalies.append("1小时内记录超过4次")
    
    # 5. 检查频繁记录模式（连续多天异常高频）
    week_ago = today - timedelta(days=7)
    week_stats = DailyStats.query.filter(
        DailyStats.user_id == user_id,
        DailyStats.date >= week_ago
    ).all()
    
    high_frequency_days = [stat for stat in week_stats if stat.total_count > 6]
    if len(high_frequency_days) >= 3:
        anomalies.append("一周内多日高频记录，异常模式")
    
    return len(anomalies) > 0, anomalies

def update_daily_stats(user_id, poop_count, record_date=None):
    """
    更新每日统计数据
    """
    if record_date is None:
        record_date = date.today()
    
    daily_stat = DailyStats.query.filter_by(
        user_id=user_id, 
        date=record_date
    ).first()
    
    if not daily_stat:
        daily_stat = DailyStats(
            user_id=user_id,
            date=record_date,
            total_count=0,
            record_count=0
        )
        db.session.add(daily_stat)
    
    daily_stat.total_count += poop_count
    daily_stat.record_count += 1
    
    return daily_stat

# 注册API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功!欢迎来到Poop Battle！'}), 201

# 登录API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'message': '欢迎回来','username':username,'user_id':user.id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# 注销API
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': '会想你的！'}), 200

# 修改昵称API
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    new_username = data.get('new_username')
    user = db.session.get(User, session['user_id'])
    if user:
        user.username = new_username
        db.session.commit()
        return jsonify({'message': '换名字啦！'}), 200
    return jsonify({'message': 'User not found'}), 404

# 记录💩数API
@app.route('/record_poop', methods=['POST'])
def record_poop():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    poop_count = data.get('poop_count')
    user = User.query.get(session['user_id'])
    ip_address = request.remote_addr

    # 处理撤回操作
    if poop_count == -1:  # 约定poop_count为-1时表示撤回上一次记录
        today = date.today()
        last_record = PoopRecord.query.filter(
            PoopRecord.user_id == user.id,
            func.date(PoopRecord.timestamp) == today
        ).order_by(PoopRecord.timestamp.desc()).first()
        
        if last_record:
            # 更新用户统计
            user.poops -= last_record.count
            user.monthly_poops -= last_record.count
            
            # 更新每日统计
            daily_stat = DailyStats.query.filter_by(
                user_id=user.id, 
                date=today
            ).first()
            if daily_stat:
                daily_stat.total_count -= last_record.count
                daily_stat.record_count -= 1
                if daily_stat.total_count <= 0:
                    db.session.delete(daily_stat)
            
            db.session.delete(last_record)
            db.session.commit()
            
            logger.info(f"User {user.username} reverted record: {last_record.count} poops")
            return jsonify({'message': '上一次记录已撤回'}), 200
        else:
            return jsonify({'message': '今天没有可撤回的记录'}), 400

    # 基本输入验证
    if not isinstance(poop_count, int) or poop_count < 0 or poop_count > 10:
        return jsonify({'message': '记录数值不合理'}), 400

    # 运行异常检测
    is_suspicious, anomaly_reasons = detect_anomalies(user.id, poop_count, ip_address)
    
    # 如果检测到异常，拒绝记录并记录日志
    if is_suspicious:
        logger.warning(f"Suspicious activity detected for user {user.username}: {', '.join(anomaly_reasons)}")
        
        # 标记用户为可疑
        if len(anomaly_reasons) >= 2:  # 多项异常时标记用户
            user.is_flagged = True
            db.session.commit()
        
        return jsonify({
            'message': '记录被拒绝：' + ', '.join(anomaly_reasons),
            'is_suspicious': True,
            'reasons': anomaly_reasons
        }), 400

    # 更新用户的排便数和每月排便数
    user.poops += poop_count
    user.monthly_poops += poop_count

    # 记录本次排便
    new_record = PoopRecord(
        user_id=user.id, 
        count=poop_count,
        is_suspicious=is_suspicious,
        ip_address=ip_address
    )
    db.session.add(new_record)
    
    # 更新每日统计
    update_daily_stats(user.id, poop_count)
    
    db.session.commit()
    
    logger.info(f"User {user.username} recorded {poop_count} poops")
    return jsonify({'message': f'{poop_count} poops recorded!'}), 200

# 获取用户每日统计数据
@app.route('/daily_stats', methods=['GET'])
def get_daily_stats():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    # 获取查询参数
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # 默认获取最近30天的数据
    if not end_date_str:
        end_date = date.today()
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    if not start_date_str:
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    user_id = session['user_id']
    
    # 查询每日统计数据
    daily_stats = DailyStats.query.filter(
        DailyStats.user_id == user_id,
        DailyStats.date >= start_date,
        DailyStats.date <= end_date
    ).order_by(DailyStats.date).all()
    
    # 生成完整的日期范围数据（包括没有记录的日期）
    stats_dict = {stat.date.isoformat(): {
        'date': stat.date.isoformat(),
        'total_count': stat.total_count,
        'record_count': stat.record_count
    } for stat in daily_stats}
    
    current_date = start_date
    complete_stats = []
    while current_date <= end_date:
        date_str = current_date.isoformat()
        if date_str in stats_dict:
            complete_stats.append(stats_dict[date_str])
        else:
            complete_stats.append({
                'date': date_str,
                'total_count': 0,
                'record_count': 0
            })
        current_date += timedelta(days=1)
    
    return jsonify({
        'daily_stats': complete_stats,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }), 200

# 获取月度统计概览
@app.route('/monthly_overview', methods=['GET'])
def get_monthly_overview():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    year = request.args.get('year', default=date.today().year, type=int)
    month = request.args.get('month', default=date.today().month, type=int)
    
    # 获取指定月份的统计数据
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)
    
    monthly_stats = DailyStats.query.filter(
        DailyStats.user_id == user_id,
        DailyStats.date >= month_start,
        DailyStats.date <= month_end
    ).all()
    
    total_poops = sum(stat.total_count for stat in monthly_stats)
    total_days_recorded = len(monthly_stats)
    average_per_day = round(total_poops / max(total_days_recorded, 1), 2)
    
    # 获取详细记录用于分析
    records = PoopRecord.query.filter(
        PoopRecord.user_id == user_id,
        func.extract('year', PoopRecord.timestamp) == year,
        func.extract('month', PoopRecord.timestamp) == month
    ).all()
    
    return jsonify({
        'year': year,
        'month': month,
        'total_poops': total_poops,
        'days_recorded': total_days_recorded,
        'average_per_day': average_per_day,
        'total_records': len(records),
        'month_start': month_start.isoformat(),
        'month_end': month_end.isoformat()
    }), 200

# 新增：排行榜API
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    current_month = datetime.utcnow().month
    users = db.session.query(User).join(PoopRecord, User.id == PoopRecord.user_id).filter(
        func.extract('month', PoopRecord.timestamp) == current_month
    ).order_by(User.monthly_poops.desc()).all()
    leaderboard_data = [
        {
            'username': user.username,
            'monthly_poops': user.monthly_poops
        }
        for user in users
    ]
    return jsonify(leaderboard_data), 200

#获取用户的所有历史poop记录API
@app.route('/poop_history', methods=['GET'])
def poop_history():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user = db.session.get(User, session['user_id'])
    if user:
        records = PoopRecord.query.filter_by(user_id=user.id).order_by(PoopRecord.timestamp.desc()).all()
        history = [
            {
                'count': record.count,
                'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for record in records
        ]
        return jsonify(history), 200
    return jsonify({'message': 'User not found'}), 404


# 首页获取用户信息和poop数API
@app.route('/user_info', methods=['GET'])
def get_user_info():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user = db.session.get(User, session['user_id'])
    if user:
        return jsonify({
            'username': user.username,
            'poop_count': user.poops
        }), 200
    return jsonify({'message': 'User not found'}), 404


# 新增：每月重置任务
def reset_monthly_poops():
    with app.app_context():
        users = User.query.all()
        for user in users:
            user.monthly_poops = 0
        db.session.commit()

# 启动定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(func=reset_monthly_poops, trigger='cron', day=1, hour=0, minute=0)
scheduler.start()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
