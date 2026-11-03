import { ref } from 'vue'

/** Se incrementa en login / registro / logout para que la nav reaccione. */
export const authTick = ref(0)

export function notifyAuthChanged() {
  authTick.value += 1
}
