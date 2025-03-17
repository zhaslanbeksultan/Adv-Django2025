import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/items/';

export const getItems = async (token) => {
    const response = await axios.get(API_URL, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
};

export const createItem = async (item, token) => {
    const response = await axios.post(API_URL, item, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
};

export const deleteItem = async (id, token) => {
    await axios.delete(`${API_URL}${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
    });
};