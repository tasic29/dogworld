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
            🐕 Dogworld Marketplace
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Discover amazing products for your furry friends
          </p>
        </div>

        <!-- View Toggle -->
        <div class="flex items-center gap-3">
          <router-link
            v-if="isStaff"
            :to="{ name: 'product-create' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            ✨ Create Product
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

      <!-- Filters Section -->
      <div
        class="bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm rounded-2xl p-6 mb-8 shadow-lg border border-white/20"
      >
        <div class="flex flex-wrap items-center gap-4">
          <!-- Search -->
          <div class="relative flex-1 min-w-64">
            <div
              class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
            >
              <span class="text-gray-400">🔍</span>
            </div>
            <input
              v-model="search"
              type="text"
              placeholder="Search for dog products..."
              class="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none focus:ring-4 focus:ring-amber-200/50 bg-white/90 dark:bg-slate-700/90 transition-all duration-200"
            />
          </div>

          <!-- Category Filter -->
          <select
            v-model="selectedCategory"
            class="px-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none bg-white/90 dark:bg-slate-700/90 min-w-48"
          >
            <option value="">🏷️ All Categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.slug"
            >
              {{ category.name }} ({{ category.products_count }})
            </option>
          </select>

          <!-- Sort Options -->
          <select
            v-model="selectedOrdering"
            class="px-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none bg-white/90 dark:bg-slate-700/90 min-w-48"
          >
            <option value="-created_at">🆕 Newest First</option>
            <option value="created_at">⏰ Oldest First</option>
            <option value="title">🔤 A to Z</option>
            <option value="-title">🔤 Z to A</option>
            <option value="price">💰 Price: Low to High</option>
            <option value="-price">💰 Price: High to Low</option>
          </select>
        </div>
      </div>

      <!-- Products Grid/List -->
      <div v-if="loading" class="text-center py-16">
        <div class="relative inline-block">
          <div
            class="animate-spin rounded-full h-12 w-12 border-4 border-amber-200 border-t-amber-500"
          ></div>
          <div
            class="absolute inset-0 rounded-full h-12 w-12 border-4 border-transparent border-t-orange-500 animate-spin"
            style="animation-delay: 0.15s"
          ></div>
        </div>
        <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
          Finding the best products for your dog...
        </p>
      </div>

      <div
        v-else-if="products.length"
        :class="
          viewMode === 'grid'
            ? 'grid grid-cols-1 lg:grid-cols-2 gap-8'
            : 'space-y-8'
        "
      >
        <div
          v-for="product in products"
          :key="product.id"
          class="bg-white dark:bg-slate-800 lg:flex rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition duration-300 border border-gray-100 dark:border-slate-700 hover:border-amber-300 dark:hover:border-amber-500"
        >
          <!-- Left: Image -->
          <div class="lg:w-1/2">
            <div
              class="h-64 lg:h-auto overflow-hidden rounded-t-3xl lg:rounded-l-3xl lg:rounded-t-none"
            >
              <img
                v-if="product.image"
                :src="product.image"
                alt=""
                class="h-full w-full object-cover"
              />
              <div
                v-else
                class="h-full w-full flex items-center justify-center bg-gradient-to-br from-amber-100 to-orange-100 dark:from-slate-600 dark:to-slate-700"
              >
                <span class="text-6xl opacity-50">🐶</span>
              </div>
            </div>
          </div>

          <!-- Right: Content -->
          <div class="py-8 px-6 lg:px-10 lg:w-1/2 space-y-4">
            <h2 class="text-2xl font-bold text-gray-800 dark:text-white">
              {{ product.title }}
            </h2>

            <div
              class="flex items-center gap-4 text-sm font-semibold text-gray-600 dark:text-gray-300"
            >
              <div
                class="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-3 py-1 rounded-full"
              >
                💰 ${{ product.price }}
              </div>
              <div
                v-if="product.category"
                class="bg-amber-100 text-amber-800 dark:bg-slate-700 dark:text-amber-300 px-3 py-1 rounded-full"
              >
                📂 {{ product.category.name }}
              </div>
            </div>

            <p
              v-if="product.description"
              class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed line-clamp-3"
            >
              {{ product.description }}
            </p>

            <p class="text-xs text-gray-500 dark:text-gray-400">
              📅 {{ formatDate(product.created_at) }}
            </p>

            <div>
              <button
                @click="handleProductClick(product)"
                :disabled="clickingProduct === product.id"
                class="mt-4 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-2 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 flex items-center gap-2 text-sm"
              >
                <span v-if="clickingProduct === product.id">
                  <div
                    class="animate-spin rounded-full h-3 w-3 border-2 border-white border-t-transparent"
                  ></div>
                </span>
                <span v-else class="flex items-center gap-1">
                  🛒 View
                  <span class="transition-transform group-hover:translate-x-1"
                    >→</span
                  >
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!loading" class="text-center py-16">
        <div class="text-8xl mb-4">🐕‍🦺</div>
        <h3 class="text-2xl font-bold text-gray-600 dark:text-gray-400 mb-2">
          No products found
        </h3>
        <p class="text-gray-500 dark:text-gray-400">
          Try adjusting your search or filter criteria
        </p>
        <button
          v-if="hasActiveFilters"
          @click="clearAllFilters"
          class="mt-4 bg-amber-500 hover:bg-amber-600 text-white px-6 py-2 rounded-full transition-colors duration-200"
        >
          Clear All Filters
        </button>
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

    <!-- Success Toast -->
    <div
      v-if="showSuccessToast"
      class="fixed bottom-6 right-6 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-4 rounded-2xl shadow-xl z-50 flex items-center gap-3 animate-bounce-in"
    >
      <span class="text-2xl">✅</span>
      <div>
        <div class="font-bold">Success!</div>
        <div class="text-sm opacity-90">Product click registered</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useToast } from "vue-toastification";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const toast = useToast();
