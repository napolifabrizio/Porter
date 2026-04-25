import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createList, deleteList, getLists } from '@/api/client'

export const LISTS_KEY = ['lists'] as const

export function useLists() {
  return useQuery({ queryKey: LISTS_KEY, queryFn: getLists })
}

export function useCreateList() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (name: string) => createList({ name }),
    onSuccess: () => qc.invalidateQueries({ queryKey: LISTS_KEY }),
  })
}

export function useDeleteList() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (listId: number) => deleteList(listId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: LISTS_KEY })
      qc.invalidateQueries({ queryKey: ['products'] })
    },
  })
}
