import clsx from 'clsx'
import { Children, Fragment, isValidElement, useEffect, useId, useMemo, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import type { CSSProperties, KeyboardEvent as ReactKeyboardEvent, ReactElement, ReactNode } from 'react'

type OptionItem = {
  value: string
  label: string
  disabled: boolean
}

type PanelStyle = CSSProperties & { ['--ds-select-max-h']?: string }

export type SelectProps = {
  label?: string
  className?: string
  value?: string
  disabled?: boolean
  name?: string
  children?: ReactNode
  onChange?: (e: { target: { value: string; name?: string } }) => void
}

function stringifyNode(node: ReactNode): string {
  if (node === null || node === undefined) return ''
  if (typeof node === 'string' || typeof node === 'number') return String(node)
  if (Array.isArray(node)) return node.map(stringifyNode).join('')
  return ''
}

function collectOptions(node: ReactNode, out: OptionItem[]) {
  Children.forEach(node, (child) => {
    if (!isValidElement(child)) return

    if (child.type === Fragment || child.type === 'optgroup') {
      collectOptions((child as ReactElement<{ children?: ReactNode }>).props.children, out)
      return
    }

    if (child.type === 'option') {
      const opt = child as ReactElement<{ value?: unknown; disabled?: boolean; children?: ReactNode }>
      const value = String(opt.props?.value ?? '')
      const label = stringifyNode(opt.props?.children) || value
      out.push({ value, label, disabled: Boolean(opt.props?.disabled) })
    }
  })
}

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n))
}

function firstEnabledIndex(items: OptionItem[]) {
  return Math.max(
    0,
    items.findIndex((x) => !x.disabled),
  )
}

function nextEnabledIndex(items: OptionItem[], from: number, delta: number) {
  if (!items.length) return -1
  const total = items.length
  for (let step = 1; step <= total; step += 1) {
    const idx = (from + delta * step + total) % total
    if (!items[idx]?.disabled) return idx
  }
  return from
}

function snapMenuHeight(px: number) {
  const row = 36
  const gap = 4
  if (px <= row) return Math.max(0, px)
  const rows = Math.max(1, Math.floor((px + gap) / (row + gap)))
  return rows * (row + gap) - gap
}

