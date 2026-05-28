<script setup lang="ts">
// This line activates the protection
definePageMeta({
  middleware: 'auth'
})

const { logout } = useAuth()
</script>

<template>
  <div class="p-10">
    <h1 class="text-2xl font-bold mb-4">Protected Dashboard</h1>
    <p class="mb-4">You can only see this because you have a token!</p>
    
    <UButton @click="logout">
      Logout
    </UButton>
  </div>
</template>
