<template>
  <section class="mt-2">
    <div
      class="bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow-lg hover:shadow-2xl transition p-8 max-w-4xl mx-auto"
    >
      <h2 class="text-lg font-bold text-amber-700 dark:text-amber-300 mb-6">
        Comments ({{ comments.length }})
      </h2>

      <!-- New Comment Form -->
      <div v-if="auth.isAuthenticated" class="mb-2">
        <textarea
          v-model="newComment"
          rows="2"
          placeholder="Please, share your thoughts..."
          class="w-full p-2 rounded-xl border border-amber-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-400 transition"
        ></textarea>
        <div class="mt-2 text-right">
          <button
            @click="submitComment"
            :disabled="isSubmitting || !newComment.trim()"
            class="bg-amber-500 hover:bg-amber-600 text-white font-semibold px-5 py-2 mb-2 rounded-xl transition disabled:opacity-50"
          >
            {{ isSubmitting ? "Posting..." : "Post Comment" }}
          </button>
        </div>
      </div>

      <!-- Comment List -->
      <div v-if="comments.length" class="space-y-4">
        <div
          v-for="comment in comments"
          :id="`comment-${comment.id}`"
          :key="comment.id"
          class="relative p-4 rounded-3xl bg-amber-50 dark:bg-slate-700/70 shadow-lg"
        >
          <!-- User & Date -->
          <p class="text-sm text-gray-600 dark:text-gray-300 mb-2">
            <strong class="text-amber-700 dark:text-amber-300">
              {{ comment.user.username }}
            </strong>
            • {{ formatDate(comment.created) }}
          </p>

          <!-- Editable Text -->
          <div v-if="editingCommentId === comment.id">
            <textarea
              v-model="editContent"
              rows="3"
              class="w-full p-3 rounded-xl border border-amber-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-400 transition"
            ></textarea>
            <div class="mt-3 text-right space-x-2">
              <button
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-1 rounded"
                @click="updateComment(comment.id)"
              >
                Save
              </button>
              <button
                class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-1 rounded"
                @click="cancelEdit"
              >
                Cancel
              </button>
            </div>
          </div>
          <p
            v-else
            class="text-gray-800 dark:text-gray-100 whitespace-pre-line"
          >
            {{ comment.content }}
          </p>

          <!-- Action Buttons -->
          <div
            v-if="canManage(comment)"
            class="absolute top-4 right-4 flex gap-3 text-sm"
          >
            <button
              class="text-blue-500 hover:underline font-medium"
              @click="startEdit(comment)"
            >
              Edit
            </button>
            <button
              class="text-red-500 hover:underline font-medium"
              @click="confirmDelete(comment.id)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <p
        v-else
        class="text-center text-gray-500 dark:text-gray-400 italic mt-4"
      >
        No comments yet. Be the first to leave a thought 🐾
      </p>
    </div>

    <!-- Confirm Dialog -->
    <ConfirmDialog
      v-if="showConfirmDialog"
      title="Delete Comment"
      message="Are you sure you want to delete this comment? 🐾"
      confirmText="Yes, delete it"
      cancelText="Cancel"
      @confirm="deleteComment"
      @cancel="
        () => {
          showConfirmDialog = false;
          commentToDelete = null;
        }
      "
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { useToast } from "vue-toastification";
import { useAuthStore } from "@/stores/auth";
import ConfirmDialog from "@/components/ConfirmDialog.vue";

const props = defineProps({
  type: { type: String, required: true }, // 'blog' or 'post'
});

const route = useRoute();
const toast = useToast();
const auth = useAuthStore();

const comments = ref([]);
const newComment = ref("");
const isSubmitting = ref(false);

const editingCommentId = ref(null);
const editContent = ref("");

const showConfirmDialog = ref(false);
const commentToDelete = ref(null);

const objectId = route.params.id;

const fetchComments = async () => {
  try {
    const res = await axios.get(
      `/content/${props.type}s/${objectId}/comments/`
    );
    comments.value = res.data.results || res.data;
  } catch (err) {
    toast.error("Failed to load comments.");
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) return;

  isSubmitting.value = true;
  try {
    await axios.post(`/content/${props.type}s/${objectId}/comments/`, {
      content: newComment.value.trim(),
    });
    newComment.value = "";
    await fetchComments();
    toast.success("Comment added!");
  } catch (err) {
    toast.error("Failed to post comment.");
  } finally {
    isSubmitting.value = false;
  }
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(fetchComments);

// Start editing
const startEdit = (comment) => {
  editingCommentId.value = comment.id;
  editContent.value = comment.content;
};

const cancelEdit = () => {
  editingCommentId.value = null;
  editContent.value = "";
};

// Update comment
const updateComment = async (id) => {
  try {
    await axios.patch(`/content/${props.type}s/${objectId}/comments/${id}/`, {
      content: editContent.value.trim(),
    });
    toast.success("Comment updated!");
    await fetchComments();
    cancelEdit();
  } catch (err) {
    toast.error("Failed to update comment.");
  }
};

// Ask before delete
const confirmDelete = (id) => {
  commentToDelete.value = id;
  showConfirmDialog.value = true;
};

// Perform delete
const deleteComment = async () => {
  if (!commentToDelete.value) return;
  try {
    await axios.delete(
      `/content/${props.type}s/${objectId}/comments/${commentToDelete.value}/`
    );
    // toast.error("Comment deleted!");
    toast.info("Comment deleted.");

    await fetchComments();
  } catch (err) {
    toast.error("Failed to delete comment.");
  } finally {
    showConfirmDialog.value = false;
    commentToDelete.value = null;
  }
};

// Check if current user can manage this comment
const canManage = (comment) => {
  const currentUser = auth.user;
  return (
    currentUser && (currentUser.id === comment.user.id || currentUser.is_staff)
  );
};
</script>
