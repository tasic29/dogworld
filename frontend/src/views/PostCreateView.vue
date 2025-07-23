<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-3xl mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg shadow"
    >
      <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-6">
        Create New Post
      </h1>

      <form @submit.prevent="submitBlog" class="space-y-6">
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
            Upload Image
          </button>

          <!-- Display selected file name -->
          <p
            v-if="form.image"
            class="mt-2 text-sm text-gray-600 dark:text-gray-400"
          >
            Selected: {{ form.image.name }} ({{
              formatFileSize(form.image.size)
            }})
          </p>
        </div>

        <!-- Error Message -->
        <p v-if="error" class="text-red-600 font-medium">{{ error }}</p>
        <p v-if="success" class="text-green-600 font-medium">{{ success }}</p>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-6 py-3 bg-amber-500 text-white font-semibold rounded shadow hover:bg-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isSubmitting ? "Submitting..." : "Submit Blog" }}
        </button>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

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

// Loading state
const isSubmitting = ref(false);

// Constants
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"];

// Fetch tags on mount
onMounted(async () => {
  try {
    const res = await axios.get("/content/tags/");
    tags.value = res.data;
  } catch (err) {
    toast.error("Failed to load tags. 🐾");
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
  }
};

// Validate YouTube URL
const isValidYouTubeUrl = (url) => {
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
  if (!form.value.title.trim()) {
    toast.error("Title is required. ✍️");
    return false;
  }

  if (!form.value.caption.trim()) {
    toast.error("caption is required. 📖");
    return false;
  }
  if (form.value.youtube_url && !isValidYouTubeUrl(form.value.youtube_url)) {
    toast.error("Please enter a valid YouTube URL. 🎥");
    return false;
  }

  return true;
};

// Submit post
const submitBlog = async () => {
  if (!validateForm()) return;

  isSubmitting.value = true;

  const formData = new FormData();
  formData.append("title", form.value.title.trim());
  formData.append("caption", form.value.caption.trim());
  formData.append("youtube_url", form.value.youtube_url.trim());
  form.value.tags.forEach((tagId) => formData.append("tag_ids", tagId));
  if (form.value.image) {
    formData.append("image", form.value.image);
  }

  try {
    await axios.post("/caption/posts/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    toast.success("Post created successfully! 🐶");

    // Reset form
    form.value = {
      title: "",
      caption: "",
      youtube_url: "",
      tags: [],
      image: null,
    };
    if (fileInput.value) {
      fileInput.value.value = "";
    }

    setTimeout(() => {
      router.push("/posts");
    }, 2000);
  } catch (err) {
    if (err.response?.data) {
      const messages = Object.values(err.response.data).flat();
      messages.forEach((msg) => toast.error(msg + " ❌"));
    } else {
      toast.error("Something went wrong. Please try again. 🐾");
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
