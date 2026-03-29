<script setup>
import { ref } from 'vue'
import { ElInput, ElButton } from 'element-plus'
import { Search, Plus, Download } from '@element-plus/icons-vue'

const props = defineProps({
  searchQuery: String
})

const emit = defineEmits(['update-search', 'new-note', 'export'])

const localSearch = ref(props.searchQuery || '')

const handleSearch = () => {
  emit('update-search', localSearch.value)
}

const handleNewNote = () => {
  emit('new-note')
}

const handleExport = () => {
  emit('export')
}
</script>

<template>
  <header class="layout-header">
    <h1 class="header-title">收藏夹</h1>
    
    <el-input
      v-model="localSearch"
      placeholder="搜索笔记（按回车）..."
      size="large"
      clearable
      class="search-input"
      @keyup.enter="handleSearch"
    />
    
    <div class="header-actions">
      <el-button size="large" round @click="handleNewNote">
        新建笔记
      </el-button>
      
      <el-button size="large" round @click="handleExport">
        导出
      </el-button>
    </div>
  </header>
</template>

<style scoped>
.layout-header {
  height: 70px;
  background: #fff;
  color: #303133;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: relative;
}

.header-title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 8px;
  font-family: 'Georgia', 'Times New Roman', serif;
  position: absolute;
  left: 24px;
}

.search-input {
  width: 25%;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

:deep(.el-input) {
  border: 2px solid #000 !important;
  border-radius: 4px !important;
}

:deep(.el-input__wrapper) {
  box-shadow: none !important;
  padding: 0 !important;
}

:deep(.el-input__inner) {
  border: none !important;
  text-align: center;
}

.header-actions {
  display: flex;
  gap: 8px;
  position: absolute;
  left: 304px;
  top: 50%;
  transform: translateY(-50%);
}

.el-button:not(.is-disabled) {
  background: #fff;
  color: #303133;
  font-weight: 600;
  letter-spacing: 2px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.el-button:not(.is-disabled):hover {
  border-color: #000;
  background: #fff !important;
}

.el-button:not(.is-disabled):focus,
.el-button:not(.is-disabled).is-active {
  border-color: #000 !important;
  background: #fff !important;
}
</style>
