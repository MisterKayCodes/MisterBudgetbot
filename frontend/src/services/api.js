import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL
})

export const userAPI = {
  register: (telegram_id, full_name, email) =>
    api.post('/users/', { telegram_id, full_name, email }),

  getUser: (telegram_id) =>
    api.get(`/users/${telegram_id}`),

  updateUser: (telegram_id, updates) =>
    api.patch(`/users/${telegram_id}`, updates)
}

export const incomeAPI = {
  addIncome: (telegram_id, amount) =>
    api.post(`/income/${telegram_id}`, { amount }),

  getIncomeHistory: (telegram_id, limit = 10) =>
    api.get(`/income/${telegram_id}?limit=${limit}`)
}

export const expensesAPI = {
  addExpense: (telegram_id, description, amount, category) =>
    api.post(`/expenses/${telegram_id}`, { description, amount, category }),

  getExpenseHistory: (telegram_id, limit = 10) =>
    api.get(`/expenses/${telegram_id}?limit=${limit}`)
}

export const goalsAPI = {
  createGoal: (telegram_id, goal_name, target_amount, deadline, auto_save_percent) =>
    api.post(`/goals/${telegram_id}`, { goal_name, target_amount, deadline, auto_save_percent }),

  getActiveGoals: (telegram_id) =>
    api.get(`/goals/${telegram_id}/active`),

  getCompletedGoals: (telegram_id) =>
    api.get(`/goals/${telegram_id}/completed`)
}

export const accountsAPI = {
  getAccounts: (telegram_id) =>
    api.get(`/accounts/${telegram_id}`),

  getTotalBalance: (telegram_id) =>
    api.get(`/accounts/${telegram_id}/balance`)
}

export const summaryAPI = {
  getWeeklySummary: (telegram_id) =>
    api.get(`/summary/${telegram_id}/weekly`),

  getMonthlySummary: (telegram_id) =>
    api.get(`/summary/${telegram_id}/monthly`),

  getAllTimeSummary: (telegram_id) =>
    api.get(`/summary/${telegram_id}/alltime`),

  exportCSV: (telegram_id) =>
    api.get(`/summary/${telegram_id}/export`, { responseType: 'blob' })
}

export const advisorAPI = {
  getSpendingAnalysis: (telegram_id) =>
    api.get(`/advisor/${telegram_id}/spending`),

  getSavingsAnalysis: (telegram_id) =>
    api.get(`/advisor/${telegram_id}/savings`),

  getRecommendations: (telegram_id) =>
    api.get(`/advisor/${telegram_id}/recommendations`)
}

export default api
