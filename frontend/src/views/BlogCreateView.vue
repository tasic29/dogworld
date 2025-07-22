<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-3xl mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg shadow"
    >
      <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-6">
        Create New Blog Post
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

        <!-- Content -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Content</label
          >
          <textarea
            v-model="form.content"
            rows="6"
            required
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          ></textarea>
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

const router = useRouter();

// Blog form fields
const form = ref({
  title: "",
  content: "",
  tags: [],
  image: null,
});

// Tags list
const tags = ref([]);

// File input reference
const fileInput = ref(null);

// Errors/success/loading states
const error = ref("");
const success = ref("");
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
    error.value = "Failed to load tags.";
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
  error.value = "";

  if (file) {
    // Validate file type
    if (!ALLOWED_TYPES.includes(file.type)) {
      error.value =
        "Please select a valid image file (JPEG, PNG, WebP, or GIF).";
      e.target.value = "";
      return;
    }

    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
      error.value = "Image size must be less than 5MB.";
      e.target.value = "";
      return;
    }

    form.value.image = file;
  }
};

// Validate form
const validateForm = () => {
  if (!form.value.title.trim()) {
    error.value = "Title is required.";
    return false;
  }

  if (!form.value.content.trim()) {
    error.value = "Content is required.";
    return false;
  }

  return true;
};

// Submit blog
const submitBlog = async () => {
  error.value = "";
  success.value = "";

  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;

  const formData = new FormData();
  formData.append("title", form.value.title.trim());
  formData.append("content", form.value.content.trim());
  form.value.tags.forEach((tagId) => formData.append("tags", tagId));
  if (form.value.image) {
    formData.append("image", form.value.image);
  }

  try {
    await axios.post("/content/blogs/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    success.value = "Blog post created successfully!";

    // Reset form
    form.value = {
      title: "",
      content: "",
      tags: [],
      image: null,
    };
    if (fileInput.value) {
      fileInput.value.value = "";
    }

    // Redirect after a short delay
    setTimeout(() => {
      router.push("/blogs");
    }, 2000);
  } catch (err) {
    if (err.response?.data) {
      const messages = Object.values(err.response.data).flat().join(" ");
      error.value = messages;
    } else {
      error.value = "Something went wrong. Please try again.";
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
