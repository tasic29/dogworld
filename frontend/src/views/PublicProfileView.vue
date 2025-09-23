<template>
  <div
    class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-12 px-4"
  >
    <div class="max-w-2xl mx-auto">
      <div
        class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-amber-200 p-8 dark:bg-slate-800/90 dark:border-slate-700"
      >
        <!-- Header -->
        <div class="text-center mb-8">
          <div
            class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full mb-4 shadow-lg"
          >
            <img
              v-if="user.profile_image"
              :src="user.profile_image"
              alt="Profile Image"
              class="w-16 h-16 rounded-full object-cover"
            />
          </div>
          <h2
            class="text-3xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300"
          >
            {{ user.full_name || "Pack Member" }}
          </h2>
          <p class="text-gray-600 dark:text-gray-300 mt-1">
            @{{ user.username }}
          </p>
        </div>

        <!-- User Info Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="space-y-1">
            <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400">
              📧 Email
            </h3>
            <p class="text-lg text-gray-800 dark:text-gray-200">
              {{ user.email }}
            </p>
          </div>

          <div class="space-y-1">
            <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400">
              📍 Location
            </h3>
            <p class="text-lg text-gray-800 dark:text-gray-200">
              {{ user.location || "Unknown" }}
            </p>
          </div>

          <div class="space-y-1">
            <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400">
              🗓️ Joined
            </h3>
            <p class="text-lg text-gray-800 dark:text-gray-200">
              {{ formatDate(user.date_joined) }}
            </p>
          </div>

          <div class="space-y-1">
            <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400">
              🏆 Status
            </h3>
            <p class="text-lg text-gray-800 dark:text-gray-200">
              {{ user.is_active ? "Active Member" : "Inactive" }}
            </p>
          </div>
        </div>

        <!-- Messaging Button -->
        <div class="mt-10 text-center">
          <router-link
            :to="{ name: 'messages' }"
            class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-xl shadow transition transform hover:scale-105"
          >
            📬 Go to Messages
          </router-link>
        </div>
      </div>

      <!-- Decorative Paws -->
      <div class="text-center mt-10">
        <div class="flex justify-center space-x-4 opacity-30">
          <span class="text-amber-400 text-sm">🐾</span>
          <span class="text-orange-400 text-xs">🐾</span>
          <span class="text-amber-500 text-sm">🐾</span>
          <span class="text-orange-500 text-xs">🐾</span>
          <span class="text-amber-400 text-sm">🐾</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { useToast } from "vue-toastification";

const route = useRoute();
const toast = useToast();

const user = ref({});
const username = route.params.username;

const formatDate = (dateString) => {
  if (!dateString) return "Unknown";
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const loadUser = async () => {
  try {
    const response = await axios.get(`/users/${username}/`);
    user.value = response.data;
  } catch (error) {
    console.error("Failed to load user profile", error);
    toast.error("Could not load profile 🐾");
  }
};

onMounted(() => {
  loadUser();
});
</script>
