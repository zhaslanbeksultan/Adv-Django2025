import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {getJobList, logoutUser} from '../api';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

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

  const handleManageJobs = () => {
    navigate('/jobs/manage');
  };

  const handleLogout = () => {
    logoutUser();
    navigate('/');
  };

  const handleMyResumes = () => {
    navigate('/my-resume');
  };

  const handlePasswordReset = () => {
    navigate('/password-reset');
  };

  return (
      <div style={{maxWidth: '800px', margin: '50px auto'}}>
          <h2>Job Listings</h2>
          <button
              onClick={handleManageJobs}
              style={{padding: '10px 20px', marginBottom: '20px', backgroundColor: '#f3f560'}}
          >
              My Jobs
          </button>
          <button
              onClick={handleMyResumes}
              style={{padding: '10px 20px', marginRight: '10px', backgroundColor: '#f3f560'}}
          >
              My Resumes
          </button>
          <button
              onClick={handleLogout}
              style={{padding: '10px 20px', backgroundColor: '#ff4d4d', color: 'white'}}
          >
              Logout
          </button>
          <button
              onClick={handlePasswordReset}
              style={{padding: '10px 20px', backgroundColor: 'skyblue', color: 'white'}}
          >
              Password Reset
          </button>
          {error && <p style={{color: 'red'}}>{error}</p>}
          {jobs.length === 0 && !error && <p>No jobs available</p>}
          {jobs.map((job) => (
              <div key={job.id} style={{border: '1px solid #ccc', padding: '10px', margin: '10px 0'}}>
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