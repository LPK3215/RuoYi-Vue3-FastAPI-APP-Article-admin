import {
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  type ColumnDef,
  type SortingState,
  useReactTable,
} from '@tanstack/react-table'
import clsx from 'clsx'
import { useMemo, useState } from 'react'

export type DataTableProps<T extends object> = {
  className?: string
  data: T[]
  columns: Array<ColumnDef<T, unknown>>
  onRowClick?: (row: T) => void
  emptyText?: string
  busy?: boolean
}

export function DataTable<T extends object>({
  className,
  data,
  columns,
  onRowClick,
  emptyText = '暂无数据',
  busy,
}: DataTableProps<T>) {
  const [sorting, setSorting] = useState<SortingState>([])
  const safeData = useMemo(() => data ?? [], [data])

  // eslint-disable-next-line react-hooks/incompatible-library
  const table = useReactTable({
    data: safeData,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  })

  const headerGroups = table.getHeaderGroups()
  const rows = table.getRowModel().rows

  return (
    <div className={clsx('ds-tableWrap', className)} aria-busy={busy ? 'true' : 'false'}>
      <table className="ds-table">
        <thead>
          {headerGroups.map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((h) => (
                <th
                  key={h.id}
                  colSpan={h.colSpan}
                  scope="col"
                  aria-sort={
                    h.column.getIsSorted() === 'asc'
                      ? 'ascending'
                      : h.column.getIsSorted() === 'desc'
                        ? 'descending'
                        : 'none'
                  }
                >
                  {h.isPlaceholder ? null : (
                    <button
                      type="button"
                      className={clsx(
                        'ds-thBtn',
                        h.column.getCanSort() && 'ds-thBtn--sortable',
                      )}
                      onClick={h.column.getToggleSortingHandler()}
                    >
                      <span className="ds-thText">
                        {flexRender(h.column.columnDef.header, h.getContext())}
                      </span>
                      {h.column.getIsSorted() === 'asc' ? (
                        <span className="ds-sortMark">↑</span>
                      ) : h.column.getIsSorted() === 'desc' ? (
                        <span className="ds-sortMark">↓</span>
                      ) : (
                        <span className="ds-sortMark ds-sortMark--idle">↕</span>
                      )}
                    </button>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {rows.length ? (
            rows.map((r) => (
              <tr
                key={r.id}
                className={clsx(onRowClick && 'ds-tr--clickable')}
                onClick={() => onRowClick?.(r.original)}
                role={onRowClick ? 'button' : undefined}
                tabIndex={onRowClick ? 0 : undefined}
                onKeyDown={(e) => {
                  if (!onRowClick) return
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    onRowClick(r.original)
                  }
                }}
              >
                {r.getVisibleCells().map((c) => (
                  <td key={c.id}>
                    {flexRender(c.column.columnDef.cell, c.getContext())}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td className="ds-tdEmpty" colSpan={columns.length}>
                {emptyText}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
