import React, { useState } from 'react';
import { createJob } from '../api';

const JobCreate = () => {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    description: '',
    location: '',
    is_active: true,
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: name === 'is_active' ? value === 'true' : value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      const response = await createJob(formData);
      setMessage('Job created successfully');
      setFormData({ title: '', company: '', description: '', location: '', is_active: true });
    } catch (err) {
      setError(err.error || 'Failed to create job');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto' }}>
      <h2>Create Job Listing</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <div>
          <label>Company:</label>
          <input
            type="text"
            name="company"
            value={formData.company}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px', margin: '5px 0', minHeight: '100px' }}
          />
        </div>
        <div>
          <label>Location:</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <div>
          <label>Active:</label>
          <select
            name="is_active"
            value={formData.is_active}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          >
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>
        <button type="submit" style={{ padding: '10px 20px', marginTop: '10px' }}>
          Create Job
        </button>
      </form>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default JobCreate;