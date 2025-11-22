import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const dishAPI = {
  getAllDishes: async () => {
    const response = await axios.get(`${API_BASE_URL}/dishes`);
    return response.data;
  },

  toggleDishStatus: async (dishId) => {
    const response = await axios.patch(`${API_BASE_URL}/dishes/${dishId}/toggle`);
    return response.data;
  }
};
