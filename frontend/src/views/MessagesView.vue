<template>
  <section
    class="min-h-screen bg-gradient-to-b from-orange-50 to-amber-100 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
  >
    <div
      class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 h-[75vh]"
    >
      <aside
        class="lg:col-span-1 bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 flex flex-col"
      >
        <h2
          class="text-2xl font-bold text-amber-700 dark:text-amber-300 mb-6 border-b pb-4 border-amber-200 dark:border-slate-700"
        >
          Conversations
        </h2>

        <div class="space-y-4 overflow-y-auto flex-1">
          <div
            v-for="conversation in conversations"
            :key="conversation.id || conversation.participant?.id"
            @click="selectConversation(conversation)"
            :class="{
              'bg-amber-100 dark:bg-amber-800/50':
                selectedConversation &&
                selectedConversation.participant?.id ===
                  conversation.participant?.id,
              'hover:bg-amber-50 dark:hover:bg-slate-700':
                selectedConversation &&
                selectedConversation.participant?.id !==
                  conversation.participant?.id,
            }"
            class="flex items-center gap-4 p-3 rounded-lg cursor-pointer transition"
          >
            <img
              :src="conversation.user.avatar || '/default-avatar.png'"
              :alt="`${conversation.user.name} avatar`"
              class="w-12 h-12 rounded-full object-cover shadow"
              @error="handleImageError"
            />
            <div class="flex-1 min-w-0">
              <h3
                class="font-semibold text-gray-800 dark:text-gray-200 truncate"
              >
                {{ conversation.user.name }}
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                {{ conversation.lastMessage }}
              </p>
            </div>
            <div class="flex flex-col items-end">
              <p class="text-xs text-gray-400 dark:text-gray-500">
                {{ conversation.lastMessageTime }}
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
            v-if="!conversations.length"
            class="text-center text-gray-500 dark:text-gray-400 mt-8"
          >
            No conversations yet.
          </p>
        </div>
      </aside>

      <div
        class="lg:col-span-2 bg-white/80 dark:bg-slate-800/90 rounded-2xl shadow-lg p-6 flex flex-col"
      >
        <div v-if="selectedConversation" class="flex flex-col h-full">
          <div
            class="flex items-center gap-4 pb-4 border-b border-amber-200 dark:border-slate-700 mb-6"
          >
            <img
              :src="selectedConversation.user.avatar || '/default-avatar.png'"
              :alt="`${selectedConversation.user.name} avatar`"
              class="w-14 h-14 rounded-full object-cover shadow"
              @error="handleImageError"
            />
            <div>
              <h2
                class="text-2xl font-semibold text-gray-800 dark:text-gray-200"
              >
                {{ selectedConversation.user.name }}
              </h2>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ selectedConversation.user.email || "Online" }}
              </p>
            </div>
          </div>

          <div
            class="space-y-4 overflow-y-auto flex-1 p-2 -m-2"
            ref="messagesContainer"
          >
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
                class="max-w-md px-4 py-2 rounded-xl"
              >
                <p>{{ message.text }}</p>
                <div class="flex justify-between items-center mt-1">
                  <p
                    class="text-xs"
                    :class="
                      message.isReceived
                        ? 'text-gray-500'
                        : 'text-amber-700 dark:text-amber-200'
                    "
                  >
                    {{ message.time }}
                  </p>
                  <span
                    v-if="!message.isReceived && message.is_read"
                    class="text-xs text-blue-500"
                  >
                    ✓✓
                  </span>
                  <span
                    v-else-if="!message.isReceived"
                    class="text-xs text-gray-400"
                  >
                    ✓
                  </span>
                </div>
              </div>
            </div>
          </div>

          <form @submit.prevent="sendMessage" class="mt-6">
            <div class="flex items-center gap-4">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type your message..."
                required
                :disabled="sending"
                class="flex-1 px-4 py-3 rounded-full border border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400 dark:bg-slate-700 dark:border-slate-600 dark:text-gray-200 disabled:opacity-50"
              />
              <button
                type="submit"
                :disabled="sending || !newMessage.trim()"
                class="px-6 py-3 bg-amber-500 text-white font-semibold rounded-full shadow hover:bg-amber-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ sending ? "Sending..." : "Send" }}
              </button>
            </div>
          </form>
        </div>

        <div
          v-else
          class="text-center text-gray-500 dark:text-gray-400 self-center m-auto"
        >
          <p>Select a conversation to start chatting!</p>
          <p class="text-6xl mt-4">🐾</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

