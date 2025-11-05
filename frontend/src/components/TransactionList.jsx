import './TransactionList.css'

const TransactionList = ({ transactions, loading, onEdit, onDelete, pagination, currentPage, onPageChange }) => {
  if (loading) {
    return <div className="loading">Loading transactions...</div>
  }

  if (!transactions || transactions.length === 0) {
    return <div className="no-data">No transactions found</div>
  }

  const totalPages = Math.ceil(pagination.count / 10)

  return (
    <div className="transaction-list">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Type</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(transaction => (
            <tr key={transaction.id}>
              <td>{new Date(transaction.date).toLocaleDateString()}</td>
              <td>
                <span className={`badge badge-${transaction.type}`}>
                  {transaction.type}
                </span>
              </td>
              <td>{transaction.category_name}</td>
              <td className={transaction.type === 'income' ? 'amount-green' : 'amount-red'}>
                ${parseFloat(transaction.amount).toFixed(2)}
              </td>
              <td>{transaction.description || '-'}</td>
              <td className="actions">
                <button onClick={() => onEdit(transaction)} className="btn-icon btn-edit" title="Edit">
                  ✏️
                </button>
                <button onClick={() => onDelete(transaction.id)} className="btn-icon btn-delete" title="Delete">
                  🗑️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {pagination.count > 10 && (
        <div className="pagination">
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={!pagination.previous}
            className="btn-page"
          >
            Previous
          </button>
          <span className="page-info">
            Page {currentPage} of {totalPages} ({pagination.count} total)
          </span>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={!pagination.next}
            className="btn-page"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

export default TransactionList

