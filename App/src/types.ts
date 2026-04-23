export interface WatchList {
  id: number
  name: string
}

export interface Product {
  id: number
  url: string
  name: string
  description: string | null
  initial_price: number
  current_price: number
  last_checked: string
  list_id: number
  currency: string
}

export interface LoginRequest {
  password: string
}

export interface LoginResponse {
  access_token: string
}

export interface CreateListRequest {
  name: string
}

export interface TrackRequest {
  url: string
  list_id?: number | null
}

export interface MoveRequest {
  target_list_id: number
}

export interface CheckSelectedRequest {
  ids: number[]
}

export interface TrackResultResponse {
  product: Product
  scraped_by_llm: boolean
}

export interface CheckResultResponse {
  product: Product
  dropped: boolean
  change_pct: number
  error: string | null
  scraped_by_llm: boolean
}
