<template>
  <div class="note-detail">
    <!-- 顶部操作栏 -->
    <div class="detail-header">
      <el-button @click="$router.back()" icon="ArrowLeft" circle />
      <span class="back-text">返回列表</span>
      
      <div class="action-buttons">
        <template v-if="isEditMode">
          <el-button @click="cancelEdit" plain>取消</el-button>
          <el-button @click="saveNote" type="primary" :loading="saving">保存</el-button>
        </template>
        <el-button v-else @click="enterEditMode" icon="Edit" type="primary">编辑</el-button>
      </div>
    </div>

    <!-- 编辑模式 -->
    <div v-if="isEditMode" class="edit-mode">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="editForm.title" placeholder="请输入笔记标题" size="large" />
        </el-form-item>

        <el-form-item label="内容">
          <el-input 
            v-model="editForm.content" 
            type="textarea" 
            :rows="20" 
            placeholder="# 在这里写 Markdown 内容..."
            resize="vertical"
          />
        </el-form-item>

        <el-form-item label="标签">
          <div class="tag-input-container">
            <el-tag 
              v-for="(tag, index) in editForm.tags" 
              :key="index" 
              closable 
              @close="removeTag(index)"
              size="large"
              style="margin-right: 8px;"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-if="tagInputVisible"
              ref="tagInputRef"
              v-model="newTag"
              size="small"
              @keyup.enter="addTag"
              @blur="addTag"
              placeholder="输入标签后按回车"
            />
            <el-button 
              v-else 
              @click="showTagInput" 
              type="primary" 
              size="small"
              link
            >
              + 添加标签
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>

    <!-- 阅读模式 -->
    <div v-else class="read-mode">
      <template v-if="note">
        <h1 class="note-title">{{ note.title }}</h1>
        
        <div class="note-meta">
          <span><el-icon><Calendar /></el-icon> {{ formatDate(note.createdAt) }}</span>
          <span v-if="note.updatedAt && note.updatedAt !== note.createdAt">
            <el-icon><Clock /></el-icon> 更新于 {{ formatDate(note.updatedAt) }}
          </span>
          <span><el-icon><Link /></el-icon> {{ note.backlinks?.length || 0 }} 个反向链接</span>
        </div>

        <div class="note-tags" v-if="note.tags && note.tags.length">
          <el-tag 
            v-for="tag in note.tags" 
            :key="tag" 
            type="info" 
            size="small"
            style="margin-right: 6px;"
          >
            #{{ tag }}
          </el-tag>
        </div>

        <div class="note-content" v-html="renderedContent"></div>

        <!-- 反向链接区域（预留） -->
        <div class="backlinks-section" v-if="note.backlinks && note.backlinks.length">
          <h3>🔗 反向链接</h3>
          <el-card shadow="hover" v-for="link in note.backlinks" :key="link.slug" class="backlink-item">
            <router-link :to="`/wiki/${link.slug}`">{{ link.title }}</router-link>
          </el-card>
        </div>
      </template>

      <el-empty v-else description="笔记不存在或已删除" />
    </div>

    <!-- 加载状态 -->
    <el-skeleton :loading="loading" :rows="10" animated />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import markdownit from 'markdown-it'
import hljs from 'highlight.js'
import { Calendar, Clock, Link, Edit } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 状态管理
const slug = route.params.slug
const loading = ref(false)
const saving = ref(false)
const isEditMode = ref(false)
const note = ref(null)
const editForm = ref({
  title: '',
  content: '',
  tags: []
})

// 标签输入相关
const tagInputVisible = ref(false)
const newTag = ref('')
const tagInputRef = ref(null)

// Markdown 渲染器
const md = markdownit({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre><code class="hljs">' + 
               hljs.highlight(str, { language: lang }).value + 
               '</code></pre>'
      } catch (_) {}
    }
    return '<pre><code class="hljs">' + md.utils.escapeHtml(str) + '</code></pre>'
  }
})

const renderedContent = computed(() => {
  if (!note.value || !note.value.content) return ''
  return md.render(note.value.content)
})

