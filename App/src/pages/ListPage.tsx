import { useEffect, useRef, useState } from 'react'
import { useParams } from '@tanstack/react-router'
import { Sidebar } from '@/components/Sidebar'
import { AddProductForm } from '@/components/AddProductForm'
import { ProductCard } from '@/components/ProductCard'
import { CheckingOverlay } from '@/components/CheckingOverlay'
import { useLists } from '@/hooks/useLists'
import {
  useCheckAllPrices,
  useCheckSelected,
  useDeleteProduct,
  useMoveProduct,
  useProducts,
  useTrackProduct,
} from '@/hooks/useProducts'
import type { CheckResultResponse } from '@/types'

export function ListPage() {
  const { listId: listIdStr } = useParams({ from: '/list/$listId' })
  const listId = Number(listIdStr)

  const { data: products = [] } = useProducts(listId)
  const { data: allLists = [] } = useLists()

  const trackProduct = useTrackProduct(listId)
  const checkAll = useCheckAllPrices(listId)
  const checkSelectedMut = useCheckSelected(listId)
  const deleteProductMut = useDeleteProduct(listId)
  const moveProductMut = useMoveProduct(listId)

  const [checkResults, setCheckResults] = useState<Map<number, CheckResultResponse>>(new Map())
  const [llmScraped, setLlmScraped] = useState<Map<number, boolean>>(new Map())
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set())
  const [selectionWarning, setSelectionWarning] = useState(false)

  // Reset state on route change
  const prevListId = useRef(listId)
  useEffect(() => {
    if (prevListId.current !== listId) {
      setCheckResults(new Map())
      setLlmScraped(new Map())
      setSelectedIds(new Set())
      prevListId.current = listId
    }
  }, [listId])

  function mergeResults(results: CheckResultResponse[]) {
    setCheckResults((prev) => {
      const next = new Map(prev)
      for (const r of results) next.set(r.product.id, r)
      return next
    })
    setLlmScraped((prev) => {
      const next = new Map(prev)
      for (const r of results) next.set(r.product.id, r.scraped_by_llm)
      return next
    })
  }

  async function handleCheckAll() {
    const results = await checkAll.mutateAsync()
    mergeResults(results)
  }

  async function handleCheckSelected() {
    if (selectedIds.size === 0) {
      setSelectionWarning(true)
      setTimeout(() => setSelectionWarning(false), 3000)
      return
    }
    const results = await checkSelectedMut.mutateAsync([...selectedIds])
    mergeResults(results)
  }

  async function handleTrack(url: string, targetListId: number) {
    const res = await trackProduct.mutateAsync({ url, listId: targetListId })
    setLlmScraped((prev) => new Map(prev).set(res.product.id, res.scraped_by_llm))
    return res
  }

  function toggleSelected(id: number, checked: boolean) {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (checked) next.add(id)
      else next.delete(id)
      return next
    })
  }

  const isCheckingAll = checkAll.isPending
  const isCheckingSelected = checkSelectedMut.isPending
  const isChecking = isCheckingAll || isCheckingSelected

  const listName = allLists.find((l) => l.id === listId)?.name ?? 'List'

  return (
    <div className="flex h-full">
      <Sidebar
        onCheckAll={handleCheckAll}
        onCheckSelected={handleCheckSelected}
        selectedCount={selectedIds.size}
        isChecking={isChecking}
      />

      <main className="flex flex-1 flex-col overflow-hidden">
        <header className="border-b border-border px-6 py-4">
          <h1 className="text-lg font-semibold">{listName}</h1>
        </header>

        <div className="border-b border-border px-6 py-3">
          <AddProductForm currentListId={listId} onTrack={handleTrack} />
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-2">
          {selectionWarning && (
            <p className="text-sm text-amber-600">Select at least one product first.</p>
          )}
          {products.length === 0 && (
            <p className="text-sm text-muted-foreground">No products in this list yet. Add one above.</p>
          )}
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              checkResult={checkResults.get(product.id)}
              isSelected={selectedIds.has(product.id)}
              onSelectChange={(checked) => toggleSelected(product.id, checked)}
              onDelete={(id) => deleteProductMut.mutate(id)}
              onMove={(productId, targetListId) => moveProductMut.mutate({ productId, targetListId })}
              allLists={allLists}
              llmScraped={llmScraped.get(product.id)}
            />
          ))}
        </div>
      </main>

      {isChecking && (
        <CheckingOverlay
          label={
            isCheckingAll
              ? 'Checking all prices, this may take ~30 s…'
              : 'Checking selected prices…'
          }
        />
      )}
    </div>
  )
}
