<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Post Content -->
      <div
        class="lg:col-span-2 bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow p-8"
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
                  <circle cx="42" cy="42" r="42" opacity="0.6" />
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

          <!-- Edit/Delete Buttons -->
          <div v-if="canEdit" class="mt-6 flex justify-end gap-4">
            <button
              @click="goToEdit"
              class="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white font-semibold rounded shadow transition"
            >
              ✏️ Edit Post
            </button>
            <button
              @click="confirmDelete"
              class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
            >
              Delete Post
            </button>
          </div>
        </div>

        <div v-else class="text-center text-gray-500 dark:text-gray-300">
          Loading post...
        </div>
      </div>

      <!-- Sidebar: Comments -->
      <aside>
        <CommentComponent type="post" />
      </aside>
    </div>

    <!-- Delete Confirm Dialog -->
    <ConfirmDialog
      v-if="showConfirmDialog"
      title="Delete Post"
      message="Are you sure you want to delete this post? 🐾"
      confirmText="Yes, delete it"
      cancelText="Cancel"
      @confirm="onDeleteConfirmed"
      @cancel="showConfirmDialog = false"
    />
  </section>
</template>

<script setup>
import CommentComponent from "../components/CommentComponent.vue";
import ConfirmDialog from "../components/ConfirmDialog.vue";
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";
import MarkdownIt from "markdown-it";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const toast = useToast();

const post = ref(null);
const postId = route.params.id;
const md = new MarkdownIt();
const showIframe = ref(false);
const showConfirmDialog = ref(false);

const formatDate = (date) =>
  new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

onMounted(async () => {
  try {
    const response = await axios.get(`/content/posts/${postId}/`);
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
    if (hostname.includes("youtube.com")) return parsed.searchParams.get("v");
    if (hostname === "youtu.be") return parsed.pathname.slice(1);
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

const canEdit = computed(() => {
  const currentUser = auth.user;
  return (
    currentUser &&
    (currentUser.id === post.value?.author?.id || currentUser.is_staff)
  );
});

const goToEdit = () => {
  if (post.value?.id) {
    router.push({ name: "post-edit", params: { id: post.value.id } });
  }
};

const confirmDelete = () => {
  showConfirmDialog.value = true;
};

const onDeleteConfirmed = async () => {
  try {
    await axios.delete(`/content/posts/${postId}/`);
    toast.success("Post deleted successfully! 🗑️");
    router.push("/posts");
  } catch (err) {
    toast.error("Failed to delete post. 😿");
  } finally {
    showConfirmDialog.value = false;
  }
};
</script>
