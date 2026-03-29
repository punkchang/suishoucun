# 📚 个人知识库系统 (Knowledge Base)

基于 `wiki-local` 的个人知识管理工具，支持局域网访问。

## 🎯 项目简介

这是一个美观、易用的个人知识库 Web 应用，用于记录和管理日常生活/工作中的经验总结。

**核心特性：**
- ✅ 全文检索（标题 + 正文 + 标签）
- ✅ 自动链接相关文章
- ✅ Markdown 格式存储（完全本地化）
- ✅ 局域网访问（192.168.119.129:3000）

## 📁 项目结构

```
knowledge-base/
├── data/
│   └── wiki/
│       ├── articles/      # Markdown 文章存储
│       └── index.json     # JSON 索引文件
├── api/                   # FastAPI 后端服务
├── frontend/              # Vue3 前端项目
├── docs/                  # 使用文档
└── README.md             # 本说明文件
```

## 🚀 快速启动（待开发完成后）

### 1. 启动后端 API
```bash
cd api
uvicorn server:app --host 192.168.119.129 --port 8000
```

### 2. 启动前端界面
```bash
cd frontend
npm run dev -- --host 192.168.119.129 --port 3000
```

### 3. 访问 Web UI
浏览器打开：`http://192.168.119.129:3000`

## 📊 数据备份

所有笔记都存储在 `data/wiki/` 目录下，建议定期备份：

```bash
# 方式一：Git 版本控制（推荐）
git add .
git commit -m "Backup at $(date)"

# 方式二：手动复制整个 data 目录
cp -r data ~/backup/knowledge-base-data-$(date +%Y%m%d)
```

## 🛠️ 技术栈

- **后端：** Python FastAPI + Node.js (wiki-local.js)
- **前端：** Vue.js 3 + Element Plus
- **存储：** Markdown + JSON（完全本地化）
- **部署：** Uvicorn + Vite Dev Server

---

**开发状态：** 🚧 开发中  
**创建时间：** 2026-03-29  
**开发者：** 灵犀 (OpenClaw Agent)
