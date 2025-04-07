// src/components/JobRecommendations.jsx
import React, { useState, useEffect } from 'react';
import { getJobRecommendations } from '../api';

const JobRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const data = await getJobRecommendations();
        setRecommendations(data.recommendations);
      } catch (err) {
        setError(err.error || 'Failed to load recommendations');
      }
    };
    fetchRecommendations();
  }, []);

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto' }}>
      <h2>Job Recommendations</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {recommendations.length === 0 && !error && <p>No recommendations available</p>}
      {recommendations.map((job) => (
        <div key={job.job_id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
          <h3>{job.title}</h3>
          <p><strong>Company:</strong> {job.company}</p>
          <p><strong>Location:</strong> {job.location || 'Not specified'}</p>
          <p><strong>Description:</strong> {job.description}</p>
          <p><strong>Posted by:</strong> {job.posted_by}</p>
          <p><strong>Match Score:</strong> {job.match_score}%</p>
          <p><strong>Matched Skills:</strong> {job.matched_skills.join(', ')}</p>
        </div>
      ))}
    </div>
  );
};

export default JobRecommendations;