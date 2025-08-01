<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-3xl mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg shadow-lg hover:shadow-2xl transition"
    >
      <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-6">
        Create New Product
      </h1>

      <form @submit.prevent="submitProduct" class="space-y-6">
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

        <!-- Description -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Description</label
          >
          <textarea
            v-model="form.description"
            rows="5"
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          ></textarea>
        </div>

        <!-- Price -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Price ($)</label
          >
          <input
            v-model="form.price"
            type="number"
            step="0.01"
            min="1"
            required
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <!-- Affiliate URL -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Affiliate URL</label
          >
          <input
            v-model="form.affiliate_url"
            type="url"
            required
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <!-- Category -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Category</label
          >
          <select
            v-model="form.category"
            required
            class="w-full px-4 py-2 rounded border border-amber-300"
          >
            <option disabled value="">Select Category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <!-- Image -->
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >Image</label
          >
          <input
            ref="fileInput"
            type="file"
            @change="handleImage"
            accept="image/*"
            class="hidden"
          />
          <button
            type="button"
            @click="fileInput?.click()"
            class="px-4 py-2 bg-amber-400 text-white rounded hover:bg-amber-500 transition"
          >
            Upload Image
          </button>
          <p
            v-if="form.image"
            class="mt-2 text-sm text-gray-600 dark:text-gray-400"
          >
            Selected: {{ form.image.name }} ({{
              formatFileSize(form.image.size)
            }})
          </p>
        </div>

        <!-- Error / Success -->
        <p v-if="error" class="text-red-600 font-medium">{{ error }}</p>
        <p v-if="success" class="text-green-600 font-medium">{{ success }}</p>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-6 py-3 bg-amber-500 text-white font-semibold rounded shadow hover:bg-amber-600 disabled:opacity-50"
        >
          {{ isSubmitting ? "Submitting..." : "Submit Product" }}
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

const form = ref({
  title: "",
  description: "",
  price: "",
  affiliate_url: "",
  category: "",
  image: null,
});

const categories = ref([]);
const fileInput = ref(null);
const isSubmitting = ref(false);
const error = ref("");
const success = ref("");

// Constants
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"];

// Format size
const formatFileSize = (bytes) => {
  if (!bytes) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

// Load categories
onMounted(async () => {
  try {
    const res = await axios.get("/api/categories/");
    categories.value = res.data.results || res.data;
  } catch (err) {
    toast.error("Failed to load categories.");
  }
});

// Handle image
const handleImage = (e) => {
  const file = e.target.files[0];
  if (!file) return;

  if (!ALLOWED_TYPES.includes(file.type)) {
    toast.error("Invalid file type.");
    return;
  }

  if (file.size > MAX_FILE_SIZE) {
    toast.error("Image size must be less than 5MB.");
    return;
  }

  form.value.image = file;
};

// Submit form
const submitProduct = async () => {
  if (!form.value.title.trim()) return toast.error("Title is required.");
  if (!form.value.price || Number(form.value.price) < 1)
    return toast.error("Valid price required.");
  if (!form.value.affiliate_url.trim())
    return toast.error("Affiliate URL is required.");
  if (!form.value.category) return toast.error("Category is required.");

  isSubmitting.value = true;

  const formData = new FormData();
  formData.append("title", form.value.title.trim());
  formData.append("description", form.value.description || "");
  formData.append("price", form.value.price);
  formData.append("affiliate_url", form.value.affiliate_url.trim());
  formData.append("category", form.value.category);
  if (form.value.image) {
    formData.append("image", form.value.image);
  }

  try {
    await axios.post("/api/products/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    toast.success("Product created successfully! 🎉");
    form.value = {
      title: "",
      description: "",
      price: "",
      affiliate_url: "",
      category: "",
      image: null,
    };
    fileInput.value.value = "";
    setTimeout(() => router.push("/marketplace"), 1500);
  } catch (err) {
    error.value = "Failed to submit product.";
    if (err.response?.data) {
      const messages = Object.values(err.response.data).flat();
      messages.forEach((msg) => toast.error(msg));
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
