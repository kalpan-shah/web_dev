// 27th May 2026

export default defineNuxtRouteMiddleware((to, from) => {
  const { token } = useAuth()

  // If no token exists, redirect to login
  if (!token.value) {
    return navigateTo('/login')
  }
})
