import { useState, useEffect, useRef } from 'react'
import * as d3 from 'd3'
import api from '../services/api'
import './Dashboard.css'

const Dashboard = () => {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const chartRef = useRef(null)

  useEffect(() => {
    fetchSummary()
  }, [])

  useEffect(() => {
    if (summary && summary.expense_by_category.length > 0) {
      drawChart()
    }
  }, [summary])

  const fetchSummary = async () => {
    try {
      setLoading(true)
      const response = await api.get('/transactions/summary/')
      setSummary(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load financial summary')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const drawChart = () => {
    // Clear previous chart
    d3.select(chartRef.current).selectAll('*').remove()

    const data = summary.expense_by_category
    const width = 400
    const height = 400
    const radius = Math.min(width, height) / 2

    const svg = d3.select(chartRef.current)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`)

    const color = d3.scaleOrdinal()
      .domain(data.map(d => d.category))
      .range(d3.schemeSet3)

    const pie = d3.pie()
      .value(d => d.amount)
      .sort(null)

    const arc = d3.arc()
      .innerRadius(0)
      .outerRadius(radius)

    const arcs = svg.selectAll('arc')
      .data(pie(data))
      .enter()
      .append('g')
      .attr('class', 'arc')

    arcs.append('path')
      .attr('d', arc)
      .attr('fill', d => color(d.data.category))
      .attr('stroke', 'white')
      .attr('stroke-width', 2)
      .on('mouseover', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('opacity', 0.7)
      })
      .on('mouseout', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('opacity', 1)
      })

    // Add labels
    arcs.append('text')
      .attr('transform', d => `translate(${arc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', 'white')
      .text(d => {
        const percent = ((d.data.amount / summary.total_expenses) * 100).toFixed(1)
        return percent > 5 ? `${percent}%` : ''
      })
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  if (!summary) {
    return <div>No data available</div>
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="summary-cards">
        <div className="card income-card">
          <h3>Total Income</h3>
          <p className="amount">${parseFloat(summary.total_income).toFixed(2)}</p>
        </div>
        <div className="card expense-card">
          <h3>Total Expenses</h3>
          <p className="amount">${parseFloat(summary.total_expenses).toFixed(2)}</p>
        </div>
        <div className="card balance-card">
          <h3>Balance</h3>
          <p className={`amount ${parseFloat(summary.balance) >= 0 ? 'positive' : 'negative'}`}>
            ${parseFloat(summary.balance).toFixed(2)}
          </p>
        </div>
      </div>

      <div className="chart-section">
        <h2>Expense Breakdown by Category</h2>
        {summary.expense_by_category.length > 0 ? (
          <div className="chart-container">
            <div ref={chartRef} className="pie-chart"></div>
            <div className="legend">
              {summary.expense_by_category.map((item, index) => (
                <div key={index} className="legend-item">
                  <span className="legend-color" style={{ 
                    backgroundColor: d3.schemeSet3[index % d3.schemeSet3.length] 
                  }}></span>
                  <span>{item.category}: ${item.amount.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="no-data">No expense data available</p>
        )}
      </div>

      <div className="recent-transactions">
        <h2>Category Summary</h2>
        <div className="category-lists">
          <div className="category-list">
            <h3>Income by Category</h3>
            {summary.income_by_category.length > 0 ? (
              <ul>
                {summary.income_by_category.map((item, index) => (
                  <li key={index}>
                    <span>{item.category}</span>
                    <span className="amount-green">${item.amount.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="no-data">No income recorded</p>
            )}
          </div>
          <div className="category-list">
            <h3>Expenses by Category</h3>
            {summary.expense_by_category.length > 0 ? (
              <ul>
                {summary.expense_by_category.map((item, index) => (
                  <li key={index}>
                    <span>{item.category}</span>
                    <span className="amount-red">${item.amount.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="no-data">No expenses recorded</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

