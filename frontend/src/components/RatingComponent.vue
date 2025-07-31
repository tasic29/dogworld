<template>
  <div class="rating-component space-y-3">
    <div
      v-if="showAverageRating"
      class="flex items-center gap-2 text-gray-700 dark:text-gray-300"
    >
      <div class="flex">
        <svg
          v-for="star in 5"
          :key="star"
          :class="{
            'text-amber-400': star <= Math.round(averageRating || 0),
            'text-gray-300 dark:text-gray-600':
              star > Math.round(averageRating || 0),
          }"
          class="w-5 h-5 fill-current"
          viewBox="0 0 24 24"
        >
          <path
            d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 18.896l-7.416 3.817 1.48-8.279L.002 9.306l8.332-1.151L12 .587z"
          />
        </svg>
      </div>
      <span class="text-sm font-semibold">
        {{ averageRating.toFixed(1) }} ({{ ratingCount }}
        {{ ratingCount === 1 ? "rating" : "ratings" }})
      </span>
    </div>

    <div v-if="auth.isAuthenticated" class="flex items-center gap-2">
      <span class="text-gray-700 dark:text-gray-300 text-sm font-medium"
        >Your rating:</span
      >
      <div class="flex">
        <button
          v-for="star in 5"
          :key="star"
          @click="setRating(star)"
          :aria-label="`Rate ${star} stars`"
          :class="{
            'text-amber-500': star <= userRating,
            'text-gray-300 dark:text-gray-600': star > userRating,
            'hover:text-amber-400 transition-colors': !isSaving,
            'cursor-not-allowed opacity-75': isSaving,
          }"
          :disabled="isSaving"
          class="w-6 h-6 fill-current focus:outline-none"
        >
          <svg viewBox="0 0 24 24">
            <path
              d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 18.896l-7.416 3.817 1.48-8.279L.002 9.306l8.332-1.151L12 .587z"
            />
          </svg>
        </button>
      </div>
      <button
        v-if="existingRatingId"
        @click="removeRating"
        :disabled="isSaving"
        class="text-xs text-red-500 hover:text-red-700 ml-2 disabled:opacity-50"
      >
        Remove
      </button>
    </div>

    <div v-else class="text-sm text-gray-500 dark:text-gray-400 italic">
      <router-link
        to="/login"
        class="text-amber-600 hover:underline dark:text-amber-400"
        >Log in</router-link
      >
      to rate.
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
const averageRating = ref(parseFloat(props.initialAverage));
const ratingCount = ref(parseInt(props.initialCount));
const existingRatingId = ref(null);
const isSaving = ref(false);

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
    await fetchOverallRating(); // Re-fetch overall average and count after successful action
  } catch (error) {
    console.error("Error setting rating:", error);
    const msg =
      error.response?.data?.non_field_errors?.[0] || // Catch Django-specific validation errors
      error.response?.data?.detail || // Catch general DRF errors
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
      fetchUserRating(); // Fetch user rating if logged in
    } else {
      userRating.value = 0; // Clear user rating if logged out
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
