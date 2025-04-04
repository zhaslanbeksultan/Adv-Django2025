import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { verifyEmail } from '../api';

const VerifyEmail = () => {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get('token');
    console.log('Frontend token:', token);
    if (!token) {
      setError('No verification token provided.');
      return;
    }

    const verify = async () => {
      try {
        const response = await verifyEmail(token);
        setMessage(response.message);
        setTimeout(() => navigate('/login'), 1000); // Redirect to /login after 2s
      } catch (err) {
        setError(err.error || 'Verification failed.');
      }
    };

    verify();
  }, [searchParams, navigate]);

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', textAlign: 'center' }}>
      <h2>Email Verification</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!message && !error && <p>Verifying your email...</p>}
    </div>
  );
};

export default VerifyEmail;