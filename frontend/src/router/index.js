import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import HomeView from "@/views/HomeView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue";
import AccountView from "@/views/AccountView.vue";
import BlogDetailView from "@/views/BlogDetailView.vue";
import BlogListView from "@/views/BlogListView.vue";
import BlogCreateView from "@/views/BlogCreateView.vue";
import PostListView from "@/views/PostListView.vue";
import PostDetailView from "@/views/PostDetailView.vue";
import PostCreateView from "@/views/PostCreateView.vue";
import PostUpdateView from "@/views/PostUpdateView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/account",
      name: "account",
      component: AccountView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/blogs",
      name: "blogs",
      component: BlogListView,
    },
    {
      path: "/blog/create",
      name: "blog-create",
      component: BlogCreateView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/blog/:id",
      name: "blog-detail",
      component: BlogDetailView,
    },
    {
      path: "/posts",
      name: "posts",
      component: PostListView,
    },
    {
      path: "/post/create",
      name: "post-create",
      component: PostCreateView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/post/:id/edit",
      name: "post-edit",
      component: PostUpdateView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/post/:id",
      name: "post-detail",
      component: PostDetailView,
    },
  ],
});

export default router;

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "login" });
  } else {
    next();
  }
});
