<template>
  <section class="min-h-screen bg-gray-100 dark:bg-slate-900 py-12 px-4">
    <div
      class="max-w-4xl mx-auto bg-white dark:bg-slate-800 rounded-3xl shadow-xl overflow-hidden"
      v-if="loading"
    >
      <div class="p-8 text-center text-gray-500 dark:text-gray-400">
        Loading product details...
      </div>
    </div>

    <div
      v-else-if="product"
      class="max-w-4xl mx-auto bg-white dark:bg-slate-800 rounded-3xl shadow-xl overflow-hidden"
    >
      <div class="flex flex-col md:flex-row">
        <div
          class="md:w-1/2 p-6 flex items-center justify-center bg-gray-50 dark:bg-slate-700"
        >
          <img
            :src="product.image"
            :alt="product.title"
            class="max-w-full h-auto max-h-96 rounded-2xl shadow-lg object-contain"
          />
        </div>

        <div class="md:w-1/2 p-8 flex flex-col justify-center">
          <h1
            class="text-4xl font-extrabold text-gray-900 dark:text-white mb-4 leading-tight"
          >
            {{ product.title }}
          </h1>

          <p class="text-xl text-gray-700 dark:text-gray-300 mb-6">
            {{ product.description }}
          </p>

          <div
            class="flex items-center justify-between border-t border-gray-200 dark:border-slate-700 pt-6 mt-6"
          >
            <p class="text-3xl font-bold text-amber-600 dark:text-amber-400">
              ${{ product.price }}
            </p>
            <a
              :href="product.affiliate_url"
              class="inline-flex items-center px-8 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
              target="_blank"
              rel="noopener noreferrer"
            >
              🛒 Buy Now
            </a>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else
      class="max-w-4xl mx-auto bg-white dark:bg-slate-800 rounded-3xl shadow-xl"
    >
      <div class="p-8 text-center text-gray-500 dark:text-gray-400">
        Product not found.
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const product = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await axios.get(`/marketplace/products/${route.params.slug}/`);
    product.value = res.data;
  } catch (err) {
    console.error("Failed to fetch product:", err);
  } finally {
    loading.value = false;
  }
});
</script>
