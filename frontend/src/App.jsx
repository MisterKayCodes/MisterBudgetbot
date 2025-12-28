import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Income from './pages/Income'
import Expenses from './pages/Expenses'
import Goals from './pages/Goals'
import Summary from './pages/Summary'
import Settings from './pages/Settings'
import Advisor from './pages/Advisor'
import { UserProvider } from './context/UserContext'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    setLoading(false)
  }, [])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <UserProvider value={{ user, setUser }}>
      <Router>
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
          <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/income" element={user ? <Income /> : <Navigate to="/login" />} />
          <Route path="/expenses" element={user ? <Expenses /> : <Navigate to="/login" />} />
          <Route path="/goals" element={user ? <Goals /> : <Navigate to="/login" />} />
          <Route path="/summary" element={user ? <Summary /> : <Navigate to="/login" />} />
          <Route path="/settings" element={user ? <Settings /> : <Navigate to="/login" />} />
          <Route path="/advisor" element={user ? <Advisor /> : <Navigate to="/login" />} />
        </Routes>
      </Router>
    </UserProvider>
  )
}

export default App
