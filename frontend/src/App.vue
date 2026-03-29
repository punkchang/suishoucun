<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElCard, ElTag, ElSkeleton, ElPagination } from 'element-plus'
import LayoutHeader from './components/LayoutHeader.vue'
import SidebarNav from './components/SidebarNav.vue'
import { getNotes } from './api/notes'

const router = useRouter()
const searchQuery = ref('')
const notes = ref([])
const loading = ref(true)

// 分页状态
const currentPage = ref(1)
const pageSize = ref(5)
const total = ref(0)

// 加载笔记列表（支持分页）
const loadNotes = async (page = 1, size = pageSize.value) => {
  if (!searchQuery.value) {
    loading.value = true
    try {
      const response = await getNotes(size, (page - 1) * size)
      notes.value = response.notes || []
      total.value = response.total || 0
      currentPage.value = page
    } catch (err) {
      ElMessage.error(err.message || '加载笔记失败')
      console.error('Failed to load notes:', err)
      notes.value = []
    } finally {
      loading.value = false
    }
  } else {
    // 搜索模式下前端过滤（暂时）
    const allData = await getNotes(100, 0)
    const filtered = allData.filter(note => 
      note.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (note.content && note.content.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      note.tags.some(tag => tag.includes(searchQuery.value))
    )
    notes.value = filtered.slice(0, size)
    total.value = filtered.length
  }
}

onMounted(() => {
  loadNotes()
})

// 分页改变
const handlePageChange = (page) => {
  loadNotes(page)
}

// 每页数量改变
const handleSizeChange = (size) => {
  pageSize.value = size
  loadNotes(1, size)
}

// 搜索功能
const handleSearch = async (query) => {
  searchQuery.value = query
  currentPage.value = 1
  
  if (!query) {
    await loadNotes(1, pageSize.value)
    return
  }
  
  ElMessage.info(`正在搜索 "${query}"...`)
  await loadNotes(1, pageSize.value)
}

// 新建笔记
const handleNewNote = () => {
  ElMessage.info('新建笔记功能开发中...')
}

// 导出功能
const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 分类点击
const handleCategoryClick = (category) => {
  ElMessage.info(`切换到分类：${category}`)
}

// 标签点击（前端过滤）
const handleTagClick = (tag) => {
  const filtered = notes.value.filter(note => 
    note.tags.includes(tag)
  )
  
  if (filtered.length === 0) {
    ElMessage.info(`暂无 "${tag}" 标签的笔记`)
  } else {
    ElMessage.success(`找到 ${filtered.length} 篇相关笔记`)
  }
}

// 打开笔记（路由跳转）
const openNote = (note) => {
  router.push(`/note/${note.slug}`)
}
</script>

<template>
  <div class="app-container">
    <!-- 顶部栏 -->
    <LayoutHeader 
      :search-query="searchQuery"
      @update-search="handleSearch"
      @new-note="handleNewNote"
      @export="handleExport"
    />

    <div class="main-layout">
      <!-- 侧边栏 -->
      <SidebarNav 
        @category-click="handleCategoryClick"
        @tag-click="handleTagClick"
      />

      <!-- 主内容区 -->
      <main class="content-area">
        <div class="content-wrapper">
          <!-- 页面标题 -->
          <div class="page-header">
            <h2 class="page-title">
              笔记列表
              <el-tag type="info" size="small">{{ total }} 篇</el-tag>
            </h2>
          </div>

          <!-- 加载中骨架屏 -->
          <el-skeleton :loading="loading" animated text rows="6">
            <!-- 笔记卡片网格 -->
            <div class="notes-grid">
              <el-card 
                v-for="note in notes" 
                :key="note.slug"
                shadow="hover"
                class="note-card"
                @click="openNote(note)"
              >
                <template #header>
                  <div class="card-header">
                    <span class="card-title">{{ note.title }}</span>
                  </div>
                </template>

                <!-- 内容摘要（显示前 100 字） -->
                <p class="card-content">
                  {{ note.content || '暂无详细内容' }}
                </p>

                <!-- 标签 -->
                <div class="card-tags">
                  <el-tag 
                    v-for="tag in note.tags" 
                    :key="tag"
                    size="small"
                    :type="tag === '效率' ? 'success' : tag === '时间管理' ? 'warning' : ''"
                  >
                    #{{ tag }}
                  </el-tag>
                </div>

                <!-- 更新时间 -->
                <div class="card-meta">
                  📅 {{ note.updated || '刚刚' }}
                </div>
              </el-card>
            </div>
          </el-skeleton>

          <!-- 分页组件 -->
          <div v-if="!loading && total > 0" class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[5, 10, 20, 50]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>

          <!-- 空状态提示 -->
          <div v-if="!loading && total === 0" class="empty-state">
            <p>暂无笔记，点击"新建笔记"开始记录</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body, html {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.content-area {
  flex: 1;
  background: #fff;
  overflow-y: auto;
}

.content-wrapper {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  margin: 0;
  font-size: 34px;
  color: #303133;
  font-weight: 600;
  letter-spacing: 8px;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  justify-content: center;
}

.note-card {
  cursor: pointer;
  transition: all 0.3s;
  height: fit-content;
}

.note-card:hover {
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-title {
  font-weight: 400;
  font-size: 16px;
  color: #303133;
  letter-spacing: 2px;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.card-content {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.card-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.card-meta {
  color: #909399;
  font-size: 12px;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
  font-family: 'Georgia', 'Times New Roman', serif;
}

/* 分页容器样式 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 32px;
  padding-bottom: 24px;
}

:deep(.el-pagination) {
  --el-pagination-bg-color: #fff;
  --el-pagination-text-color: #606266;
}

:deep(.el-pagination .el-pager li) {
  border-radius: 4px;
  margin: 0 4px;
  transition: all 0.3s;
}

:deep(.el-pagination .el-pager li:hover) {
  color: #000;
  background-color: #f5f7fa;
}

:deep(.el-pagination .el-pager li.is-active) {
  background-color: #000 !important;
  color: #fff !important;
}

:deep(.el-pagination button:hover) {
  color: #000;
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #909399;
}
</style>
