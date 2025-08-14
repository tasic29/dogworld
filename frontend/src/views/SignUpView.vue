<template>
  <div
    class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-12 px-4"
  >
    <div class="max-w-md mx-auto">
      <!-- Decorative paw prints -->
      <!-- <div class="text-center mb-6">
        <div class="flex justify-center space-x-2 mb-4">
          <span class="text-amber-400 text-2xl animate-bounce">🐾</span>
          <span class="text-orange-400 text-xl animate-bounce delay-75"
            >🐾</span
          >
          <span class="text-amber-500 text-lg animate-bounce delay-150"
            >🐾</span
          >
        </div>
      </div> -->

      <div
        class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-amber-200 p-8 dark:bg-slate-800/90 dark:border-slate-700"
      >
        <!-- Header with dog theme -->
        <div class="text-center mb-8">
          <div
            class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full mb-4 shadow-lg"
          >
            <span class="text-2xl">🦴</span>
          </div>
          <h2
            class="text-3xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300 animate-bounce delay-100"
          >
            Join the Pack!
          </h2>
          <!-- <p class="text-gray-600 dark:text-gray-300 mt-2">
            Create your DOGWORLD account and start your tail-wagging journey
          </p> -->
        </div>

        <form @submit.prevent="submitForm" class="space-y-6">
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
                class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="Choose your pack name..."
                required
              />
              <!-- <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-amber-400">🐕</span>
              </div> -->
            </div>
            <div
              v-if="errors.username"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.username }}
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
                required
              />
              <!-- <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-amber-400">📮</span>
              </div> -->
            </div>
            <div
              v-if="errors.email"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.email }}
            </div>
          </div>

          <!-- Password Field -->
          <div class="group">
            <label
              for="password"
              class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
            >
              <span class="mr-2">🔒</span>
              Password
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                type="password"
                id="password"
                class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="Create a strong password..."
                required
              />
              <!-- <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-amber-400">🛡️</span>
              </div> -->
            </div>
            <div
              v-if="errors.password"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.password }}
            </div>
          </div>

          <!-- Confirm Password Field -->
          <div class="group">
            <label
              for="password2"
              class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
            >
              <span class="mr-2">🔐</span>
              Confirm Password
            </label>
            <div class="relative">
              <input
                v-model="form.password2"
                type="password"
                id="password2"
                class="w-full px-4 py-3 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="Confirm your password..."
                required
              />
              <!-- <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-amber-400">✅</span>
              </div> -->
            </div>
            <div
              v-if="errors.password2"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.password2 }}
            </div>
            <div
              v-if="errors.non_field_errors"
              class="mt-2 text-sm text-red-500 flex items-center"
            >
              <span class="mr-1">⚠️</span>
              {{ errors.non_field_errors }}
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full relative overflow-hidden bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-amber-300 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none dark:from-amber-600 dark:to-orange-600 dark:hover:from-amber-700 dark:hover:to-orange-700"
            :disabled="isSubmitting"
          >
            <template v-if="isSubmitting">
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
                <span>Joining the pack...</span>
                <span class="ml-2">🐕‍🦺</span>
              </div>
            </template>
            <div v-else class="flex items-center justify-center">
              <span class="mr-2">🦴</span>
              <span>Join the Pack!</span>
              <span class="ml-2">🐾</span>
            </div>

            <!-- Button hover effect -->
            <div
              class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity duration-300"
            ></div>
          </button>
        </form>

        <!-- Footer with playful message -->
        <div class="mt-8 text-center">
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            Already part of the pack?
            <router-link
              to="/login"
              class="text-amber-600 hover:text-amber-700 font-semibold transition-colors duration-300 dark:text-amber-400 dark:hover:text-amber-300"
            >
              Login here! 🐕‍🦺
            </router-link>
          </p>
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
import { reactive, ref } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const toast = useToast();
const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  username: "",
  email: "",
  password: "",
  password2: "",
});

const errors = ref({});
const isSubmitting = ref(false);

const clearErrors = () => {
  errors.value = {};
};

const submitForm = async () => {
  clearErrors();

  if (form.password !== form.password2) {
    toast.error("Passwords do not match 🐾");
    return;
  }

  isSubmitting.value = true;
  try {
    const response = await axios.post("/auth/users/", {
      username: form.username,
      email: form.email,
      password: form.password,
      re_password: form.password2,
    });

    console.log("Registration successful:", response.data);

    await authStore.login({
      email: form.email,
      password: form.password,
    });

    // Clear form
    Object.keys(form).forEach((key) => {
      form[key] = "";
    });

    toast.success("Welcome to the pack! Account created and logged in! 🐶");
    router.push("account");
  } catch (error) {
    console.error("Registration error:", error);

    if (error.response && error.response.data) {
      // Handle validation errors from Django/DRF
      const errorData = error.response.data;
      console.log("Error data:", errorData);

      if (typeof errorData === "object") {
        // Set field-specific errors
        errors.value = errorData;

        // Show specific error messages with dog emojis
        Object.keys(errorData).forEach((field) => {
          const fieldError = Array.isArray(errorData[field])
            ? errorData[field][0]
            : errorData[field];
          toast.error(`${field}: ${fieldError} 🐕`);
        });
      } else {
        toast.error("Registration failed. Please try again. 🐾");
      }
    } else if (error.response) {
      toast.error(`Server error: ${error.response.status} 🦮`);
    } else if (error.request) {
      toast.error("Network error. Please check your connection. 🐕‍🦺");
    } else {
      toast.error("Something went wrong, but don't worry! 🐾");
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
