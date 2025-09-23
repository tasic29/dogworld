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
              class="space-y-4 overflow-y-auto flex-1 p-2 -m-2 messages-container"
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
import { ref, computed, watch, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "vue-toastification";
import axios from "axios";

import UserSearchModal from "../components/UserSearchModal.vue";
import { useAuthStore } from "../stores/auth";

// 🔧 Setup
const toast = useToast();
const route = useRoute();
const authStore = useAuthStore();

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// 🔧 State
const conversations = ref([]);
const messages = ref([]);
const newMessage = ref("");
const selectedConversation = ref(null);

const loadingConversations = ref(false);
const loadingMessages = ref(false);
const sending = ref(false);
const totalUnreadCount = ref(0);

const error = ref("");
const success = ref("");
const showSearchModal = ref(false);
const messagesContainer = ref(null);

// 🔧 Computed
const currentUserId = computed(() => authStore.user?.id ?? null);

// ==============
// Utility funcs
// ==============
const handleImageError = (event) => {
  event.target.src = `${API_BASE_URL}/media/profile_images/default.webp`;
};

const getAvatarUrl = (user) =>
  user?.profile_image
    ? user.profile_image.startsWith("http")
      ? user.profile_image
      : `${API_BASE_URL}${user.profile_image}`
    : `${API_BASE_URL}/media/profile_images/default.webp`;

const getDisplayName = (user) =>
  user?.full_name ||
  `${user?.first_name || ""} ${user?.last_name || ""}`.trim() ||
  user?.username ||
  "Unknown User";

const getLastMessagePreview = (msg) =>
  msg?.content
    ? msg.content.length > 50
      ? msg.content.substring(0, 50) + "..."
      : msg.content
    : "No messages yet";

const isSelected = (conv) =>
  selectedConversation.value?.participant?.id === conv.participant?.id;

const formatTime = (timestamp) => {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  const diffHrs = (Date.now() - date) / (1000 * 60 * 60);
  if (diffHrs < 1) return "Just now";
  if (diffHrs < 24) return `${Math.floor(diffHrs)}h ago`;
  if (diffHrs < 48) return "Yesterday";
  return date.toLocaleDateString();
};

const formatMessageTime = (timestamp) =>
  timestamp
    ? new Date(timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    : "";

// UI feedback
const showError = (msg) => {
  error.value = msg;
  setTimeout(() => (error.value = ""), 5000);
};
const showSuccess = (msg) => {
  success.value = msg;
  setTimeout(() => (success.value = ""), 3000);
};

// Scroll
const scrollToBottom = async (force = false) => {
  await nextTick();

  if (messagesContainer.value) {
    const container = messagesContainer.value;
    const scrollHeight = container.scrollHeight;
    const clientHeight = container.clientHeight;

    // Only scroll if there are messages to scroll to or if forced
    if (scrollHeight > clientHeight || force) {
      container.scrollTop = scrollHeight;

      // Double-check with a small delay to ensure DOM is fully rendered
      setTimeout(() => {
        if (
          container.scrollHeight >
          container.scrollTop + container.clientHeight
        ) {
          container.scrollTop = container.scrollHeight;
        }
      }, 10);

      // Triple-check with a longer delay for slow renders
      setTimeout(() => {
        if (
          container.scrollHeight >
          container.scrollTop + container.clientHeight
        ) {
          container.scrollTop = container.scrollHeight;
        }
      }, 100);
    }
  }
};

// ==============
// API functions
// ==============
const fetchUnreadCount = async () => {
  try {
    const { data } = await axios.get("/messaging/messages/unread_count/");
    totalUnreadCount.value = data.unread_count;
  } catch (err) {
    console.error("Failed to fetch unread count:", err);
  }
};

const fetchConversations = async () => {
  loadingConversations.value = true;
  try {
    const { data } = await axios.get("/messaging/messages/conversations/");
    conversations.value = data || [];
    await fetchUnreadCount();
  } catch (err) {
    console.error("Failed to fetch conversations:", err);
    showError("Failed to load conversations");
    if (err.response?.status === 401) authStore.logout();
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
    const { data } = await axios.get(
      `/messaging/messages/conversation/?user_id=${userId}`
    );
    const results = data.results || data;
    messages.value = results.map((m) => ({
      ...m,
      isReceived: m.sender.id !== currentUserId.value,
    }));

    // Mark as read if needed
    if (conversation.unread_count > 0) {
      await markConversationAsRead();
    }

    conversation.unread_count = 0;
    await fetchUnreadCount();
  } catch (err) {
    console.error("Failed to fetch messages:", err);
    toast.error("Failed to load messages");
    messages.value = [];
  } finally {
    loadingMessages.value = false;

    // Ensure scroll happens after loading is complete
    await nextTick();
    // Force scroll to bottom when opening a conversation
    await scrollToBottom(true);
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedConversation.value || sending.value)
    return;

  sending.value = true;
  const content = newMessage.value.trim();

  // Create the optimistic message
  const tempMessage = {
    id: `temp-${Date.now()}`,
    content,
    isReceived: false,
    sender: { id: currentUserId.value },
    sent_at: new Date().toISOString(),
    is_read: false,
    sending: true,
  };

  // Add optimistic message to the UI
  messages.value.push(tempMessage);
  const prevScrollHeight = messagesContainer.value.scrollHeight;
  const prevScrollTop = messagesContainer.value.scrollTop;
  newMessage.value = "";

  await nextTick();
  scrollToBottom();

  try {
    // Send the actual message to the backend
    const { data } = await axios.post("/messaging/messages/", {
      receiver_id: selectedConversation.value.participant.id,
      content,
    });

    // Find and replace the temporary message with the real one
    const tempIndex = messages.value.findIndex((m) => m.id === tempMessage.id);
    if (tempIndex !== -1) {
      messages.value[tempIndex] = { ...data, isReceived: false };
    } else {
      // Fallback in case findIndex fails: remove temp and add real
      messages.value = messages.value.filter((m) => m.id !== tempMessage.id);
      messages.value.push({ ...data, isReceived: false });
    }

    // Update the conversation sidebar with the new message
    const conv = conversations.value.find(
      (c) => c.participant.id === selectedConversation.value.participant.id
    );
    if (conv) {
      conv.latest_message = data;
      conv.last_activity = data.sent_at;
      // Move this conversation to the top
      const index = conversations.value.findIndex(
        (c) => c.participant.id === conv.participant.id
      );
      if (index > 0) {
        const [movedConv] = conversations.value.splice(index, 1);
        conversations.value.unshift(movedConv);
      }
    }

    await nextTick();
    scrollToBottom();
  } catch (err) {
    console.error("Send failed:", err.response?.data);
    // Rollback: remove the optimistic message on failure
    messages.value = messages.value.filter((m) => m.id !== tempMessage.id);
    // Restore scroll position
    await nextTick();
    messagesContainer.value.scrollTop = prevScrollTop;

    const msg =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      Object.values(err.response?.data || {})
        .flat()
        .join(", ") ||
      "Failed to send message.";
    toast.err(msg);
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
    selectedConversation.value.unread_count = 0;
    messages.value.forEach((m) => {
      if (m.isReceived) m.is_read = true;
    });
    await fetchUnreadCount();
  } catch (err) {
    console.error("Failed to mark as read:", err);
    showError("Failed to mark conversation as read");
  }
};

const deleteConversation = async () => {
  if (!selectedConversation.value) return;
  if (!confirm("Are you sure you want to delete this conversation?")) return;

  try {
    // Corrected to use POST, which is a more reliable method for custom actions
    await axios.post("/messaging/messages/delete_conversation/", {
      user_id: selectedConversation.value.participant.id,
    });

    // Optimistically update the UI
    conversations.value = conversations.value.filter(
      (c) => c.participant.id !== selectedConversation.value.participant.id
    );
    selectedConversation.value = null;
    messages.value = [];
    await fetchUnreadCount();
    toast.success("Conversation deleted");
  } catch (err) {
    console.error("Delete failed:", err);
    toast.error("Failed to delete conversation");
  }
};

const loadOlderMessages = async () => {
  if (!selectedConversation.value) return;

  loadingMessages.value = true;

  try {
    const oldestMessage = messages.value[0];
    const { data } = await axios.get(
      `/messaging/messages/conversation/?user_id=${selectedConversation.value.participant.id}&before=${oldestMessage.id}`
    );

    const olderMessages = data.results || data;

    if (olderMessages.length > 0) {
      // Remember current scroll position before adding messages
      const prevScrollHeight = messagesContainer.value.scrollHeight;

      // Prepend the new (older) messages
      messages.value = [
        ...olderMessages.map((m) => ({
          ...m,
          isReceived: m.sender.id !== currentUserId.value,
        })),
        ...messages.value,
      ];

      await nextTick();

      // Adjust scroll so user stays at the same spot
      const newScrollHeight = messagesContainer.value.scrollHeight;
      messagesContainer.value.scrollTop = newScrollHeight - prevScrollHeight;
    }
  } catch (err) {
    console.error("Failed to load older messages:", err);
  } finally {
    loadingMessages.value = false;
  }
};

// ==============
// Search modal
// ==============
const handleSelectUser = async (user) => {
  let conv = conversations.value.find((c) => c.participant.id === user.id);

  if (conv) {
    await selectConversation(conv);
    toast.success(`Conversation with ${getDisplayName(user)} selected!`);
  } else {
    conv = { participant: user, latest_message: null, unread_count: 0 };
    selectedConversation.value = conv;
    messages.value = [];
    toast.success(`Conversation with ${getDisplayName(user)} started!`);

    // For new conversations, ensure we scroll after DOM updates
    await nextTick();
    await scrollToBottom(true);
  }

  showSearchModal.value = false;
};

// ==============
// Route handling
// ==============
const openConversationByUserId = async (userId) => {
  const conv = conversations.value.find(
    (c) => c.participant.id.toString() === userId
  );
  if (conv) {
    await selectConversation(conv);
  } else {
    console.warn("No conversation found for user", userId);
  }
};

onMounted(async () => {
  await fetchConversations();
  if (route.params.userId) {
    await openConversationByUserId(route.params.userId);
  }
});

watch(
  () => route.params.userId,
  async (newUserId) => {
    if (newUserId) await openConversationByUserId(newUserId);
  }
);

watch(
  messages,
  async (newMessages, oldMessages) => {
    // Only auto-scroll if we added a message (not when loading a conversation)
    if (newMessages.length > oldMessages.length) {
      await nextTick();
      scrollToBottom();
    }
  },
  { deep: true, immediate: false }
);
</script>

<style scoped>
.messages-container {
  scroll-behavior: smooth;
}
</style>
