import axios from 'axios';

const API_URL = 'http://localhost:8000/auth/';

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}register/`, userData);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const verifyEmail = async (token) => {
  try {
    const response = await axios.get(`${API_URL}verify-email/?token=${token}`);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}login/`, credentials);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const requestPasswordReset = async (email) => {
  try {
    const response = await axios.post(`${API_URL}password-reset/`, { email });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const confirmPasswordReset = async (data) => {
  try {
    const response = await axios.post(`${API_URL}password-reset-confirm/`, data);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};