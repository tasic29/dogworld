<template>
  <div class="rating-component space-y-3">
    <!-- ✅ Fixed condition - check for averageRating OR ratingCount -->
    <div
      v-if="showAverageRating && (averageRating > 0 || ratingCount > 0)"
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
        {{ averageRating ? averageRating.toFixed(1) : "0.0" }} ({{
          ratingCount
        }}
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
      <!-- ✅ Add button to remove rating -->
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

// ✅ Debug logging
console.log("Rating component props:", {
  initialAverage: props.initialAverage,
  initialCount: props.initialCount,
  parsedAverage: parseFloat(props.initialAverage),
  parsedCount: parseInt(props.initialCount),
});

const fetchUserRating = async () => {
  if (!auth.isAuthenticated || (!props.blogId && !props.postId)) {
    return;
  }

  try {
    // ✅ Fixed URL structure to match your backend
    const url = props.blogId
      ? `/content/blogs/${props.blogId}/ratings/`
      : `/content/posts/${props.postId}/ratings/`;

    const response = await axios.get(url);
    const userRatings = response.data.results || response.data;

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

  // ✅ Fixed URL structure
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
    method = "put";
    url = `${url}${existingRatingId.value}/`;
  } else {
    method = "post";
  }

  try {
    const response = await axios[method](url, payload);
    userRating.value = response.data.score;
    existingRatingId.value = response.data.id;
    toast.success(`You rated ${score} stars! Thank you for your feedback! 🐾`);

    // ✅ Re-fetch overall rating after successful submission
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
    if (!existingRatingId.value) {
      userRating.value = 0;
    }
  } finally {
    isSaving.value = false;
  }
};

// ✅ Add remove rating function
const removeRating = async () => {
  if (!existingRatingId.value || isSaving.value) return;

  isSaving.value = true;

  try {
    const url = props.blogId
      ? `/content/blogs/${props.blogId}/ratings/${existingRatingId.value}/`
      : `/content/posts/${props.postId}/ratings/${existingRatingId.value}/`;

    await axios.delete(url);

    userRating.value = 0;
    existingRatingId.value = null;
    toast.success("Rating removed successfully!");

    await fetchOverallRating();
  } catch (error) {
    console.error("Error removing rating:", error);
    toast.error("Failed to remove rating. Please try again.");
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

    // ✅ Debug logging
    console.log("Fetched overall rating:", {
      avg_rating: response.data.avg_rating,
      rating_count: response.data.rating_count,
    });

    averageRating.value = parseFloat(response.data.avg_rating) || 0;
    ratingCount.value = parseInt(response.data.rating_count) || 0;
  } catch (error) {
    console.error("Error fetching overall rating:", error);
  }
};

onMounted(() => {
  if (auth.isAuthenticated) {
    fetchUserRating();
  }
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
</script>
