import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegisterForm from './components/RegisterForm';
import VerifyEmail from './components/VerifyEmail';
import Login from './components/Login';
import PasswordResetRequest from './components/PasswordResetRequest';
import PasswordResetConfirm from './components/PasswordResetConfirm';

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
        </Routes>
      </div>
    </Router>
  );
}

export default App;