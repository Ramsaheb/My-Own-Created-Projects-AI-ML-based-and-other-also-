import React from 'react';

const sentimentColors = {
  positive: '#4CAF50',
  neutral: '#2196F3',
  negative: '#F44336'
};

const ArticleCard = ({ article }) => {
  // Fallback sentiment to 'neutral' if missing
  const sentiment = article.sentiment || 'neutral';

  return (
    <div className="article-card" style={{
      border: `1px solid ${sentimentColors[sentiment]}`,
      borderRadius: '8px',
      padding: '16px',
      marginBottom: '16px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
    }}>
      <div className="article-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span 
          className="sentiment-badge" 
          style={{ 
            backgroundColor: sentimentColors[sentiment], 
            color: 'white', 
            padding: '4px 8px', 
            borderRadius: '12px',
            textTransform: 'capitalize',
            fontWeight: '600',
            fontSize: '0.85rem'
          }}
        >
          {sentiment}
        </span>
        <span className="article-source" style={{ fontStyle: 'italic', fontSize: '0.9rem', color: '#666' }}>
          {article.source?.name || article.source || 'Unknown Source'}
        </span>
      </div>

      <h3 className="article-title" style={{ margin: '0 0 8px 0', fontSize: '1.25rem' }}>
        <a href={article.url} target="_blank" rel="noopener noreferrer" style={{ color: '#333', textDecoration: 'none' }}>
          {article.title}
        </a>
      </h3>

      <p className="article-summary" style={{ color: '#555', fontSize: '1rem', lineHeight: '1.4' }}>
        {article.description || 'No summary available.'}
      </p>

      <div className="article-footer" style={{ marginTop: '12px', fontSize: '0.85rem', color: '#999' }}>
        <span className="article-date">{article.publishedAt ? new Date(article.publishedAt).toLocaleDateString() : 'Unknown Date'}</span>
      </div>
    </div>
  );
};

export default ArticleCard;