const authStore = useAuthStore();
const isStaff = computed(() => authStore.user?.is_staff);

// Reactive state
const products = ref([]);
const categories = ref([]);
const search = ref("");
const selectedCategory = ref("");
const selectedOrdering = ref("-created_at");
const viewMode = ref("grid");
const next = ref(null);
const previous = ref(null);
const currentPage = ref(1);
const loading = ref(false);
const clickingProduct = ref(null);
const showSuccessToast = ref(false);

// Enhanced button classes
const activeBtnClass =
  "px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl shadow-lg font-semibold";
const inactiveBtnClass =
  "px-4 py-2 bg-white/80 dark:bg-slate-700/80 backdrop-blur-sm border-2 border-amber-200 dark:border-slate-600 text-amber-600 dark:text-amber-300 rounded-xl hover:border-amber-400 hover:bg-amber-50 dark:hover:bg-slate-600 transition-all duration-200 font-semibold";

// Computed properties
const hasActiveFilters = computed(() => {
  return search.value || selectedCategory.value;
});

// Helper functions
const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

const getCategoryName = (slug) => {
  const category = categories.value.find((cat) => cat.slug === slug);
  return category ? category.name : slug;
};

// API functions
const fetchCategories = async () => {
  try {
    const res = await axios.get("/marketplace/categories/");
    categories.value = res.data.results || res.data;
  } catch (err) {
    console.error("Failed to fetch categories:", err);
  }
};

const fetchProducts = async (page = 1) => {
  loading.value = true;
  try {
    const params = {
      page,
      search: search.value,
      ordering: selectedOrdering.value,
    };

    if (selectedCategory.value) {
      params["category"] = selectedCategory.value;
    }

    const res = await axios.get("/marketplace/products/", { params });
    products.value = res.data.results;
    next.value = res.data.next;
    previous.value = res.data.previous;
    currentPage.value = page;
  } catch (err) {
    console.error("Error fetching products:", err);
    products.value = [];
  } finally {
    loading.value = false;
  }
};

const handleProductClick = async (product) => {
  clickingProduct.value = product.id;

  try {
    // Register the click
    await axios.post(`/marketplace/products/${product.id}/click/`);
    showSuccessToast.value = true;
    setTimeout(() => {
      showSuccessToast.value = false;
    }, 4000);

    // Open affiliate URL in new tab
    window.open(product.affiliate_url, "_blank");
  } catch (err) {
    console.error("Error registering click:", err);
  } finally {
    clickingProduct.value = null;
  }
};

// Filter management
const clearAllFilters = () => {
  search.value = "";
  selectedCategory.value = "";
  selectedOrdering.value = "-created_at";
};

// Pagination controls
const nextPage = () => {
  if (next.value) {
    fetchProducts(currentPage.value + 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

const prevPage = () => {
  if (previous.value) {
    fetchProducts(currentPage.value - 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

// Lifecycle and watchers
onMounted(() => {
  fetchCategories();
  fetchProducts();
});

// Watch filters and refetch products
watch([search, selectedCategory, selectedOrdering], () => {
  fetchProducts(1);
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3) translate(20px, 20px);
    opacity: 0;
  }
  50% {
    transform: scale(1.05) translate(0, 0);
  }
  70% {
    transform: scale(0.9) translate(0, 0);
  }
  100% {
    transform: scale(1) translate(0, 0);
    opacity: 1;
  }
}

.animate-bounce-in {
  animation: bounce-in 0.6s ease-out;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom gradient text */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

/* Enhanced hover effects */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

.group:hover .group-hover\:translate-x-1 {
  transform: translateX(0.25rem);
}
</style>
