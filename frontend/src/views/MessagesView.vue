<template>
  <div>
    <section
      class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
    >
      <div
        class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 h-[75vh]"
      >
        <!-- Conversations Sidebar -->
        <aside
          class="lg:col-span-1 bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 flex flex-col"
        >
          <div
            class="flex items-center justify-between mb-6 pb-4 border-b border-amber-200 dark:border-slate-700"
          >
            <div class="flex items-center gap-2">
              <button
                @click="showSearchModal = true"
                class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold py-3 px-6 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
                title="Start new conversation"
              >
                New Message
              </button>
              <span
                v-if="totalUnreadCount > 0"
                class="bg-red-500 text-white text-sm rounded-full px-3 py-1"
              >
                {{ totalUnreadCount }}
              </span>
            </div>
          </div>
          <!-- Loading State -->
          <div v-if="loadingConversations" class="flex justify-center py-8">
            <div
              class="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"
            ></div>
          </div>
          <!-- Conversations List -->
          <div v-else class="space-y-4 overflow-y-auto flex-1">
            <div
              v-for="conversation in conversations"
              :key="conversation.participant?.id"
              @click="selectConversation(conversation)"
              :class="{
                'bg-amber-100 dark:bg-amber-800/50': isSelected(conversation),
                'hover:bg-amber-50 dark:hover:bg-slate-700':
                  !isSelected(conversation),
              }"
              class="flex items-center gap-4 p-3 rounded-lg cursor-pointer transition-all duration-200"
            >
              <div class="relative">
                <img
                  :src="getAvatarUrl(conversation.participant)"
                  :alt="`${getDisplayName(conversation.participant)} avatar`"
                  class="w-12 h-12 rounded-full object-cover shadow"
                  @error="handleImageError"
                />
                <div
                  v-if="conversation.unread_count > 0"
                  class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
                >
                  {{
                    conversation.unread_count > 9
                      ? "9+"
                      : conversation.unread_count
                  }}
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <h3
                  class="font-semibold text-gray-800 dark:text-gray-200 truncate"
                >
                  {{ getDisplayName(conversation.participant) }}
                </h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                  {{ getLastMessagePreview(conversation.latest_message) }}
                </p>
              </div>
              <div class="flex flex-col items-end">
                <p class="text-xs text-gray-400 dark:text-gray-500">
                  {{ formatTime(conversation.last_activity) }}
                </p>
                <span
                  v-if="conversation.unread_count > 0"
                  class="bg-red-500 text-white text-xs rounded-full px-2 py-1 mt-1"
                >
                  {{ conversation.unread_count }}
                </span>
              </div>
            </div>
            <p
              v-if="!conversations.length && !loadingConversations"
              class="text-center text-gray-500 dark:text-gray-400 mt-8"
            >
              No conversations yet. Start chatting with someone!
            </p>
          </div>
        </aside>
        <!-- Messages Area -->
        <div
          class="lg:col-span-2 bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow-lg p-6 flex flex-col"
        >
          <!-- Selected Conversation View -->
          <div v-if="selectedConversation" class="flex flex-col h-full">
            <!-- Conversation Header -->
            <div
              class="flex items-center gap-4 pb-4 border-b border-amber-200 dark:border-slate-700 mb-6"
            >
              <img
                :src="getAvatarUrl(selectedConversation.participant)"
                :alt="`${getDisplayName(
                  selectedConversation.participant
                )} avatar`"
                class="w-14 h-14 rounded-full object-cover shadow"
                @error="handleImageError"
              />
              <div class="flex-1">
                <h2
                  class="text-2xl font-semibold text-gray-800 dark:text-gray-200"
                >
                  {{ getDisplayName(selectedConversation.participant) }}
                </h2>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ selectedConversation.participant.email || "Active now" }}
                </p>
              </div>
              <!-- Conversation Actions -->
              <div class="flex gap-2">
                <button
                  v-if="selectedConversation.unread_count > 0"
                  @click="markConversationAsRead"
                  class="px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition"
                >
                  Mark as Read
                </button>
                <button
                  @click="deleteConversation"
                  class="px-3 py-2 text-sm bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition"
                >
                  Delete
                </button>
              </div>
            </div>
            <!-- Messages Container -->
            <div
              class="space-y-4 overflow-y-auto flex-1 p-2 -m-2"
              ref="messagesContainer"
              @scroll="handleScroll"
            >
              <!-- Loading older messages -->
              <div v-if="loadingMessages" class="flex justify-center py-4">
                <div
                  class="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-500"
                ></div>
              </div>
              <!-- Messages -->
              <div
                v-for="message in messages"
                :key="message.id"
                :class="{
                  'flex justify-start': message.isReceived,
                  'flex justify-end': !message.isReceived,
                }"
              >
                <div
                  :class="{
                    'bg-gray-200 dark:bg-slate-700 text-gray-800 dark:text-gray-200':
                      message.isReceived,
                    'bg-amber-100 dark:bg-amber-800 text-amber-900 dark:text-amber-100':
                      !message.isReceived,
                  }"
                  class="max-w-md px-4 py-2 rounded-xl shadow-sm"
                >
                  <p class="whitespace-pre-wrap break-words">
                    {{ message.content }}
                  </p>
                  <div class="flex justify-between items-center mt-2">
                    <p
                      class="text-xs"
                      :class="
                        message.isReceived
                          ? 'text-gray-500'
                          : 'text-amber-700 dark:text-amber-200'
                      "
                    >
                      {{ formatMessageTime(message.sent_at) }}
                    </p>
                    <div
                      v-if="!message.isReceived"
                      class="flex items-center gap-1"
                    >
                      <span
                        v-if="message.is_read"
                        class="text-xs text-blue-500"
                        title="Read"
                      >
                        ✓✓
                      </span>
                      <span v-else class="text-xs text-gray-400" title="Sent">
                        ✓
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Message Input -->
            <form @submit.prevent="sendMessage" class="mt-6">
              <div class="flex items-center gap-4">
                <input
                  v-model="newMessage"
                  type="text"
                  placeholder="Type your message..."
                  required
                  :disabled="sending"
                  maxlength="1000"
                  class="flex-1 px-4 py-3 rounded-full border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400 dark:bg-slate-700 dark:border-slate-600 dark:text-gray-200 disabled:opacity-50 transition"
                />
                <button
                  type="submit"
                  :disabled="sending || !newMessage.trim()"
                  class="px-6 py-3 bg-amber-500 text-white font-semibold rounded-full shadow hover:bg-amber-600 focus:ring-2 focus:ring-amber-400 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ sending ? "Sending..." : "Send" }}
                </button>
              </div>
              <p
                v-if="newMessage.length > 900"
                class="text-xs text-gray-500 mt-1"
              >
                {{ 1000 - newMessage.length }} characters remaining
              </p>
            </form>
          </div>
          <!-- No Conversation Selected -->
          <div
            v-else
            class="text-center text-gray-500 dark:text-gray-400 self-center m-auto"
          >
            <p class="text-lg">Select a conversation to start chatting!</p>
            <p class="text-6xl mt-4">💬</p>
          </div>
        </div>
      </div>
      <!-- Error Toast -->
      <div
        v-if="error"
        class="fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50"
      >
        {{ error }}
        <button
          @click="error = ''"
          class="ml-2 hover:bg-red-600 px-2 py-1 rounded"
        >
          ×
        </button>
      </div>
      <!-- Success Toast -->
      <div
        v-if="success"
        class="fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50"
      >
        {{ success }}
        <button
          @click="success = ''"
          class="ml-2 hover:bg-green-600 px-2 py-1 rounded"
        >
          ×
        </button>
      </div>
    </section>
    <UserSearchModal
      :show="showSearchModal"
      :API_BASE_URL="API_BASE_URL"
      :currentUserId="currentUserId"
      @close="showSearchModal = false"
      @selectUser="handleSelectUser"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, watch } from "vue";
import UserSearchModal from "../components/UserSearchModal.vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

// State variables
const conversations = ref([]);
const messages = ref([]);
const newMessage = ref("");
const selectedConversation = ref(null);
const sending = ref(false);
const loadingConversations = ref(false);
const loadingMessages = ref(false);
const messagesContainer = ref(null);
const error = ref("");
const success = ref("");
const totalUnreadCount = ref(0);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const authStore = useAuthStore();

// Computed properties
const currentUserId = computed(() => authStore.user?.id ?? null);

const showSearchModal = ref(false);
// Utility functions
const handleSelectUser = async (user) => {
  showSearchModal.value = false;
  await fetchConversations();
  const newConv = conversations.value.find(
    (conv) => conv.participant.id === user.id
  );
  if (newConv) {
    await selectConversation(newConv);
  }
  showSuccess(`Conversation with ${getDisplayName(user)} started!`);
};
const handleImageError = (event) => {
  event.target.src = "/default-avatar.png";
};

const getAvatarUrl = (participant) => {
  if (!participant?.profile_image) {
    return `${API_BASE_URL}/media/profile_images/default.webp`;
  }
  return participant.profile_image.startsWith("http")
    ? participant.profile_image
    : `${API_BASE_URL}${participant.profile_image}`;
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

const getLastMessagePreview = (message) => {
  if (!message) return "No messages yet";
  return message.content?.length > 50
    ? `${message.content.substring(0, 50)}...`
    : message.content;
};

const isSelected = (conversation) => {
  return (
    selectedConversation.value?.participant?.id === conversation.participant?.id
  );
};

const formatTime = (timestamp) => {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  const now = new Date();
  const diffInHours = (now - date) / (1000 * 60 * 60);

  if (diffInHours < 1) return "Just now";
  if (diffInHours < 24) return `${Math.floor(diffInHours)}h ago`;
  if (diffInHours < 48) return "Yesterday";
  return date.toLocaleDateString();
};

const formatMessageTime = (timestamp) => {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const showError = (message) => {
  error.value = message;
  setTimeout(() => (error.value = ""), 5000);
};

const showSuccess = (message) => {
  success.value = message;
  setTimeout(() => (success.value = ""), 3000);
};

// Auto-scroll to bottom
const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// API functions
const fetchUnreadCount = async () => {
  try {
    const res = await axios.get("/messaging/messages/unread_count/");
    totalUnreadCount.value = res.data.unread_count;
  } catch (err) {
    console.error("Failed to fetch unread count:", err);
  }
};

const fetchConversations = async () => {
  loadingConversations.value = true;
  try {
    const res = await axios.get("/messaging/messages/conversations/");
    conversations.value = res.data || [];
    await fetchUnreadCount();
  } catch (err) {
    console.error("Failed to fetch conversations:", err);
    showError("Failed to load conversations");
    if (err.response?.status === 401) {
      // Handle authentication error
      authStore.logout();
    }
  } finally {
    loadingConversations.value = false;
  }
};

const selectConversation = async (conversation) => {
  if (isSelected(conversation)) return;

  selectedConversation.value = conversation;
  loadingMessages.value = true;

  try {
    const userId = conversation.participant.id;
    const res = await axios.get(
      `/messaging/messages/conversation/?user_id=${userId}`
    );

    const messageData = res.data.results || res.data;
    messages.value = messageData.map((message) => ({
      ...message,
      isReceived: message.sender.id !== currentUserId.value,
    }));

    // Update conversation unread count locally
    conversation.unread_count = 0;
    await fetchUnreadCount();

    scrollToBottom();
  } catch (err) {
    console.error("Failed to fetch conversation messages:", err);
    showError("Failed to load messages");
    messages.value = [];
  } finally {
    loadingMessages.value = false;
  }
};
watch(messages, () => scrollToBottom());

const sendMessage = async () => {
  if (
    !newMessage.value.trim() ||
    !selectedConversation.value ||
    sending.value
  ) {
    return;
  }

  const messageContent = newMessage.value.trim();
  sending.value = true;

  try {
    const response = await axios.post("/messaging/messages/", {
      receiver_id: selectedConversation.value.participant.id,
      content: messageContent,
    });

    // Add message to local state immediately
    const newMsg = {
      ...response.data,
      isReceived: false,
    };
    messages.value.push(newMsg);

    // Clear input and scroll
    newMessage.value = "";
    scrollToBottom();

    // Update conversations list
    await fetchConversations();
  } catch (err) {
    console.error("Failed to send message:", err);
    console.error("Error response:", err.response?.data);
    console.error("Error status:", err.response?.status);

    const errorMsg =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      Object.values(err.response?.data || {})
        .flat()
        .join(", ") ||
      "Failed to send message. Please try again.";
    showError(errorMsg);
  } finally {
    sending.value = false;
  }
};

const markConversationAsRead = async () => {
  if (!selectedConversation.value) return;

  try {
    await axios.post("/messaging/messages/mark_conversation_as_read/", {
      user_id: selectedConversation.value.participant.id,
    });

    // Update local state
    selectedConversation.value.unread_count = 0;
    messages.value.forEach((msg) => {
      if (msg.isReceived) msg.is_read = true;
    });

    await fetchUnreadCount();
    showSuccess("Conversation marked as read");
  } catch (err) {
    console.error("Failed to mark conversation as read:", err);
    showError("Failed to mark conversation as read");
  }
};

const deleteConversation = async () => {
  if (!selectedConversation.value) return;

  if (!confirm("Are you sure you want to delete this conversation?")) {
    return;
  }

  try {
    await axios.delete("/messaging/messages/delete_conversation/", {
      data: { user_id: selectedConversation.value.participant.id },
    });

    // Remove from local state
    conversations.value = conversations.value.filter(
      (conv) =>
        conv.participant.id !== selectedConversation.value.participant.id
    );
    selectedConversation.value = null;
    messages.value = [];

    await fetchUnreadCount();
    showSuccess("Conversation deleted");
  } catch (err) {
    console.error("Failed to delete conversation:", err);
    showError("Failed to delete conversation");
  }
};

const handleScroll = (event) => {
  // Could implement infinite scroll for older messages here
  const { scrollTop } = event.target;
  if (scrollTop === 0) {
    // Load older messages if needed
    console.log("Reached top - could load older messages");
  }
};

// Auto-dismiss toasts
watch(error, (newError) => {
  if (newError) {
    setTimeout(() => (error.value = ""), 5000);
  }
});

watch(success, (newSuccess) => {
  if (newSuccess) {
    setTimeout(() => (success.value = ""), 3000);
  }
});

// Initialize
onMounted(() => {
  fetchConversations();
});
</script>
