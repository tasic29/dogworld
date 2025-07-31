<template>
  <div class="rating-component">
    <!-- Average Rating Display -->
    <div
      v-if="showAverageRating"
      class="mb-4 p-4 bg-gradient-to-r from-amber-50 to-orange-50 dark:from-gray-800 dark:to-gray-700 rounded-xl border border-amber-100 dark:border-gray-600"
    >
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="flex items-center">
            <svg
              v-for="star in 5"
              :key="star"
              class="w-5 h-5 drop-shadow-sm"
              :class="{
                'text-amber-400': averageRating >= star,
                'text-amber-300':
                  averageRating >= star - 0.5 && averageRating < star,
                'text-gray-300 dark:text-gray-500': averageRating < star - 0.5,
              }"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 18.896l-7.416 3.817 1.48-8.279L.002 9.306l8.332-1.151L12 .587z"
              />
            </svg>
          </div>
          <div class="text-gray-700 dark:text-gray-200">
            <span class="text-lg font-bold">{{
              averageRating.toFixed(1)
            }}</span>
            <span class="text-sm ml-1">out of 5</span>
          </div>
        </div>
        <div class="text-right">
          <div class="text-sm text-gray-600 dark:text-gray-400">
            {{ ratingCount }} {{ ratingCount === 1 ? "rating" : "ratings" }}
          </div>
        </div>
      </div>
    </div>

    <!-- User Rating Section -->
    <div v-if="auth.isAuthenticated" class="space-y-4">
      <div class="text-center">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
          Rate this {{ props.blogId ? "blog" : "post" }}
        </h3>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
          {{
            userRating > 0
              ? "You rated this " + userRating + " stars"
              : "Click on stars to rate"
          }}
        </p>
      </div>

      <!-- Interactive Star Rating -->
      <div class="flex justify-center items-center gap-2">
        <button
          v-for="star in 5"
          :key="star"
          @click="setRating(star)"
          @mouseenter="hoverRating = star"
          @mouseleave="hoverRating = 0"
          :aria-label="`Rate ${star} stars`"
          :class="{
            'text-amber-500 scale-110 drop-shadow-lg':
              star <= (hoverRating || userRating),
            'text-gray-300 dark:text-gray-600 hover:text-amber-300':
              star > (hoverRating || userRating),
            'cursor-not-allowed opacity-50': isSaving,
            'transform transition-all duration-200 ease-in-out hover:scale-125':
              !isSaving,
          }"
          :disabled="isSaving"
          class="w-10 h-10 fill-current focus:outline-none focus:ring-2 focus:ring-amber-400 focus:ring-opacity-50 rounded-full p-1"
        >
          <svg viewBox="0 0 24 24" class="w-full h-full">
            <path
              d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 18.896l-7.416 3.817 1.48-8.279L.002 9.306l8.332-1.151L12 .587z"
            />
          </svg>
        </button>
      </div>

      <!-- Rating Labels -->
      <div class="flex justify-center">
        <div
          class="text-xs text-gray-500 dark:text-gray-400 text-center max-w-xs"
        >
          {{ getRatingLabel(hoverRating || userRating) }}
        </div>
      </div>

      <!-- Remove Rating Button -->
      <div v-if="existingRatingId" class="flex justify-center">
        <button
          @click="removeRating"
          :disabled="isSaving"
          class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            ></path>
          </svg>
          Remove Rating
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isSaving" class="flex justify-center">
        <div
          class="inline-flex items-center gap-2 px-4 py-2 text-sm text-amber-600 dark:text-amber-400"
        >
          <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Saving...
        </div>
      </div>
    </div>

    <!-- Login Prompt -->
    <div
      v-else
      class="text-center p-6 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-600"
    >
      <div class="mb-4">
        <svg
          class="w-12 h-12 mx-auto text-gray-400 dark:text-gray-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
          ></path>
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
        Want to rate this {{ props.blogId ? "blog" : "post" }}?
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Join our community to share your thoughts and help others discover great
        content.
      </p>
      <router-link
        to="/login"
        class="inline-flex items-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
          ></path>
        </svg>
        Log in to Rate
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

