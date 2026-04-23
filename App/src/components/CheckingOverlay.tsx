interface CheckingOverlayProps {
  label: string
}

export function CheckingOverlay({ label }: CheckingOverlayProps) {
  return (
    <div
      className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm"
      style={{ pointerEvents: 'all' }}
    >
      <div className="flex flex-col items-center gap-4">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-border border-t-primary" />
        <p className="text-sm text-muted-foreground">{label}</p>
      </div>
    </div>
  )
}
