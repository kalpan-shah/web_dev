<template>

  <!-- the root wrapper -->
  <UApp>
    <UHeader>
      <template #left>
        <NuxtLink to="/">
          <!-- Update with your logo -->
        </NuxtLink>
        <!-- TODO: Update with menu to switch between Todo and wishlist -->
        <!-- <TemplateMenu /> -->
      </template>

      <template #right>
        
        <!-- TODO: Update with out github repo url -->
        <UButton
        to="https://github.com/kalpan-shah/web_dev"
        target="_blank"
        icon="i-simple-icons-github"
        aria-label="GitHub"
        color="neutral"
        variant="ghost"
        />
        <!-- TODO: Logout button -->
         <UButton
          to="/loggedout"
          icon="i-heroicons-arrow-right-on-box"
          aria-label="Logout"
          color="neutral"
          variant="ghost"
        />
        <!-- Will display a you have been logged out message
        and then in 7 seconds will redirect to the login page  
        -->
        <UColorModeButton />
      </template>
    </UHeader>
    <!-- the container for the primary content -->
    <UMain>
      <!-- so this directly routes to pages/index.vue, you can add more pages and link to them from the header menu 
        1. default is the Todo, crud page and the second page is the wishlist page, linked from the header menu 
      -->
      <NuxtPage />
    </UMain>

    <!-- <USeparator icon="i-heroicons-fire" /> -->

    <UFooter>
      <template #left>
        <!-- TODO: Update name with github profile hyperlink -->
        <p class="text-sm text-muted">
          Built with Love❤️ By <NuxtLink to="https://github.com/kalpan-shah" target="_blank" class="underline">Kalpan Shah</NuxtLink> • © {{ new Date().getFullYear() }}
        </p>
      </template>

      <template #right>
        <!-- TODO: Update with something-->
      </template>
    </UFooter>
  </UApp>
</template>
