import React from 'react';

const SentimentFilter = ({ activeFilter, setFilter }) => {
  const filters = ['all', 'positive', 'neutral', 'negative'];

  return (
    <div className="sentiment-filter">
      {filters.map((filter) => (
        <button
          key={filter}
          className={`filter-button ${activeFilter === filter ? 'active' : ''}`}
          onClick={() => setFilter(filter)}
        >
          {filter.charAt(0).toUpperCase() + filter.slice(1)}
        </button>
      ))}
    </div>
  );
};

export default SentimentFilter;