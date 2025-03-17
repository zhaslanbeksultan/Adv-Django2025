import { createRouter, createWebHistory } from 'vue-router';
import ItemList from '../components/ItemList.vue';
import LoginPage from '../views/LoginPage.vue';
import AdminPanel from '../views/AdminPanel.vue';
import RegisterPage from '../views/RegisterPage.vue';
import store from '../store';

const routes = [
    { path: '/', component: ItemList },
    { path: '/login', component: LoginPage },
    { path: '/admin', component: AdminPanel, meta: { requiresAdmin: true } },
    { path: '/register', component: RegisterPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAdmin) {
        await store.dispatch('fetchUser');
        if (store.state.user?.role === 'admin') {
            next();
        } else {
            next('/login');
        }
    } else {
        next();
    }
});

export default router;