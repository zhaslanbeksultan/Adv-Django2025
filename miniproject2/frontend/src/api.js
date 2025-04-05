import axios from 'axios';

const API_URL = 'http://localhost:8000/';

const getAuthHeaders = () => {
  const tokens = JSON.parse(localStorage.getItem('tokens') || '{}');
  return { Authorization: `Bearer ${tokens.access}` };
};

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}auth/register/`, userData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const verifyEmail = async (token) => {
  try {
    const response = await axios.get(`${API_URL}auth/verify-email/?token=${token}`);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}auth/login/`, credentials);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const requestPasswordReset = async (email) => {
  try {
    const response = await axios.post(`${API_URL}auth/password-reset/`, { email });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const confirmPasswordReset = async (data) => {
  try {
    const response = await axios.post(`${API_URL}auth/password-reset-confirm/`, data);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const uploadResume = async (formData) => {
  try {
    const response = await axios.post(`${API_URL}resumes/upload/`, formData, {
      headers: { ...getAuthHeaders(), 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    throw error.response.data || error.message;
  }
};