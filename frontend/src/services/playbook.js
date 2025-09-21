import { useAuthStore } from '@/store/auth';

const BASE_URL = '/api/v1';

const request = async (url, options = {}) => {
  const authStore = useAuthStore();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (authStore.isAuthenticated) {
    headers['Authorization'] = `Bearer ${authStore.token}`;
  }

  const response = await fetch(`${BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error('API request failed');
  }

  return response.json();
};

export const playbookService = {
  getPlaybooks() {
    return request('/playbooks');
  },

  runPlaybook(playbookName, data) {
    return request(`/playbooks/${playbookName}/run`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getTaskResult(taskId) {
    return request(`/tasks/${taskId}`);
  },
};

export default playbookService;