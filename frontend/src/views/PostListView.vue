<template>
  <section
    class="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-12 px-4"
  >
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1
            class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 dark:from-amber-400 dark:to-orange-400"
          >
            🐕 User's Posts
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Browse and manage your published posts
          </p>
        </div>

        <!-- View Toggle -->
        <div class="flex items-center gap-3">
          <router-link
            v-if="authStore.isAuthenticated"
            :to="{ name: 'post-create' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Create Post
          </router-link>
          <button
            @click="viewMode = 'grid'"
            :class="viewMode === 'grid' ? activeBtnClass : inactiveBtnClass"
          >
            🗂 Grid
          </button>
          <button
            @click="viewMode = 'list'"
            :class="viewMode === 'list' ? activeBtnClass : inactiveBtnClass"
          >
            📋 List
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div
        class="bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm rounded-2xl p-6 mb-8 shadow-lg border border-white/20"
      >
        <div class="flex flex-wrap items-center gap-4">
          <div class="relative flex-1 min-w-64">
            <div
              class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
            >
              <span class="text-gray-400">🔍</span>
            </div>
            <input
              v-model="search"
              type="text"
              placeholder="Search posts..."
              class="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none focus:ring-4 focus:ring-amber-200/50 bg-white/90 dark:bg-slate-700/90 transition-all duration-200"
            />
          </div>

          <select
            v-model="selectedTag"
            class="px-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none bg-white/90 dark:bg-slate-700/90 min-w-48"
          >
            <option value="">🏷️ All Tags</option>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>

          <select
            v-model="selectedOrdering"
            class="px-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none bg-white/90 dark:bg-slate-700/90 min-w-48"
          >
            <option value="-created_at">🆕 Newest</option>
            <option value="created_at">⏰ Oldest</option>
            <option value="title">🔤 Title A–Z</option>
            <option value="-title">🔤 Title Z–A</option>
          </select>
        </div>
      </div>

      <!-- Posts -->
      <div
        v-if="posts.length"
        :class="
          viewMode === 'grid'
            ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10'
            : 'space-y-8'
        "
      >
        <router-link
          v-for="post in posts"
          :key="post.id"
          :to="`/post/${post.id}`"
          class="rounded-2xl overflow-hidden shadow-xl flex flex-col bg-amber-100/40 dark:bg-slate-700/60 border border-orange-200 dark:border-slate-700 hover:border-amber-400 transition-all duration-300 transform hover:scale-105"
        >
          <!-- Image -->
          <div class="relative">
            <div
              class="flex items-center justify-center p-4 h-60 bg-white dark:bg-white"
            >
              <img
                v-if="post.image"
                :src="post.image"
                alt="Post"
                class="w-auto h-auto max-w-full max-h-full object-contain rounded-2xl"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-100 to-orange-100 dark:from-slate-600 dark:to-slate-700"
              >
                <span class="text-6xl opacity-50">🐾</span>
              </div>
            </div>
          </div>

          <!-- Content -->
          <div class="px-6 py-4 mb-auto">
            <h2
              class="cursor-pointer font-semibold text-xl inline-block text-amber-700 dark:text-amber-300 hover:text-amber-600 dark:hover:text-amber-400 transition duration-300 mb-2"
            >
              {{ post.title }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">
              By {{ post.author.username }} • {{ formatDate(post.created_at) }}
            </p>

            <!-- Tags -->
            <div v-if="post.tags?.length" class="mt-2 flex flex-wrap gap-2">
              <span
                v-for="tag in post.tags"
                :key="tag.id"
                class="px-3 py-1 text-xs rounded-full bg-amber-200 dark:bg-slate-600 text-amber-800 dark:text-amber-300 font-semibold"
              >
                #{{ tag.name }}
              </span>
            </div>
          </div>

          <!-- Footer -->
          <div
            class="px-6 py-4 flex justify-between items-center bg-amber-100/40 dark:bg-slate-700/60 rounded-b-2xl"
          >
            <router-link
              :to="`/post/${post.id}`"
              class="text-sm font-medium text-amber-600 dark:text-amber-400 hover:underline"
            >
              📖 Read more →
            </router-link>
          </div>
        </router-link>
      </div>

      <!-- No Posts -->
      <div v-else class="text-center py-16">
        <div class="text-8xl mb-4">📭</div>
        <h3 class="text-2xl font-bold text-gray-600 dark:text-gray-400 mb-2">
          No posts found
        </h3>
        <p class="text-gray-500 dark:text-gray-400">
          Try adjusting your search or filter criteria
        </p>
      </div>

      <!-- Pagination -->
      <div class="mt-12 flex justify-center items-center gap-4">
        <button
          @click="prevPage"
          :disabled="!previous"
          class="flex items-center gap-2 px-6 py-3 rounded-xl bg-white dark:bg-slate-800 border-2 border-amber-200 dark:border-slate-600 hover:border-amber-400 hover:bg-amber-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-gray-700 dark:text-gray-300 transition-all duration-200"
        >
          <span>←</span> Previous
        </button>

        <div class="px-4 py-2 bg-amber-500 text-white rounded-lg font-bold">
          Page {{ currentPage }}
        </div>

        <button
          @click="nextPage"
          :disabled="!next"
          class="flex items-center gap-2 px-6 py-3 rounded-xl bg-white dark:bg-slate-800 border-2 border-amber-200 dark:border-slate-600 hover:border-amber-400 hover:bg-amber-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-gray-700 dark:text-gray-300 transition-all duration-200"
        >
          Next <span>→</span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useAuthStore } from "../stores/auth";
import { useToast } from "vue-toastification";
import axios from "axios";

const toast = useToast();
const authStore = useAuthStore();

// Reactive state
const posts = ref([]);
const tags = ref([]);
const search = ref("");
const selectedTag = ref("");
const selectedOrdering = ref("-created_at");
const viewMode = ref("grid");
const next = ref(null);
const previous = ref(null);
const currentPage = ref(1);

// Classes
const activeBtnClass =
  "px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl shadow-lg font-semibold";
const inactiveBtnClass =
  "px-4 py-2 bg-white/80 dark:bg-slate-700/80 backdrop-blur-sm border-2 border-amber-200 dark:border-slate-600 text-amber-600 dark:text-amber-300 rounded-xl hover:border-amber-400 hover:bg-amber-50 dark:hover:bg-slate-600 transition-all duration-200 font-semibold";

// Date formatter
const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

// Fetch all available tags
const fetchTags = async () => {
  try {
    const res = await axios.get("/content/tags/");
    tags.value = res.data;
  } catch (err) {
    toast.error("Failed to fetch tags.");
  }
};

// Fetch posts with filters
const fetchPosts = async (page = 1) => {
  try {
    const params = {
      page,
      search: search.value,
      ordering: selectedOrdering.value,
    };

    if (selectedTag.value) {
      params["tags"] = selectedTag.value;
    }

    const res = await axios.get("/content/posts/", { params });
    posts.value = res.data.results;
    next.value = res.data.next;
    previous.value = res.data.previous;
    currentPage.value = page;
  } catch (err) {
    toast.error("Failed to load posts.");
  }
};

// Pagination controls
const nextPage = () => {
  if (next.value) fetchPosts(currentPage.value + 1);
};
const prevPage = () => {
  if (previous.value) fetchPosts(currentPage.value - 1);
};

// Initial load
onMounted(() => {
  fetchTags();
  fetchPosts();
});

// Watch filters and refetch posts
watch([search, selectedTag, selectedOrdering], () => {
  fetchPosts(1);
});
</script>
