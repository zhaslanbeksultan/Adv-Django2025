// src/components/JobManage.jsx
import React, { useState, useEffect } from 'react';
import { getJobList, updateJob, deleteJob } from '../api';

const JobManage = () => {
  const [jobs, setJobs] = useState([]);
  const [editJob, setEditJob] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const username = user.username;
        if (!username) {
          throw new Error('No username found in localStorage');
        }
        console.log('Fetching jobs for user:', username);
        const data = await getJobList();
        console.log('Raw job data:', data);
        const filteredJobs = data.jobs.filter(job => job.posted_by === username);
        console.log('Filtered jobs:', filteredJobs);
        setJobs(filteredJobs);
      } catch (err) {
        console.error('Error fetching jobs:', err);
        setError(err.message || 'Failed to load jobs');
      }
    };
    fetchJobs();
  }, []);

  const handleEdit = (job) => {
    setEditJob({ ...job });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const updatedJob = await updateJob(editJob.id, editJob);
      setJobs(jobs.map(job => (job.id === updatedJob.id ? updatedJob : job)));
      setEditJob(null);
    } catch (err) {
      setError('Failed to update job');
    }
  };

  const handleDelete = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await deleteJob(jobId);
        setJobs(jobs.filter(job => job.id !== jobId));
      } catch (err) {
        setError('Failed to delete job');
      }
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto' }}>
      <h2>Manage Your Jobs</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {jobs.length === 0 && !error && <p>No jobs found for you</p>}
      {jobs.map((job) => (
        <div key={job.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
          {editJob && editJob.id === job.id ? (
            <form onSubmit={handleUpdate}>
              <input
                type="text"
                value={editJob.title}
                onChange={(e) => setEditJob({ ...editJob, title: e.target.value })}
                required
                style={{ width: '100%', padding: '8px', margin: '5px 0' }}
              />
              <input
                type="text"
                value={editJob.company}
                onChange={(e) => setEditJob({ ...editJob, company: e.target.value })}
                required
                style={{ width: '100%', padding: '8px', margin: '5px 0' }}
              />
              <textarea
                value={editJob.description}
                onChange={(e) => setEditJob({ ...editJob, description: e.target.value })}
                required
                style={{ width: '100%', padding: '8px', margin: '5px 0', minHeight: '100px' }}
              />
              <input
                type="text"
                value={editJob.location}
                onChange={(e) => setEditJob({ ...editJob, location: e.target.value })}
                style={{ width: '100%', padding: '8px', margin: '5px 0' }}
              />
              <select
                value={editJob.is_active}
                onChange={(e) => setEditJob({ ...editJob, is_active: e.target.value === 'true' })}
                style={{ width: '100%', padding: '8px', margin: '5px 0' }}
              >
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
              <button type="submit" style={{ padding: '5px 10px', marginRight: '10px' }}>Save</button>
              <button type="button" onClick={() => setEditJob(null)} style={{ padding: '5px 10px' }}>Cancel</button>
            </form>
          ) : (
            <>
              <h3>{job.title}</h3>
              <p><strong>Company:</strong> {job.company}</p>
              <p><strong>Location:</strong> {job.location || 'Not specified'}</p>
              <p><strong>Description:</strong> {job.description}</p>
              <p><strong>Status:</strong> {job.is_active ? 'Active' : 'Inactive'}</p>
              <button onClick={() => handleEdit(job)} style={{ padding: '5px 10px', marginRight: '10px' }}>Edit</button>
              <button onClick={() => handleDelete(job.id)} style={{ padding: '5px 10px' }}>Delete</button>
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default JobManage;