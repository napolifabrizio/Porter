import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  checkAllPrices,
  checkSelected,
  deleteProduct,
  getProducts,
  moveProduct,
  renameProduct,
  trackProduct,
} from '@/api/client'
import type { CheckResultResponse, TrackResultResponse } from '@/types'

export const productsKey = (listId?: number) =>
  listId !== undefined ? ['products', listId] : ['products']

export function useProducts(listId: number) {
  return useQuery({
    queryKey: productsKey(listId),
    queryFn: () => getProducts(listId),
  })
}

export function useTrackProduct(listId: number) {
  const qc = useQueryClient()
  return useMutation<TrackResultResponse, Error, { url: string; listId?: number }>({
    mutationFn: ({ url, listId: lid }) => trackProduct({ url, list_id: lid }),
    onSuccess: () => qc.invalidateQueries({ queryKey: productsKey(listId) }),
  })
}

export function useCheckAllPrices(listId: number) {
  const qc = useQueryClient()
  return useMutation<CheckResultResponse[], Error, void>({
    mutationFn: () => checkAllPrices(listId),
    onSuccess: () => qc.invalidateQueries({ queryKey: productsKey(listId) }),
  })
}

export function useCheckSelected(listId: number) {
  const qc = useQueryClient()
  return useMutation<CheckResultResponse[], Error, number[]>({
    mutationFn: (ids) => checkSelected({ ids }),
    onSuccess: () => qc.invalidateQueries({ queryKey: productsKey(listId) }),
  })
}

export function useDeleteProduct(listId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (productId: number) => deleteProduct(productId),
    onSuccess: () => qc.invalidateQueries({ queryKey: productsKey(listId) }),
  })
}

export function useMoveProduct(listId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ productId, targetListId }: { productId: number; targetListId: number }) =>
      moveProduct(productId, { target_list_id: targetListId }),
    onSuccess: () => qc.invalidateQueries({ queryKey: productsKey(listId) }),
  })
}

export function useRenameProduct(listId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ productId, name }: { productId: number; name: string }) =>
      renameProduct(productId, name),
    onSuccess: () => qc.invalidateQueries({ queryKey: productsKey(listId) }),
  })
}
