// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegisterForm from './components/RegisterForm';
import VerifyEmail from './components/VerifyEmail';
import Login from './components/Login';
import PasswordResetRequest from './components/PasswordResetRequest';
import PasswordResetConfirm from './components/PasswordResetConfirm';
import ResumeUpload from './components/ResumeUpload';
import ResumeFeedback from './components/ResumeFeedback'; // Add this import

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<RegisterForm />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/password-reset" element={<PasswordResetRequest />} />
          <Route path="/password-reset-confirm" element={<PasswordResetConfirm />} />
          <Route path="/upload-resume" element={<ResumeUpload />} />
          <Route path="/resume-feedback" element={<ResumeFeedback />} /> {/* Add this route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;