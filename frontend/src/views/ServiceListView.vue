<template>
  <section
    class="py-12 px-4 bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 min-h-screen"
  >
    <div class="max-w-6xl mx-auto">
      <header class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300">
          Find Pet Services
        </h1>
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
      </header>

      <div class="flex flex-wrap gap-4 mb-6">
        <input
          v-model="search"
          placeholder="Search..."
          class="px-4 py-2 rounded-lg border border-amber-300 focus:ring-2 focus:ring-amber-400"
        />
        <select
          v-model="selectedType"
          class="px-4 py-2 rounded-lg border border-amber-300"
        >
          <option value="">All Types</option>
          <option v-for="(label, key) in SERVICE_TYPES" :key="key" :value="key">
            {{ label }}
          </option>
        </select>
        <input
          v-model="selectedCity"
          placeholder="City..."
          class="px-4 py-2 rounded-lg border border-amber-300"
        />
      </div>

      <div
        v-if="services.length"
        :class="viewMode === 'grid' ? 'grid md:grid-cols-2 gap-6' : 'space-y-6'"
      >
        <div
          v-for="service in services"
          :key="service.id"
          class="bg-white/80 dark:bg-slate-800 rounded-xl p-6 shadow-lg hover:shadow-2xl transition"
        >
          <img
            v-if="service.image"
            :src="service.image"
            alt="Service"
            class="w-full h-32 object-cover rounded-lg mb-4 shadow"
          />
          <h2 class="text-xl font-semibold text-amber-700 dark:text-amber-300">
            {{ service.name }}
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ service.city }} • {{ SERVICE_TYPES[service.service_type] }}
          </p>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
            {{ service.description }}
          </p>
          <a
            :href="service.website_url"
            target="_blank"
            class="mt-2 block text-amber-600 dark:text-amber-400 hover:underline text-sm"
            >Visit website →</a
          >
        </div>
      </div>

      <p v-else class="text-center text-gray-500 dark:text-gray-400">
        No services found.
      </p>

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
    console.error("Error fetching services:", err);
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
