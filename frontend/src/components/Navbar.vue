<template>
  <nav class="bg-white border-gray-200 py-2.5 dark:bg-gray-900 transition-all">
    <div
      class="flex flex-wrap items-center justify-between max-w-screen-xl px-4 mx-auto"
    >
      <router-link :to="{ name: 'home' }" class="flex items-center">
        <img :src="logo" alt="Dogworld Logo" class="h-10 w-auto" />
        <span
          class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
          >DOGWORLD</span
        >
      </router-link>
      <div class="flex items-center lg:order-2">
        <div class="hidden mt-2 mr-4 sm:inline-block">
          <span></span>
        </div>

        <router-link
          :to="{ name: 'signup' }"
          class="text-white bg-emerald-600 hover:bg-emerald-700 focus:ring-4 focus:ring-green-500 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 sm:mr-2 lg:mr-0 dark:bg-purple-600 dark:hover:bg-emerald-600 focus:outline-none dark:focus:ring-purple-800"
          >Sign up</router-link
        >

        <button
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          type="button"
          class="inline-flex items-center p-2 ml-1 text-sm text-gray-600 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
          aria-controls="mobile-menu-2"
          :aria-expanded="isMobileMenuOpen.toString()"
        >
          <span class="sr-only">Open main menu</span>
          <svg
            v-if="!isMobileMenuOpen"
            class="w-6 h-6"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
              clip-rule="evenodd"
            ></path>
          </svg>
          <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </button>
      </div>
      <div
        :class="[
          'items-center justify-between w-full lg:flex lg:w-auto lg:order-1',
          isMobileMenuOpen ? 'block' : 'hidden',
        ]"
        id="mobile-menu-2"
      >
        <ul
          class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0"
        >
          <li>
            <router-link
              :to="{ name: 'home' }"
              class="block py-2 pl-3 pr-4 text-white bg-emerald-600 rounded lg:bg-transparent lg:text-emerald-600 lg:p-0 dark:text-white"
              aria-current="page"
              >Home</router-link
            >
          </li>
          <li>
            <a
              href="#"
              class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-emerald-600 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
              >Blog</a
            >
          </li>
          <li>
            <a
              href="#"
              class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-emerald-600 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
              >Posts</a
            >
          </li>
          <li>
            <a
              href="#"
              class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-emerald-600 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
              >Marketplace</a
            >
          </li>
          <li>
            <a
              href="#"
              class="block py-2 pl-3 pr-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-emerald-600 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
              >Services</a
            >
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
