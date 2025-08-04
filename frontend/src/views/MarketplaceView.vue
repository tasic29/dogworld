<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300">
          Marketplace
        </h1>

        <!-- View Toggle -->
        <div class="flex items-center gap-2">
          <router-link
            v-if="isStaff"
            :to="{ name: 'product-create' }"
            class="bg-white text-amber-600 border border-amber-500 hover:bg-amber-100 font-bold py-3 px-6 rounded-full shadow transition"
          >
            Create Product
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
      <div class="flex flex-wrap items-center gap-4 mb-6">
        <!-- Search -->
        <input
          v-model="search"
          type="text"
          placeholder="Search products..."
          class="px-4 py-2 rounded-lg border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
        />

        <!-- Category Filter -->
        <select
          v-model="selectedCategory"
          class="px-4 py-2 rounded-lg border border-amber-300"
        >
          <option value="">All Categories</option>
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
          class="px-4 py-2 rounded-lg border border-amber-300"
        >
          <option value="-created_at">Newest</option>
          <option value="created_at">Oldest</option>
          <option value="title">Title A–Z</option>
          <option value="-title">Title Z–A</option>
          <option value="price">Price: Low to High</option>
          <option value="-price">Price: High to Low</option>
        </select>
      </div>

      <!-- Products Grid/List -->
      <div v-if="loading" class="text-center py-12">
        <div
          class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"
        ></div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Loading products...</p>
      </div>

      <div
        v-else-if="products.length"
        :class="viewMode === 'grid' ? 'grid md:grid-cols-2 gap-6' : 'space-y-6'"
      >
        <div
          v-for="product in products"
          :key="product.id"
          class="bg-white/80 dark:bg-slate-800 rounded-xl p-6 shadow-lg hover:shadow-2xl transition flex flex-col md:flex-row gap-4"
          :class="viewMode === 'grid' ? '' : 'md:items-center'"
        >
          <!-- Product Image -->
          <img
            v-if="product.image"
            :src="product.image"
            alt="Product preview"
            class="w-full md:w-48 h-32 object-cover rounded-lg shadow"
          />

          <div>
            <h2
              class="text-xl font-semibold text-amber-700 dark:text-amber-300"
            >
              {{ product.title }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              ${{ product.price }} • {{ formatDate(product.created_at) }}
            </p>

            <p
              v-if="product.description"
              class="text-gray-600 dark:text-gray-300 text-sm mt-2 line-clamp-3"
            >
              {{ product.description }}
            </p>

            <!-- Category -->
            <div v-if="product.category" class="mt-2">
              <span
                class="inline-block px-2 py-1 text-xs rounded-full bg-amber-100 dark:bg-slate-700 text-amber-700 dark:text-amber-300 font-medium"
              >
                📂 {{ product.category.name }}
              </span>
            </div>

            <button
              @click="handleProductClick(product)"
              :disabled="clickingProduct === product.id"
              class="inline-block mt-2 text-amber-600 dark:text-amber-400 hover:underline text-sm"
            >
              <span v-if="clickingProduct === product.id">Processing...</span>
              <span v-else>View Product →</span>
            </button>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <p
        v-else-if="!loading"
        class="text-center text-gray-500 dark:text-gray-400"
      >
        No products found.
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

    <!-- Success Toast -->
    <div
      v-if="showSuccessToast"
      class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-bounce"
    >
      ✅ Product click registered successfully!
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

// Classes
const activeBtnClass = "px-3 py-2 bg-amber-500 text-white rounded-md shadow";
const inactiveBtnClass =
  "px-3 py-2 bg-white dark:bg-slate-700 border border-amber-300 text-amber-600 dark:text-amber-300 rounded-md";

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
    }, 3000);

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

@keyframes bounce {
  0%,
  20%,
  53%,
  80%,
  100% {
    transform: translate3d(0, 0, 0);
  }
  40%,
  43% {
    transform: translate3d(0, -30px, 0);
  }
  70% {
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
}

.animate-bounce {
  animation: bounce 1s ease-in-out;
}
</style>
