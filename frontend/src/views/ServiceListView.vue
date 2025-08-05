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
            🐕 Find Pet Services
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Discover trusted services for your furry friends
          </p>
        </div>

        <div class="flex items-center gap-3">
          <router-link
            v-if="isStaff"
            :to="{ name: 'service-create' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            Create Service
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
              placeholder="Search for services..."
              class="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none focus:ring-4 focus:ring-amber-200/50 bg-white/90 dark:bg-slate-700/90 transition-all duration-200"
            />
          </div>

          <select
            v-model="selectedType"
            class="px-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none bg-white/90 dark:bg-slate-700/90 min-w-48"
          >
            <option value="">🏷️ All Types</option>
            <option
              v-for="(label, key) in SERVICE_TYPES"
              :key="key"
              :value="key"
            >
              {{ label }}
            </option>
          </select>

          <input
            v-model="selectedCity"
            type="text"
            placeholder="🏙️ City"
            class="px-4 py-3 rounded-xl border-2 border-amber-200 focus:border-amber-400 focus:outline-none bg-white/90 dark:bg-slate-700/90 min-w-48"
          />
        </div>
      </div>

      <!-- Services Grid/List -->
      <div
        v-if="services.length"
        :class="
          viewMode === 'grid'
            ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10'
            : 'space-y-8'
        "
      >
        <div
          v-for="service in services"
          :key="service.id"
          class="rounded-2xl overflow-hidden shadow-xl flex flex-col bg-amber-100/40 dark:bg-slate-700/60 border border-orange-200 dark:border-slate-700 hover:border-amber-400 transition-all duration-300 transform hover:scale-105"
        >
          <!-- Image -->
          <div class="relative">
            <div
              class="flex items-center justify-center p-4 h-60 bg-white dark:bg-white"
            >
              <img
                v-if="service.image"
                :src="service.image"
                alt="Service"
                class="w-auto h-auto max-w-full max-h-full object-contain rounded-2xl"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-100 to-orange-100 dark:from-slate-600 dark:to-slate-700"
              >
                <span class="text-6xl opacity-50">🐶</span>
              </div>
            </div>
          </div>

          <!-- Content -->
          <div class="px-6 py-4 mb-auto">
            <h2
              class="cursor-default font-semibold text-xl inline-block text-amber-700 dark:text-amber-300 mb-2"
            >
              {{ service.name }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">
              {{ service.city }} • {{ SERVICE_TYPES[service.service_type] }}
            </p>
            <p class="text-gray-600 dark:text-gray-300 text-sm line-clamp-3">
              {{ service.description }}
            </p>
          </div>

          <!-- Website Link -->
          <div
            class="px-6 py-4 flex justify-between items-center bg-amber-100/40 dark:bg-slate-700/60 rounded-b-2xl"
          >
            <a
              :href="service.website_url"
              target="_blank"
              class="text-sm font-medium text-amber-600 dark:text-amber-400 hover:underline"
            >
              🌐 Visit Website →
            </a>
          </div>
        </div>
      </div>

      <!-- No Services -->
      <div v-else-if="!loading" class="text-center py-16">
        <div class="text-8xl mb-4">🐾</div>
        <h3 class="text-2xl font-bold text-gray-600 dark:text-gray-400 mb-2">
          No services found
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
import { useToast } from "vue-toastification";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const toast = useToast();
const authStore = useAuthStore();
const isStaff = computed(() => authStore.user?.is_staff);
const loading = ref(false);

const SERVICE_TYPES = {
  vet: "Veterinarian",
  grooming: "Grooming",
  walking: "Dog Walking",
  boarding: "Boarding / Pet Sitting",
  training: "Training",
  breeding: "Breeding",
  nutrition: "Nutrition / Diet Consultation",
  insurance: "Pet Insurance",
  photography: "Pet Photography",
  transport: "Pet Transport",
  other: "Other",
};

const services = ref([]);
const search = ref("");
const selectedType = ref("");
const selectedCity = ref("");
const viewMode = ref("grid");
const next = ref(null);
const previous = ref(null);
const currentPage = ref(1);

const activeBtnClass = "px-3 py-2 bg-amber-500 text-white rounded-md shadow";
const inactiveBtnClass =
  "px-3 py-2 bg-white dark:bg-slate-700 border border-amber-300 text-amber-600 dark:text-amber-300 rounded-md";

// API fetcher
const fetchServices = async (page = 1) => {
  loading.value = true;
  try {
    const params = {
      page,
      search: search.value,
      service_type: selectedType.value,
      city: selectedCity.value,
      ordering: "name",
    };
    const res = await axios.get("/services/", { params });
    services.value = res.data.results;
    next.value = res.data.next;
    previous.value = res.data.previous;
    currentPage.value = page;
  } catch (err) {
    toast.error("Failed to load services.");
  } finally {
    loading.value = false;
  }
};

const nextPage = () => {
  if (next.value) fetchServices(currentPage.value + 1);
};
const prevPage = () => {
  if (previous.value) fetchServices(currentPage.value - 1);
};

onMounted(() => fetchServices());
watch([search, selectedType, selectedCity], () => fetchServices(1));
</script>
