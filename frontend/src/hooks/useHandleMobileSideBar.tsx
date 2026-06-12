import { useCallback, useState } from 'react'

export function useHandleMobileSideBar() {
  const [isOpen, setIsOpen] = useState(false)

  const handleOpen = useCallback(() => {
    setIsOpen(current => !current)
  }, [])

  const handleClose = useCallback(() => {
    setIsOpen(false)
  }, [])

  return {
    isOpen,
    handleOpen,
    handleClose,
  }
}
