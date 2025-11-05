import { useState, useEffect } from 'react'
import './BudgetForm.css'

const BudgetForm = ({ budget, categories, onSubmit, onCancel }) => {
  const currentDate = new Date()
  const [formData, setFormData] = useState({
    month: currentDate.getMonth() + 1,
    year: currentDate.getFullYear(),
    amount: '',
    category: ''
  })
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (budget) {
      setFormData({
        month: budget.month,
        year: budget.year,
        amount: budget.amount,
        category: budget.category || ''
      })
    }
  }, [budget])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    setErrors(prev => ({ ...prev, [name]: '' }))
  }

  const validate = () => {
    const newErrors = {}

    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    }

    if (!formData.month || formData.month < 1 || formData.month > 12) {
      newErrors.month = 'Invalid month'
    }

    if (!formData.year || formData.year < 2000) {
      newErrors.year = 'Invalid year'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validate()) {
      return
    }

    setSubmitting(true)

    try {
      const submitData = {
        ...formData,
        category: formData.category || null
      }
      await onSubmit(submitData)
    } catch (error) {
      if (error.response?.data) {
        setErrors(error.response.data)
      } else {
        setErrors({ general: 'Failed to save budget' })
      }
      setSubmitting(false)
    }
  }

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  const years = Array.from({ length: 5 }, (_, i) => currentDate.getFullYear() + i)

  return (
    <div className="budget-form">
      <h2>{budget ? 'Edit Budget' : 'Set Budget'}</h2>
      <form onSubmit={handleSubmit}>
        {errors.general && <div className="error-message">{errors.general}</div>}

        <div className="form-group">
          <label htmlFor="month">Month *</label>
          <select
            id="month"
            name="month"
            value={formData.month}
            onChange={handleChange}
            required
          >
            {months.map((month, index) => (
              <option key={index} value={index + 1}>{month}</option>
            ))}
          </select>
          {errors.month && <span className="error">{errors.month}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="year">Year *</label>
          <select
            id="year"
            name="year"
            value={formData.year}
            onChange={handleChange}
            required
          >
            {years.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
          {errors.year && <span className="error">{errors.year}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="amount">Budget Amount *</label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            step="0.01"
            min="0.01"
            required
          />
          {errors.amount && <span className="error">{errors.amount}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="category">Category (Optional)</label>
          <select
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
          >
            <option value="">Overall Budget</option>
            {categories && categories.length > 0 && categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
          <small>Leave blank for overall monthly budget</small>
          {errors.category && <span className="error">{errors.category}</span>}
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn-primary" disabled={submitting}>
            {submitting ? 'Saving...' : 'Save Budget'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default BudgetForm
