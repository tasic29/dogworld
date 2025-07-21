<template>
  <nav
    class="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-100 border-b-4 border-amber-300 py-3 dark:bg-gradient-to-r dark:from-slate-800 dark:via-slate-900 dark:to-slate-800 dark:border-amber-600 transition-all duration-300 shadow-lg"
  >
    <div
      class="flex flex-wrap items-center justify-between max-w-screen-xl px-4 mx-auto"
    >
      <!-- Logo Section with Paw Prints -->
      <router-link :to="{ name: 'home' }" class="flex items-center group">
        <div class="relative">
          <img
            :src="logo"
            alt="Dogworld Logo"
            class="h-12 w-auto rounded-full border-2 border-amber-300 group-hover:border-amber-400 transition-all duration-300"
          />
          <!-- Animated paw print -->
          <div class="absolute -top-1 -right-1 text-amber-600 animate-bounce">
            🐾
          </div>
        </div>
        <span
          class="ml-3 text-2xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300 hover:scale-105 transition-transform duration-300"
        >
          DOGWORLD
        </span>
        <!-- Floating paw prints -->
        <div class="hidden lg:flex ml-2 space-x-1">
          <span class="text-amber-500 text-sm animate-pulse">🐾</span>
          <span class="text-orange-500 text-xs animate-pulse delay-75">🐾</span>
        </div>
      </router-link>

      <!-- Right side buttons -->
      <div class="flex items-center lg:order-2">
        <!-- Sign up button with dog theme -->
        <router-link
          :to="{ name: 'signup' }"
          class="relative overflow-hidden text-white bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 focus:ring-4 focus:ring-amber-300 font-semibold rounded-full text-sm px-6 py-3 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl dark:from-amber-600 dark:to-orange-600 dark:hover:from-amber-700 dark:hover:to-orange-700 dark:focus:ring-amber-500"
        >
          <span class="relative z-10 flex items-center">
            🦴 Join the Pack
          </span>
          <!-- Hover effect overlay -->
          <div
            class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity duration-300"
          ></div>
        </router-link>

        <!-- Mobile menu button -->
        <button
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          type="button"
          class="inline-flex items-center p-3 ml-3 text-amber-600 rounded-full lg:hidden hover:bg-amber-100 focus:outline-none focus:ring-2 focus:ring-amber-300 dark:text-amber-300 dark:hover:bg-slate-700 dark:focus:ring-amber-500 transition-all duration-300"
          aria-controls="mobile-menu-2"
          :aria-expanded="isMobileMenuOpen.toString()"
        >
          <span class="sr-only">Open main menu</span>
          <!-- Hamburger with dog bone style -->
          <div class="relative w-6 h-6">
            <div v-if="!isMobileMenuOpen" class="space-y-1.5">
              <div class="w-6 h-1 bg-amber-600 rounded-full"></div>
              <div class="w-6 h-1 bg-amber-600 rounded-full"></div>
              <div class="w-6 h-1 bg-amber-600 rounded-full"></div>
            </div>
            <svg
              v-else
              class="w-6 h-6 text-amber-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </button>
      </div>

      <!-- Navigation menu -->
      <div
        :class="[
          'items-center justify-between w-full lg:flex lg:w-auto lg:order-1 transition-all duration-300',
          isMobileMenuOpen ? 'block animate-slideDown' : 'hidden',
        ]"
        id="mobile-menu-2"
      >
        <ul
          class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-2 lg:mt-0 bg-white lg:bg-transparent rounded-lg lg:rounded-none shadow-lg lg:shadow-none dark:bg-slate-800 lg:dark:bg-transparent"
        >
          <li>
            <router-link
              :to="{ name: 'home' }"
              class="flex items-center py-3 px-4 text-amber-700 bg-amber-100 rounded-lg lg:bg-transparent lg:text-amber-600 font-semibold hover:bg-amber-200 lg:hover:bg-amber-100 lg:rounded-full transition-all duration-300 dark:text-amber-300 lg:dark:hover:bg-slate-700"
              aria-current="page"
            >
              🏠 Home
            </router-link>
          </li>
          <li>
            <a
              href="#"
              class="flex items-center py-3 px-4 text-gray-700 hover:bg-amber-100 lg:hover:bg-amber-100 lg:rounded-full lg:hover:text-amber-700 transition-all duration-300 dark:text-gray-300 dark:hover:bg-slate-700 dark:hover:text-amber-300"
            >
              📝 Blog
            </a>
          </li>
          <li>
            <a
              href="#"
              class="flex items-center py-3 px-4 text-gray-700 hover:bg-amber-100 lg:hover:bg-amber-100 lg:rounded-full lg:hover:text-amber-700 transition-all duration-300 dark:text-gray-300 dark:hover:bg-slate-700 dark:hover:text-amber-300"
            >
              📸 Posts
            </a>
          </li>
          <li>
            <a
              href="#"
              class="flex items-center py-3 px-4 text-gray-700 hover:bg-amber-100 lg:hover:bg-amber-100 lg:rounded-full lg:hover:text-amber-700 transition-all duration-300 dark:text-gray-300 dark:hover:bg-slate-700 dark:hover:text-amber-300"
            >
              🛒 Marketplace
            </a>
          </li>
          <li>
            <a
              href="#"
              class="flex items-center py-3 px-4 text-gray-700 hover:bg-amber-100 lg:hover:bg-amber-100 lg:rounded-full lg:hover:text-amber-700 transition-all duration-300 dark:text-gray-300 dark:hover:bg-slate-700 dark:hover:text-amber-300"
            >
              🐕‍🦺 Services
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from "vue";
import logo from "../assets/logo.webp";

const isMobileMenuOpen = ref(false);
</script>

<style scoped>
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideDown {
  animation: slideDown 0.3s ease-out;
}

/* Custom paw print animation */
@keyframes pawBounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}
</style>
