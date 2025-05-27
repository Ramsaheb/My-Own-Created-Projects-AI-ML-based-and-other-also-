import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';
import ArticleCard from './ArticleCard';
import SentimentFilter from './SentimentFilter';
import StatsCard from './StatsCard';
import Loader from './Loader';
import { fetchArticles } from '../services/api';

const Dashboard = () => {
  const [articles, setArticles] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]);
  const [sentimentFilter, setSentimentFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState({
    positive: 0,
    neutral: 0,
    negative: 0
  });

  // Simulate adding sentiment to articles if missing (replace with your real sentiment logic)
  const addSentimentToArticles = (articles) => {
    return articles.map(article => {
      // Simple dummy sentiment logic (random for demo)
      const sentiments = ['positive', 'neutral', 'negative'];
      return {
        ...article,
        sentiment: sentiments[Math.floor(Math.random() * sentiments.length)]
      };
    });
  };

  const handleSearch = async (query) => {
    setIsLoading(true);
    try {
      const data = await fetchArticles(query);
      const articlesWithSentiment = addSentimentToArticles(data);
      setArticles(articlesWithSentiment);
      updateStats(articlesWithSentiment);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateStats = (articles) => {
    const newStats = {
      positive: articles.filter(a => a.sentiment === 'positive').length,
      neutral: articles.filter(a => a.sentiment === 'neutral').length,
      negative: articles.filter(a => a.sentiment === 'negative').length
    };
    setStats(newStats);
  };

  useEffect(() => {
    if (sentimentFilter === 'all') {
      setFilteredArticles(articles);
    } else {
      setFilteredArticles(articles.filter(a => a.sentiment === sentimentFilter));
    }
  }, [sentimentFilter, articles]);

  return (
    <div className="dashboard" style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      <div className="dashboard-header" style={{ marginBottom: '20px', textAlign: 'center' }}>
        <h2>Media Sentiment Analysis</h2>
        <p>Track public perception of brands, topics, and personalities</p>
      </div>

      <SearchBar onSearch={handleSearch} isLoading={isLoading} />

      {isLoading ? (
        <Loader />
      ) : (
        <>
          {articles.length > 0 && (
            <>
              <StatsCard stats={stats} />
              <SentimentFilter 
                activeFilter={sentimentFilter} 
                setFilter={setSentimentFilter} 
              />
            </>
          )}

          <div className="articles-grid" style={{ marginTop: '20px' }}>
            {filteredArticles.length > 0 ? (
              filteredArticles.map((article, index) => (
                <ArticleCard key={index} article={article} />
              ))
            ) : articles.length > 0 ? (
              <div className="no-results" style={{ textAlign: 'center', marginTop: '40px', color: '#777' }}>
                <p>No articles match the selected sentiment filter.</p>
              </div>
            ) : (
              <div className="welcome-message" style={{ textAlign: 'center', marginTop: '40px', color: '#555' }}>
                <h3>Welcome to Media Pulse</h3>
                <p>Enter a topic or keyword to analyze media sentiment</p>
                <div className="example-topics" style={{ marginTop: '12px', fontStyle: 'italic' }}>
                  <p>Try: <span style={{fontWeight: '600'}}>Apple</span>, <span style={{fontWeight: '600'}}>Nike Sustainability</span>, <span style={{fontWeight: '600'}}>Elon Musk</span></p>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
