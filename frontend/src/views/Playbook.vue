<template>
  <div>
    <h2>Playbooks</h2>
    <div v-if="error">{{ error }}</div>
    <div v-if="playbooks.length">
      <select v-model="selectedPlaybook">
        <option disabled value="">Please select one</option>
        <option v-for="playbook in playbooks" :key="playbook" :value="playbook">
          {{ playbook }}
        </option>
      </select>
      <button @click="runPlaybook" :disabled="!selectedPlaybook || isLoading">
        {{ isLoading ? 'Running...' : 'Run Playbook' }}
      </button>
    </div>
    <div v-else>
      <p>No playbooks found.</p>
    </div>

    <div v-if="taskId">
      <h3>Task Status</h3>
      <p>Task ID: {{ taskId }}</p>
      <p>Status: {{ taskStatus }}</p>
      <pre v-if="taskResult">{{ taskResult }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import playbookService from '@/services/playbook'; 

const playbooks = ref([]);
const selectedPlaybook = ref('');
const error = ref(null);
const isLoading = ref(false);
const taskId = ref(null);
const taskStatus = ref(null);
const taskResult = ref(null);
let pollInterval = null;

onMounted(async () => {
  try {
    const response = await playbookService.listPlaybooks();
    playbooks.value = response.playbooks;
  } catch (err) {
    error.value = 'Failed to load playbooks.';
  }
});

const runPlaybook = async () => {
  if (!selectedPlaybook.value) return;
  isLoading.value = true;
  error.value = null;
  taskId.value = null;
  taskStatus.value = null;
  taskResult.value = null;

  try {
    const inventory = 'localhost,'; 
    const response = await playbookService.runPlaybook(selectedPlaybook.value, { inventory });
    taskId.value = response.task_id;
    pollTaskStatus();
  } catch (err) {
    error.value = 'Failed to run playbook.';
    isLoading.value = false;
  }
};

const pollTaskStatus = () => {
  pollInterval = setInterval(async () => {
    try {
      const result = await playbookService.getTaskResult(taskId.value);
      taskStatus.value = result.status;
      if (result.status === 'completed' || result.status === 'failed') {
        taskResult.value = result.data;
        isLoading.value = false;
        clearInterval(pollInterval);
      }
    } catch (err) {
      error.value = 'Failed to get task status.';
      isLoading.value = false;
      clearInterval(pollInterval);
    }
  }, 2000); 
};

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval);
  }
});
</script>