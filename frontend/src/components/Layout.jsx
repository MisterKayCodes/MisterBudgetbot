import { Link, useNavigate } from 'react-router-dom'
import { useUser } from '../context/UserContext'
import '../styles/Layout.css'

function Layout({ children }) {
  const { user, setUser } = useUser()
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('user')
    setUser(null)
    navigate('/login')
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="navbar-brand">
          <h1>Mister Budget</h1>
        </div>
        <div className="navbar-menu">
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/income" className="nav-link">Income</Link>
          <Link to="/expenses" className="nav-link">Expenses</Link>
          <Link to="/goals" className="nav-link">Goals</Link>
          <Link to="/summary" className="nav-link">Summary</Link>
          <Link to="/advisor" className="nav-link">Advisor</Link>
          <Link to="/settings" className="nav-link">Settings</Link>
        </div>
        <div className="navbar-user">
          <span className="user-name">{user?.full_name}</span>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout
