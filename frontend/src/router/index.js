import { createRouter, createWebHistory } from 'vue-router'

// 懒加载路由（提升首屏性能）
const NoteList = () => import('../views/NoteList.vue')
const NoteDetail = () => import('../views/NoteDetail.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: NoteList,
    meta: { title: '收藏夹 - 笔记列表' }
  },
  {
    path: '/wiki/:slug',
    name: 'NoteDetail',
    component: NoteDetail,
    props: true,
    meta: { title: '笔记详情' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 每次路由切换滚动到顶部
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由前置守卫（设置页面标题）
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '收藏夹'
  next()
})

export default router
