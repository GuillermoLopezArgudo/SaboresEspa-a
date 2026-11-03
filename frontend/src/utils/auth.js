import { computed } from 'vue'
import { isTokenValid } from '../api'
import { authTick, notifyAuthChanged } from './authBus'

export { notifyAuthChanged, authTick }

export function useAuth() {
  const loggedIn = computed(() => {
    void authTick.value
    return isTokenValid(localStorage.getItem('userToken'))
  })

  const userName = computed(() => {
    void authTick.value
    return localStorage.getItem('userName') || localStorage.getItem('email') || 'Usuario'
  })

  return { loggedIn, userName, authTick, notifyAuthChanged }
}
