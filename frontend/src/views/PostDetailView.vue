<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-4xl mx-auto bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow p-8"
    >
      <div v-if="post" class="space-y-6">
        <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300">
          {{ post.title }}
        </h1>

        <p class="text-gray-500 text-sm dark:text-gray-400">
          By {{ post.author.username }} • {{ formatDate(post.created_at) }}
        </p>

        <img
          v-if="post.image"
          :src="post.image"
          alt="post image"
          class="rounded-lg w-full object-cover max-h-[500px] shadow"
        />

        <!-- Caption -->
        <div class="prose dark:prose-invert max-w-none">
          <div v-html="renderedCaption"></div>
        </div>

        <!-- YouTube Lazy Video -->
        <div v-if="youtubeVideoId" class="relative mt-6">
          <div
            v-if="!showIframe"
            class="relative cursor-pointer group aspect-w-16 aspect-h-9"
            @click="showIframe = true"
          >
            <img
              :src="youtubeThumbnailUrl"
              alt="YouTube video thumbnail"
              class="w-full h-full object-cover rounded-lg shadow"
            />
            <div
              class="absolute inset-0 bg-black/40 flex items-center justify-center transition group-hover:bg-black/50 rounded-lg"
            >
              <svg
                class="w-16 h-16 text-white opacity-80 group-hover:scale-110 transition-transform"
                fill="currentColor"
                viewBox="0 0 84 84"
              >
                <circle
                  cx="42"
                  cy="42"
                  r="42"
                  fill="currentColor"
                  opacity="0.6"
                />
                <polygon points="33,26 61,42 33,58" fill="white" />
              </svg>
            </div>
          </div>

          <div v-else class="aspect-w-16 aspect-h-9">
            <iframe
              :src="`https://www.youtube.com/embed/${youtubeVideoId}?autoplay=1`"
              class="w-full h-full rounded-lg shadow"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              loading="lazy"
            ></iframe>
          </div>
        </div>

        <!-- Tags -->
        <div v-if="post.tags.length" class="flex flex-wrap gap-2 mt-6">
          <span
            v-for="tag in post.tags"
            :key="tag.id"
            class="bg-amber-100 text-amber-800 text-sm px-3 py-1 rounded-full dark:bg-slate-700 dark:text-amber-300"
          >
            #{{ tag.name }}
          </span>
        </div>
      </div>

      <div v-else class="text-center text-gray-500 dark:text-gray-300">
        Loading post...
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import MarkdownIt from "markdown-it";

const route = useRoute();
const post = ref(null);
const md = new MarkdownIt();
const showIframe = ref(false);

const formatDate = (date) =>
  new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

onMounted(async () => {
  try {
    const response = await axios.get(`/content/posts/${route.params.id}/`);
    post.value = response.data;
  } catch (error) {
    console.error("Failed to load post:", error);
  }
});

const renderedCaption = computed(() => {
  return post.value?.caption ? md.render(post.value.caption) : "";
});

const youtubeVideoId = computed(() => {
  const url = post.value?.youtube_url;
  if (!url) return null;

  try {
    const parsed = new URL(url);
    const hostname = parsed.hostname;

    if (hostname.includes("youtube.com")) {
      return parsed.searchParams.get("v");
    } else if (hostname === "youtu.be") {
      return parsed.pathname.slice(1);
    }

    return null;
  } catch {
    return null;
  }
});

const youtubeThumbnailUrl = computed(() => {
  return youtubeVideoId.value
    ? `https://img.youtube.com/vi/${youtubeVideoId.value}/hqdefault.jpg`
    : null;
});
</script>

<style scoped>
/* fallback in case aspect-ratio plugin is not enabled */
/* .aspect-w-16 {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
}
.aspect-w-16 > * {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
} */
</style>
