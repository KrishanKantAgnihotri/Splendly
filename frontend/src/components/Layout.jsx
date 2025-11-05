import { Outlet, NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Layout.css'

const Layout = () => {
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>💰 Spendly</h1>
        </div>
        <div className="nav-links">
          <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
            Dashboard
          </NavLink>
          <NavLink to="/transactions" className={({ isActive }) => isActive ? 'active' : ''}>
            Transactions
          </NavLink>
          <NavLink to="/budget" className={({ isActive }) => isActive ? 'active' : ''}>
            Budget
          </NavLink>
        </div>
        <div className="nav-user">
          <span>Welcome, {user?.username}</span>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout

