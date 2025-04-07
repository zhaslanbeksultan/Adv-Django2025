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
    // Store tokens and user separately
    localStorage.setItem('tokens', JSON.stringify(response.data.tokens));
    localStorage.setItem('user', JSON.stringify({ username: response.data.username }));
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
  const headers = { ...getAuthHeaders(), 'Content-Type': 'multipart/form-data' };
  console.log('Headers being sent:', headers);
  try {
    const response = await axios.post(`${API_URL}resumes/upload/`, formData, { headers });
    return response.data;
  } catch (error) {
    console.log('Error response:', error.response);
    throw error.response.data || error.message;
  }
};

export const getJobList = async () => {
  try {
    const response = await axios.get(`${API_URL}jobs/`);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const createJob = async (jobData) => {
  const headers = getAuthHeaders();
  try {
    const response = await axios.post(`${API_URL}jobs/create/`, jobData, { headers });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const updateJob = async (jobId, jobData) => {
  const headers = getAuthHeaders();
  try {
    const response = await axios.put(`${API_URL}jobs/${jobId}/update/`, jobData, { headers });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const deleteJob = async (jobId) => {
  const headers = getAuthHeaders();
  try {
    const response = await axios.delete(`${API_URL}jobs/${jobId}/delete/`, { headers });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getJobRecommendations = async () => {
  const headers = getAuthHeaders();
  try {
    const response = await axios.get(`${API_URL}jobs/recommendations/`, { headers });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};