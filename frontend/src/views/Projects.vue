<template>
  <div class="projects-container">
    <!-- Header Section -->
    <section class="projects-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="page-title">Projects</h1>
          <p class="page-subtitle">Manage your Ansible project repositories</p>
        </div>
        <button 
          @click="openCreateModal" 
          class="btn-primary"
          :disabled="loading"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          New Project
        </button>
      </div>
    </section>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-error">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
      </svg>
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading && projects.length === 0" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading projects...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && projects.length === 0" class="empty-state">
      <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
      </svg>
      <h3>No projects yet</h3>
      <p>Create your first project to get started with Ansible automation</p>
      <button @click="openCreateModal" class="btn-primary">
        Create Project
      </button>
    </div>

    <!-- Projects Grid -->
    <div v-else class="projects-grid">
      <div v-for="project in projects" :key="project.id" class="project-card">
        <div class="project-header">
          <div class="project-info">
            <h3 class="project-name">{{ project.name }}</h3>
            <p class="project-description">{{ project.description || 'No description' }}</p>
          </div>
          <div class="project-status">
            <span :class="['status-badge', getStatusClass(project.status)]">
              {{ project.status }}
            </span>
          </div>
        </div>

        <div class="project-details">
          <div class="detail-item">
            <span class="detail-label">Repository:</span>
            <a :href="project.git_url" target="_blank" class="detail-value link">
              {{ project.git_url }}
            </a>
          </div>
          <div class="detail-item">
            <span class="detail-label">Branch:</span>
            <span class="detail-value">{{ project.branch }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Created:</span>
            <span class="detail-value">{{ formatDate(project.created_at) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Last Sync:</span>
            <span class="detail-value">{{ formatDate(project.last_sync) }}</span>
          </div>
        </div>

        <div class="project-actions">
          <button 
            @click="syncProject(project)" 
            class="btn-secondary"
            :disabled="syncingProjects.has(project.id) || loading"
          >
            <svg v-if="syncingProjects.has(project.id)" class="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            {{ syncingProjects.has(project.id) ? 'Syncing...' : 'Sync' }}
          </button>
          <button @click="openEditModal(project)" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
            Edit
          </button>
          <button @click="deleteProject(project)" class="btn-danger">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ modalTitle }}</h2>
          <button @click="closeModal" class="modal-close">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveProject" class="modal-form">
          <div class="form-group">
            <label for="name" class="form-label">Project Name *</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              class="form-input"
              placeholder="Enter project name"
              required
            />
          </div>

          <div class="form-group">
            <label for="description" class="form-label">Description</label>
            <textarea
              id="description"
              v-model="form.description"
              class="form-textarea"
              placeholder="Enter project description"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="git_url" class="form-label">Git Repository URL *</label>
            <input
              id="git_url"
              v-model="form.git_url"
              type="url"
              class="form-input"
              placeholder="https://github.com/username/repository.git"
              required
            />
          </div>

          <div class="form-group">
            <label for="branch" class="form-label">Branch</label>
            <input
              id="branch"
              v-model="form.branch"
              type="text"
              class="form-input"
              placeholder="main"
            />
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary" :disabled="loading">
              <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Saving...' : (isEditing ? 'Update Project' : 'Create Project') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { projectService } from '@/services/projectService'

const projects = ref([])
const loading = ref(false)
const error = ref('')
const showModal = ref(false)
const editingProject = ref(null)
const syncingProjects = ref(new Set())

// Form data
const form = ref({
  name: '',
  description: '',
  git_url: '',
  branch: 'main'
})

// Computed properties
const isEditing = computed(() => editingProject.value !== null)
const modalTitle = computed(() => isEditing.value ? 'Edit Project' : 'Create New Project')

// Load projects
const loadProjects = async () => {
  loading.value = true
  error.value = ''
  try {
    projects.value = await projectService.getProjects()
  } catch (err) {
    error.value = 'Failed to load projects. Please try again.'
    console.error('Error loading projects:', err)
  } finally {
    loading.value = false
  }
}

// Open modal for creating new project
const openCreateModal = () => {
  editingProject.value = null
  form.value = {
    name: '',
    description: '',
    git_url: '',
    branch: 'main'
  }
  showModal.value = true
}

// Open modal for editing project
const openEditModal = (project) => {
  editingProject.value = project
  form.value = {
    name: project.name,
    description: project.description,
    git_url: project.git_url,
    branch: project.branch
  }
  showModal.value = true
}

// Close modal
const closeModal = () => {
  showModal.value = false
  editingProject.value = null
  form.value = {
    name: '',
    description: '',
    git_url: '',
    branch: 'main'
  }
}

// Save project (create or update)
const saveProject = async () => {
  if (!form.value.name || !form.value.git_url) {
    error.value = 'Please fill in all required fields'
    return
  }

  loading.value = true
  error.value = ''
  
  try {
    if (isEditing.value) {
      await projectService.updateProject(editingProject.value.id, form.value)
    } else {
      await projectService.createProject(form.value)
    }
    
    await loadProjects()
    closeModal()
  } catch (err) {
    error.value = `Failed to ${isEditing.value ? 'update' : 'create'} project. Please try again.`
    console.error('Error saving project:', err)
  } finally {
    loading.value = false
  }
}

// Delete project
const deleteProject = async (project) => {
  if (!confirm(`Are you sure you want to delete "${project.name}"? This action cannot be undone.`)) {
    return
  }

  loading.value = true
  error.value = ''
  
  try {
    await projectService.deleteProject(project.id)
    await loadProjects()
  } catch (err) {
    error.value = 'Failed to delete project. Please try again.'
    console.error('Error deleting project:', err)
  } finally {
    loading.value = false
  }
}

// Sync project with Git repository
const syncProject = async (project) => {
  syncingProjects.value.add(project.id)
  error.value = ''
  
  try {
    const result = await projectService.syncProject(project.id)
    if (result.status === 'success') {
      await loadProjects() // Reload to get updated status
    } else {
      error.value = `Sync failed: ${result.message}`
    }
  } catch (err) {
    error.value = 'Failed to sync project. Please try again.'
    console.error('Error syncing project:', err)
  } finally {
    syncingProjects.value.delete(project.id)
  }
}

// Format date
const formatDate = (dateString) => {
  if (!dateString) return 'Never'
  return new Date(dateString).toLocaleString()
}

// Get status badge class
const getStatusClass = (status) => {
  switch (status) {
    case 'active': return 'bg-green-100 text-green-800'
    case 'syncing': return 'bg-yellow-100 text-yellow-800'
    case 'error': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

// Load projects on component mount
onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
}

/* Header */
.projects-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.header-content {
  flex: 1;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.section-description {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #e9ecef;
}

.btn-secondary:hover {
  background: #e9ecef;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-icon-small {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.btn-icon-small:hover {
  background: #e9ecef;
  transform: scale(1.1);
}

.btn-icon-small.btn-danger:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.btn-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Projects Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
}

.project-card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.project-header {
  padding: 1.5rem 1.5rem 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.project-info {
  flex: 1;
}

.project-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.project-description {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.project-actions {
  display: flex;
  gap: 0.5rem;
}

.project-details {
  padding: 0 1.5rem 1rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #666;
  min-width: 80px;
}

.detail-value {
  font-size: 0.9rem;
  color: #333;
}

.repo-link {
  color: #667eea;
  text-decoration: none;
  word-break: break-all;
}

.repo-link:hover {
  text-decoration: underline;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-syncing {
  background: rgba(255, 193, 7, 0.1);
  color: #f57c00;
}

.status-error {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.project-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-date {
  color: #666;
  font-size: 0.8rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.empty-state p {
  margin-bottom: 2rem;
  font-size: 1rem;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.loading-spinner {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 1s linear infinite;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #666;
}

.modal-close:hover {
  background: #e9ecef;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

/* Form Elements */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

/* Alerts */
.alert {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.alert-error {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
  color: #721c24;
}

.alert-success {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
  color: #155724;
}

.alert-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .projects-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .project-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .project-actions {
    align-self: flex-end;
  }
  
  .modal-content {
    margin: 1rem;
    max-width: none;
  }
}
</style>