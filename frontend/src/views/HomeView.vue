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
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
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
            v-if="authStore.isAuthenticated"
            :to="{ name: 'marketplace' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Explore Marketplace
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

      <!-- Enhanced Featured Blog Posts -->
      <div class="mb-16 animate-jump-in">
        <!-- Section Header with decorative elements -->
        <div class="text-center mb-12">
          <!-- <div
            class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full mb-4 shadow-lg"
          >
            <span class="text-2xl">📰</span>
          </div> -->
          <h2
            class="text-3xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent mb-2"
          >
            Latest from the Blog
          </h2>
          <div
            class="w-24 h-1 bg-gradient-to-r from-amber-400 to-orange-500 mx-auto rounded-full"
          ></div>
        </div>

        <div v-if="blogs.length" class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <router-link
            :to="`/blog/${blog.id}`"
            v-for="blog in blogs"
            :key="blog.id"
            class="group relative bg-white/90 dark:bg-slate-700/90 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-amber-200/50 dark:border-slate-600/50"
          >
            <!-- Image with overlay -->
            <div class="relative overflow-hidden">
              <img
                v-if="blog.image"
                :src="blog.image"
                alt="Blog Image"
                class="w-full h-56 object-cover transition-transform duration-500 group-hover:scale-110"
              />
              <div
                class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              ></div>
              <!-- Floating date badge -->
              <div
                class="absolute top-4 right-4 bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg"
              >
                {{ formatDate(blog.created) }}
              </div>
            </div>

            <!-- Content -->
            <div class="p-6">
              <!-- Author info -->
              <div class="flex items-center gap-2 mb-3">
                <div
                  class="w-8 h-8 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center text-white text-sm font-bold"
                >
                  {{ blog.author.username.charAt(0).toUpperCase() }}
                </div>
                <span
                  class="text-sm text-gray-600 dark:text-gray-400 font-medium"
                >
                  By {{ blog.author.username }}
                </span>
              </div>

              <!-- Title -->
              <h3
                class="text-xl font-bold text-gray-800 dark:text-white mb-3 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors duration-300 line-clamp-2"
              >
                {{ blog.title }}
              </h3>

              <!-- Content preview -->
              <p
                class="text-gray-600 dark:text-gray-300 text-sm line-clamp-3 mb-4 leading-relaxed"
              >
                {{ blog.content }}
              </p>

              <!-- Tags -->
              <div class="flex flex-wrap gap-2 mb-4">
                <span
                  v-for="tag in blog.tags.slice(0, 3)"
                  :key="tag.id"
                  class="inline-flex items-center bg-gradient-to-r from-amber-100 to-orange-100 dark:from-amber-900/30 dark:to-orange-900/30 text-amber-700 dark:text-amber-300 text-xs font-medium px-3 py-1 rounded-full border border-amber-200 dark:border-amber-700"
                >
                  #{{ tag.name }}
                </span>
                <span
                  v-if="blog.tags.length > 3"
                  class="text-xs text-gray-500 dark:text-gray-400 px-2 py-1"
                >
                  +{{ blog.tags.length - 3 }} more
                </span>
              </div>

              <!-- Read more link -->
              <div class="flex items-center justify-between">
                <span
                  class="inline-flex items-center gap-2 text-amber-600 dark:text-amber-400 hover:text-orange-600 dark:hover:text-orange-400 font-semibold text-sm group-hover:gap-3 transition-all duration-300"
                >
                  Read more
                  <svg
                    class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M9 5l7 7-7 7"
                    ></path>
                  </svg>
                </span>
              </div>
            </div>
          </router-link>
        </div>

        <div v-else class="text-center py-12">
          <div
            class="w-20 h-20 bg-gray-100 dark:bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <span class="text-3xl">📝</span>
          </div>
          <p class="text-gray-500 dark:text-gray-400 text-lg">
            No blog posts available yet.
          </p>
        </div>

        <!-- View All Button -->
        <div class="text-center mt-12">
          <router-link
            to="/blogs"
            class="group inline-flex items-center gap-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-4 px-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
          >
            <span>View All Blog Posts</span>
            <svg
              class="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
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

      <!-- Enhanced Stats Section -->
      <div class="relative overflow-hidden">
        <!-- Background decoration -->
        <div
          class="absolute inset-0 bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800 rounded-3xl"
        ></div>
        <div
          class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-amber-200/30 to-transparent rounded-full -translate-y-32 translate-x-32"
        ></div>
        <div
          class="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-tr from-orange-200/30 to-transparent rounded-full translate-y-24 -translate-x-24"
        ></div>

        <div class="relative p-8 md:p-12">
          <!-- Section Header -->
          <div class="text-center mb-12">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-400 to-amber-500 rounded-full mb-4 shadow-lg"
            >
              <span class="text-2xl">📊</span>
            </div>
            <h2
              class="text-3xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2"
            >
              Community Stats
            </h2>
            <div
              class="w-24 h-1 bg-gradient-to-r from-orange-400 to-amber-500 mx-auto rounded-full"
            ></div>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
            <!-- Blog Posts Stat -->
            <div class="group relative">
              <div
                class="bg-white/70 dark:bg-slate-700/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-amber-200/50 dark:border-slate-600/50"
              >
                <div
                  class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300"
                >
                  <span class="text-2xl">📝</span>
                </div>
                <p
                  class="text-4xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2 group-hover:scale-105 transition-transform duration-300"
                >
                  {{ blogCount }}
                </p>
                <p class="text-gray-700 dark:text-gray-300 font-medium text-lg">
                  Blog Posts
                </p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">
                  Shared by community
                </p>
              </div>
            </div>

            <!-- User Posts Stat -->
            <div class="group relative">
              <div
                class="bg-white/70 dark:bg-slate-700/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-amber-200/50 dark:border-slate-600/50"
              >
                <div
                  class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-400 to-amber-500 rounded-2xl mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300"
                >
                  <span class="text-2xl">💬</span>
                </div>
                <p
                  class="text-4xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2 group-hover:scale-105 transition-transform duration-300"
                >
                  {{ postCount }}
                </p>
                <p class="text-gray-700 dark:text-gray-300 font-medium text-lg">
                  User Posts
                </p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">
                  Community discussions
                </p>
              </div>
            </div>

            <!-- Ratings Stat -->
            <div class="group relative">
              <div
                class="bg-white/70 dark:bg-slate-700/70 backdrop-blur-sm p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-amber-200/50 dark:border-slate-600/50"
              >
                <div
                  class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300"
                >
                  <span class="text-2xl">⭐</span>
                </div>
                <p
                  class="text-4xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2 group-hover:scale-105 transition-transform duration-300"
                >
                  {{ ratingsCount }}
                </p>
                <p class="text-gray-700 dark:text-gray-300 font-medium text-lg">
                  Ratings
                </p>
                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">
                  Community feedback
                </p>
              </div>
            </div>
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
const ratingsCount = ref(0);

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

    // Fetch ratings count
    const ratingsCountRes = await axios.get("/content/ratings/");
    ratingsCount.value =
      ratingsCountRes.data.count || ratingsCountRes.data.length;
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
