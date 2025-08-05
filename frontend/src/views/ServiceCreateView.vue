<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-3xl mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg shadow-lg hover:shadow-2xl transition"
    >
      <h1 class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-6">
        Create New Service
      </h1>

      <form @submit.prevent="submitService" class="space-y-6">
        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
          >
            Service Name
          </label>
          <input
            v-model="form.name"
            type="text"
            required
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
          >
            Service Type
          </label>
          <select
            v-model="form.service_type"
            required
            class="w-full px-4 py-2 rounded border border-amber-300"
          >
            <option disabled value="">Select Service Type</option>
            <option
              v-for="type in serviceTypes"
              :key="type.value"
              :value="type.value"
            >
              {{ type.label }}
            </option>
          </select>
        </div>

        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
          >
            Description
          </label>
          <textarea
            v-model="form.description"
            rows="5"
            class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
          ></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label
              class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >
              Contact Email
            </label>
            <input
              v-model="form.contact_email"
              type="email"
              class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
          <div>
            <label
              class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >
              Phone Number
            </label>
            <input
              v-model="form.phone_number"
              type="tel"
              class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label
              class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >
              Website URL
            </label>
            <input
              v-model="form.website_url"
              type="url"
              class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
          <div>
            <label
              class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
            >
              City
            </label>
            <input
              v-model="form.city"
              type="text"
              required
              class="w-full px-4 py-2 rounded border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            v-model="form.is_active"
            type="checkbox"
            class="accent-amber-500 w-5 h-5"
            id="isActive"
          />
          <label
            for="isActive"
            class="ml-2 text-gray-700 dark:text-gray-300 font-medium"
          >
            Active
          </label>
        </div>

        <div>
          <label
            class="block font-semibold mb-1 text-gray-700 dark:text-gray-300"
          >
            Service Image
          </label>
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

        <p v-if="error" class="text-red-600 font-medium">{{ error }}</p>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-6 py-3 bg-amber-500 text-white font-semibold rounded shadow hover:bg-amber-600 disabled:opacity-50"
        >
          {{ isSubmitting ? "Submitting..." : "Create Service" }}
        </button>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

const form = ref({
  name: "",
  service_type: "",
  description: null,
  contact_email: null,
  phone_number: null,
  website_url: null,
  city: "",
  image: null,
  is_active: true,
});

const serviceTypes = [
  { value: "vet", label: "Veterinarian" },
  { value: "grooming", label: "Grooming" },
  { value: "walking", label: "Dog Walking" },
  { value: "boarding", label: "Boarding / Pet Sitting" },
  { value: "training", label: "Training" },
  { value: "breeding", label: "Breeding" },
  { value: "nutrition", label: "Nutrition / Diet Consultation" },
  { value: "insurance", label: "Pet Insurance" },
  { value: "photography", label: "Pet Photography" },
  { value: "transport", label: "Pet Transport" },
  { value: "other", label: "Other" },
];

const fileInput = ref(null);
const isSubmitting = ref(false);
const error = ref("");

const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"];

const formatFileSize = (bytes) => {
  if (!bytes) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

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

const submitService = async () => {
  if (!form.value.name.trim()) return toast.error("Service name is required.");
  if (!form.value.service_type) return toast.error("Service type is required.");
  if (!form.value.city.trim()) return toast.error("City is required.");

  isSubmitting.value = true;

  const formData = new FormData();
  formData.append("name", form.value.name.trim());
  formData.append("service_type", form.value.service_type);
  if (form.value.description) {
    formData.append("description", form.value.description.trim());
  }
  if (form.value.contact_email) {
    formData.append("contact_email", form.value.contact_email.trim());
  }
  if (form.value.phone_number) {
    formData.append("phone_number", form.value.phone_number.trim());
  }
  if (form.value.website_url) {
    formData.append("website_url", form.value.website_url.trim());
  }
  formData.append("city", form.value.city.trim());
  formData.append("is_active", form.value.is_active);
  if (form.value.image) {
    formData.append("image", form.value.image);
  }

  try {
    // The endpoint will be based on your Django REST Framework router setup.
    // Assuming a root path like /services/
    await axios.post("/services/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    toast.success("Service created successfully! 🎉");
    resetForm();
    setTimeout(() => router.push("/services"), 1500); // Adjust redirect path as needed
  } catch (err) {
    error.value = "Failed to submit service.";
    if (err.response?.data) {
      const messages = Object.values(err.response.data).flat();
      messages.forEach((msg) => toast.error(msg));
    }
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  form.value = {
    name: "",
    service_type: "",
    description: null,
    contact_email: null,
    phone_number: null,
    website_url: null,
    city: "",
    image: null,
    is_active: true,
  };
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};
</script>
