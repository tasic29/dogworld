<template>
  <nav
    class="sticky top-0 z-50 bg-gradient-to-r from-amber-50 to-orange-50 dark:from-slate-800 dark:to-slate-800 border-b-4 border-amber-300 dark:border-amber-600 shadow-xl transition-all duration-300"
  >
    <div
      class="max-w-screen-xl mx-auto flex items-center justify-between px-4 py-3"
    >
      <router-link :to="{ name: 'home' }" class="flex items-center group">
        <div class="relative">
          <img
            :src="logo"
            alt="Dogworld Logo"
            class="h-12 w-auto rounded-full border-2 border-amber-300 group-hover:border-amber-400 transition-all duration-300 shadow-md"
          />
          <div
            class="absolute -top-1 -right-1 text-amber-600 dark:text-amber-300 animate-bounce"
          >
            🐾
          </div>
        </div>
        <span
          class="ml-3 text-2xl font-bold bg-gradient-to-r from-amber-700 to-orange-600 bg-clip-text text-transparent dark:from-amber-300 dark:to-orange-300 group-hover:scale-105 group-hover:from-amber-600 group-hover:to-orange-500 transition-all duration-300 ease-in-out"
        >
          DOGWORLD
        </span>
        <div class="hidden lg:flex ml-2 space-x-1">
          <span class="text-amber-500 text-sm animate-pulse">🐾</span>
          <span class="text-orange-500 text-xs animate-pulse delay-75">🐾</span>
        </div>
      </router-link>

      <ul class="hidden lg:flex space-x-4 font-medium items-center">
        <li>
          <router-link
            :to="{ name: 'home' }"
            class="flex items-center text-gray-700 dark:text-gray-300 px-3 py-2 rounded-full transition-all hover:bg-amber-100 dark:hover:bg-slate-700 hover:text-amber-700 dark:hover:text-amber-300"
          >
            🏠 Home
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'blogs' }"
            class="flex items-center text-gray-700 dark:text-gray-300 px-3 py-2 rounded-full transition-all hover:bg-amber-100 dark:hover:bg-slate-700 hover:text-amber-700 dark:hover:text-amber-300"
          >
            📝 Blog
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'posts' }"
            class="flex items-center text-gray-700 dark:text-gray-300 px-3 py-2 rounded-full transition-all hover:bg-amber-100 dark:hover:bg-slate-700 hover:text-amber-700 dark:hover:text-amber-300"
          >
            📸 Posts
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'marketplace' }"
            class="flex items-center text-gray-700 dark:text-gray-300 px-3 py-2 rounded-full transition-all hover:bg-amber-100 dark:hover:bg-slate-700 hover:text-amber-700 dark:hover:text-amber-300"
          >
            🛒 Marketplace
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'services' }"
            class="flex items-center text-gray-700 dark:text-gray-300 px-3 py-2 rounded-full transition-all hover:bg-amber-100 dark:hover:bg-slate-700 hover:text-amber-700 dark:hover:text-amber-300"
          >
            🐕‍🦺 Services
          </router-link>
        </li>
        <li>
          <router-link
            v-if="authStore.isAuthenticated"
            :to="{ name: 'messages' }"
            class="flex items-center text-gray-700 dark:text-gray-300 px-3 py-2 rounded-full transition-all hover:bg-amber-100 dark:hover:bg-slate-700 hover:text-amber-700 dark:hover:text-amber-300"
          >
            💬 Messages
          </router-link>
        </li>
      </ul>

      <div class="hidden lg:flex items-center gap-3">
        <template v-if="!authStore.isAuthenticated">
          <router-link
            :to="{ name: 'signup' }"
            class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white px-4 py-2 rounded-full shadow-lg font-medium transition transform hover:scale-105"
          >
            🦴 Join the Pack
          </router-link>
          <router-link
            :to="{ name: 'login' }"
            class="text-amber-700 font-medium hover:text-amber-900 dark:text-amber-300 dark:hover:text-white transition"
          >
            🔐 Login
          </router-link>
        </template>
        <template v-else>
          <router-link
            v-if="authStore.isAuthenticated && authStore.user"
            :to="{
              name: 'public-profile',
              params: { username: authStore.user.username },
            }"
          >
            <p
              class="text-sm font-medium text-amber-700 dark:text-amber-300 px-4 py-2 bg-gradient-to-r from-amber-100 to-orange-100 dark:from-slate-700 dark:to-slate-800 rounded-full border border-amber-400 dark:border-slate-600 shadow-md transition transform hover:scale-105"
            >
              Welcome, {{ authStore.user.username }}!
            </p>
          </router-link>

          <div class="relative" ref="accountDropdownRef">
            <button
              @click="showDropdown = !showDropdown"
              class="focus:outline-none"
            >
              <img
                v-if="authStore.user && authStore.user.profile_image"
                :src="authStore.user.profile_image"
                alt="Profile"
                class="h-10 w-10 rounded-full border-2 border-amber-400 object-cover hover:border-amber-500 transition-all duration-300 shadow-md"
              />
              <div
                v-else
                class="h-10 w-10 rounded-full bg-amber-300 flex items-center justify-center text-amber-900 text-xl font-bold border-2 border-amber-400 shadow-md"
              >
                {{ authStore.user?.username[0].toUpperCase() }}
              </div>
            </button>

            <div
              v-if="showDropdown"
              class="absolute right-0 mt-2 w-48 bg-white dark:bg-slate-800 shadow-lg rounded-lg z-50 border border-amber-200 dark:border-slate-600"
            >
              <router-link
                :to="{ name: 'account' }"
                class="block w-full text-left py-2 px-4 hover:bg-amber-100 dark:hover:bg-slate-700 rounded-md transition"
              >
                ⚙️ Profile Settings
              </router-link>
              <button
                @click="logout"
                class="block w-full text-left py-2 px-4 text-red-600 hover:bg-amber-100 dark:hover:bg-slate-700 rounded-md transition"
              >
                🚪 Logout
              </button>
            </div>
          </div>

          <div class="relative mr-3" ref="notifRef">
            <button
              class="text-xl relative text-amber-700 dark:text-amber-300"
              @click="showNotifDropdown = !showNotifDropdown"
            >
              🔔
              <span
                v-if="notifications.length"
                class="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full px-1"
              >
                {{ notifications.length }}
              </span>
            </button>

            <div
              v-if="showNotifDropdown"
              class="absolute right-0 mt-2 w-72 bg-white dark:bg-slate-800 shadow-xl rounded-lg z-50 border border-amber-200 dark:border-slate-700 max-h-96 overflow-y-auto"
            >
              <p
                v-if="!notifications.length"
                class="p-4 text-gray-600 dark:text-gray-300 text-sm text-center"
              >
                No new notifications
              </p>

              <ul v-else>
                <li
                  v-for="notif in notifications"
                  :key="notif.id"
                  @click="handleNotificationClick(notif)"
                  class="px-4 py-2 hover:bg-amber-100 dark:hover:bg-slate-700 cursor-pointer text-sm border-b dark:border-slate-600"
                >
                  {{ notif.message }}
                </li>
              </ul>
            </div>
          </div>
        </template>
      </div>

      <button
        @click="isMobileMenuOpen = !isMobileMenuOpen"
        class="lg:hidden text-amber-600 dark:text-amber-300 focus:outline-none"
      >
        <span class="sr-only">Toggle menu</span>
        <svg
          v-if="!isMobileMenuOpen"
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>

    <div v-if="isMobileMenuOpen" class="px-4 pb-4 lg:hidden">
      <div
        v-if="authStore.isAuthenticated"
        class="mb-3 px-4 py-2 bg-gradient-to-r from-amber-100 to-orange-100 dark:from-slate-700 dark:to-slate-800 rounded-lg border border-amber-200 dark:border-slate-600"
      >
        <router-link
          v-if="authStore.isAuthenticated && authStore.user"
          :to="{
            name: 'public-profile',
            params: { username: authStore.user.username },
          }"
        >
          <p class="text-sm font-medium text-amber-700 dark:text-amber-300">
            🐕 Welcome, {{ authStore.user.username }}!
          </p>
        </router-link>
      </div>

      <ul class="space-y-2">
        <li>
          <router-link
            :to="{ name: 'home' }"
            class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
          >
            🏠 Home
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'blogs' }"
            class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
          >
            📝 Blog
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'posts' }"
            class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
            >📸 Posts</router-link
          >
        </li>
        <li>
          <router-link
            :to="{ name: 'marketplace' }"
            class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
            >🛒 Marketplace</router-link
          >
        </li>
        <li>
          <router-link
            :to="{ name: 'services' }"
            class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
            >🐕‍🦺 Services</router-link
          >
        </li>
        <router-link
          :to="{ name: 'messages' }"
          class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
        >
          💬 Messages
        </router-link>
        <template v-if="!authStore.isAuthenticated">
          <li>
            <router-link
              :to="{ name: 'signup' }"
              class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
            >
              🦴 Join the Pack
            </router-link>
          </li>
          <li>
            <router-link
              :to="{ name: 'login' }"
              class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
            >
              🔐 Login
            </router-link>
          </li>
        </template>
        <template v-else>
          <li>
            <router-link
              :to="{ name: 'account' }"
              class="block px-4 py-2 rounded hover:bg-amber-100 dark:hover:bg-slate-700"
            >
              ⚙️ Profile Settings
            </router-link>
          </li>
          <li>
            <button
              @click="logout"
              class="block w-full text-left py-2 px-4 text-red-600 hover:bg-amber-100 dark:hover:bg-slate-700 rounded"
            >
              🚪 Logout
            </button>
          </li>
        </template>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import logo from "../assets/logo.webp";
