import axios from 'axios'

// API 基础地址（通过代理转发到后端）
const API_BASE = '/api'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器（可添加 token 等）
apiClient.interceptors.request.use(
  config => {
    return config
  },
  error => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器（统一错误处理）
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Response Error:', error)
    
    // 提取友好的错误信息
    let message = '请求失败，请稍后重试'
    
    if (error.response) {
      switch (error.response.status) {
        case 404:
          message = '未找到资源'
          break
        case 500:
          message = '服务器错误'
          break
        case 504:
          message = '请求超时'
          break
        default:
          message = error.response.data?.detail || message
      }
    } else if (error.request) {
      message = '无法连接到服务器，请检查后端服务是否运行'
    }
    
    return Promise.reject(new Error(message))
  }
)

// === API 方法封装 ===

/**
 * 获取笔记列表（支持分页）
 * @param {number} limit - 每页数量
 * @param {number} offset - 偏移量
 * @returns {Promise<Object>} { notes: Array, total: number }
 */
export const getNotes = async (limit = 20, offset = 0) => {
  return await apiClient.get('/wiki/list', { params: { limit, offset } })
}

/**
 * 获取单篇笔记详情
 * @param {string} slug - 笔记唯一标识
 * @returns {Promise<Object>} 笔记对象
 */
export const getNoteById = async (slug) => {
  return await apiClient.get(`/wiki/${slug}`)
}

/**
 * 新建笔记
 * @param {Object} data - 笔记数据
 * @param {string} data.title - 标题
 * @param {string} data.content - 内容
 * @param {Array<string>} data.tags - 标签数组
 * @returns {Promise<Object>} 创建的笔记对象（包含 slug）
 */
export const createNote = async (data) => {
  return await apiClient.post('/wiki/add', data)
}

/**
 * 更新笔记
 * @param {string} slug - 笔记唯一标识
 * @param {Object} data - 更新的数据（只传需要更新的字段）
 * @returns {Promise<Object>} 更新后的笔记对象
 */
export const updateNote = async (slug, data) => {
  return await apiClient.put(`/wiki/${slug}`, data)
}

/**
 * 删除笔记
 * @param {string} slug - 笔记唯一标识
 * @returns {Promise<Object>} 删除结果
 */
export const deleteNote = async (slug) => {
  return await apiClient.delete(`/wiki/${slug}`)
}

/**
 * 搜索笔记
 * @param {string} query - 搜索关键词
 * @param {number} limit - 返回数量限制
 * @returns {Promise<Array>} 搜索结果数组
 */
export const searchNotes = async (query, limit = 20) => {
  const response = await apiClient.get('/wiki/search', { params: { query, limit } })
  return response.results || []
}

/**
 * 获取统计信息
 * @returns {Promise<Object>} 统计数据
 */
export const getStats = async () => {
  return await apiClient.get('/wiki/stats')
}

/**
 * 获取反向链接
 * @param {string} slug - 笔记唯一标识
 * @returns {Promise<Array>} 反向链接数组
 */
export const getBacklinks = async (slug) => {
  return await apiClient.get(`/wiki/backlinks/${slug}`)
}

export default {
  getNotes,
  getNoteById,
  createNote,
  updateNote,
  deleteNote,
  searchNotes,
  getStats,
  getBacklinks
}
