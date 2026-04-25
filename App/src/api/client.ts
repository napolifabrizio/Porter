import type {
  CheckResultResponse,
  CheckSelectedRequest,
  CreateListRequest,
  LoginRequest,
  LoginResponse,
  MoveRequest,
  Product,
  TrackRequest,
  TrackResultResponse,
  WatchList,
} from '@/types'

const BASE_URL = (import.meta.env.VITE_API_URL as string) ?? 'http://localhost:8000'

// Lazily imported so auth module can be set up after this module loads.
// We use a getter function to avoid circular import issues.
let _getToken: (() => string | null) | null = null
let _onUnauthorized: (() => void) | null = null

export function configureClient(opts: {
  getToken: () => string | null
  onUnauthorized: () => void
}) {
  _getToken = opts.getToken
  _onUnauthorized = opts.onUnauthorized
}

async function request<T>(
  path: string,
  init: RequestInit = {},
  auth = true,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(init.headers as Record<string, string>),
  }

  if (auth && _getToken) {
    const token = _getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers })

  if (res.status === 401 && auth) {
    _onUnauthorized?.()
    throw new Error('Unauthorized')
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error((body as { detail?: string }).detail ?? `HTTP ${res.status}`)
  }

  if (res.status === 204) return undefined as unknown as T
  return res.json() as Promise<T>
}

// ── Auth ──────────────────────────────────────────────────────────────────────

export function login(body: LoginRequest): Promise<LoginResponse> {
  return request<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(body),
  }, false)
}

// ── Lists ─────────────────────────────────────────────────────────────────────

export function getLists(): Promise<WatchList[]> {
  return request<WatchList[]>('/lists')
}

export function createList(body: CreateListRequest): Promise<WatchList> {
  return request<WatchList>('/lists', { method: 'POST', body: JSON.stringify(body) })
}

export function deleteList(listId: number): Promise<void> {
  return request<void>(`/lists/${listId}`, { method: 'DELETE' })
}

// ── Products ──────────────────────────────────────────────────────────────────

export function getProducts(listId?: number): Promise<Product[]> {
  const qs = listId !== undefined ? `?list_id=${listId}` : ''
  return request<Product[]>(`/products${qs}`)
}

export function trackProduct(body: TrackRequest): Promise<TrackResultResponse> {
  return request<TrackResultResponse>('/products', { method: 'POST', body: JSON.stringify(body) })
}

export function checkAllPrices(listId?: number): Promise<CheckResultResponse[]> {
  const qs = listId !== undefined ? `?list_id=${listId}` : ''
  return request<CheckResultResponse[]>(`/products/check${qs}`, { method: 'POST' })
}

export function checkSelected(body: CheckSelectedRequest): Promise<CheckResultResponse[]> {
  return request<CheckResultResponse[]>('/products/check-selected', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export function deleteProduct(productId: number): Promise<void> {
  return request<void>(`/products/${productId}`, { method: 'DELETE' })
}

export function moveProduct(productId: number, body: MoveRequest): Promise<void> {
  return request<void>(`/products/${productId}/list`, { method: 'PATCH', body: JSON.stringify(body) })
}

export function renameProduct(productId: number, name: string): Promise<Product> {
  return request<Product>(`/products/${productId}`, { method: 'PATCH', body: JSON.stringify({ name }) })
}
