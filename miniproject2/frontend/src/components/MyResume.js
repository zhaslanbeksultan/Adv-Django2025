// src/components/MyResume.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getResumeList } from '../api';

const MyResume = () => {
  const [resume, setResume] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchResume = async () => {
      try {
        const data = await getResumeList();
        if (data.resumes && data.resumes.length > 0) {
          setResume(data.resumes[0]); // Latest resume
        }
      } catch (err) {
        setError('Failed to load resume');
      }
    };
    fetchResume();
  }, []);

  const handleUploadResume = () => {
    navigate('/upload-resume');
  };

  const handleRecommendations = () => {
    navigate('/jobs/recommendations');
  };

  const handleResumeFeedback = () => {
    navigate('/resume-feedback');
  };

  return (
      <div style={{maxWidth: '800px', margin: '50px auto'}}>
        <h2>My Latest Resume</h2>
        <button
            onClick={handleUploadResume}
            style={{padding: '10px 20px', marginBottom: '20px', backgroundColor: '#4CAF50', color: 'white'}}
        >
          Upload Resume
        </button>
        <button
            onClick={handleResumeFeedback}
            style={{padding: '10px 20px', marginBottom: '20px', backgroundColor: '#4CAF50', color: 'white'}}
        >
          Resume Feedback
        </button>
        <button
            onClick={handleRecommendations}
            style={{padding: '10px 20px', marginBottom: '20px', backgroundColor: '#4CAF50', color: 'white'}}
        >
          Job Recommendations
        </button>
        {error && <p style={{color: 'red'}}>{error}</p>}
        {!resume && !error && <p>No resume uploaded yet</p>}
        {resume && (
            <div style={{border: '1px solid #ccc', padding: '10px'}}>
              <p><strong>File:</strong> <a href={resume.file} target="_blank"
                                           rel="noopener noreferrer">{resume.file_name || 'Download Resume'}</a></p>
              <p><strong>Uploaded:</strong> {new Date(resume.uploaded_at).toLocaleString()}</p>
              {resume.title && <p><strong>Title:</strong> {resume.title}</p>}
            </div>
        )}
      </div>
  );
};

export default MyResume;