<template>
  <div
    class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-12 px-4"
  >
    <div class="max-w-2xl mx-auto">
      <div
        class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-amber-200 p-8 dark:bg-slate-800/90 dark:border-slate-700"
      >
        <!-- Header with dog theme -->
        <div class="text-center mb-8">
          <div
            class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full mb-4 shadow-lg"
          >
            <span class="text-2xl">🐕‍🦺</span>
          </div>
          <h2
            class="text-3xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300 animate-bounce delay-100"
          >
            Pack Member Profile
          </h2>
          <p class="text-gray-600 dark:text-gray-300 mt-2">
            Update your pack information and preferences
          </p>
        </div>

        <!-- Profile Form -->
        <form @submit.prevent="updateProfile" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- First Name Field -->
            <div class="group">
              <label
                for="firstName"
                class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
              >
                <span class="mr-2">🐾</span>
                First Name
              </label>
              <div class="relative">
                <input
                  v-model="form.first_name"
                  type="text"
                  id="firstName"
                  class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                  placeholder="Your first name..."
                />
              </div>
              <div
                v-if="errors.first_name"
                class="mt-2 text-sm text-red-500 flex items-center"
              >
                <span class="mr-1">⚠️</span>
                {{ errors.first_name }}
              </div>
            </div>

            <!-- Last Name Field -->
            <div class="group">
              <label
                for="lastName"
                class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
              >
                <span class="mr-2">🐕</span>
                Last Name
              </label>
              <div class="relative">
                <input
                  v-model="form.last_name"
                  type="text"
                  id="lastName"
                  class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                  placeholder="Your last name..."
                />
              </div>
              <div
                v-if="errors.last_name"
                class="mt-2 text-sm text-red-500 flex items-center"
              >
                <span class="mr-1">⚠️</span>
                {{ errors.last_name }}
              </div>
            </div>
          </div>

          <!-- Username Field -->
          <div class="group">
            <label
              for="username"
              class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
            >
              <span class="mr-2">👤</span>
              Username
            </label>
            <div class="relative">
              <input
                v-model="form.username"
                type="text"
                id="username"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl bg-gray-100 dark:bg-slate-600 dark:border-slate-500 dark:text-gray-300"
              />
            </div>
          </div>

          <!-- Email Field -->
          <div class="group">
            <label
              for="email"
              class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
            >
              <span class="mr-2">📧</span>
              Email
            </label>
            <div class="relative">
              <input
                v-model="form.email"
                type="email"
                id="email"
                class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="your.email@dogworld.com"
              />
            </div>
            <div
              v-if="errors.email"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.email }}
            </div>
          </div>

          <!-- Location Field -->
          <div class="group">
            <label
              for="location"
              class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
            >
              <span class="mr-2">📍</span>
              Location
            </label>
            <div class="relative">
              <input
                v-model="form.location"
                type="text"
                id="location"
                class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="Where's your pack located? (City, Country)"
              />
            </div>
            <div
              v-if="errors.location"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.location }}
            </div>
          </div>

          <!-- Submit Button -->
          <div class="flex flex-col sm:flex-row gap-4 pt-6">
            <button
              type="submit"
              class="flex-1 relative overflow-hidden bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-amber-300 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none dark:from-amber-600 dark:to-orange-600 dark:hover:from-amber-700 dark:hover:to-orange-700"
              :disabled="isUpdating"
            >
              <template v-if="isUpdating">
                <div class="flex items-center justify-center">
                  <svg
                    class="animate-spin h-5 w-5 mr-3 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    />
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                    />
                  </svg>
                  <span>Updating pack info...</span>
                  <span class="ml-2">🐕‍🦺</span>
                </div>
              </template>
              <div v-else class="flex items-center justify-center">
                <span class="mr-2">💾</span>
                <span>Update Profile</span>
                <span class="ml-2">🐾</span>
              </div>

              <!-- Button hover effect -->
              <div
                class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity duration-300"
              ></div>
            </button>

            <button
              type="button"
              @click="loadUserData"
              class="sm:w-auto px-6 py-4 border-2 border-amber-400 text-amber-600 hover:bg-amber-50 font-semibold rounded-xl transition-all duration-300 dark:border-amber-400 dark:text-amber-400 dark:hover:bg-amber-900/20 flex items-center justify-center"
            >
              <span class="mr-2">🔄</span>
              Reset
            </button>
          </div>
        </form>

        <!-- Account Stats/Info Section -->
        <div class="mt-8 pt-8 border-t border-amber-200 dark:border-slate-600">
          <h3
            class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center"
          >
            <span class="mr-2">📊</span>
            Pack Member Info
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="bg-amber-50 dark:bg-slate-700/50 p-4 rounded-xl">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400"
                  >Member Since</span
                >
                <span class="text-amber-600 dark:text-amber-400">🗓️</span>
              </div>
              <div
                class="text-lg font-semibold text-gray-800 dark:text-gray-200"
              >
                {{ formatDate(userInfo.date_joined) }}
              </div>
            </div>
            <div class="bg-orange-50 dark:bg-slate-700/50 p-4 rounded-xl">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400"
                  >Pack Status</span
                >
                <span class="text-orange-600 dark:text-orange-400">🏆</span>
              </div>
              <div
                class="text-lg font-semibold text-gray-800 dark:text-gray-200"
              >
                {{ userInfo.is_active ? "Active Member" : "Inactive" }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom decorative paws -->
      <div class="text-center mt-8">
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
import { reactive, ref, onMounted } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
import { useAuthStore } from "../stores/auth";

const toast = useToast();
const authStore = useAuthStore();

const form = reactive({
  username: "",
  email: "",
  first_name: "",
  last_name: "",
  location: "",
});

const userInfo = ref({
  date_joined: null,
  is_active: true,
});

const errors = ref({});
const isUpdating = ref(false);

const clearErrors = () => {
  errors.value = {};
};

const formatDate = (dateString) => {
  if (!dateString) return "Unknown";
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const loadUserData = async () => {
  try {
    const response = await axios.get("/auth/users/me/");
    const userData = response.data;

    form.username = userData.username || "";
    form.email = userData.email || "";
    form.first_name = userData.first_name || "";
    form.last_name = userData.last_name || "";
    form.location = userData.location || "";

    userInfo.value.date_joined = userData.date_joined;
    userInfo.value.is_active = userData.is_active;

    console.log("User data loaded:", userData);
  } catch (error) {
    console.error("Error loading user data:", error);
    toast.error("Failed to load profile data 🐕");
  }
};

const updateProfile = async () => {
  clearErrors();
  isUpdating.value = true;

  try {
    const updateData = {
      username: form.username,
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      location: form.location,
    };

    const response = await axios.patch("/auth/users/me/", updateData);

    console.log("Profile updated successfully:", response.data);
    toast.success("Pack profile updated successfully! 🐶");

    // Update the auth store if needed
    await authStore.fetchUser();
  } catch (error) {
    console.error("Profile update error:", error);

    if (error.response && error.response.data) {
      const errorData = error.response.data;
      console.log("Error data:", errorData);

      if (typeof errorData === "object") {
        errors.value = errorData;

        Object.keys(errorData).forEach((field) => {
          const fieldError = Array.isArray(errorData[field])
            ? errorData[field][0]
            : errorData[field];
          toast.error(`${field}: ${fieldError} 🐕`);
        });
      } else {
        toast.error("Profile update failed. Please try again. 🐾");
      }
    } else if (error.response) {
      toast.error(`Server error: ${error.response.status} 🦮`);
    } else if (error.request) {
      toast.error("Network error. Please check your connection. 🐕‍🦺");
    } else {
      toast.error("Something went wrong updating your profile! 🐾");
    }
  } finally {
    isUpdating.value = false;
  }
};

onMounted(() => {
  loadUserData();
});
</script>
