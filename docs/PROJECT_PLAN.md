# 📋 个人知识库项目开发计划

## ✅ Phase 1: Vue3 + Vite 初始化（已完成）

**完成时间：** 2026-03-29 18:22  
**成果：**
- ✅ 项目脚手架搭建（Vue 3 + Vite 8.0.3）
- ✅ Element Plus UI 库集成
- ✅ @element-plus/icons-vue 图标库安装
- ✅ vite.config.js 配置（端口 3000，API 代理 localhost:8002）

---

## ✅ Phase 2: 布局框架搭建（已完成）

**完成时间：** 2026-03-29 20:21  
**成果：**

### 顶部导航栏 (LayoutHeader.vue)
- "收藏夹"标题（Georgia/Times 艺术字体，加粗）
- 居中搜索框（黑边框，无图标，文字居中对齐）
- 新建笔记/导出按钮（对齐边栏右边界 304px，hover 显示黑色边框）

### 左侧边栏 (SidebarNav.vue)
- **分类导航菜单**：全部笔记 + 技术/学习/效率/生活（无 emoji）
- **标签云区域**：示例标签展示
- **反向链接列表**：点击选中保持黑框，hover 显示黑框
- **一级标题 hover 效果**：分类导航/标签云/相关笔记鼠标停留出现黑框

### 主内容区 (App.vue)
- "笔记列表"标题居中（34px 艺术字体，字间距 8px）
- 响应式卡片网格布局（`justify-content: center`）
- 卡片样式：标题/正文/更新时间统一使用 Georgia/Times 衬线体
- 完整样式系统（滚动条美化、hover 动画）

### 整体视觉风格
- ✅ 三区域白色一体化设计（无分割线，无缝衔接）
- ✅ 统一艺术字体体系（Georgia/Times New Roman serif）
- ✅ 极简黑框交互反馈（hover/选中状态）

---

## 🚧 Phase 3: 动态数据加载与 API 对接（进行中）

**目标：** 打通前后端数据流，实现基础的笔记增删改查  
**预计时间：** 1.5-2 小时

### TODO List

#### 1. 创建 API 服务层 (`src/api/notes.js`) ⭐
- [ ] 封装笔记 CRUD 接口：
  - `getNotes()` - 获取所有笔记列表
  - `getNoteById(id)` - 获取单条笔记详情
  - `createNote(data)` - 新建笔记
  - `updateNote(id, data)` - 更新笔记
  - `deleteNote(id)` - 删除笔记
- [ ] 使用 axios/fetch 统一请求处理
- [ ] 错误处理和 loading 状态管理

#### 2. 重构 App.vue 为动态数据驱动 ⭐⭐
- [ ] 替换模拟数据为真实 API 调用
- [ ] 添加 loading/skeleton 骨架屏（Element Plus）
- [ ] 实现笔记列表刷新机制（手动刷新按钮）
- [ ] 错误提示（ElMessage 反馈）

#### 3. 创建笔记详情页面 ⭐⭐
- [ ] 新建 `src/views/NoteDetail.vue`
- [ ] 点击卡片跳转到详情页（使用 Vue Router）
- [ ] 显示完整笔记内容（标题、正文、标签、更新时间）
- [ ] "返回列表"按钮功能
- [ ] 编辑/删除操作入口

#### 4. 新建笔记表单弹窗 ⭐⭐
- [ ] 使用 Element Plus Dialog 组件
- [ ] 表单字段：
  - 标题输入框（el-input，必填）
  - 正文内容区（**先用 textarea，暂不引入 Markdown 编辑器**）
  - 标签选择器（el-select，支持多选/自定义）
  - 分类选择（下拉单选）
- [ ] 保存/取消操作逻辑

#### 5. 后端 API 对接测试 ⭐⭐⭐
- [ ] 检查 FastAPI 服务是否运行（localhost:8002）
- [ ] CORS 配置验证（允许前端跨域访问）
- [ ] 数据格式联调（请求/响应结构对齐）
- [ ] 错误码处理统一

---

## 📅 Phase 4: Markdown 编辑器集成（规划中）

**目标：** 提升笔记编辑体验，支持富文本格式  
**预计时间：** 2-3 小时

### 技术方案选择（待评估）
- **方案 A:** `@toast-ui/editor` - 功能完整，所见即所得 + Markdown 源码切换
- **方案 B:** `markdown-it` + 自定义 UI - 轻量级，自己实现预览分栏
- **方案 C:** `vue3-markdown-editor` - Vue 专用封装

### 功能清单（待定）
- [ ] 实时预览（左右分栏或弹窗预览）
- [ ] 代码高亮（集成 highlight.js / prism.js）
- [ ] 工具栏快捷操作（粗体、斜体、链接、图片等）
- [ ] Markdown 语法提示

---

## 🔮 Phase 5: 高级功能扩展（规划中）

**目标：** 完善知识库特性，提升使用体验

### 待开发功能
- [ ] 笔记全文搜索（Elasticsearch / 本地模糊匹配）
- [ ] 笔记关联推荐（基于标签/内容相似度）
- [ ] 导出功能（单个 Markdown / 批量 ZIP）
- [ ] 版本历史（Git 集成或简单快照）
- [ ] 主题切换（浅色/深色模式）

---

## 📊 项目状态总览

| 阶段 | 名称 | 状态 | 完成度 | 备注 |
|------|------|------|--------|------|
| Phase 1 | Vue3 + Vite 初始化 | ✅ 已完成 | 100% | - |
| Phase 2 | 布局框架搭建 | ✅ 已完成 | 100% | 视觉风格统一完成 |
| Phase 3 | 动态数据加载与 API 对接 | 🚧 进行中 | 0% | **当前重点** |
| Phase 4 | Markdown 编辑器集成 | ⏳ 规划中 | 0% | Phase 3 完成后启动 |
| Phase 5 | 高级功能扩展 | ⏳ 规划中 | 0% | 视需求优先级推进 |

---

## 🛠️ 技术栈总结

### 前端
- **框架:** Vue 3 (Composition API) + Vite 8.0.3
- **UI 库:** Element Plus + @element-plus/icons-vue
- **路由:** Vue Router（Phase 3 引入）
- **HTTP:** Axios（Phase 3 引入）
- **状态管理:** Pinia（可选，视复杂度决定）

### 后端
- **框架:** Python FastAPI
- **数据库:** SQLite / JSON 文件存储
- **部署:** Uvicorn ASGI Server

### 设计原则
- ✅ 极简主义视觉风格
- ✅ 白底一体化布局
- ✅ 艺术字体统一（Georgia/Times）
- ✅ 黑框交互反馈
- ✅ 渐进式功能迭代（先核心后高级）

---

**最后更新：** 2026-03-29 20:25  
**维护者：** 灵犀 (OpenClaw Agent)
