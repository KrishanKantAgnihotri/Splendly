import { useState, useEffect, useRef } from 'react'
import * as d3 from 'd3'
import api from '../services/api'
import BudgetForm from '../components/BudgetForm'
import './Budget.css'

const Budget = () => {
  const [budgets, setBudgets] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingBudget, setEditingBudget] = useState(null)
  const chartRef = useRef(null)

  useEffect(() => {
    fetchCategories()
    fetchBudgets()
  }, [])

  useEffect(() => {
    if (budgets.length > 0) {
      drawChart()
    }
  }, [budgets])

  const fetchCategories = async () => {
    try {
      // Get all expense categories without pagination
      const response = await api.get('/categories/?type=expense&page_size=100')
      // Handle both paginated and non-paginated responses
      const categoriesData = response.data.results || response.data
      setCategories(Array.isArray(categoriesData) ? categoriesData : [])
    } catch (error) {
      console.error('Error fetching categories:', error)
      setCategories([])
    }
  }

  const fetchBudgets = async () => {
    try {
      setLoading(true)
      const response = await api.get('/budgets/current_month/')
      setBudgets(Array.isArray(response.data) ? response.data : [])
    } catch (error) {
      console.error('Error fetching budgets:', error)
      setBudgets([])
    } finally {
      setLoading(false)
    }
  }

  const drawChart = () => {
    // Clear previous chart
    d3.select(chartRef.current).selectAll('*').remove()

    const data = budgets.filter(b => b.actual_expenses > 0 || b.amount > 0)
    
    if (data.length === 0) return

    const margin = { top: 20, right: 30, bottom: 40, left: 100 }
    const width = 600 - margin.left - margin.right
    const height = Math.max(300, data.length * 60) - margin.top - margin.bottom

    const svg = d3.select(chartRef.current)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // Y scale (categories)
    const y = d3.scaleBand()
      .domain(data.map(d => d.category_name || 'Overall Budget'))
      .range([0, height])
      .padding(0.3)

    // X scale (amounts)
    const maxValue = d3.max(data, d => Math.max(d.amount, d.actual_expenses))
    const x = d3.scaleLinear()
      .domain([0, maxValue * 1.1])
      .range([0, width])

    // Add Y axis
    svg.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('font-size', '12px')

    // Add X axis
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(5).tickFormat(d => `$${d}`))
      .selectAll('text')
      .style('font-size', '12px')

    // Add budget bars (background)
    svg.selectAll('.bar-budget')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar-budget')
      .attr('x', 0)
      .attr('y', d => y(d.category_name || 'Overall Budget'))
      .attr('width', d => x(d.amount))
      .attr('height', y.bandwidth())
      .attr('fill', '#e0e0e0')

    // Add actual expense bars
    svg.selectAll('.bar-actual')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar-actual')
      .attr('x', 0)
      .attr('y', d => y(d.category_name || 'Overall Budget'))
      .attr('width', d => x(d.actual_expenses))
      .attr('height', y.bandwidth())
      .attr('fill', d => d.percentage_used > 100 ? '#e74c3c' : '#3498db')

    // Add labels
    svg.selectAll('.label')
      .data(data)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', d => x(Math.max(d.amount, d.actual_expenses)) + 5)
      .attr('y', d => y(d.category_name || 'Overall Budget') + y.bandwidth() / 2)
      .attr('dy', '.35em')
      .style('font-size', '11px')
      .text(d => `${d.percentage_used.toFixed(1)}%`)
  }

  const handleAddBudget = () => {
    setEditingBudget(null)
    setShowForm(true)
  }

  const handleEditBudget = (budget) => {
    setEditingBudget(budget)
    setShowForm(true)
  }

  const handleDeleteBudget = async (id) => {
    if (!window.confirm('Are you sure you want to delete this budget?')) {
      return
    }

    try {
      await api.delete(`/budgets/${id}/`)
      fetchBudgets()
    } catch (error) {
      console.error('Error deleting budget:', error)
      alert('Failed to delete budget')
    }
  }

  const handleFormSubmit = async (data) => {
    try {
      if (editingBudget) {
        await api.put(`/budgets/${editingBudget.id}/`, data)
      } else {
        await api.post('/budgets/', data)
      }
      setShowForm(false)
      setEditingBudget(null)
      fetchBudgets()
    } catch (error) {
      console.error('Error saving budget:', error)
      throw error
    }
  }

  const currentDate = new Date()
  const currentMonth = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })

  return (
    <div className="budget-page">
      <div className="page-header">
        <div>
          <h1>Budget Management</h1>
          <p className="subtitle">Current Month: {currentMonth}</p>
        </div>
        <button onClick={handleAddBudget} className="btn-primary">
          + Set Budget
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading budgets...</div>
      ) : (
        <>
          {budgets.length > 0 ? (
            <>
              <div className="budget-chart">
                <h2>Budget vs Actual Expenses</h2>
                <div ref={chartRef} className="chart-container"></div>
              </div>

              <div className="budget-list">
                <h2>Budget Details</h2>
                <div className="budget-cards">
                  {budgets.map(budget => (
                    <div key={budget.id} className="budget-card">
                      <div className="budget-card-header">
                        <h3>{budget.category_name || 'Overall Budget'}</h3>
                        <div className="budget-actions">
                          <button onClick={() => handleEditBudget(budget)} className="btn-icon">✏️</button>
                          <button onClick={() => handleDeleteBudget(budget.id)} className="btn-icon">🗑️</button>
                        </div>
                      </div>
                      <div className="budget-card-body">
                        <div className="budget-row">
                          <span>Budget Amount:</span>
                          <span className="amount">${parseFloat(budget.amount).toFixed(2)}</span>
                        </div>
                        <div className="budget-row">
                          <span>Actual Expenses:</span>
                          <span className={budget.percentage_used > 100 ? 'amount-red' : 'amount'}>
                            ${budget.actual_expenses.toFixed(2)}
                          </span>
                        </div>
                        <div className="budget-row">
                          <span>Remaining:</span>
                          <span className={budget.remaining < 0 ? 'amount-red' : 'amount-green'}>
                            ${budget.remaining.toFixed(2)}
                          </span>
                        </div>
                        <div className="budget-progress">
                          <div
                            className={`budget-progress-bar ${budget.percentage_used > 100 ? 'over-budget' : ''}`}
                            style={{ width: `${Math.min(budget.percentage_used, 100)}%` }}
                          ></div>
                        </div>
                        <div className="budget-percentage">
                          {budget.percentage_used.toFixed(1)}% used
                          {budget.percentage_used > 100 && ' (Over Budget!)'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="no-data">
              <p>No budgets set for the current month.</p>
              <button onClick={handleAddBudget} className="btn-primary">
                Set Your First Budget
              </button>
            </div>
          )}
        </>
      )}

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowForm(false)}>×</button>
            <BudgetForm
              budget={editingBudget}
              categories={categories}
              onSubmit={handleFormSubmit}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default Budget

