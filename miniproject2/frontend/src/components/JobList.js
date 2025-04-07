import React, { useState, useEffect } from 'react';
import { getJobList } from '../api';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const data = await getJobList();
        setJobs(data.jobs);
      } catch (err) {
        setError('Failed to load jobs');
      }
    };
    fetchJobs();
  }, []);

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto' }}>
      <h2>Job Listings</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {jobs.length === 0 && !error && <p>No jobs available</p>}
      {jobs.map((job) => (
        <div key={job.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
          <h3>{job.title}</h3>
          <p><strong>Company:</strong> {job.company}</p>
          <p><strong>Location:</strong> {job.location || 'Not specified'}</p>
          <p><strong>Description:</strong> {job.description}</p>
          <p><strong>Posted by:</strong> {job.posted_by}</p>
          <p><strong>Created:</strong> {new Date(job.created_at).toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
};

export default JobList;