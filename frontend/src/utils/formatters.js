export const CURRENCY_SYMBOLS = {
  NGN: '₦',
  USD: '$',
  EUR: '€'
}

export const formatCurrency = (amount, currency = 'NGN') => {
  const symbol = CURRENCY_SYMBOLS[currency] || currency
  return `${symbol}${parseFloat(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export const calculateProgress = (current, target) => {
  if (target <= 0) return 0
  return Math.min((current / target) * 100, 100)
}
