<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1
          class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 dark:from-amber-400 dark:to-orange-400"
        >
          🐕 User's Posts
        </h1>

        <!-- View Toggle -->
        <div class="flex items-center gap-2">
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
      <div class="flex flex-wrap items-center gap-4 mb-6">
        <input
          v-model="search"
          type="text"
          placeholder="Search blogs..."
          class="px-4 py-2 rounded-lg border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
        />

        <select
          v-model="selectedTag"
          class="px-4 py-2 rounded-lg border border-amber-300"
        >
          <option value="">All Tags</option>
          <option v-for="tag in tags" :key="tag.id" :value="tag.name">
            #{{ tag.name }}
          </option>
        </select>

        <select
          v-model="selectedOrdering"
          class="px-4 py-2 rounded-lg border border-amber-300"
        >
          <option value="-created">Newest</option>
          <option value="created">Oldest</option>
          <option value="title">Title A–Z</option>
          <option value="-title">Title Z–A</option>
        </select>
      </div>

      <!-- Post List -->
      <div
        v-if="posts.length"
        :class="viewMode === 'grid' ? 'grid md:grid-cols-2 gap-6' : 'space-y-6'"
      >
        <router-link
          v-for="post in posts"
          :key="post.id"
          :to="`/post/${post.id}`"
          class="bg-white/80 dark:bg-slate-800 rounded-xl p-6 shadow-lg hover:shadow-2xl transition flex flex-col md:flex-row gap-4"
          :class="viewMode === 'grid' ? '' : 'md:items-center'"
        >
          <img
            v-if="post.image"
            :src="post.image"
            alt="Post preview"
            class="w-full md:w-48 h-32 object-cover rounded-lg shadow"
          />

          <div>
            <h2
              class="text-xl font-semibold text-amber-700 dark:text-amber-300"
            >
              {{ post.title }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              By {{ post.author.username }} • {{ formatDate(post.created_at) }}
            </p>

            <!-- Post-specific tags -->
            <div v-if="post.tags?.length" class="mt-2 flex flex-wrap gap-1">
              <span
                v-for="tag in post.tags"
                :key="tag.id"
                class="px-2 py-1 text-xs rounded-full bg-amber-100 dark:bg-slate-700 text-amber-700 dark:text-amber-300 font-medium"
              >
                #{{ tag.name }}
              </span>
            </div>

            <router-link
              :to="`/post/${post.id}`"
              class="inline-block mt-2 text-amber-600 dark:text-amber-400 hover:underline text-sm"
            >
              Read more →
            </router-link>
          </div>
        </router-link>
      </div>

      <!-- No Results -->
      <p v-else class="text-center text-gray-500 dark:text-gray-400">
        No posts found.
      </p>

      <!-- Pagination -->
      <div class="mt-8 flex justify-center gap-4">
        <button
          @click="prevPage"
          :disabled="!previous"
          class="px-4 py-2 rounded bg-amber-400 text-white font-semibold disabled:opacity-50"
        >
          Previous
        </button>
        <button
          @click="nextPage"
          :disabled="!next"
          class="px-4 py-2 rounded bg-amber-400 text-white font-semibold disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

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
const activeBtnClass = "px-3 py-2 bg-amber-500 text-white rounded-md shadow";
const inactiveBtnClass =
  "px-3 py-2 bg-white dark:bg-slate-700 border border-amber-300 text-amber-600 dark:text-amber-300 rounded-md";

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
    console.error("Failed to fetch tags:", err);
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
      params["tags__name"] = selectedTag.value;
    }

    const res = await axios.get("/content/posts/", { params });
    posts.value = res.data.results;
    next.value = res.data.next;
    previous.value = res.data.previous;
    currentPage.value = page;
  } catch (err) {
    console.error("Error fetching blogs:", err);
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
