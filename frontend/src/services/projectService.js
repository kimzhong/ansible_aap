import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const projectService = {
  // Get all projects
  async getProjects() {
    try {
      const response = await api.get('/projects/')
      return response.data
    } catch (error) {
      console.error('Error fetching projects:', error)
      throw error
    }
  },

  // Get project by ID
  async getProject(projectId) {
    try {
      const response = await api.get(`/projects/${projectId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching project:', error)
      throw error
    }
  },

  // Create new project
  async createProject(projectData) {
    try {
      const response = await api.post('/projects/', projectData)
      return response.data
    } catch (error) {
      console.error('Error creating project:', error)
      throw error
    }
  },

  // Update project
  async updateProject(projectId, projectData) {
    try {
      const response = await api.put(`/projects/${projectId}`, projectData)
      return response.data
    } catch (error) {
      console.error('Error updating project:', error)
      throw error
    }
  },

  // Delete project
  async deleteProject(projectId) {
    try {
      const response = await api.delete(`/projects/${projectId}`)
      return response.data
    } catch (error) {
      console.error('Error deleting project:', error)
      throw error
    }
  },

  // Sync project with Git repository
  async syncProject(projectId) {
    try {
      const response = await api.post(`/projects/${projectId}/sync`)
      return response.data
    } catch (error) {
      console.error('Error syncing project:', error)
      throw error
    }
  },

  // Get project playbooks
  async getProjectPlaybooks(projectId) {
    try {
      const response = await api.get(`/projects/${projectId}/playbooks`)
      return response.data
    } catch (error) {
      console.error('Error fetching project playbooks:', error)
      throw error
    }
  }
}

export default projectService