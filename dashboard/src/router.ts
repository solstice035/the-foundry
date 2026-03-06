import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'forge-floor', component: () => import('./pages/ForgeFloor.vue') },
    { path: '/armoury', name: 'armoury', component: () => import('./pages/Armoury.vue') },
    { path: '/proving/:date', name: 'proving-ground', component: () => import('./pages/ProvingGround.vue') },
    { path: '/ore', name: 'ore-seam', component: () => import('./pages/OreSeam.vue') },
    { path: '/blueprints', name: 'blueprints', component: () => import('./pages/BlueprintRoom.vue') },
    { path: '/ledger', name: 'ledger', component: () => import('./pages/Ledger.vue') },
    { path: '/rejections', name: 'rejections', component: () => import('./pages/RejectionPile.vue') },
    { path: '/social', name: 'social', component: () => import('./pages/SocialQueue.vue') },
    { path: '/furnace', name: 'furnace', component: () => import('./pages/Furnace.vue') },
  ],
})

export default router
