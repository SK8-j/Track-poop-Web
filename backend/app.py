from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 配置CORS，允许前端访问后端并携带凭证
CORS(app, supports_credentials=True, origins=['http://localhost:8080'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    poops = db.Column(db.Integer, default=0)
    monthly_poops = db.Column(db.Integer, default=0)  # 新增：记录每月排便数

class PoopRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('poop_records', lazy=True))

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

    # 检查5分钟内的限制
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    recent_records = PoopRecord.query.filter(
        PoopRecord.user_id == user.id,
        PoopRecord.timestamp >= five_minutes_ago
    ).all()
    recent_count = sum([record.count for record in recent_records])
    if recent_count + poop_count > 2:
        return jsonify({'message': '5分钟内最多只能添加2个💩'}), 400

    # 检查一天内的限制
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    daily_records = PoopRecord.query.filter(
        PoopRecord.user_id == user.id,
        PoopRecord.timestamp >= one_day_ago
    ).all()
    daily_count = sum([record.count for record in daily_records])
    if daily_count + poop_count > 4:
        return jsonify({'message': '一天内最多只能添加4个💩'}), 400

    # 更新用户的排便数和每月排便数
    user.poops += poop_count
    user.monthly_poops += poop_count

    # 记录本次排便
    new_record = PoopRecord(user_id=user.id, count=poop_count)
    db.session.add(new_record)
    db.session.commit()

    return jsonify({'message': f'{poop_count} poops recorded!'}), 200

# 新增：排行榜API
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    current_month = datetime.utcnow().month
    users = User.query.filter(
        db.extract('month', PoopRecord.timestamp) == current_month
    ).order_by(User.monthly_poops.desc()).all()
    leaderboard_data = [
        {
            'username': user.username,
            'monthly_poops': user.monthly_poops
        }
        for user in users
    ]
    return jsonify(leaderboard_data), 200



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
