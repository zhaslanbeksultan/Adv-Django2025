// components/ResumeFeedback.jsx
import React, {useState, useEffect, useCallback} from 'react';
import axios from 'axios';
import './ResumeFeedback.css'; // Optional: for styling

const ResumeFeedback = () => {
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Get tokens from localStorage
  const getAuthHeaders = () => {
    const tokens = JSON.parse(localStorage.getItem('tokens') || '{}');
    return { Authorization: `Bearer ${tokens.access}` };
  };

  // Fetch feedback from the backend
  const fetchFeedback = useCallback(async () => {
    const headers = getAuthHeaders();
    console.log('Feedback request headers:', headers);
    try {
      const response = await axios.get('http://localhost:8000/resumes/resume-feedback/', {
        headers,
      });
      console.log('Feedback response:', response.data);
      setFeedback(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Feedback error:', err.response);
      setError(err.response?.data?.error || 'Failed to load feedback');
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFeedback();
  }, [fetchFeedback]);

  if (loading) {
    return <div>Loading feedback...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="resume-feedback-container">
      <h2>Resume Feedback</h2>

      {/* Skill Gaps Section */}
      <section className="feedback-section">
        <h3>Skill Gaps</h3>
        <div>
          <strong>Present Skills:</strong>
          <ul>
            {feedback.skill_gaps.present.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
        <div>
          <strong>Missing Skills:</strong>
          <ul>
            {feedback.skill_gaps.missing.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
        <p><strong>Suggestion:</strong> {feedback.skill_gaps.suggestion}</p>
      </section>

      {/* Formatting Section */}
      <section className="feedback-section">
        <h3>Formatting</h3>
        {Array.isArray(feedback.formatting) ? (
          <ul>
            {feedback.formatting.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        ) : (
          <p>{feedback.formatting}</p>
        )}
      </section>

      {/* ATS Optimization Section */}
      <section className="feedback-section">
        <h3>ATS Optimization</h3>
        <div>
          <strong>Present Keywords:</strong>
          <ul>
            {feedback.ats_optimization.present.map((keyword, index) => (
              <li key={index}>{keyword}</li>
            ))}
          </ul>
        </div>
        <div>
          <strong>Missing Keywords:</strong>
          <ul>
            {feedback.ats_optimization.missing.map((keyword, index) => (
              <li key={index}>{keyword}</li>
            ))}
          </ul>
        </div>
        <p><strong>Suggestion:</strong> {feedback.ats_optimization.suggestion}</p>
      </section>
    </div>
  );
};

export default ResumeFeedback;