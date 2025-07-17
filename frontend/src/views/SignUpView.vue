<template>
  <div
    class="max-w-md mx-auto mt-10 p-6 bg-emerald-50 rounded-lg shadow-md dark:bg-gray-900"
  >
    <h2
      class="text-2xl font-bold mb-6 text-center text-emerald-600 dark:text-white"
    >
      Create Your Account
    </h2>
    <form @submit.prevent="submitForm">
      <div class="mb-4">
        <label
          for="username"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Username</label
        >
        <input
          v-model="form.username"
          type="text"
          id="username"
          class="mt-1 block w-full px-4 py-2 border rounded-md focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <div class="mb-4">
        <label
          for="email"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Email</label
        >
        <input
          v-model="form.email"
          type="email"
          id="email"
          class="mt-1 block w-full px-4 py-2 border rounded-md focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <div class="mb-6">
        <label
          for="password"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Password</label
        >
        <input
          v-model="form.password"
          type="password"
          id="password"
          class="mt-1 block w-full px-4 py-2 border rounded-md focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <div class="mb-6">
        <label
          for="password2"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Confirm password</label
        >
        <input
          v-model="form.password2"
          type="password"
          id="password2"
          class="mt-1 block w-full px-4 py-2 border rounded-md focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-800 dark:text-white"
          required
        />
      </div>

      <button
        type="submit"
        class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 px-4 rounded-lg focus:outline-none focus:ring-4 focus:ring-green-300 dark:bg-purple-600 dark:hover:bg-emerald-600 dark:focus:ring-purple-800 flex items-center justify-center"
      >
        <template v-if="isSubmitting">
          <svg
            class="animate-spin h-5 w-5 mr-2 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
          <span>Signing Up...</span>
        </template>
        <span v-else>Sign Up</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const toast = useToast();
const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  username: "",
  email: "",
  password: "",
  password2: "",
});

const isSubmitting = ref(false);

const submitForm = async () => {
  if (form.password !== form.password2) {
    toast.error("Passwords do not match 🐾");
    return;
  }

  isSubmitting.value = true;
  try {
    await axios.post("/auth/users/", {
      username: form.username,
      email: form.email,
      password: form.password,
    });

    await authStore.login({
      username: form.username,
      password: form.password,
    });

    toast.success("Account created and logged in! 🐶");
    router.push("/"); // or dashboard/home route
  } catch (error) {
    toast.error("Something went wrong 🐾");
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>
