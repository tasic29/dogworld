<template>
  <div>
    <section
      class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
    >
      <div
        class="max-w-4xl mx-auto bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow p-8"
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
          <!-- Tags -->
          <div v-if="blog.tags.length" class="flex flex-wrap gap-2 mt-6">
            <span
              v-for="tag in blog.tags"
              :key="tag.id"
              class="bg-amber-100 text-amber-800 text-sm px-3 py-1 rounded-full dark:bg-slate-700 dark:text-amber-300"
            >
              #{{ tag.name }}
            </span>
          </div>
        </div>
        <div v-else class="text-center text-gray-500 dark:text-gray-300">
          Loading blog post...
        </div>
      </div>
    </section>
    <CommentComponent type="blog" />
  </div>
</template>

<script setup>
import CommentComponent from "../components/CommentComponent.vue";
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
    const response = await axios.get(`/content/blogs/${route.params.id}/`);
    blog.value = response.data;
  } catch (error) {
    console.error("Failed to load blog:", error);
  }
});

const renderedContent = computed(() => {
  if (blog.value?.content) {
    return md.render(blog.value.content);
  }
  return "";
});
</script>
