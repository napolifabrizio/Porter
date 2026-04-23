import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useLists } from '@/hooks/useLists'
import type { TrackResultResponse } from '@/types'

interface AddProductFormProps {
  currentListId: number
  onTrack: (url: string, listId: number) => Promise<TrackResultResponse>
}

export function AddProductForm({ currentListId, onTrack }: AddProductFormProps) {
  const { data: lists = [] } = useLists()
  const [url, setUrl] = useState('')
  const [listId, setListId] = useState(String(currentListId))
  const [loading, setLoading] = useState(false)
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; msg: string } | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!url.trim()) return
    setLoading(true)
    setFeedback(null)
    try {
      const res = await onTrack(url.trim(), Number(listId))
      setFeedback({
        type: 'success',
        msg: `Added: ${res.product.name} — ${res.product.currency} ${res.product.current_price.toFixed(2)}`,
      })
      setUrl('')
    } catch (err: unknown) {
      setFeedback({ type: 'error', msg: err instanceof Error ? err.message : 'Failed to add product.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <div className="flex gap-2">
        <Input
          type="url"
          placeholder="Paste product URL…"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={loading}
          className="flex-1"
        />
        <Select value={listId} onValueChange={setListId} disabled={loading}>
          <SelectTrigger className="w-36">
            <SelectValue placeholder="List" />
          </SelectTrigger>
          <SelectContent>
            {lists.map((l) => (
              <SelectItem key={l.id} value={String(l.id)}>
                {l.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Button type="submit" disabled={loading || !url.trim()}>
          {loading ? 'Adding…' : 'Add Product'}
        </Button>
      </div>
      {feedback && (
        <p className={`text-sm ${feedback.type === 'success' ? 'text-green-600' : 'text-destructive'}`}>
          {feedback.msg}
        </p>
      )}
    </form>
  )
}
