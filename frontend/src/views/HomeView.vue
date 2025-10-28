<!-- HomeView.vue -->
<template>
  <section
    class="min-h-screen bg-gradient-to-b from-amber-100 to-orange-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4 sm:px-6 md:px-8"
  >
    <div class="max-w-6xl mx-auto">
      <!-- Hero Section -->
      <div class="text-center mb-12">
        <h1
          class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-amber-700 dark:text-amber-300 mb-4"
        >
          Welcome to Dogworld 🐾
        </h1>
        <p
          class="text-base sm:text-lg text-gray-700 dark:text-gray-300 max-w-2xl mx-auto"
        >
          A vibrant community for dog lovers to share, connect, and help each
          other!
        </p>
        <div class="mt-8 flex flex-wrap justify-center gap-3 sm:gap-4 md:gap-6">
          <router-link
            v-if="!authStore.isAuthenticated"
            :to="{ name: 'signup' }"
            class="bg-amber-500 hover:bg-amber-600 text-white font-bold py-2.5 px-5 sm:py-3 sm:px-6 rounded-full shadow transition text-sm sm:text-base"
          >
            Join the Pack
          </router-link>
          <router-link
            :to="{ name: 'posts' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-2.5 px-5 sm:py-3 sm:px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-sm sm:text-base"
          >
            Explore Posts
          </router-link>
          <router-link
            v-if="authStore.isAuthenticated"
            :to="{ name: 'post-create' }"
            class="bg-white text-amber-600 border border-amber-500 hover:bg-amber-100 font-bold py-2.5 px-5 sm:py-3 sm:px-6 rounded-full shadow transition text-sm sm:text-base"
          >
            Create Post
          </router-link>
          <router-link
            v-if="authStore.isAuthenticated"
            :to="{ name: 'marketplace' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-2.5 px-5 sm:py-3 sm:px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-sm sm:text-base"
          >
            Explore Marketplace
          </router-link>
          <router-link
            v-if="isStaff"
            to="/blog/create"
            class="bg-white text-amber-600 border border-amber-500 hover:bg-amber-100 font-bold py-2.5 px-5 sm:py-3 sm:px-6 rounded-full shadow transition text-sm sm:text-base"
          >
            📝 Create New Blog Post
          </router-link>
        </div>
      </div>

      <!-- Blog Section -->
      <div class="mb-16 animate-jump-in">
        <div class="text-center mb-10">
          <h2
            class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent mb-2"
          >
            Latest from the Blog
          </h2>
          <div
            class="w-20 sm:w-24 h-1 bg-gradient-to-r from-amber-400 to-orange-500 mx-auto rounded-full"
          ></div>
        </div>

        <div
          v-if="blogs.length"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8"
        >
          <router-link
            v-for="blog in blogs"
            :key="blog.id"
            :to="`/blog/${blog.id}`"
            class="group bg-white/90 dark:bg-slate-700/90 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-amber-200/50 dark:border-slate-600/50 flex flex-col"
          >
            <!-- ✅ Responsive Image Container -->
            <div
              class="relative w-full aspect-[16/10] sm:aspect-[4/3] md:aspect-[16/9] overflow-hidden rounded-t-2xl"
            >
              <img
                v-if="blog.image"
                :src="blog.image"
                alt="Blog Image"
                class="w-full h-full object-cover transform hover:scale-105 transition duration-500"
              />
              <div
                class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              ></div>
              <div
                class="absolute top-3 right-3 sm:top-4 sm:right-4 bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg"
              >
                {{ formatDate(blog.created) }}
              </div>
            </div>

            <div class="p-5 sm:p-6 flex flex-col flex-grow">
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

              <h3
                class="text-lg sm:text-xl font-bold text-gray-800 dark:text-white mb-3 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors duration-300 line-clamp-2"
              >
                {{ blog.title }}
              </h3>

              <p
                class="text-gray-600 dark:text-gray-300 text-sm line-clamp-3 mb-4 leading-relaxed"
              >
                {{ blog.content }}
              </p>

              <div class="flex flex-wrap gap-2 mb-4">
                <span
                  v-for="tag in blog.tags.slice(0, 3)"
                  :key="tag.id"
                  class="inline-flex items-center bg-gradient-to-r from-amber-100 to-orange-100 dark:from-amber-900/30 dark:to-orange-900/30 text-amber-700 dark:text-amber-300 text-xs font-medium px-3 py-1 rounded-full border border-amber-200 dark:border-amber-700"
                >
                  #{{ tag.name }}
                </span>
              </div>

              <div class="mt-auto">
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
                    />
                  </svg>
                </span>
              </div>
            </div>
          </router-link>
        </div>

        <div v-else class="text-center py-12">
          <p class="text-gray-500 dark:text-gray-400 text-lg">
            No blog posts available yet.
          </p>
        </div>

        <div class="text-center mt-10">
          <router-link
            to="/blogs"
            class="group inline-flex items-center gap-2 sm:gap-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 sm:py-4 px-6 sm:px-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 text-sm sm:text-base"
          >
            <span>View All Blog Posts</span>
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 transition-transform duration-300 group-hover:translate-x-1"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="relative overflow-hidden">
        <div
          class="absolute inset-0 bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800 rounded-3xl"
        ></div>

        <div class="relative p-6 sm:p-8 md:p-12">
          <div class="text-center mb-10">
            <h2
              class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2"
            >
              Community Stats
            </h2>
            <div
              class="w-20 sm:w-24 h-1 bg-gradient-to-r from-orange-400 to-amber-500 mx-auto rounded-full"
            ></div>
          </div>

          <div
            class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 text-center"
          >
            <div
              v-for="(item, i) in stats"
              :key="i"
              class="bg-white/70 dark:bg-slate-700/70 p-6 sm:p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 border border-amber-200/50 dark:border-slate-600/50"
            >
              <div
                class="inline-flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl mb-4 shadow-lg"
              >
                <span class="text-xl sm:text-2xl">{{ item.icon }}</span>
              </div>
              <p
                class="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-2"
              >
                {{ item.value }}
              </p>
              <p
                class="text-gray-700 dark:text-gray-300 font-medium text-base sm:text-lg"
              >
                {{ item.label }}
              </p>
              <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">
                {{ item.subtext }}
              </p>
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

const blogs = ref([]);
const blogCount = ref(0);
const postCount = ref(0);
const ratingsCount = ref(0);

const stats = computed(() => [
  {
    icon: "📝",
    value: blogCount.value,
    label: "Blog Posts",
    subtext: "Shared by community",
  },
  {
    icon: "💬",
    value: postCount.value,
    label: "User Posts",
    subtext: "Community discussions",
  },
  {
    icon: "⭐",
    value: ratingsCount.value,
    label: "Ratings",
    subtext: "Community feedback",
  },
]);

const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

onMounted(async () => {
  try {
    const [blogPreviewRes, blogCountRes, postCountRes, ratingsCountRes] =
      await Promise.all([
        axios.get("/content/blogs/", {
          params: { ordering: "-created", page_size: 3 },
        }),
        axios.get("/content/blogs/"),
        axios.get("/content/posts/"),
        axios.get("/content/ratings/"),
      ]);

    blogs.value = blogPreviewRes.data.results || blogPreviewRes.data;
    blogCount.value = blogCountRes.data.count || blogCountRes.data.length;
    postCount.value = postCountRes.data.count || postCountRes.data.length;
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