import axios from "axios";

const isMobileMenuOpen = ref(false);
const showDropdown = ref(false);
const accountDropdownRef = ref(null);
const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const notifications = ref([]);
const showNotifDropdown = ref(false);
const notifRef = ref(null);

const fetchNotifications = async () => {
  if (!authStore.isAuthenticated) return;

  try {
    const response = await axios.get("/messaging/notifications/");
    notifications.value = response.data.filter((n) => !n.is_read);
  } catch (error) {
    // Only log actual errors, not auth issues
    if (error.response?.status !== 401) {
      console.error("Failed to fetch notifications:", error);
    }
  }
};

const markAsRead = async (id) => {
  try {
    await axios.patch(`/messaging/notifications/${id}/mark_as_read/`);
    notifications.value = notifications.value.filter((n) => n.id !== id);
  } catch (err) {
    console.error("Error marking notification as read:", err);

    if (err.response?.status === 403) {
      toast.error(
        "You don't have permission to mark this notification as read"
      );
    } else if (err.response?.status === 404) {
      toast.error("Notification not found");
      // Remove from local array anyway since it doesn't exist
      notifications.value = notifications.value.filter((n) => n.id !== id);
    } else {
      toast.error("Failed to mark notification as read");
    }
  }
};

const handleNotificationClick = async (notif) => {
  try {
    await markAsRead(notif.id);
    showNotifDropdown.value = false;

    if (notif.target_url) {
      // Check if the URL is a message URL
      const regex = /^\/messages\/conversation\/\?user_id=(\d+)$/;
      const match = notif.target_url.match(regex);

      if (match) {
        const userId = match[1];
        // Use router.push with a named route and parameters
        router.push({
          name: "messages",
          params: { userId: userId },
        });
      } else {
        // Fallback for other types of notifications
        router.push(notif.target_url);
      }
    } else {
      toast.info("This notification has no link.");
    }
  } catch (err) {
    console.error("Failed to handle notification click:", err);
    toast.error("Failed to open notification");
  }
};

