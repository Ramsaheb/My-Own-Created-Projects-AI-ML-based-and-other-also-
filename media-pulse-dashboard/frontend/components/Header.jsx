import React from 'react';
import { useAuth } from '../services/auth';

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <span className="logo-icon">📊</span>
          <h1>Media Pulse</h1>
        </div>
        <nav className="nav">
          {user ? (
            <button onClick={logout} className="auth-button logout">
              Logout
            </button>
          ) : (
            <a href="/login" className="auth-button login">
              Login
            </a>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;