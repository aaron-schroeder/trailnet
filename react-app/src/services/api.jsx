// src/services/api.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL || 'http://localhost:8000/postgis/';

export const getTrailSegments = async () => {
    const response = await axios.get(`${API_URL}trail-segments/`);
    console.log('Full response: ', response);
    console.log('Data: ', response.data)
    return response.data;
};

// export const createTrailSegment = async (segment) => {
//     const response = await axios.post(`${API_URL}trail-segments/`, segment);
//     return response.data;
// };

export const getRoutes = async () => {
    const response = await axios.get(`${API_URL}routes/`);
    return response.data;
};

// export const createRoute = async (route) => {
//     const response = await axios.post(`${API_URL}routes/`, route);
//     return response.data;
// };
