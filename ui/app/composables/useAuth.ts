// 27th May 2026

const API_BASE_URL = 'http://localhost:8000/api/v1/users/token'

interface AuthResponse {
    access_token: string
}

export const useAuth = () => {
    // Stateless Accessible cookie
    const token = useCookie('auth_token')
    // const user = useState('current_user')

    const login = async (email: string, password: string) => {
        const payload = { 
            email: email,
            password: password
        }
        console.log('Login payload:', payload)
        try {
            const response = await $fetch<AuthResponse>(API_BASE_URL, {
                method: 'POST',
                body: payload,
                headers: {
                    'Content-Type': 'application/json'
                }
            })

            token.value = response.access_token

        } catch (error) {
            console.error('Login failed:', error)
            throw error;
        }
    }

    const logout = () => {
        token.value = null
        navigateTo('/loggedout')
    }

    return { token, login, logout }
}