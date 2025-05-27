import React from 'react';

const StatsCard = ({ stats }) => {
  const total = stats.positive + stats.neutral + stats.negative;

  const getPercentage = (value) => {
    return total > 0 ? Math.round((value / total) * 100) : 0;
  };

  return (
    <div className="stats-card">
      <h3 className="stats-title">Sentiment Analysis</h3>
      <div className="stats-grid">
        <div className="stat-item positive">
          <span className="stat-value">{stats.positive}</span>
          <span className="stat-label">Positive</span>
          <div className="stat-bar">
            <div 
              className="stat-bar-fill" 
              style={{ width: `${getPercentage(stats.positive)}%` }}
            ></div>
          </div>
          <span className="stat-percentage">{getPercentage(stats.positive)}%</span>
        </div>
        <div className="stat-item neutral">
          <span className="stat-value">{stats.neutral}</span>
          <span className="stat-label">Neutral</span>
          <div className="stat-bar">
            <div 
              className="stat-bar-fill" 
              style={{ width: `${getPercentage(stats.neutral)}%` }}
            ></div>
          </div>
          <span className="stat-percentage">{getPercentage(stats.neutral)}%</span>
        </div>
        <div className="stat-item negative">
          <span className="stat-value">{stats.negative}</span>
          <span className="stat-label">Negative</span>
          <div className="stat-bar">
            <div 
              className="stat-bar-fill" 
              style={{ width: `${getPercentage(stats.negative)}%` }}
            ></div>
          </div>
          <span className="stat-percentage">{getPercentage(stats.negative)}%</span>
        </div>
      </div>
    </div>
  );
};

export default StatsCard;