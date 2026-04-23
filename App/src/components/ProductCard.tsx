import { useState } from 'react'
import { Checkbox } from '@/components/ui/checkbox'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import type { CheckResultResponse, Product, WatchList } from '@/types'

interface ProductCardProps {
  product: Product
  checkResult?: CheckResultResponse
  isSelected: boolean
  onSelectChange: (selected: boolean) => void
  onDelete: (id: number) => void
  onMove: (productId: number, targetListId: number) => void
  allLists: WatchList[]
  llmScraped?: boolean
}

function formatPrice(product: Product, result?: CheckResultResponse) {
  const price = result ? result.product.current_price : product.current_price
  return `${product.currency} ${price.toFixed(2)}`
}

function PriceStatus({ product, result }: { product: Product; result?: CheckResultResponse }) {
  if (!result) {
    return <span className="text-sm text-muted-foreground">{formatPrice(product)}</span>
  }
  if (result.error) {
    return <span className="text-sm text-destructive">Error</span>
  }
  const pct = result.change_pct
  if (result.dropped) {
    return (
      <span className="text-sm font-medium text-green-600">
        ↓ {Math.abs(pct).toFixed(1)}% · {formatPrice(product, result)}
      </span>
    )
  }
  if (pct > 0) {
    return (
      <span className="text-sm font-medium text-red-600">
        ↑ +{pct.toFixed(1)}% · {formatPrice(product, result)}
      </span>
    )
  }
  return <span className="text-sm text-muted-foreground">{formatPrice(product, result)}</span>
}

function stripeColor(result?: CheckResultResponse) {
  if (!result) return null
  if (result.error) return 'bg-red-500'
  if (result.dropped) return 'bg-green-500'
  return null
}

export function ProductCard({
  product,
  checkResult,
  isSelected,
  onSelectChange,
  onDelete,
  onMove,
  allLists,
  llmScraped,
}: ProductCardProps) {
  const [expanded, setExpanded] = useState(false)
  const stripe = stripeColor(checkResult)
  const otherLists = allLists.filter((l) => l.id !== product.list_id)

  return (
    <div className={`relative flex flex-col rounded-lg border border-border bg-card overflow-hidden ${stripe ? 'border-l-4' : ''}`}
      style={stripe ? { borderLeftColor: stripe === 'bg-green-500' ? '#16a34a' : '#ef4444' } : {}}>
      {/* Header row */}
      <div className="flex items-center gap-2 px-3 py-2">
        <Checkbox
          checked={isSelected}
          onCheckedChange={(v) => onSelectChange(!!v)}
          className="flex-shrink-0"
        />
        <button
          onClick={() => setExpanded((e) => !e)}
          className="flex-1 text-left text-sm font-medium hover:underline truncate"
        >
          <span className="mr-1">{expanded ? '▼' : '▶'}</span>
          {product.name}
        </button>
        <PriceStatus product={product} result={checkResult} />
        {!!llmScraped && (
          <span title="This product was scraped via LLM fallback" className="cursor-help text-base">
            🤖
          </span>
        )}
        <button
          onClick={() => onDelete(product.id)}
          className="text-muted-foreground hover:text-destructive transition-colors"
          title="Delete product"
        >
          🗑
        </button>
      </div>

      {/* Expanded details */}
      {expanded && (
        <div className="border-t border-border px-4 py-3 space-y-2 text-sm text-muted-foreground">
          {product.description && (
            <p>{product.description.slice(0, 160)}{product.description.length > 160 ? '…' : ''}</p>
          )}
          <p>
            <span className="font-medium text-foreground">URL: </span>
            <a href={product.url} target="_blank" rel="noreferrer" className="underline break-all">
              {product.url}
            </a>
          </p>
          <p>
            <span className="font-medium text-foreground">Initial price: </span>
            {product.currency} {product.initial_price.toFixed(2)}
          </p>
          {otherLists.length > 0 && (
            <div className="flex items-center gap-2 pt-1">
              <span className="font-medium text-foreground">Move to:</span>
              <Select
                value=""
                onValueChange={(val) => {
                  if (val) onMove(product.id, Number(val))
                }}
              >
                <SelectTrigger className="h-8 w-36 text-xs">
                  <SelectValue placeholder="Select list…" />
                </SelectTrigger>
                <SelectContent>
                  {otherLists.map((l) => (
                    <SelectItem key={l.id} value={String(l.id)}>
                      {l.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
