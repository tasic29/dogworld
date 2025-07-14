<!-- src/components/Navbar.vue -->
<template>
  <nav class="bg-white shadow-md p-4 flex justify-between items-center">
    <router-link to="/" class="text-xl font-bold text-blue-600"
      >Dog World</router-link
    >

    <div class="space-x-4">
      <router-link to="/" class="text-gray-700 hover:text-blue-600"
        >Home</router-link
      >
      <router-link to="/blogs" class="text-gray-700 hover:text-blue-600"
        >Blogs</router-link
      >
      <router-link to="/posts" class="text-gray-700 hover:text-blue-600"
        >Posts</router-link
      >
      <router-link to="/marketplace" class="text-gray-700 hover:text-blue-600"
        >Shop</router-link
      >
      <router-link to="/login" class="text-gray-700 hover:text-blue-600"
        >Login</router-link
      >
    </div>
  </nav>
</template>

<script setup></script>
