import { useState } from 'react'
import './TransactionFilters.css'

const TransactionFilters = ({ categories, onFilterChange }) => {
  const [filters, setFilters] = useState({
    type: '',
    category: '',
    date_from: '',
    date_to: '',
    amount_min: '',
    amount_max: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    const newFilters = { ...filters, [name]: value }
    setFilters(newFilters)
  }

  const handleApply = () => {
    // Remove empty filters
    const activeFilters = Object.entries(filters).reduce((acc, [key, value]) => {
      if (value) acc[key] = value
      return acc
    }, {})
    onFilterChange(activeFilters)
  }

  const handleClear = () => {
    const clearedFilters = {
      type: '',
      category: '',
      date_from: '',
      date_to: '',
      amount_min: '',
      amount_max: ''
    }
    setFilters(clearedFilters)
    onFilterChange({})
  }

  return (
    <div className="transaction-filters">
      <h3>Filters</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label>Type</label>
          <select name="type" value={filters.type} onChange={handleChange}>
            <option value="">All</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Category</label>
          <select name="category" value={filters.category} onChange={handleChange}>
            <option value="">All Categories</option>
            {categories && categories.length > 0 && categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>From Date</label>
          <input
            type="date"
            name="date_from"
            value={filters.date_from}
            onChange={handleChange}
          />
        </div>

        <div className="filter-group">
          <label>To Date</label>
          <input
            type="date"
            name="date_to"
            value={filters.date_to}
            onChange={handleChange}
          />
        </div>

        <div className="filter-group">
          <label>Min Amount</label>
          <input
            type="number"
            name="amount_min"
            value={filters.amount_min}
            onChange={handleChange}
            step="0.01"
            min="0"
          />
        </div>

        <div className="filter-group">
          <label>Max Amount</label>
          <input
            type="number"
            name="amount_max"
            value={filters.amount_max}
            onChange={handleChange}
            step="0.01"
            min="0"
          />
        </div>
      </div>

      <div className="filter-actions">
        <button onClick={handleClear} className="btn-secondary">Clear Filters</button>
        <button onClick={handleApply} className="btn-primary">Apply Filters</button>
      </div>
    </div>
  )
}

export default TransactionFilters

