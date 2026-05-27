<script setup lang="ts">
const { login } = useAuth();
const errorMessage = ref('');
const loading = ref(false);

const fields = [
    { name: 'email', label: 'Email', type: 'email', required: true },
    { name: 'password', label: 'Password', type: 'password', required: true },
];

const validate = (state: any) => {
    const errors = [];
    if (!state.email) {
        errors.push({ path: 'email', message: 'Email is required' });
    } else if (!/\S+@\S+\.\S+/.test(state.email)) {
        errors.push({ path: 'email', message: 'Email is invalid' });
    }
    if (!state.password) {
        errors.push({ path: 'password', message: 'Password is required' });
    }
    return errors;
}

const handleLogin = async (state: any) => {
    console.log('Login form submitted with:', state.data);
    loading.value = true;
    errorMessage.value = '';
    try {
        await login(state.data.email, state.data.password);
        // Redirect to the home page after successful login
        await navigateTo('/');
    } catch (error: any) {
        errorMessage.value = error.message || 'Login failed. Please check your credentials and try again.';
    } finally {
        loading.value = false;
    }
}

</script>

<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">

        <UPageCard class="w-full max-w-md">
            <template #header>
                <h1 class="text-2xl font-bold text-center text-gray-800 dark:text-gray-200">Login</h1>
            </template>

            <!-- Error Message -->

            <UAlert v-if="errorMessage" icon="i-heroicons-exclamation-triangle" color="red" variant="soft" title="Error"
                :description="errorMessage" class="mb-4" />
            

            <!-- Nuxt UI Auth Form -->
            <UAuthForm :fields="fields" :validate="validate" :loading="loading" align="top" title="Welcome back"
                icon="i-heroicons-lock-closed" @submit="handleLogin" />
        </UPageCard>
    </div>
</template>