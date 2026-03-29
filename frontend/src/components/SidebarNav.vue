<script setup>
import { ref } from 'vue'
import { ElMenu, ElTag } from 'element-plus'

const categories = [
  { id: '1', name: '技术', icon: '' },
  { id: '2', name: '学习', icon: '' },
  { id: '3', name: '效率', icon: '' },
  { id: '4', name: '生活', icon: '' }
]

const backlinks = [
  { slug: 'pomodoro-technique', title: 'Pomodoro-Technique' },
  { slug: 'time-management', title: 'Time-Management' }
]

const tags = [
  { name: '效率', count: 2, color: '#409EFF' },
  { name: '时间管理', count: 1, color: '#67C23A' },
  { name: 'test', count: 1, color: '#E6A23C' }
]

const activeBacklink = ref(null)

const emit = defineEmits(['category-click', 'tag-click'])

const handleBacklinkClick = (slug) => {
  activeBacklink.value = slug
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-content">
      <!-- 分类导航 -->
      <div class="section">
        <h3 class="section-title">
          分类导航
        </h3>
        <el-menu
          default-active="all"
          @select="(index) => emit('category-click', index)"
        >
          <el-menu-item index="all">
            <span>全部笔记</span>
          </el-menu-item>
          <el-menu-item v-for="cat in categories" :key="cat.id" :index="cat.id">
            <span>{{ cat.name }}</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 标签云 -->
      <div class="section">
        <h3 class="section-title">
          标签云
        </h3>
        <div class="tags-cloud">
          <el-tag
            v-for="tag in tags"
            :key="tag.name"
            :type="tag.color === '#409EFF' ? 'primary' : tag.color === '#67C23A' ? 'success' : 'warning'"
            size="small"
            @click="emit('tag-click', tag.name)"
          >
            {{ tag.name }} ({{ tag.count }})
          </el-tag>
        </div>
      </div>

      <!-- 反向链接 -->
      <div class="section">
        <h3 class="section-title">
          相关笔记
        </h3>
        <div class="backlinks-list">
          <div 
            v-for="link in backlinks" 
            :key="link.slug"
            class="backlink-item"
            :class="{ 'is-active': activeBacklink === link.slug }"
            @click="handleBacklinkClick(link.slug)"
          >
            {{ link.title }}
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 280px;
  background: #fff;
  overflow-y: auto;
}

.sidebar-content {
  padding: 24px 20px;
}

.section {
  margin-bottom: 30px;
}

.section-title {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  font-family: 'Georgia', 'Times New Roman', serif;
  padding: 8px 12px;
  border: 2px solid transparent;
  border-radius: 6px;
  transition: all 0.3s;
  cursor: default;
}

.section-title:hover {
  border-color: #000;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.backlinks-list {
  color: #606266;
  font-size: 14px;
}

.backlink-item {
  padding: 8px 12px;
  margin-bottom: 8px;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.backlink-item:hover {
  border-color: #000;
  background: #fff;
}

.backlink-item.is-active {
  border-color: #000 !important;
  background: #fff !important;
}

:deep(.el-menu) {
  border: none;
  background: transparent;
}

:deep(.el-menu-item) {
  border-radius: 6px;
  margin-bottom: 4px;
  font-weight: 300;
  letter-spacing: 2px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

:deep(.el-menu-item:hover) {
  border-color: #000;
  background-color: #fff;
}

:deep(.el-menu-item.is-active) {
  border-color: #000 !important;
  background-color: #fff !important;
  color: #000 !important;
}
</style>
