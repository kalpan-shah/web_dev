 <script setup>
  setTimeout(() => {
    // Redirect to the login page after 7 seconds
    navigateTo('/login');
  }, 7000);
</script>

<template>
  <div class="p-10 text-center">
    <h1 class="text-2xl font-bold">You have been logged out</h1>
    <UButton to="/login" class="mt-4">
      Go back to Login
    </UButton>
  </div>
</template>

