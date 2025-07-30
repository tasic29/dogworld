<!-- HomeView.vue -->
<template>
  <section
    class="min-h-screen bg-gradient-to-b from-amber-100 to-orange-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div class="max-w-5xl mx-auto">
      <!-- Hero Section -->
      <div class="text-center mb-10">
        <h1
          class="text-4xl md:text-5xl font-extrabold text-amber-700 dark:text-amber-300 mb-4"
        >
          Welcome to Dogworld 🐾
        </h1>
        <p class="text-lg text-gray-700 dark:text-gray-300">
          A vibrant community for dog lovers to share, connect, and help each
          other!
        </p>
        <div class="mt-6 flex justify-center gap-4">
          <router-link
            v-if="!authStore.isAuthenticated"
            :to="{ name: 'signup' }"
            class="bg-amber-500 hover:bg-amber-600 text-white font-bold py-3 px-6 rounded-full shadow transition"
          >
            Join the Pack
          </router-link>
          <router-link
            :to="{ name: 'posts' }"
            class="bg-white text-amber-600 border border-amber-500 hover:bg-amber-100 font-bold py-3 px-6 rounded-full shadow transition"
          >
            Explore Posts
          </router-link>
          <router-link
            v-if="authStore.isAuthenticated"
            :to="{ name: 'post-create' }"
            class="bg-white text-amber-600 border border-amber-500 hover:bg-amber-100 font-bold py-3 px-6 rounded-full shadow transition"
          >
            Create Post
          </router-link>
          <router-link
            v-if="isStaff"
            to="/blog/create"
            class="bg-white text-amber-600 border border-amber-500 hover:bg-amber-100 font-bold py-3 px-6 rounded-full shadow transition"
          >
            📝 Create New Blog Post
          </router-link>
        </div>
      </div>

      <!-- Featured Blog Posts -->
      <div class="mb-16 animate-jump-in">
        <h2
          class="text-2xl font-bold text-gray-700 dark:text-white mb-6 flex items-center"
        >
          <span class="mr-2">📰</span> Latest from the Blog
        </h2>
        <div v-if="blogs.length" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <router-link
            :to="`/blog/${blog.id}`"
            v-for="blog in blogs"
            :key="blog.id"
            class="bg-white/80 dark:bg-slate-700 rounded-xl p-6 shadow-lg hover:shadow-2xl transition"
          >
            <img
              v-if="blog.image"
              :src="blog.image"
              alt="Blog Image"
              class="rounded-lg mb-4 w-full h-48 object-cover"
            />
            <h3
              class="text-xl font-semibold text-amber-700 dark:text-amber-300 mb-1"
            >
              {{ blog.title }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
              By {{ blog.author.username }} | {{ formatDate(blog.created) }}
            </p>
            <p class="text-gray-600 dark:text-gray-300 text-sm line-clamp-3">
              {{ blog.content }}
            </p>
            <div class="mt-2 flex flex-wrap gap-2">
              <span
                v-for="tag in blog.tags"
                :key="tag.id"
                class="bg-amber-200 text-amber-800 text-xs font-medium px-2 py-1 rounded"
              >
                #{{ tag.name }}
              </span>
            </div>
            <div class="mt-4">
              <router-link
                :to="`/blog/${blog.id}`"
                class="inline-block text-amber-600 dark:text-amber-400 hover:underline font-semibold"
              >
                Read more →
              </router-link>
            </div>
          </router-link>
        </div>
        <p v-else class="text-gray-500 dark:text-gray-400">
          No blog posts available yet.
        </p>
        <div class="text-center mt-8">
          <router-link
            to="/blogs"
            class="inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white dark:bg-amber-600 dark:hover:bg-amber-700 font-bold py-3 px-6 rounded-full shadow transition duration-300 hover:shadow-lg"
          >
            <span>View All Blog Posts</span>
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M9 5l7 7-7 7"
              ></path>
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="bg-amber-50 dark:bg-slate-700/50 p-8 rounded-xl shadow">
        <h2
          class="text-2xl font-bold text-gray-800 dark:text-white mb-6 flex items-center"
        >
          <span class="mr-2">📊</span> Community Stats
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
          <div>
            <p class="text-3xl font-bold text-orange-600 dark:text-orange-300">
              {{ blogCount }}
            </p>
            <p class="text-gray-600 dark:text-gray-300">Blog Posts Shared</p>
          </div>
          <div>
            <p class="text-3xl font-bold text-orange-600 dark:text-orange-300">
              {{ postCount }}
            </p>
            <p class="text-gray-600 dark:text-gray-300">User Posts</p>
          </div>
          <div>
            <p class="text-3xl font-bold text-orange-600 dark:text-orange-300">
              🚧
            </p>
            <p class="text-gray-600 dark:text-gray-300">Ratings Coming Soon</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const isStaff = computed(() => authStore.user?.is_staff);

// Blog previews for Hero section
const blogs = ref([]);

// Community stats
const blogCount = ref(0);
const postCount = ref(0);

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

onMounted(async () => {
  try {
    // Fetch latest blog previews
    const blogPreviewRes = await axios.get("/content/blogs/", {
      params: {
        ordering: "-created",
        page_size: 3,
      },
    });
    blogs.value = blogPreviewRes.data.results || blogPreviewRes.data;

    // Fetch blog post count
    const blogCountRes = await axios.get("/content/blogs/");
    blogCount.value = blogCountRes.data.count || blogCountRes.data.length;

    // Fetch user post count
    const postCountRes = await axios.get("/content/posts/");
    postCount.value = postCountRes.data.count || postCountRes.data.length;
  } catch (error) {
    console.error("Failed to fetch stats or blog posts:", error);
  }
});
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