// Also add this to refresh notifications after sending a message
const refreshNotifications = () => {
  if (authStore.isAuthenticated) {
    fetchNotifications();
  }
};
// const fetchNotifications = async () => {
//   if (!authStore.isAuthenticated) return;
//   try {
//     const response = await axios.get("/messaging/notifications/");
//     notifications.value = response.data.filter((n) => !n.is_read);
//   } catch (error) {
//     // toast.error("Failed to fetch notifications");
//   }
// };

// const markAsRead = async (id) => {
//   try {
//     // Debug logging
//     console.log("Auth store state:", {
//       isAuthenticated: authStore.isAuthenticated,
//       hasJwtToken: !!authStore.jwtToken,
//       hasUser: !!authStore.user,
//       userId: authStore.user?.id,
//       jwtToken: authStore.jwtToken ? "exists" : "missing",
//     });

//     // Check if axios has the auth header
//     console.log("Axios default headers:", axios.defaults.headers.common);

//     // Make the request
//     const response = await axios.patch(
//       `/messaging/notifications/${id}/mark_as_read/`
//     );
//     console.log("Mark as read response:", response.data);

//     notifications.value = notifications.value.filter((n) => n.id !== id);
//   } catch (err) {
//     console.error("Error marking notification:", {
//       status: err.response?.status,
//       statusText: err.response?.statusText,
//       data: err.response?.data,
//       config: err.config,
//       headers: err.response?.headers,
//     });
//     toast.error("Failed to mark notification as read");
//   }
// };

// const handleNotificationClick = async (notif) => {
//   try {
//     await markAsRead(notif.id);
//     if (notif.target_url) {
//       router.push(notif.target_url);
//     } else {
//       toast.info("This notification has no link.");
//     }
//   } catch (err) {
//     toast.error("Failed to open notification");
//   }
// };

const handleClickOutside = (e) => {
  if (notifRef.value && !notifRef.value.contains(e.target)) {
    showNotifDropdown.value = false;
  }
  if (
    accountDropdownRef.value &&
    !accountDropdownRef.value.contains(e.target)
  ) {
    showDropdown.value = false;
  }
};

watch(
  () => authStore.isAuthenticated,
  (newVal) => {
    if (newVal) {
      showDropdown.value = false;
    }
  }
);

onMounted(() => {
  if (authStore.isAuthenticated) {
    fetchNotifications();
  }
  const hash = window.location.hash;
  if (hash && hash.startsWith("#comment-")) {
    const el = document.querySelector(hash);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      el.classList.add("bg-yellow-100", "transition", "duration-500");
      setTimeout(() => el.classList.remove("bg-yellow-100"), 2000);
    }
  }
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

const logout = () => {
  authStore.logout();
  toast.success("You've been logged out 🐾");
  router.push("/login");
};
</script>
