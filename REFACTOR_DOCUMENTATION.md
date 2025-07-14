# Track-poop-Web 重构文档

## 项目概述

Track-poop-Web 是一个现代化的每日便便记录系统，经过全面重构后现在支持严谨的后端逻辑、多端适配以及现代化的用户界面。

## 重构主要改进

### 🔒 后端安全与数据完整性

#### 增强的异常检测系统
- **多层级验证**：实现了5层异常检测机制
  - 单日记录数量限制（>8次标记异常）
  - 单次记录合理性检查（>3次拒绝）
  - 短时间频率限制（5分钟内>2次）
  - 中期频率限制（1小时内>4次）
  - 长期模式分析（一周内3天以上高频记录）

#### 数据模型改进
```python
# 新增字段
class User(db.Model):
    is_flagged = db.Column(db.Boolean, default=False)  # 可疑用户标记
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PoopRecord(db.Model):
    is_suspicious = db.Column(db.Boolean, default=False)  # 可疑记录标记
    ip_address = db.Column(db.String(45))  # IP地址追踪

class DailyStats(db.Model):  # 新增日统计表
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)
    total_count = db.Column(db.Integer, default=0)
    record_count = db.Column(db.Integer, default=0)
```

#### 智能日志记录
- 所有异常行为自动记录到日志
- IP地址追踪支持安全审计
- 用户行为模式分析

### 📊 数据分析与统计

#### 新增API端点
1. **每日统计** (`/daily_stats`)
   - 支持日期范围查询
   - 自动填充缺失日期数据
   - 提供日历视图所需数据

2. **月度概览** (`/monthly_overview`)
   - 月度总计和平均值
   - 记录天数统计
   - 趋势分析数据

#### 数据聚合优化
- 实时更新每日统计
- 高效的数据库查询
- 缓存友好的数据结构

### 🎨 现代化前端界面

#### 设计风格
- **Glassmorphism（玻璃态）设计**：半透明背景、模糊效果
- **渐变背景**：动态色彩过渡
- **现代卡片布局**：阴影效果、圆角设计
- **响应式动画**：hover效果、过渡动画

#### 组件架构
```vue
<!-- 新增核心组件 -->
DailyDashboard.vue        # 每日概览仪表板
  ├── 月度统计卡片
  ├── 日历视图组件
  └── 最近记录时间线

HomePage.vue (重构)       # 主页面
  ├── 用户信息卡片
  ├── 快速记录区域
  ├── 今日统计快览
  └── 集成DailyDashboard
```

### 📱 多端适配支持

#### 响应式断点设计
```css
/* 桌面端 (>1200px) */
.sidebar { display: block; }
.record-buttons { grid-template-columns: repeat(4, 1fr); }

/* 平板端 (768px-1200px) */
.sidebar { display: none; }
.record-buttons { grid-template-columns: repeat(2, 1fr); }

/* 移动端 (<768px) */
.main-wrapper { padding: 10px; }
.record-buttons { grid-template-columns: 1fr; }
.user-header { flex-direction: column; }
```

#### 触控优化
- 按钮最小44px触控区域
- 手势友好的交互设计
- 移动端优化的表单控件

## 技术栈

### 后端技术
- **Flask** - 轻量级Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **Flask-CORS** - 跨域资源共享
- **APScheduler** - 定时任务调度
- **Bcrypt** - 密码安全加密

### 前端技术
- **Vue 3** - 现代JavaScript框架
- **Element Plus** - 企业级UI组件库
- **Axios** - HTTP客户端
- **CSS Grid/Flexbox** - 现代布局技术

## API文档

### 异常检测相关

#### POST /record_poop
记录便便数据，包含异常检测

**请求参数：**
```json
{
  "poop_count": 1  // 1-10之间的整数，-1表示撤回
}
```

**成功响应：**
```json
{
  "message": "1 poops recorded!"
}
```

**异常检测响应：**
```json
{
  "message": "记录被拒绝：单日记录超过8次，可能异常",
  "is_suspicious": true,
  "reasons": ["单日记录超过8次，可能异常", "单次记录超过3次，不合理"]
}
```

### 统计数据相关

#### GET /daily_stats
获取每日统计数据

**查询参数：**
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)

**响应示例：**
```json
{
  "daily_stats": [
    {
      "date": "2025-07-14",
      "total_count": 2,
      "record_count": 1
    }
  ],
  "start_date": "2025-06-14",
  "end_date": "2025-07-14"
}
```

#### GET /monthly_overview
获取月度统计概览

**查询参数：**
- `year`: 年份
- `month`: 月份

**响应示例：**
```json
{
  "year": 2025,
  "month": 7,
  "total_poops": 15,
  "days_recorded": 10,
  "average_per_day": 1.5,
  "total_records": 12
}
```

## 部署说明

### 开发环境

#### 后端启动
```bash
cd backend
pip install flask flask-bcrypt flask-sqlalchemy flask-cors apscheduler
python app.py
```

#### 前端启动
```bash
cd frontend
npm install
npm run serve
```

### 生产环境建议
- 使用WSGI服务器（如Gunicorn）部署Flask应用
- 配置Nginx作为反向代理
- 使用PostgreSQL替代SQLite
- 实施Redis缓存策略
- 配置HTTPS和安全头

## 安全特性

### 数据保护
- 密码Bcrypt加密存储
- SQL注入防护（SQLAlchemy ORM）
- CSRF保护（Flask内置）
- 异常行为监控和记录

### 隐私保护
- 最小化数据收集
- IP地址仅用于异常检测
- 用户数据本地存储

## 未来规划

### 功能扩展
- [ ] 用户偏好设置（主题、通知）
- [ ] 数据导出功能（CSV、PDF）
- [ ] 更丰富的数据可视化
- [ ] 多语言支持
- [ ] PWA支持（离线功能）

### 性能优化
- [ ] 数据库索引优化
- [ ] 前端代码分割
- [ ] 图片懒加载
- [ ] API响应缓存

### 监控与运维
- [ ] 系统监控仪表板
- [ ] 错误追踪集成
- [ ] 性能监控
- [ ] 自动化测试覆盖

## 故障排除

### 常见问题

**Q: 数据库错误 "no such column"**
A: 删除现有database.db文件，重启应用自动创建新表结构

**Q: 前端依赖安装失败**
A: 清理npm缓存：`npm cache clean --force`，然后重新安装

**Q: 异常检测过于严格**
A: 可在`app.py`中调整`detect_anomalies`函数的阈值参数

**Q: 移动端显示异常**
A: 确保视口meta标签正确配置，检查CSS媒体查询断点

### 调试技巧

1. **后端调试**：
   ```python
   # 在app.py中启用详细日志
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **前端调试**：
   ```javascript
   // 在浏览器控制台查看网络请求
   console.log('API Response:', response.data);
   ```

3. **数据库检查**：
   ```bash
   # 使用SQLite命令行工具
   sqlite3 backend/database.db
   .tables
   .schema user
   ```

## 贡献指南

### 代码规范
- Python代码遵循PEP 8标准
- JavaScript代码使用ESLint配置
- 提交信息使用约定式提交格式

### 开发流程
1. Fork项目仓库
2. 创建功能分支
3. 编写代码和测试
4. 提交Pull Request
5. 代码审查和合并

---

**版本**: 2.0.0  
**更新日期**: 2025-07-14  
**维护者**: Track Poop Web Team