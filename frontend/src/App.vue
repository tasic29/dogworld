<template>
  <div>
    <Navbar />
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "./stores/auth"; // ✅ make sure path is correct
import Navbar from "./components/Navbar.vue";

onMounted(() => {
  const auth = useAuthStore();
  if (auth.jwtToken && !auth.user) {
    auth.fetchUser();
  }
});
</script>
