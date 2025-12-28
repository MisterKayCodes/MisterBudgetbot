import { useState } from 'react'
import { useUser } from '../context/UserContext'
import { incomeAPI } from '../services/api'
import { formatCurrency } from '../utils/formatters'
import Layout from '../components/Layout'

function Income() {
  const { user } = useUser()
  const [amount, setAmount] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const result = await incomeAPI.addIncome(user.telegram_id, parseFloat(amount))
      const data = result.data

      let msg = `Income added successfully!\n\nAmount: ${formatCurrency(parseFloat(amount), user.currency)}\n\nSplit:\n`
      msg += `Spending: ${formatCurrency(data.splits.spending, user.currency)}\n`
      msg += `Savings: ${formatCurrency(data.splits.savings, user.currency)}\n`
      msg += `Business: ${formatCurrency(data.splits.business, user.currency)}`

      setMessage({ type: 'success', text: msg })
      setAmount('')
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Error adding income' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="page-container">
        <h1>Add Income</h1>

        {message && (
          <div className={message.type === 'success' ? 'success-message' : 'error-message'} style={{ whiteSpace: 'pre-line' }}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Income Amount</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Enter amount"
              required
              min="0.01"
              step="0.01"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Processing...' : 'Add Income'}
          </button>
        </form>
      </div>
    </Layout>
  )
}

export default Income
