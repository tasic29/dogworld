<template>
  <div
    class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-12 px-4"
  >
    <div class="max-w-md mx-auto">
      <!-- Decorative welcome paw prints -->
      <div class="text-center mb-6">
        <div class="flex justify-center space-x-3 mb-4">
          <span class="text-amber-400 text-3xl animate-pulse">🐕</span>
          <span class="text-orange-400 text-2xl animate-pulse delay-100"
            >🦴</span
          >
          <span class="text-amber-500 text-3xl animate-pulse delay-200"
            >🐕</span
          >
        </div>
      </div>

      <div
        class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-amber-200 p-8 dark:bg-slate-800/90 dark:border-slate-700"
      >
        <!-- Header with welcome back theme -->
        <div class="text-center mb-8">
          <div
            class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full mb-4 shadow-lg transform hover:scale-105 transition-transform duration-300"
          >
            <span class="text-3xl">🏠</span>
          </div>
          <h2
            class="text-3xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300 mb-2"
          >
            Welcome Back!
          </h2>
          <p class="text-gray-600 dark:text-gray-300">
            The pack missed you! Let's get you back home 🐾
          </p>
        </div>

        <form @submit.prevent="submitForm" class="space-y-6">
          <!-- Email Field -->
          <div class="group">
            <label
              for="email"
              class="flex items-center text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
            >
              <span class="mr-2">📧</span>
              Email Address
            </label>
            <div class="relative">
              <input
                v-model="form.email"
                type="email"
                id="email"
                class="w-full px-4 py-3 pl-12 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="your.email@dogworld.com"
                required
              />
              <div class="absolute inset-y-0 left-0 flex items-center pl-4">
                <span class="text-amber-500 text-lg">📮</span>
              </div>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-amber-400">🐕‍🦺</span>
              </div>
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
                class="w-full px-4 py-3 pl-12 border-2 border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
                placeholder="Enter your secret password..."
                required
              />
              <div class="absolute inset-y-0 left-0 flex items-center pl-4">
                <span class="text-amber-500 text-lg">🔑</span>
              </div>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-amber-400">🛡️</span>
              </div>
            </div>
          </div>

          <!-- Error Messages -->
          <div
            v-if="form.errors.length"
            class="bg-red-50 border border-red-200 rounded-xl p-4 dark:bg-red-900/20 dark:border-red-800"
          >
            <div
              v-for="error in form.errors"
              :key="error"
              class="text-red-600 dark:text-red-400 text-sm flex items-center"
            >
              <span class="mr-2">🚨</span>
              {{ error }}
            </div>
          </div>

          <!-- Login Button -->
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
                <span>Coming home...</span>
                <span class="ml-2">🏃‍♂️</span>
              </div>
            </template>
            <div v-else class="flex items-center justify-center">
              <span class="mr-2">🏠</span>
              <span>Welcome Home!</span>
              <span class="ml-2">🐕</span>
            </div>

            <!-- Button hover effect -->
            <div
              class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity duration-300"
            ></div>
          </button>

          <!-- Forgot Password Link -->
          <div class="text-center">
            <a
              href="#"
              class="text-amber-600 hover:text-amber-700 text-sm font-medium transition-colors duration-300 dark:text-amber-400 dark:hover:text-amber-300 flex items-center justify-center"
            >
              <span class="mr-1">🤔</span>
              Forgot your password?
            </a>
          </div>
        </form>

        <!-- Footer with signup link -->
        <div class="mt-8 text-center">
          <div class="flex items-center justify-center space-x-2 mb-4">
            <div class="h-px bg-amber-200 flex-1 dark:bg-slate-600"></div>
            <span class="text-gray-500 text-sm px-3 dark:text-gray-400"
              >or</span
            >
            <div class="h-px bg-amber-200 flex-1 dark:bg-slate-600"></div>
          </div>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            New to the neighborhood?
            <router-link
              to="/signup"
              class="text-amber-600 hover:text-amber-700 font-semibold transition-colors duration-300 dark:text-amber-400 dark:hover:text-amber-300"
            >
              Join our pack! 🐕‍🦺
            </router-link>
          </p>
        </div>
      </div>

      <!-- Bottom decorative elements -->
      <div class="text-center mt-8">
        <div class="flex justify-center items-center space-x-2">
          <span class="text-amber-400 text-sm animate-bounce">🐾</span>
          <span class="text-gray-400 text-xs dark:text-gray-500"
            >Safe & Secure Login</span
          >
          <span class="text-amber-400 text-sm animate-bounce delay-300"
            >🐾</span
          >
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
  email: "",
  password: "",
  errors: [],
});

const isSubmitting = ref(false);

const submitForm = async () => {
  form.errors = []; // Clear previous errors
  isSubmitting.value = true;

  try {
    await authStore.login({
      email: form.email,
      password: form.password,
    });
    toast.success("Welcome home! You're back in the pack! 🐶🏠");
    router.push("/");
  } catch (error) {
    form.errors = error.response?.data?.non_field_errors || [
      "Login failed - wrong credentials? 🐕",
    ];
    toast.error(`${form.errors[0]} 🐾`);
  } finally {
    isSubmitting.value = false;
  }
};
</script>