// API 调用
const fetchNote = async () => {
  loading.value = true
  try {
    const res = await fetch(`/api/wiki/${slug}`)
    if (!res.ok) throw new Error('获取笔记失败')
    note.value = await res.json()
    
    // 初始化编辑表单
    editForm.value = {
      title: note.value.title || '',
      content: note.value.content || '',
      tags: [...(note.value.tags || [])]
    }
  } catch (error) {
    ElMessage.error(error.message || '获取笔记失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const saveNote = async () => {
  if (!editForm.value.title.trim()) {
    ElMessage.warning('请输入笔记标题')
    return
  }

  saving.value = true
  try {
    console.log('[saveNote] 开始保存，slug:', slug)
    console.log('[saveNote] 编辑表单数据:', editForm.value)
    
    const res = await fetch(`/api/wiki/${slug}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm.value)
    })

    console.log('[saveNote] 响应状态:', res.status, res.statusText)
    
    const responseText = await res.text()
    console.log('[saveNote] 原始响应:', responseText)
    
    if (!res.ok) {
      let errorMsg = '保存失败'
      try {
        const errorData = JSON.parse(responseText)
        errorMsg = errorData.detail || errorData.error || errorMsg
      } catch {}
      throw new Error(errorMsg)
    }
    
    ElMessage.success('笔记已保存')
    isEditMode.value = false
    await fetchNote() // 重新获取最新数据
  } catch (error) {
    console.error('[saveNote] 错误:', error)
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 编辑模式切换
const enterEditMode = () => {
  isEditMode.value = true
  // 确保表单数据是最新的
  if (note.value) {
    editForm.value = {
      title: note.value.title || '',
      content: note.value.content || '',
      tags: [...(note.value.tags || [])]
    }
  }
}

const cancelEdit = () => {
  isEditMode.value = false
  // 恢复原始数据
  if (note.value) {
    editForm.value = {
      title: note.value.title || '',
      content: note.value.content || '',
      tags: [...(note.value.tags || [])]
    }
  }
}

// 标签操作
const showTagInput = () => {
  tagInputVisible.value = true
  nextTick(() => {
    tagInputRef.value?.focus()
  })
}

const addTag = () => {
  const tag = newTag.value.trim().replace(/^#/, '')
  if (tag && !editForm.value.tags.includes(tag)) {
    editForm.value.tags.push(tag)
  }
  newTag.value = ''
  tagInputVisible.value = false
}

const removeTag = (index) => {
  editForm.value.tags.splice(index, 1)
}

// 工具函数
const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 生命周期
onMounted(() => {
  fetchNote()
})
</script>

<style scoped>
.note-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.back-text {
  margin-left: 12px;
  color: #606266;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

/* 编辑模式 */
.edit-mode {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 阅读模式 */
.read-mode {
  background: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.note-title {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 15px;
  line-height: 1.4;
}

.note-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 13px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.note-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.note-tags {
  margin-bottom: 30px;
}

.note-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.note-content h1, 
.note-content h2, 
.note-content h3, 
.note-content h4 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.4;
}

.note-content p {
  margin-bottom: 16px;
}

.note-content code {
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9em;
}

.note-content pre {
  background-color: #282c34;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 16px;
}

.note-content pre code {
  background-color: transparent;
  padding: 0;
  color: #abb2bf;
}

.note-content blockquote {
  border-left: 4px solid #409eff;
  padding-left: 16px;
  margin: 16px 0;
  color: #606266;
  background-color: #f5f7fa;
  padding: 12px 16px;
  border-radius: 4px;
}

.note-content ul, 
.note-content ol {
  padding-left: 24px;
  margin-bottom: 16px;
}

.note-content table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
}

.note-content th, 
.note-content td {
  border: 1px solid #dcdfe6;
  padding: 12px;
  text-align: left;
}

.note-content th {
  background-color: #f5f7fa;
  font-weight: 600;
}

/* 反向链接 */
.backlinks-section {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 2px solid #ebeef5;
}

.backlinks-section h3 {
  margin-bottom: 20px;
  color: #303133;
}

.backlink-item {
  margin-bottom: 12px;
  transition: all 0.3s;
}

.backlink-item:hover {
  transform: translateX(4px);
}

.backlink-item a {
  color: #409eff;
  text-decoration: none;
  font-size: 15px;
}

.backlink-item a:hover {
  text-decoration: underline;
}

/* 标签输入容器 */
.tag-input-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
