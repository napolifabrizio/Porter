import { createRootRoute, createRoute, createRouter, redirect } from '@tanstack/react-router'
import { LoginPage } from '@/pages/LoginPage'
import { ListPage } from '@/pages/ListPage'
import { useAuthStore } from '@/store/auth'

const rootRoute = createRootRoute()

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  beforeLoad: () => {
    const token = useAuthStore.getState().token
    if (token) throw redirect({ to: '/list/$listId', params: { listId: '1' } })
    throw redirect({ to: '/login' })
  },
})

const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/login',
  component: LoginPage,
})

const listRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/list/$listId',
  beforeLoad: () => {
    const token = useAuthStore.getState().token
    if (!token) throw redirect({ to: '/login' })
  },
  component: ListPage,
})

const routeTree = rootRoute.addChildren([indexRoute, loginRoute, listRoute])

export const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
