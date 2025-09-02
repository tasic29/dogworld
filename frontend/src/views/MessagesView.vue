<template>
  <div class="flex h-[80vh]">
    <!-- Conversations list -->
    <aside class="w-1/3 border-r overflow-y-auto">
      <div
        v-for="conv in conversations"
        :key="conv.participant.id"
        class="p-4 border-b hover:bg-amber-50 cursor-pointer"
        @click="selectConversation(conv.participant.id)"
      >
        <p class="font-semibold">{{ conv.participant.username }}</p>
        <p class="text-sm text-gray-600 truncate">
          {{ conv.latest_message?.content || "No messages yet" }}
        </p>
        <p class="text-xs text-gray-400">
          {{ conv.latest_message?.time_ago }}
        </p>
        <span
          v-if="conv.unread_count > 0"
          class="ml-2 bg-amber-500 text-white text-xs px-2 py-0.5 rounded-full"
        >
          {{ conv.unread_count }}
        </span>
      </div>
    </aside>

    <!-- Messages area -->
    <section class="flex-1 flex flex-col">
      <!-- Message list -->
      <div class="flex-1 overflow-y-auto p-4">
        <div
          v-if="!activePartnerId"
          class="h-full flex items-center justify-center text-gray-400"
        >
          Select a conversation to start chatting
        </div>

        <div
          v-else
          v-for="msg in messages"
          :key="msg.id"
          class="mb-2"
          :class="
            msg.sender.id === authStore.user.id ? 'text-right' : 'text-left'
          "
        >
          <span
            class="inline-block px-3 py-2 rounded-xl"
            :class="
              msg.sender.id === authStore.user.id
                ? 'bg-orange-200'
                : 'bg-amber-100'
            "
          >
            {{ msg.content }}
          </span>
          <div class="text-xs text-gray-400 mt-1">
            {{ msg.time_ago }}
          </div>
        </div>
      </div>

      <!-- Input box -->
      <div v-if="activePartnerId" class="border-t p-3 flex">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type a message..."
          class="flex-1 border rounded px-3 py-2"
          @keyup.enter="sendMessage"
        />
        <button
          @click="sendMessage"
          class="ml-2 bg-amber-500 text-white px-4 py-2 rounded"
        >
          Send
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const authStore = useAuthStore();

const conversations = ref([]);
const messages = ref([]);
const newMessage = ref("");
const activePartnerId = ref(null);

const fetchConversations = async () => {
  const res = await axios.get("/messaging/messages/conversations/");
  conversations.value = res.data;
};

const selectConversation = async (partnerId) => {
  activePartnerId.value = partnerId;
  const res = await axios.get(
    `/messaging/messages/conversation/?user_id=${partnerId}`
  );
  messages.value = res.data.results || res.data; // handle paginated or plain
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !activePartnerId.value) return;

  await axios.post("/messaging/messages/", {
    receiver_id: activePartnerId.value,
    content: newMessage.value,
  });

  newMessage.value = "";
  await selectConversation(activePartnerId.value);
  await fetchConversations(); // refresh unread counts
};

onMounted(fetchConversations);
</script>
