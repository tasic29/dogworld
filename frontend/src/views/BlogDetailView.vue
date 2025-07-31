<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div
        class="lg:col-span-2 bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow-lg hover:shadow-2xl transition p-8"
      >
        <div v-if="blog" class="space-y-6">
          <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300">
            {{ blog.title }}
          </h1>
          <p class="text-gray-500 text-sm dark:text-gray-400">
            By {{ blog.author.username }} • {{ formatDate(blog.created) }}
          </p>
          <img
            v-if="blog.image"
            :src="blog.image"
            alt="Blog image"
            class="rounded-lg w-full object-cover max-h-[500px] shadow"
          />
          <div class="prose dark:prose-invert max-w-none">
            <div v-html="renderedContent"></div>
          </div>

          <div
            v-if="blog.tags && blog.tags.length"
            class="flex flex-wrap gap-2 mt-6"
          >
            <span
              v-for="tag in blog.tags"
              :key="tag.id"
              class="bg-amber-100 text-amber-800 text-sm px-3 py-1 rounded-full dark:bg-slate-700 dark:text-amber-300"
            >
              #{{ tag.name }}
            </span>
          </div>

          <div class="mt-8 pt-8 border-t border-gray-200 dark:border-slate-700">
            <h3
              class="text-lg font-semibold mb-3 text-gray-800 dark:text-gray-200"
            >
              Rate this blog
            </h3>
            <RatingComponent
              :blog-id="blog.id"
              :initial-average="blog.average_rating"
              :initial-count="blog.total_ratings"
              :show-average-rating="true"
              @rating-updated="handleRatingUpdate"
            />
          </div>
        </div>

        <div v-else class="text-center text-gray-500 dark:text-gray-300">
          <div class="animate-pulse">
            <div class="h-8 bg-gray-300 rounded mb-4"></div>
            <div class="h-4 bg-gray-300 rounded mb-2"></div>
            <div class="h-64 bg-gray-300 rounded"></div>
          </div>
        </div>
      </div>

      <div class="space-y-8">
        <div class="bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow-md">
          <CommentComponent type="blog" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import CommentComponent from "../components/CommentComponent.vue";
import RatingComponent from "../components/RatingComponent.vue";
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import MarkdownIt from "markdown-it";

const route = useRoute();
const blog = ref(null);
const md = new MarkdownIt();

const formatDate = (date) =>
  new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

onMounted(async () => {
  try {
    const blogId = route.params.id;
    const { data } = await axios.get(`/content/blogs/${blogId}/`);
    blog.value = data;
  } catch (err) {
    toast.error("Failed to load blog.");
  }
});

const handleRatingUpdate = ({ average, count }) => {
  if (blog.value) {
    blog.value.average_rating = average;
    blog.value.total_ratings = count;
  }
};

const renderedContent = computed(() => {
  return blog.value?.content ? md.render(blog.value.content) : "";
});
</script>