const props = defineProps({
  blogId: Number,
  postId: Number,
  initialAverage: { type: [Number, String], default: 0 },
  initialCount: { type: [Number, String], default: 0 },
  showAverageRating: { type: Boolean, default: true },
});

const emit = defineEmits(["rating-updated"]);

const auth = useAuthStore();
const toast = useToast();

const userRating = ref(0);
const hoverRating = ref(0);
const averageRating = ref(parseFloat(props.initialAverage));
const ratingCount = ref(parseInt(props.initialCount));
const existingRatingId = ref(null);
const isSaving = ref(false);

const getRatingLabel = (rating) => {
  const labels = {
    0: "Select a rating",
    1: "Poor - Not what I expected",
    2: "Fair - Could be better",
    3: "Good - Met my expectations",
    4: "Very Good - Exceeded expectations",
    5: "Excellent - Outstanding content!",
  };
  return labels[rating] || labels[0];
};

const fetchUserRating = async () => {
  if (!auth.isAuthenticated || (!props.blogId && !props.postId)) return;

  try {
    const url = props.blogId
      ? `/content/blogs/${props.blogId}/ratings/`
      : `/content/posts/${props.postId}/ratings/`;

    const response = await axios.get(url);
    const userRatings = response.data.results || response.data;

    const userSpecificRating = userRatings.find(
      (rating) => rating.user.id === auth.user.id
    );
    if (userSpecificRating) {
      userRating.value = userSpecificRating.score;
      existingRatingId.value = userSpecificRating.id;
    }
  } catch (error) {
    toast.error("Failed to fetch user rating. Please try again.");
  }
};

const fetchOverallRating = async () => {
  if (!props.blogId && !props.postId) return;

  try {
    const url = props.blogId
      ? `/content/blogs/${props.blogId}/`
      : `/content/posts/${props.postId}/`;

    const response = await axios.get(url);

    averageRating.value = parseFloat(response.data.average_rating) || 0;
    ratingCount.value = parseInt(response.data.total_ratings) || 0;

    emit("rating-updated", {
      average: averageRating.value,
      count: ratingCount.value,
    });
  } catch (error) {
    toast.error("Failed to fetch overall rating. Please try again.");
  }
};

const setRating = async (score) => {
  if (isSaving.value) return;

  isSaving.value = true;
  const payload = { score };
  let url = props.blogId
    ? `/content/blogs/${props.blogId}/ratings/`
    : `/content/posts/${props.postId}/ratings/`;

  const method = existingRatingId.value ? "put" : "post";
  if (existingRatingId.value) url += `${existingRatingId.value}/`;

  try {
    const response = await axios[method](url, payload);
    userRating.value = response.data.score;
    existingRatingId.value = response.data.id;
    toast.success(`You rated ${score} stars! Thank you 🐾`);
    await fetchOverallRating();
  } catch (error) {
    console.error("Error setting rating:", error);
    const msg =
      error.response?.data?.non_field_errors?.[0] ||
      error.response?.data?.detail ||
      "Failed to submit rating. Please try again.";
    toast.error(msg);
    if (!existingRatingId.value) userRating.value = 0;
  } finally {
    isSaving.value = false;
  }
};

const removeRating = async () => {
  if (!existingRatingId.value || isSaving.value) return;

  isSaving.value = true;
  const url = props.blogId
    ? `/content/blogs/${props.blogId}/ratings/${existingRatingId.value}/`
    : `/content/posts/${props.postId}/ratings/${existingRatingId.value}/`;

  try {
    await axios.delete(url);
    userRating.value = 0;
    existingRatingId.value = null;
    toast.success("Rating removed successfully!");
    await fetchOverallRating();
  } catch (error) {
    toast.error("Failed to remove rating. Please try again.");
  } finally {
    isSaving.value = false;
  }
};

onMounted(() => {
  if (auth.isAuthenticated) fetchUserRating();
  fetchOverallRating();
});

watch(
  () => auth.isAuthenticated,
  (newVal) => {
    if (newVal) {
      fetchUserRating();
    } else {
      userRating.value = 0;
      existingRatingId.value = null;
    }
  }
);

watch(
  () => [props.blogId, props.postId],
  () => {
    fetchUserRating();
    fetchOverallRating();
  }
);
</script>
