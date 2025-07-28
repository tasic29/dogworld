<template>
  <div
    class="fixed inset-0 z-50 bg-black/40 flex items-center justify-center backdrop-blur-sm"
  >
    <div
      class="bg-white dark:bg-slate-800 rounded-xl shadow-lg max-w-md w-full p-6 space-y-4 border border-amber-200 dark:border-slate-700"
    >
      <h2 class="text-xl font-semibold text-gray-800 dark:text-white">
        {{ title }}
      </h2>

      <p class="text-gray-600 dark:text-gray-300">{{ message }}</p>

      <div class="flex justify-end gap-3 pt-2">
        <button
          @click="$emit('cancel')"
          class="px-4 py-2 rounded text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700 transition"
        >
          {{ cancelText }}
        </button>

        <button
          @click="$emit('confirm')"
          class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded shadow transition"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: "Are you sure?" },
  message: { type: String, default: "This action cannot be undone." },
  confirmText: { type: String, default: "Confirm" },
  cancelText: { type: String, default: "Cancel" },
});
</script>
