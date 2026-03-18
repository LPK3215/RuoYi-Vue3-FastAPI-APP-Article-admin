export async function runThemeModeTransition(event, currentIsDark, applyThemeMode) {
  const x = event?.clientX || window.innerWidth / 2
  const y = event?.clientY || window.innerHeight / 2
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const isSupported = typeof document.startViewTransition === 'function' && !isReducedMotion

  if (!isSupported) {
    await applyThemeMode()
    return
  }

  try {
    const transition = document.startViewTransition(async () => {
      await new Promise((resolve) => window.setTimeout(resolve, 10))
      await applyThemeMode()
    })
    await transition.ready

    const endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y),
    )
    const clipPath = [`circle(0px at ${x}px ${y}px)`, `circle(${endRadius}px at ${x}px ${y}px)`]
    const revealOldSnapshot = !currentIsDark

    document.documentElement.animate(
      {
        clipPath: revealOldSnapshot ? [...clipPath].reverse() : clipPath,
      },
      {
        duration: 650,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        fill: 'forwards',
        pseudoElement: revealOldSnapshot ? '::view-transition-old(root)' : '::view-transition-new(root)',
      },
    )

    await transition.finished
  } catch (error) {
    console.warn('View transition failed, falling back to immediate toggle:', error)
    await applyThemeMode()
  }
}
