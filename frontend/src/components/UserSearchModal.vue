<template>
  <!-- Modal Overlay -->
  <Transition name="fade">
    <div
      v-if="show"
      @click.self="emit('close')"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm transition-opacity"
    >
      <!-- Modal Content -->
      <div
        class="relative bg-white/90 dark:bg-slate-800/90 rounded-2xl shadow-xl max-w-lg w-[90%] lg:w-full p-8 transition-all duration-300 transform scale-95"
      >
        <!-- Close Button -->
        <button
          @click="emit('close')"
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors"
          aria-label="Close modal"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M18 6L6 18M6 6l12 12"></path>
          </svg>
        </button>

        <div class="text-center mb-6">
          <div
            class="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full mb-4 shadow-lg"
          >
            <span class="text-2xl">🔎</span>
          </div>
          <h2
            class="text-2xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300"
          >
            Start a New Conversation
          </h2>
          <p class="text-gray-600 dark:text-gray-300 mt-2">
            Search for a user by name or username to start chatting.
          </p>
        </div>

        <!-- Search Input -->
        <div class="mb-6">
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search for users..."
            class="w-full px-4 py-3 border-2 border-amber-200 rounded-full focus:ring-2 focus:ring-amber-300 focus:border-amber-400 transition-all duration-300 bg-white/50 dark:bg-slate-700/50 dark:border-slate-600 dark:text-white dark:focus:border-amber-400 placeholder-gray-400"
          />
        </div>

        <!-- Search Results -->
        <div class="max-h-60 overflow-y-auto">
          <!-- Loading State -->
          <div v-if="loading" class="flex justify-center py-4">
            <div
              class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"
            ></div>
          </div>

          <!-- Results List -->
          <ul v-else-if="searchResults.length" class="space-y-3">
            <li
              v-for="user in searchResults"
              :key="user.id"
              @click="emit('selectUser', user)"
              class="flex items-center gap-4 p-3 rounded-lg cursor-pointer bg-amber-50 hover:bg-amber-100 dark:bg-slate-700 dark:hover:bg-slate-600 transition-colors"
            >
              <img
                :src="getAvatarUrl(user)"
                :alt="`${getDisplayName(user)} avatar`"
                class="w-10 h-10 rounded-full object-cover shadow"
                @error="handleImageError"
              />
              <div class="flex-1 min-w-0">
                <h3
                  class="font-semibold text-gray-800 dark:text-gray-200 truncate"
                >
                  {{ getDisplayName(user) }}
                </h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                  {{ user.email || user.username }}
                </p>
              </div>
            </li>
          </ul>

          <!-- No Results State -->
          <div
            v-else-if="searchQuery.length > 2 && !loading"
            class="text-center text-gray-500 dark:text-gray-400 py-8"
          >
            <p>No users found matching "{{ searchQuery }}"</p>
          </div>

          <!-- Initial State -->
          <div v-else class="text-center text-gray-500 dark:text-gray-400 py-8">
            <p>Type at least 3 characters to start searching.</p>
          </div>
        </div>

        <!-- Error Toast -->
        <div
          v-if="error"
          class="mt-4 text-center bg-red-100 text-red-700 px-4 py-2 rounded-lg"
        >
          {{ error }}
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  API_BASE_URL: {
    type: String,
    required: true,
  },
  currentUserId: {
    type: [Number, String, null],
    required: false,
    default: null,
  },
});

const emit = defineEmits(["close", "selectUser"]);

// State variables
const searchQuery = ref("");
const searchResults = ref([]);
const loading = ref(false);
const error = ref("");

// Utility functions
const handleImageError = (event) => {
  event.target.src = `${props.API_BASE_URL}/media/profile_images/default.webp`;
};

const getAvatarUrl = (participant) => {
  if (!participant?.profile_image) {
    return `${props.API_BASE_URL}/media/profile_images/default.webp`;
  }
  return participant.profile_image.startsWith("http")
    ? participant.profile_image
    : `${props.API_BASE_URL}${participant.profile_image}`;
};

const getDisplayName = (participant) => {
  if (!participant) return "Unknown User";
  return (
    participant.full_name ||
    `${participant.first_name || ""} ${participant.last_name || ""}`.trim() ||
    participant.username ||
    "Unknown User"
  );
};

// Search logic with debounce
const searchUsers = async () => {
  if (searchQuery.value.length < 3) {
    searchResults.value = [];
    return;
  }
  loading.value = true;
  error.value = "";

  try {
    const res = await axios.get(
      `/users/search/?query=${encodeURIComponent(searchQuery.value)}`
    );
    // Filter out the current user from the results
    searchResults.value = res.data.results.filter(
      (user) => user.id !== props.currentUserId
    );
  } catch (err) {
    console.error("User search failed:", err);
    error.value = err.response?.data?.detail || "Failed to search for users.";
    searchResults.value = [];
  } finally {
    loading.value = false;
  }
};

// Watch for modal visibility to reset state when it's opened
watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      searchQuery.value = "";
      searchResults.value = [];
      error.value = "";
    }
  }
);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
