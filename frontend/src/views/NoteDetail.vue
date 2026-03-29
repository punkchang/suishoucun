<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, Skeleton, Button, Tag, Icon } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getNoteById } from '../api/notes'

const route = useRoute()
const router = useRouter()

// 响应式数据
const note = ref(null)
const loading = ref(true)
const error = ref(null)

// 加载笔记详情
onMounted(async () => {
  try {
    const data = await getNoteById(route.params.slug)
    note.value = data
  } catch (err) {
    error.value = err.message
    ElMessage.error(err.message || '加载笔记失败')
  } finally {
    loading.value = false
  }
})

// 返回列表
const goBack = () => {
  router.push('/')
}
</script>

<template>
  <div class="detail-container">
    <!-- 加载中 -->
    <Skeleton :loading="loading" animated>
      <div class="detail-content">
        <!-- 返回按钮 -->
        <button class="back-btn" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </button>

        <!-- 笔记内容 -->
        <div v-if="note && !error" class="note-wrapper">
          <!-- 标题 -->
          <h1 class="note-title">{{ note.title }}</h1>

          <!-- 元信息 -->
          <div class="note-meta">
            <span class="meta-item">📅 {{ note.updated || '刚刚' }}</span>
            
            <!-- 标签 -->
            <div class="tags-container">
              <el-tag 
                v-for="tag in note.tags" 
                :key="tag"
                size="small"
                :type="tag === '效率' ? 'success' : tag === '时间管理' ? 'warning' : ''"
              >
                #{{ tag }}
              </el-tag>
            </div>
          </div>

          <!-- 正文内容 -->
          <div class="note-content">
            {{ note.content }}
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-else-if="error" class="error-wrapper">
          <el-icon size="48" color="#909399"><Icon name="warning" /></el-icon>
          <p>{{ error }}</p>
          <button class="back-btn" @click="goBack">返回列表</button>
        </div>
      </div>
    </Skeleton>
  </div>
</template>

<style scoped>
.detail-container {
  min-height: 100vh;
  background: #fff;
  padding: 40px 20px;
}

.detail-content {
  max-width: 900px;
  margin: 0 auto;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #fff;
  border: 2px solid transparent;
  border-radius: 6px;
  font-size: 14px;
  color: #303133;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 30px;
  font-family: 'Georgia', 'Times New Roman', serif;
  letter-spacing: 2px;
}

.back-btn:hover {
  border-color: #000;
}

.note-wrapper {
  animation: fadeIn 0.4s ease-out;
}

.note-title {
  font-size: 38px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 24px;
  letter-spacing: 4px;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 24px;
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 30px;
}

.meta-item {
  color: #909399;
  font-size: 14px;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.tags-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.note-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
  white-space: pre-wrap;
  font-family: 'Georgia', 'Times New Roman', serif;
}

.error-wrapper {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
