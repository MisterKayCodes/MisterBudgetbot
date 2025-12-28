import { createContext, useContext } from 'react'

const UserContext = createContext(null)

export const UserProvider = UserContext.Provider

export const useUser = () => {
  const context = useContext(UserContext)
  if (!context) {
    throw new Error('useUser must be used within UserProvider')
  }
  return context
}
