import React, { useState } from 'react';

const SearchBar = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <div className="search-input-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter a topic or keyword (e.g., Apple, Nike Sustainability)"
          className="search-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className={`search-button ${isLoading ? 'loading' : ''}`}
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="button-loader"></span>
          ) : (
            <span>Analyze</span>
          )}
        </button>
      </div>
    </form>
  );
};

export default SearchBar;