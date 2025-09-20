import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  createTask() {
    return apiClient.post('/tasks');
  },
  getTask(taskId) {
    return apiClient.get(`/tasks/${taskId}`);
  }
};