export function Select({
  className,
  label,
  value,
  onChange,
  disabled,
  name,
  children,
}: SelectProps) {
  const labelId = useId()
  const triggerId = useId()
  const listboxId = useId()

  const triggerRef = useRef<HTMLButtonElement | null>(null)
  const menuRef = useRef<HTMLDivElement | null>(null)
  const optionRefs = useRef<Array<HTMLButtonElement | null>>([])

  const options = useMemo(() => {
    const out: OptionItem[] = []
    collectOptions(children, out)
    return out
  }, [children])

  const currentValue = String(value ?? '')
  const selected = options.find((x) => x.value === currentValue)
  const selectedLabel = selected?.label ?? ''

  const [open, setOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(-1)
  const [panelStyle, setPanelStyle] = useState<PanelStyle>({})

  function closeMenu() {
    setOpen(false)
    setActiveIndex(-1)
  }

  function commit(nextValue: string) {
    onChange?.({ target: { value: nextValue, name } })
    closeMenu()
    triggerRef.current?.focus()
  }

  function updatePosition() {
    const el = triggerRef.current
    if (!el) return
    const rect = el.getBoundingClientRect()
    const gap = 8
    const margin = 10
    const maxH = 440
    const popoverPadding = 6
    const popoverBorder = 1
    const overhead = popoverPadding * 2 + popoverBorder * 2
    const vw = window.innerWidth
    const vh = window.innerHeight

    const availableBelow = vh - rect.bottom - margin
    const availableAbove = rect.top - margin
    const allowedBelow = Math.max(0, availableBelow - gap - overhead)
    const allowedAbove = Math.max(0, availableAbove - gap - overhead)
    const openAbove = allowedAbove > allowedBelow
    const allowed = openAbove ? allowedAbove : allowedBelow

    const height = snapMenuHeight(clamp(allowed, 120, maxH))

    const width = Math.max(220, rect.width)
    const left = clamp(rect.left, margin, vw - margin - width)

    if (openAbove) {
      setPanelStyle({
        left,
        width,
        bottom: vh - rect.top + gap,
        ['--ds-select-max-h']: `${height}px`,
      })
    } else {
      setPanelStyle({
        left,
        width,
        top: rect.bottom + gap,
        ['--ds-select-max-h']: `${height}px`,
      })
    }
  }

  function openMenu(preferredIndex?: number) {
    if (disabled) return
    const selectedIndex = options.findIndex((x) => x.value === currentValue)
    const base =
      typeof preferredIndex === 'number'
        ? preferredIndex
        : selectedIndex >= 0
          ? selectedIndex
          : firstEnabledIndex(options)

    setActiveIndex(base)
    setOpen(true)
  }

  function handleTriggerKeyDown(e: ReactKeyboardEvent<HTMLButtonElement>) {
    if (disabled) return
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      if (!open) openMenu()
      else setActiveIndex((i) => nextEnabledIndex(options, i < 0 ? 0 : i, 1))
      return
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault()
      if (!open) openMenu()
      else setActiveIndex((i) => nextEnabledIndex(options, i < 0 ? 0 : i, -1))
      return
    }
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      if (!open) openMenu()
      else {
        const item = options[activeIndex]
        if (item && !item.disabled) commit(item.value)
      }
      return
    }
    if (e.key === 'Escape') {
      if (open) {
        e.preventDefault()
        closeMenu()
      }
    }
  }

  function handleMenuKeyDown(e: ReactKeyboardEvent<HTMLDivElement>) {
    if (e.key === 'Escape') {
      e.preventDefault()
      closeMenu()
      return
    }
    if (e.key === 'Tab') {
      closeMenu()
      return
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setActiveIndex((i) => nextEnabledIndex(options, i < 0 ? 0 : i, 1))
      return
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault()
      setActiveIndex((i) => nextEnabledIndex(options, i < 0 ? 0 : i, -1))
      return
    }
    if (e.key === 'Home') {
      e.preventDefault()
      setActiveIndex(firstEnabledIndex(options))
      return
    }
    if (e.key === 'End') {
      e.preventDefault()
      for (let i = options.length - 1; i >= 0; i -= 1) {
        if (!options[i]?.disabled) {
          setActiveIndex(i)
          break
        }
      }
      return
    }
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      const item = options[activeIndex]
      if (item && !item.disabled) commit(item.value)
    }
  }

  useEffect(() => {
    if (!open) return

    updatePosition()
    const raf = window.requestAnimationFrame(() => {
      updatePosition()
      menuRef.current?.focus()
    })

    function onResize() {
      updatePosition()
    }

    function onScroll() {
      updatePosition()
    }

    function onPointerDown(ev: MouseEvent | TouchEvent) {
      const t = ev.target as Node | null
      if (!t) return
      if (triggerRef.current?.contains(t)) return
      if (menuRef.current?.contains(t)) return
      closeMenu()
    }

    window.addEventListener('resize', onResize)
    window.addEventListener('scroll', onScroll, true)
    document.addEventListener('mousedown', onPointerDown, true)
    document.addEventListener('touchstart', onPointerDown, true)

    return () => {
      window.cancelAnimationFrame(raf)
      window.removeEventListener('resize', onResize)
      window.removeEventListener('scroll', onScroll, true)
      document.removeEventListener('mousedown', onPointerDown, true)
      document.removeEventListener('touchstart', onPointerDown, true)
    }
  }, [open])

  useEffect(() => {
    if (!open) return
    if (activeIndex < 0) return
    optionRefs.current[activeIndex]?.scrollIntoView({ block: 'nearest' })
  }, [open, activeIndex])

  return (
    <div className={clsx('ds-field', className)}>
      {label ? (
        <span
          className="ds-label"
          id={labelId}
          onClick={() => {
            if (disabled) return
            triggerRef.current?.focus()
            if (!open) openMenu()
          }}
        >
          {label}
        </span>
      ) : null}

      <button
        ref={triggerRef}
        type="button"
        className={clsx('ds-select', open && 'ds-select--open')}
        id={triggerId}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={open ? listboxId : undefined}
        aria-labelledby={label ? `${labelId} ${triggerId}` : triggerId}
        disabled={disabled}
        onClick={() => (open ? closeMenu() : openMenu())}
        onKeyDown={handleTriggerKeyDown}
      >
        <span className="ds-selectValue" title={selectedLabel}>
          {selectedLabel || '—'}
        </span>
        <span className="ds-selectChevron" aria-hidden="true">
          <svg viewBox="0 0 20 20" width="16" height="16" focusable="false" aria-hidden="true">
            <path
              d="M5.2 7.6a1 1 0 0 1 1.4 0L10 11l3.4-3.4a1 1 0 1 1 1.4 1.4l-4.1 4.1a1 1 0 0 1-1.4 0L5.2 9a1 1 0 0 1 0-1.4Z"
              fill="currentColor"
            />
          </svg>
        </span>
      </button>

      {open
        ? createPortal(
            <div className="ds-selectPopover" style={panelStyle}>
              <div
                ref={menuRef}
                id={listboxId}
                className="ds-selectMenu"
                role="listbox"
                aria-labelledby={label ? labelId : undefined}
                tabIndex={-1}
                onKeyDown={handleMenuKeyDown}
              >
                {options.length ? (
                  options.map((item, idx) => (
                    <button
                      key={`${item.value}__${idx}`}
                      ref={(el) => {
                        optionRefs.current[idx] = el
                      }}
                      type="button"
                      role="option"
                      aria-selected={item.value === currentValue}
                      disabled={item.disabled}
                      className={clsx(
                        'ds-selectOption',
                        idx === activeIndex && 'is-active',
                        item.value === currentValue && 'is-selected',
                      )}
                      onMouseEnter={() => setActiveIndex(idx)}
                      onClick={() => {
                        if (!item.disabled) commit(item.value)
                      }}
                    >
                      <span className="ds-selectOptionText">{item.label}</span>
                      {item.value === currentValue ? (
                        <span className="ds-selectOptionMark" aria-hidden="true">
                          ✓
                        </span>
                      ) : null}
                    </button>
                  ))
                ) : (
                  <div className="ds-selectEmpty">暂无选项</div>
                )}
              </div>
            </div>,
            document.body,
          )
        : null}
    </div>
  )
}
