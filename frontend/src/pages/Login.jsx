import { useState } from 'react'
import { useUser } from '../context/UserContext'
import { userAPI } from '../services/api'
import { useNavigate } from 'react-router-dom'
import '../styles/Login.css'

function Login() {
  const [isRegister, setIsRegister] = useState(false)
  const [telegramId, setTelegramId] = useState('')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { setUser } = useUser()
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await userAPI.getUser(parseInt(telegramId))
      const userData = response.data

      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      navigate('/')
    } catch (err) {
      setError('User not found. Please register first.')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await userAPI.register(parseInt(telegramId), fullName, email)
      const userData = response.data

      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Mister Budget</h1>
        <p className="subtitle">Manage your finances with ease</p>

        {error && <div className="error-message">{error}</div>}

        {!isRegister ? (
          <form onSubmit={handleLogin}>
            <h2>Login</h2>
            <div className="form-group">
              <label>Telegram ID</label>
              <input
                type="number"
                value={telegramId}
                onChange={(e) => setTelegramId(e.target.value)}
                placeholder="Enter your Telegram ID"
                required
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>

            <p className="toggle-text">
              Don't have an account?{' '}
              <button type="button" onClick={() => setIsRegister(true)} className="link-button">
                Register
              </button>
            </p>
          </form>
        ) : (
          <form onSubmit={handleRegister}>
            <h2>Register</h2>
            <div className="form-group">
              <label>Telegram ID</label>
              <input
                type="number"
                value={telegramId}
                onChange={(e) => setTelegramId(e.target.value)}
                placeholder="Enter your Telegram ID"
                required
              />
            </div>

            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Enter your full name"
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Registering...' : 'Register'}
            </button>

            <p className="toggle-text">
              Already have an account?{' '}
              <button type="button" onClick={() => setIsRegister(false)} className="link-button">
                Login
              </button>
            </p>
          </form>
        )}
      </div>
    </div>
  )
}

export default Login
