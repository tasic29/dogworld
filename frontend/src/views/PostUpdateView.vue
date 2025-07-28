<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-3xl mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg shadow"
    >
      <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-6">
        Update Post
      </h1>

      <div v-if="loading" class="text-center py-8">
        <p class="text-gray-600 dark:text-gray-400">Loading post...</p>
      </div>

      <form v-else @submit.prevent="updatePost" class="space-y-6">
        <!-- Title -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Title</label
          >
          <input
            v-model="form.title"
            type="text"
            required
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <!-- Caption -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Caption</label
          >
          <textarea
            v-model="form.caption"
            rows="8"
            required
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          ></textarea>
        </div>

        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >YouTube URL</label
          >
          <input
            v-model="form.youtube_url"
            type="text"
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <!-- Tags -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Tags</label
          >
          <div class="flex flex-wrap gap-2">
            <label
              v-for="tag in tags"
              :key="tag.id"
              class="flex items-center gap-2 text-sm"
            >
              <input
                type="checkbox"
                :value="tag.id"
                v-model="form.tags"
                class="accent-amber-500"
              />
              #{{ tag.name }}
            </label>
          </div>
        </div>

        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Image</label
          >

          <!-- Current image display -->
          <div v-if="currentImageUrl && !form.image" class="mb-4">
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Current image:
            </p>
            <img
              :src="currentImageUrl"
              alt="Current post image"
              class="max-w-xs rounded border shadow-sm"
            />
            <button
              type="button"
              @click="removeCurrentImage"
              class="mt-2 px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600 transition"
            >
              Remove Current Image
            </button>
          </div>

          <!-- Hidden file input -->
          <input
            ref="fileInput"
            type="file"
            @change="handleImage"
            accept="image/jpeg,image/png,image/webp,image/gif"
            class="hidden"
          />

          <!-- Button to trigger file input -->
          <button
            type="button"
            @click="fileInput?.click()"
            class="px-4 py-2 bg-amber-400 text-white rounded hover:bg-amber-500 transition"
          >
            {{
              form.image || !currentImageUrl ? "Upload Image" : "Replace Image"
            }}
          </button>

          <!-- Display selected file name -->
          <p
            v-if="form.image"
            class="mt-2 text-sm text-gray-600 dark:text-gray-400"
          >
            New image: {{ form.image.name }} ({{
              formatFileSize(form.image.size)
            }})
          </p>
        </div>

        <!-- Error Message -->
        <p v-if="error" class="text-red-600 font-medium">{{ error }}</p>
        <p v-if="success" class="text-green-600 font-medium">{{ success }}</p>

        <!-- Submit -->
        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-6 py-3 bg-amber-500 text-white font-semibold rounded shadow hover:bg-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? "Updating..." : "Update Post" }}
          </button>

          <button
            type="button"
            @click="router.back()"
            class="px-6 py-3 bg-gray-500 text-white font-semibold rounded shadow hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { useToast } from "vue-toastification";

const router = useRouter();
const route = useRoute();
const toast = useToast();

// Get post ID from route params
const postId = route.params.id;

// Post form fields
const form = ref({
  title: "",
  caption: "",
  youtube_url: "",
  tags: [],
  image: null,
});

// Tags list
const tags = ref([]);

// File input reference
const fileInput = ref(null);

// Loading states
const loading = ref(true);
const isSubmitting = ref(false);

// Current image URL
const currentImageUrl = ref(null);
const removeImage = ref(false);

// Error and success messages
const error = ref("");
const success = ref("");

// Constants
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"];

// Load post data and tags on mount
onMounted(async () => {
  try {
    // Load tags and post data in parallel
    const [tagsRes, postRes] = await Promise.all([
      axios.get("/content/tags/"),
      axios.get(`/content/posts/${postId}/`),
    ]);

    tags.value = tagsRes.data;

    // Populate form with existing data
    const post = postRes.data;
    form.value = {
      title: post.title || "",
      caption: post.caption || "",
      youtube_url: post.youtube_url || "",
      tags: post.tags ? post.tags.map((tag) => tag.id) : [],
      image: null,
    };

    // Set current image URL if exists
    if (post.image) {
      currentImageUrl.value = post.image;
    }

    loading.value = false;
  } catch (err) {
    loading.value = false;
    if (err.response?.status === 404) {
      toast.error("Post not found. 🐾");
      router.push("/posts");
    } else {
      toast.error("Failed to load post data. 🐾");
    }
  }
});

// Format file size helper
const formatFileSize = (bytes) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

// Handle file upload with validation
const handleImage = (e) => {
  const file = e.target.files[0];

  if (file) {
    if (!ALLOWED_TYPES.includes(file.type)) {
      toast.error("Please select a valid image (JPG, PNG, WebP, GIF). 📷");
      e.target.value = "";
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      toast.error("Image size must be less than 5MB. 🐘");
      e.target.value = "";
      return;
    }

    form.value.image = file;
    removeImage.value = false;
  }
};

// Remove current image
const removeCurrentImage = () => {
  removeImage.value = true;
  currentImageUrl.value = null;
  form.value.image = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};

// Validate YouTube URL
const isValidYouTubeUrl = (url) => {
  if (!url.trim()) return true; // Empty URL is valid
  try {
    const parsed = new URL(url);
    return (
      parsed.hostname.includes("youtube.com") || parsed.hostname === "youtu.be"
    );
  } catch {
    return false;
  }
};

// Validate form
const validateForm = () => {
  error.value = "";

  if (!form.value.title.trim()) {
    error.value = "Title is required. ✍️";
    return false;
  }

  if (!form.value.caption.trim()) {
    error.value = "Caption is required. 📖";
    return false;
  }

  if (form.value.youtube_url && !isValidYouTubeUrl(form.value.youtube_url)) {
    error.value = "Please enter a valid YouTube URL. 🎥";
    return false;
  }

  return true;
};

// Update post
const updatePost = async () => {
  if (!validateForm()) return;

  isSubmitting.value = true;
  error.value = "";
  success.value = "";

  const formData = new FormData();
  formData.append("title", form.value.title.trim());
  formData.append("caption", form.value.caption.trim());
  formData.append("youtube_url", form.value.youtube_url.trim());
  form.value.tags.forEach((tagId) => formData.append("tag_ids", tagId));

  // Handle image updates
  if (form.value.image) {
    formData.append("image", form.value.image);
  } else if (removeImage.value) {
    formData.append("remove_image", "true");
  }

  try {
    await axios.put(`/content/posts/${postId}/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    toast.success("Post updated successfully! 🐶");
    success.value = "Post updated successfully!";

    setTimeout(() => {
      router.push("/posts");
    }, 2000);
  } catch (err) {
    if (err.response?.data) {
      const messages = Object.values(err.response.data).flat();
      error.value = messages.join(", ");
      messages.forEach((msg) => toast.error(msg + " ❌"));
    } else {
      error.value = "Something went wrong. Please try again.";
      toast.error("Something went wrong. Please try again. 🐾");
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
