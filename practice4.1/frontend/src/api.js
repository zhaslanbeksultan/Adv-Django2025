import axios from 'axios';



const API_URL = 'http://127.0.0.1:8000/api/items/';



export const getItems = async () => {

    const response = await axios.get(API_URL);

    return response.data;

};



export const createItem = async (item) => {

    const response = await axios.post(API_URL, item);

    return response.data;

};