// State variables
const conversations = ref([]);
const messages = ref([]);
const newMessage = ref("");
const selectedConversation = ref(null);
const sending = ref(false);
const messagesContainer = ref(null);
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Import your auth store
const authStore = useAuthStore();

// Handle image errors by setting a default avatar
const handleImageError = (event) => {
  event.target.src = "/default-avatar.png";
};

// Helper functions for data mapping
const mapConversationData = (apiData) => {
  return apiData.map((item) => ({
    // Map participant data to user object
    user: {
      id: item.participant.id,
      name: item.participant.full_name || item.participant.username,
      email: item.participant.email,
      // Fix: Build full URL for avatar with your server URL
      avatar: item.participant.profile_image
        ? `${API_BASE_URL}${item.participant.profile_image}`
        : `${API_BASE_URL}/media/profile_images/default.webp`,
    },
    // Map latest message data
    lastMessage: item.latest_message?.content || "No messages yet",
    lastMessageTime: item.latest_message?.time_ago || "",
    // Include unread count and other data
    unread_count: item.unread_count || 0,
    last_activity: item.last_activity,
    // Store the raw conversation data
    participant: item.participant,
    latest_message: item.latest_message,
  }));
};

const mapMessagesData = (apiData, currentUserId) => {
  return apiData.map((message) => ({
    id: message.id,
    text: message.content,
    time: message.time_ago,
    // Fix: Check sender vs current user, not receiver
    isReceived: message.sender.id !== currentUserId,
    is_read: message.is_read,
    sender: message.sender,
    receiver: message.receiver,
  }));
};

// Auto-scroll to bottom of messages
const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// API calls and logic
const fetchConversations = async () => {
  try {
    const res = await axios.get("/messaging/messages/conversations/");
    console.log("Conversations response:", res.data); // Debug log
    conversations.value = mapConversationData(res.data);
  } catch (error) {
    console.error("Failed to fetch conversations:", error);
    // Handle different error types
    if (error.response?.status === 401) {
      console.error("Authentication required");
    }
  }
};

const selectConversation = async (conversation) => {
  selectedConversation.value = conversation;

  try {
    const userId = conversation.participant.id;
    const res = await axios.get(
      `/messaging/messages/conversation/?user_id=${userId}`
    );

    console.log("Messages response:", res.data); // Debug log

    const currentUserId = authStore.user?.id;
    messages.value = mapMessagesData(
      res.data.results || res.data,
      currentUserId
    );

    // Mark messages as read
    await markMessagesAsRead(userId);

    // Scroll to bottom
    scrollToBottom();
  } catch (error) {
    console.error("Failed to fetch conversation messages:", error);
    messages.value = [];
  }
};

const markMessagesAsRead = async (senderId) => {
  try {
    await axios.post(`/messaging/messages/mark-read/`, {
      sender_id: senderId,
    });
  } catch (error) {
    console.error("Failed to mark messages as read:", error);
  }
};

const sendMessage = async () => {
  if (
    !newMessage.value.trim() ||
    !selectedConversation.value ||
    sending.value
  ) {
    return;
  }

  sending.value = true;

  try {
    const response = await axios.post("/messaging/messages/", {
      receiver_id: selectedConversation.value.participant.id,
      content: newMessage.value,
    });

    console.log("Message sent:", response.data); // Debug log

    // Add the new message to the local messages array immediately
    const newMsg = {
      id: response.data.id,
      text: newMessage.value,
      time: "Just now",
      isReceived: false,
      is_read: false,
    };
    messages.value.push(newMsg);

    // Clear the input
    newMessage.value = "";

    // Scroll to bottom
    scrollToBottom();

    // Refresh conversations to update timestamps and unread counts
    await fetchConversations();
  } catch (error) {
    console.error("Failed to send message:", error);
    // Show error message to user
    alert("Failed to send message. Please try again.");
  } finally {
    sending.value = false;
  }
};

onMounted(() => {
  fetchConversations();
});
</script>
