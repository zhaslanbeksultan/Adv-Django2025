import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadResume } from '../api';

const ResumeUpload = () => {
  const [formData, setFormData] = useState({
    title: '',
    file: null,
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'file') {
      setFormData({ ...formData, file: files[0] }); // Handle file input
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    const data = new FormData();
    data.append('file', formData.file); // Required field
    if (formData.title) data.append('title', formData.title); // Optional field

    try {
      await uploadResume(data);
      setMessage('Resume uploaded successfully');
      setTimeout(() => navigate('/my-resume'), 1000); // Redirect after success
    } catch (err) {
      setError(err.error || 'Failed to upload resume');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto' }}>
      <h2>Upload Resume</h2>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div>
          <label>Title (optional):</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <div>
          <label>File:</label>
          <input
            type="file"
            name="file"
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px', margin: '5px 0' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', marginTop: '10px' }}>
          Upload
        </button>
      </form>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default ResumeUpload;