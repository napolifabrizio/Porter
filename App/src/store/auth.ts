import { create } from 'zustand'

const SESSION_KEY = 'porter_token'

interface AuthState {
  token: string | null
  setToken: (token: string) => void
  clearToken: () => void
}

export const useAuthStore = create<AuthState>(() => ({
  token: sessionStorage.getItem(SESSION_KEY),
  setToken: (token: string) => {
    sessionStorage.setItem(SESSION_KEY, token)
    useAuthStore.setState({ token })
  },
  clearToken: () => {
    sessionStorage.removeItem(SESSION_KEY)
    useAuthStore.setState({ token: null })
  },
}))
