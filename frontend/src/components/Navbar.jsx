import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Activity, LogOut, User, Cpu } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="nav-logo">
          <Cpu className="w-6 h-6" />
          <span>VOICE.AI</span>
        </Link>

        <div className="nav-links">
          <Link to="/" className="nav-link">INTERFACE</Link>
          {user ? (
            <>
              <Link to="/dashboard" className="nav-link flex items-center gap-2">
                <Activity className="w-4 h-4" />
                DASHBOARD
              </Link>
              <div className="flex items-center gap-4 ml-4 pl-4" style={{ borderLeft: '1px solid var(--glass-border)' }}>
                <span className="text-xs text-gray-400 flex items-center gap-1">
                  <User className="w-3 h-3" />
                  {user.username}
                </span>
                <button 
                  onClick={handleLogout}
                  className="p-2 rounded-full hover:bg-[var(--glass-border)] text-red-400 transition-colors"
                  title="Logout"
                  style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-4">
              <Link to="/login" className="nav-link">LOGIN</Link>
              <Link to="/register" className="btn-access">
                ACCESS
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
