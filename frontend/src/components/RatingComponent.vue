<template>
  <div class="rating-component space-y-3">
    <div
      v-if="showAverageRating && (averageRating > 0 || ratingCount > 0)"
      class="flex items-center gap-2 text-gray-700 dark:text-gray-300"
    >
      <div class="flex">
        <svg
          v-for="star in 5"
          :key="star"
          :class="{
            'text-amber-400': star <= Math.round(averageRating),
            'text-gray-300 dark:text-gray-600':
              star > Math.round(averageRating),
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
        {{ averageRating.toFixed(1) }} ({{ ratingCount }} ratings)
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
import { useAuthStore } from "@/stores/auth"; // Adjust path if needed
import { useToast } from "vue-toastification"; // Assuming you have this set up

const props = defineProps({
  blogId: {
    type: Number,
    default: null,
  },
  postId: {
    type: Number,
    default: null,
  },
  initialAverage: {
    type: [Number, String],
    default: 0,
  },
  initialCount: {
    type: [Number, String],
    default: 0,
  },
  showAverageRating: {
    type: Boolean,
    default: true,
  },
});

const auth = useAuthStore();
const toast = useToast();

const userRating = ref(0);
const averageRating = ref(parseFloat(props.initialAverage) || 0);
const ratingCount = ref(parseInt(props.initialCount) || 0);
const existingRatingId = ref(null);
const isSaving = ref(false);

const fetchUserRating = async () => {
  if (!auth.isAuthenticated || (!props.blogId && !props.postId)) {
    return;
  }

  try {
    const url = props.blogId
      ? `/content/blogs/${props.blogId}/ratings/`
      : `/content/posts/${props.postId}/ratings/`;

    const response = await axios.get(url, {
      params: { user: auth.user.id }, // Filter by current user's ID
    });

    const userRatings = response.data.results || response.data; // DRF list view returns 'results'

    if (userRatings.length > 0) {
      const userSpecificRating = userRatings.find(
        (rating) => rating.user.id === auth.user.id
      );
      if (userSpecificRating) {
        userRating.value = userSpecificRating.score;
        existingRatingId.value = userSpecificRating.id;
      }
    }
  } catch (error) {
    console.error("Error fetching user rating:", error);
  }
};

const setRating = async (score) => {
  if (isSaving.value) return;

  isSaving.value = true;
  const payload = { score: score };
  let url = "";
  let method = "";

  if (props.blogId) {
    url = `/content/blogs/${props.blogId}/ratings/`;
  } else if (props.postId) {
    url = `/content/posts/${props.postId}/ratings/`;
  } else {
    toast.error("Rating target (blog or post) not specified.");
    isSaving.value = false;
    return;
  }

  if (existingRatingId.value) {
    // Update existing rating
    method = "put";
    url = `${url}${existingRatingId.value}/`;
  } else {
    // Create new rating
    method = "post";
  }

  try {
    const response = await axios[method](url, payload);
    userRating.value = response.data.score;
    existingRatingId.value = response.data.id;
    toast.success(`You rated ${score} stars! Thank you for your feedback! 🐾`);
    // Re-fetch average rating and count after successful submission
    await fetchOverallRating();
  } catch (error) {
    console.error("Error setting rating:", error);
    if (error.response?.data?.non_field_errors) {
      toast.error(error.response.data.non_field_errors[0]);
    } else if (error.response?.data?.detail) {
      toast.error(error.response.data.detail);
    } else {
      toast.error("Failed to submit rating. Please try again.");
    }
    // Revert userRating if error and it was a new rating attempt
    if (!existingRatingId.value) {
      userRating.value = 0;
    }
  } finally {
    isSaving.value = false;
  }
};

const fetchOverallRating = async () => {
  if (!props.blogId && !props.postId) return;

  try {
    const url = props.blogId
      ? `/content/blogs/${props.blogId}/`
      : `/content/posts/${props.postId}/`;

    const response = await axios.get(url);
    averageRating.value = parseFloat(response.data.avg_rating) || 0;
    ratingCount.value = parseInt(response.data.rating_count) || 0;
  } catch (error) {
    console.error("Error fetching overall rating:", error);
  }
};

watch(
  () => auth.isAuthenticated,
  (newVal) => {
    if (newVal) {
      fetchUserRating();
    } else {
      userRating.value = 0; // Clear user rating if logged out
      existingRatingId.value = null;
    }
  }
);
</script>
