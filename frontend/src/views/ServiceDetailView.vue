<template>
  <section
    class="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-12 px-4"
  >
    <div
      class="max-w-4xl mx-auto bg-white/70 dark:bg-slate-800/80 backdrop-blur-md shadow-xl rounded-3xl overflow-hidden border border-amber-200 dark:border-slate-700"
    >
      <div class="p-8">
        <!-- Header -->
        <div class="mb-6">
          <h1
            class="text-4xl font-extrabold text-amber-700 dark:text-amber-300 mb-2"
          >
            {{ service.name }}
          </h1>
          <p class="text-gray-500 dark:text-gray-400 text-sm">
            📍 {{ service.city }} • {{ SERVICE_TYPES[service.service_type] }}
          </p>
        </div>

        <!-- Image -->
        <div class="mb-6">
          <img
            v-if="service.image"
            :src="service.image"
            alt="Service Image"
            class="w-full h-auto max-h-[400px] object-contain rounded-xl border"
          />
          <div
            v-else
            class="w-full h-64 flex items-center justify-center bg-gradient-to-br from-amber-100 to-orange-100 dark:from-slate-700 dark:to-slate-800 rounded-xl"
          >
            <span class="text-6xl opacity-50">🐾</span>
          </div>
        </div>

        <!-- Description -->
        <div class="mb-6">
          <h2
            class="text-xl font-semibold text-amber-600 dark:text-amber-300 mb-2"
          >
            Description
          </h2>
          <p
            class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line"
          >
            {{ service.description }}
          </p>
        </div>

        <!-- Website Button -->
        <div class="mt-8 text-center">
          <button
            @click="handleClick"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            🌐 Visit Website
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useToast } from "vue-toastification";

const toast = useToast();
const route = useRoute();
const service = ref({});

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

const fetchService = async () => {
  try {
    const res = await axios.get(`/services/${route.params.slug}/`);
    service.value = res.data;
  } catch (err) {
    toast.error("Failed to load service.");
  }
};

const handleClick = async () => {
  try {
    await axios.post(`/services/${service.value.slug}/click/`);
  } catch (err) {
    console.warn("Click tracking failed:", err);
  } finally {
    window.open(service.value.website_url, "_blank");
  }
};

onMounted(fetchService);
</script>
