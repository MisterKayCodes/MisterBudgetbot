import { useState, useEffect } from 'react'
import { useUser } from '../context/UserContext'
import { accountsAPI, goalsAPI, summaryAPI } from '../services/api'
import { formatCurrency } from '../utils/formatters'
import Layout from '../components/Layout'
import '../styles/Dashboard.css'

function Dashboard() {
  const { user } = useUser()
  const [stats, setStats] = useState({
    totalBalance: 0,
    monthlyIncome: 0,
    monthlyExpenses: 0,
    activeGoals: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      fetchDashboardData()
    }
  }, [user])

  const fetchDashboardData = async () => {
    try {
      const [balanceRes, summaryRes, goalsRes] = await Promise.all([
        accountsAPI.getTotalBalance(user.telegram_id),
        summaryAPI.getMonthlySummary(user.telegram_id),
        goalsAPI.getActiveGoals(user.telegram_id)
      ])

      setStats({
        totalBalance: balanceRes.data.total_balance,
        monthlyIncome: summaryRes.data.income_total,
        monthlyExpenses: summaryRes.data.expense_total,
        activeGoals: goalsRes.data.length
      })
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="loading">Loading dashboard...</div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Welcome back, {user?.full_name}</h1>
          <p className="subtitle">Here's your financial overview</p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">💰</div>
            <div className="stat-content">
              <h3>Total Balance</h3>
              <p className="stat-value">{formatCurrency(stats.totalBalance, user.currency)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3>Monthly Income</h3>
              <p className="stat-value">{formatCurrency(stats.monthlyIncome, user.currency)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📉</div>
            <div className="stat-content">
              <h3>Monthly Expenses</h3>
              <p className="stat-value">{formatCurrency(stats.monthlyExpenses, user.currency)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-content">
              <h3>Active Goals</h3>
              <p className="stat-value">{stats.activeGoals}</p>
            </div>
          </div>
        </div>

        <div className="net-summary">
          <h3>Net This Month</h3>
          <p className={stats.monthlyIncome - stats.monthlyExpenses >= 0 ? 'positive' : 'negative'}>
            {formatCurrency(stats.monthlyIncome - stats.monthlyExpenses, user.currency)}
          </p>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
