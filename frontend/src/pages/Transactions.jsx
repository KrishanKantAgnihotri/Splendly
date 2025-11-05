import { useState, useEffect } from 'react'
import api from '../services/api'
import TransactionForm from '../components/TransactionForm'
import TransactionList from '../components/TransactionList'
import TransactionFilters from '../components/TransactionFilters'
import './Transactions.css'

const Transactions = () => {
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingTransaction, setEditingTransaction] = useState(null)
  const [pagination, setPagination] = useState({ count: 0, next: null, previous: null })
  const [filters, setFilters] = useState({})
  const [currentPage, setCurrentPage] = useState(1)

  useEffect(() => {
    fetchCategories()
  }, [])

  useEffect(() => {
    fetchTransactions()
  }, [filters, currentPage])

  const fetchCategories = async () => {
    try {
      console.log('Fetching categories...')
      // Get all categories without pagination
      const response = await api.get('/categories/?page_size=100')
      console.log('Categories response:', response.data)
      
      // Handle both paginated and non-paginated responses
      const categoriesData = response.data.results || response.data
      console.log('Categories count:', categoriesData.length)
      
      setCategories(Array.isArray(categoriesData) ? categoriesData : [])
    } catch (error) {
      console.error('Error fetching categories:', error)
      console.error('Error details:', error.response?.data)
      setCategories([])
    }
  }

  const fetchTransactions = async () => {
    try {
      setLoading(true)
      const params = {
        ...filters,
        page: currentPage
      }
      const response = await api.get('/transactions/', { params })
      const results = response.data.results || response.data
      setTransactions(Array.isArray(results) ? results : [])
      setPagination({
        count: response.data.count || 0,
        next: response.data.next || null,
        previous: response.data.previous || null
      })
    } catch (error) {
      console.error('Error fetching transactions:', error)
      setTransactions([])
    } finally {
      setLoading(false)
    }
  }

  const handleAddTransaction = () => {
    setEditingTransaction(null)
    setShowForm(true)
  }

  const handleEditTransaction = (transaction) => {
    setEditingTransaction(transaction)
    setShowForm(true)
  }

  const handleDeleteTransaction = async (id) => {
    if (!window.confirm('Are you sure you want to delete this transaction?')) {
      return
    }

    try {
      await api.delete(`/transactions/${id}/`)
      fetchTransactions()
    } catch (error) {
      console.error('Error deleting transaction:', error)
      alert('Failed to delete transaction')
    }
  }

  const handleFormSubmit = async (data) => {
    try {
      if (editingTransaction) {
        await api.put(`/transactions/${editingTransaction.id}/`, data)
      } else {
        await api.post('/transactions/', data)
      }
      setShowForm(false)
      setEditingTransaction(null)
      fetchTransactions()
    } catch (error) {
      console.error('Error saving transaction:', error)
      throw error
    }
  }

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
    setCurrentPage(1)
  }

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <div className="transactions-page">
      <div className="page-header">
        <h1>Transactions</h1>
        <button onClick={handleAddTransaction} className="btn-primary">
          + Add Transaction
        </button>
      </div>

      <TransactionFilters
        categories={categories}
        onFilterChange={handleFilterChange}
      />

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowForm(false)}>×</button>
            <TransactionForm
              transaction={editingTransaction}
              categories={categories}
              onSubmit={handleFormSubmit}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}

      <TransactionList
        transactions={transactions}
        loading={loading}
        onEdit={handleEditTransaction}
        onDelete={handleDeleteTransaction}
        pagination={pagination}
        currentPage={currentPage}
        onPageChange={handlePageChange}
      />
    </div>
  )
}

export default Transactions

