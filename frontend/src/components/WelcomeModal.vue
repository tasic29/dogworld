<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
  >
    <div
      class="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-md p-6 text-center transform transition-all duration-300 scale-100"
    >
      <img
        src="../assets/pawprint.webp"
        alt="Dog Avatar"
        class="w-16 h-16 mx-auto mb-4 animate-bounce"
      />
      <h2 class="text-2xl font-bold text-emerald-600 dark:text-white mb-2">
        Welcome to DogWorld!
      </h2>
      <p class="text-sm text-gray-600 dark:text-gray-300 mb-6">
        Find your furry friend 🐕
      </p>
      <button
        @click="closeModal"
        class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 px-4 rounded-full transition"
      >
        Let's Go!
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

const show = ref(true);
const router = useRouter();

const closeModal = () => {
  show.value = false;
  router.push("/");
};
</script>
