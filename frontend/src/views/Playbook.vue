<template>
  <div class="playbook-container">
    <!-- Header Section -->
    <div class="playbook-header">
      <div class="header-content">
        <h3 class="section-title">🎭 Playbook Execution</h3>
        <p class="section-description">Select and execute Ansible playbooks with real-time monitoring</p>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-error">
      <div class="alert-icon">⚠️</div>
      <div class="alert-content">
        <strong>Error:</strong> {{ error }}
      </div>
    </div>

    <!-- Playbook Selection Card -->
    <div class="card playbook-selection-card">
      <div class="card-header">
        <h4 class="card-title">📋 Select Playbook</h4>
      </div>
      <div class="card-body">
        <div class="form-group">
          <label for="playbook-select" class="form-label">Available Playbooks:</label>
          <div class="select-wrapper">
            <select 
              id="playbook-select"
              v-model="selectedPlaybook" 
              class="form-select"
              :disabled="isRunning"
            >
              <option value="">Choose a playbook...</option>
              <option 
                v-for="playbook in playbooks" 
                :key="playbook" 
                :value="playbook"
              >
                {{ playbook }}
              </option>
            </select>
            <div class="select-arrow">▼</div>
          </div>
        </div>
        
        <button 
          @click="runPlaybook" 
          :disabled="!selectedPlaybook || isRunning"
          class="btn btn-primary"
        >
          <span v-if="isRunning" class="btn-spinner">⏳</span>
          <span v-else class="btn-icon">🚀</span>
          {{ isRunning ? 'Running...' : 'Execute Playbook' }}
        </button>
      </div>
    </div>

    <!-- Task Status Card -->
    <div v-if="taskId" class="card task-status-card">
      <div class="card-header">
        <h4 class="card-title">⚡ Task Status</h4>
        <div class="status-badge" :class="statusClass">
          <div class="status-indicator"></div>
          {{ taskStatus }}
        </div>
      </div>
      <div class="card-body">
        <div class="task-info">
          <div class="info-item">
            <span class="info-label">Task ID:</span>
            <code class="info-value">{{ taskId }}</code>
          </div>
          <div class="info-item">
            <span class="info-label">Playbook:</span>
            <span class="info-value">{{ selectedPlaybook }}</span>
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-container">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :class="progressClass"
              :style="{ width: progressWidth }"
            ></div>
          </div>
          <span class="progress-text">{{ progressText }}</span>
        </div>

        <!-- Task Output -->
        <div v-if="taskOutput" class="task-output">
          <h5 class="output-title">📄 Output:</h5>
          <pre class="output-content">{{ taskOutput }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { playbookService } from '@/services/playbook';

const playbooks = ref([]);
const selectedPlaybook = ref('');
const taskId = ref('');
const taskStatus = ref('');
const taskOutput = ref('');
const error = ref('');
const isRunning = ref(false);

// Computed properties for UI states
const statusClass = computed(() => {
  switch (taskStatus.value) {
    case 'running': return 'status-running';
    case 'completed': return 'status-completed';
    case 'failed': return 'status-failed';
    default: return 'status-pending';
  }
});

const progressClass = computed(() => {
  switch (taskStatus.value) {
    case 'running': return 'progress-running';
    case 'completed': return 'progress-completed';
    case 'failed': return 'progress-failed';
    default: return 'progress-pending';
  }
});

const progressWidth = computed(() => {
  switch (taskStatus.value) {
    case 'running': return '50%';
    case 'completed': return '100%';
    case 'failed': return '100%';
    default: return '0%';
  }
});

const progressText = computed(() => {
  switch (taskStatus.value) {
    case 'running': return 'Executing...';
    case 'completed': return 'Completed successfully';
    case 'failed': return 'Execution failed';
    default: return 'Ready to start';
  }
});

onMounted(async () => {
  try {
    const response = await playbookService.getPlaybooks();
    playbooks.value = response.playbooks || [];
  } catch (err) {
    error.value = 'Failed to load playbooks';
  }
});

const runPlaybook = async () => {
  if (!selectedPlaybook.value) return;
  
  try {
    error.value = '';
    isRunning.value = true;
    const response = await playbookService.runPlaybook(selectedPlaybook.value);
    taskId.value = response.task_id;
    taskStatus.value = 'running';
    
    // Poll for status
    pollTaskStatus();
  } catch (err) {
    error.value = 'Failed to run playbook';
    isRunning.value = false;
  }
};

const pollTaskStatus = async () => {
  try {
    const status = await playbookService.getTaskStatus(taskId.value);
    taskStatus.value = status.status;
    taskOutput.value = status.output || '';
    
    if (status.status === 'running') {
      setTimeout(pollTaskStatus, 2000);
    } else {
      isRunning.value = false;
    }
  } catch (err) {
    error.value = 'Failed to get task status';
    isRunning.value = false;
  }
};
</script>

<style scoped>
.playbook-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0;
}

/* Header */
.playbook-header {
  margin-bottom: 2rem;
}

.header-content {
  text-align: center;
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

/* Cards */
.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.card-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
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

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  transition: all 0.3s ease;
  appearance: none;
}

.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-select:disabled {
  background: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  pointer-events: none;
  font-size: 0.8rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Status Badge */
.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-pending {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
}

.status-pending .status-indicator {
  background: #6c757d;
}

.status-running {
  background: rgba(255, 193, 7, 0.1);
  color: #f57c00;
}

.status-running .status-indicator {
  background: #f57c00;
  animation: pulse 1.5s ease-in-out infinite;
}

.status-completed {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.status-completed .status-indicator {
  background: #28a745;
}

.status-failed {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.status-failed .status-indicator {
  background: #dc3545;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Task Info */
.task-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 0.95rem;
  color: #333;
}

.info-value code {
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.85rem;
}

/* Progress Bar */
.progress-container {
  margin-bottom: 1.5rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-pending {
  background: #6c757d;
}

.progress-running {
  background: linear-gradient(45deg, #f57c00, #ff9800);
  animation: shimmer 1.5s ease-in-out infinite;
}

.progress-completed {
  background: linear-gradient(45deg, #28a745, #20c997);
}

.progress-failed {
  background: linear-gradient(45deg, #dc3545, #e74c3c);
}

@keyframes shimmer {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.progress-text {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

/* Task Output */
.task-output {
  border-top: 1px solid #e9ecef;
  padding-top: 1.5rem;
}

.output-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 1rem 0;
}

.output-content {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.85rem;
  line-height: 1.5;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
  margin: 0;
}

/* Alert */
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

.alert-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .task-info {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>