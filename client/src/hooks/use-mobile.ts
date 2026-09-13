import * as React from "react"

const MOBILE_BREAKPOINT = 768

const getMediaQuery = () =>
  window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)

export function useIsMobile() {
  const subscribe = React.useCallback((onStoreChange: () => void) => {
    const mediaQuery = getMediaQuery()
    mediaQuery.addEventListener("change", onStoreChange)
    return () => mediaQuery.removeEventListener("change", onStoreChange)
  }, [])

  const getSnapshot = React.useCallback(() => getMediaQuery().matches, [])
  const getServerSnapshot = React.useCallback(() => false, [])

  return React.useSyncExternalStore(
    subscribe,
    getSnapshot,
    getServerSnapshot
  )
}
