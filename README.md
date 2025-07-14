# Track-poop-Web

Keep track of our daily poop count with advanced anomaly detection and modern UI!

## 🎉 最新重构特性

- **🔒 强化异常检测系统**: 防止不合理数据（如一天记录10次以上）
- **📊 每日数据聚合**: 完整的统计分析和趋势监控
- **🎨 现代化界面设计**: 使用Element Plus组件和glassmorphism设计
- **📱 多端完美适配**: 支持手机、平板、桌面等各种设备
- **🛡️ 严谨后端逻辑**: 多层级数据验证和安全审计

## 快速开始

### 后端启动
```bash
cd backend
pip install flask flask-bcrypt flask-sqlalchemy flask-cors apscheduler
python app.py
```

### 前端启动
```bash
cd frontend
npm install
npm run serve
```

## 项目文档

详细的重构说明和API文档请参考 [REFACTOR_DOCUMENTATION.md](./REFACTOR_DOCUMENTATION.md)

## 技术栈

- **后端**: Flask + SQLAlchemy + 异常检测系统
- **前端**: Vue 3 + Element Plus + 响应式设计
- **数据库**: SQLite (开发) / PostgreSQL (生产推荐)
