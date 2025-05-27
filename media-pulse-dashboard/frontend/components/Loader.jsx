import React from 'react';

const Loader = () => {
  return (
    <div className="loader-container">
      <div className="loader">
        <div className="loader-dot"></div>
        <div className="loader-dot"></div>
        <div className="loader-dot"></div>
      </div>
      <p>Analyzing media sentiment...</p>
    </div>
  );
};

export default Loader;