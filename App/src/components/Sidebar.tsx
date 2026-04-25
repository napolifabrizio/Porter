import { useState } from 'react'
import { useNavigate, useParams } from '@tanstack/react-router'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { useCreateList, useDeleteList, useLists } from '@/hooks/useLists'

export function Sidebar() {
  const navigate = useNavigate()
  const params = useParams({ strict: false })
  const activeId = Number((params as Record<string, string>).listId ?? 0)

  const { data: lists = [] } = useLists()
  const createList = useCreateList()
  const deleteList = useDeleteList()

  const [newListName, setNewListName] = useState('')
  const [showNewList, setShowNewList] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<{ id: number; name: string } | null>(null)

  async function handleCreateList(e: React.FormEvent) {
    e.preventDefault()
    if (!newListName.trim()) return
    await createList.mutateAsync(newListName.trim())
    setNewListName('')
    setShowNewList(false)
  }

  async function handleDeleteList() {
    if (!deleteTarget) return
    await deleteList.mutateAsync(deleteTarget.id)
    setDeleteTarget(null)
    if (activeId === deleteTarget.id) {
      await navigate({ to: '/list/$listId', params: { listId: '1' } })
    }
  }

  return (
    <aside className="flex w-56 flex-shrink-0 flex-col border-r border-border bg-sidebar h-full">
      <div className="p-4 border-b border-border">
        <h2 className="text-base font-semibold text-sidebar-foreground">Porter</h2>
      </div>

      {/* Lists */}
      <nav className="flex-1 overflow-y-auto p-2 space-y-0.5">
        {lists.map((list) => (
          <div key={list.id} className="flex items-center group">
            <button
              onClick={() => navigate({ to: '/list/$listId', params: { listId: String(list.id) } })}
              className={`flex-1 rounded-md px-3 py-2 text-left text-sm transition-colors ${
                list.id === activeId
                  ? 'bg-sidebar-accent text-sidebar-accent-foreground font-medium'
                  : 'text-sidebar-foreground hover:bg-sidebar-accent/50'
              }`}
            >
              {list.name}
            </button>
            {list.id !== 1 && (
              <button
                onClick={() => setDeleteTarget({ id: list.id, name: list.name })}
                className="ml-1 p-1 rounded opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive transition-opacity"
                title="Delete list"
              >
                🗑
              </button>
            )}
          </div>
        ))}
      </nav>

      {/* New List */}
      <div className="p-2 border-t border-border">
        {showNewList ? (
          <form onSubmit={handleCreateList} className="space-y-1">
            <Input
              value={newListName}
              onChange={(e) => setNewListName(e.target.value)}
              placeholder="List name"
              className="h-8 text-sm"
              autoFocus
            />
            <div className="flex gap-1">
              <Button type="submit" size="sm" className="flex-1 h-7 text-xs" disabled={createList.isPending}>
                Create
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-7 text-xs"
                onClick={() => { setShowNewList(false); setNewListName('') }}
              >
                Cancel
              </Button>
            </div>
          </form>
        ) : (
          <button
            onClick={() => setShowNewList(true)}
            className="w-full rounded-md px-3 py-2 text-left text-sm text-muted-foreground hover:bg-sidebar-accent/50 transition-colors"
          >
            + New List
          </button>
        )}
      </div>

      {/* Delete confirmation dialog */}
      <Dialog open={!!deleteTarget} onOpenChange={(open) => !open && setDeleteTarget(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete list</DialogTitle>
            <DialogDescription>
              Delete &quot;{deleteTarget?.name}&quot;? Products in this list will move to Standard.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setDeleteTarget(null)}>Cancel</Button>
            <Button variant="destructive" onClick={handleDeleteList} disabled={deleteList.isPending}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </aside>
  )
}
