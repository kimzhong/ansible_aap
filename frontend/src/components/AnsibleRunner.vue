<template>
  <div class="ansible-runner">
    <h2>Ansible Playbook Runner</h2>
    
    <div class="playbook-list">
      <h3>Available Playbooks</h3>
      <ul>
        <li v-for="playbook in playbooks" :key="playbook">
          {{ playbook }}
          <button @click="runPlaybook(playbook)" :disabled="runningPlaybook === playbook">Run</button>
        </li>
      </ul>
    </div>

    <div v-if="runningPlaybook" class="task-status">
      <h3>Running: {{ runningPlaybook }}</h3>
      <p>Status: {{ taskStatus }}</p>
      <pre v-if="taskResult">{{ taskResult }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      playbooks: [],
      runningPlaybook: null,
      taskStatus: null,
      taskResult: null,
      pollingInterval: null,
    };
  },
  created() {
    this.fetchPlaybooks();
  },
  methods: {
    async fetchPlaybooks() {
      try {
        const response = await axios.get('/api/v1/playbooks');
        this.playbooks = response.data.playbooks;
      } catch (error) {
        console.error('Error fetching playbooks:', error);
      }
    },
    async runPlaybook(playbookName) {
      this.runningPlaybook = playbookName;
      this.taskStatus = 'running';
      this.taskResult = null;

      try {
        const response = await axios.post(`/api/v1/playbooks/${playbookName}/run`);
        const taskId = response.data.task_id;
        this.pollTaskStatus(taskId);
      } catch (error) {
        console.error(`Error running playbook ${playbookName}:`, error);
        this.taskStatus = 'error';
      }
    },
    pollTaskStatus(taskId) {
      this.pollingInterval = setInterval(async () => {
        try {
          const response = await axios.get(`/api/v1/tasks/${taskId}`);
          const task = response.data;
          this.taskStatus = task.status;

          if (task.status === 'success' || task.status === 'error') {
            this.taskResult = task;
            clearInterval(this.pollingInterval);
          }
        } catch (error) {
          console.error(`Error fetching task status for ${taskId}:`, error);
          this.taskStatus = 'error';
          clearInterval(this.pollingInterval);
        }
      }, 2000); // Poll every 2 seconds
    },
  },
  beforeUnmount() {
    clearInterval(this.pollingInterval);
  },
};
</script>

<style scoped>
.ansible-runner {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.playbook-list ul {
  list-style: none;
  padding: 0;
}

.playbook-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
}

.task-status {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #eee;
  background-color: #f9f9f9;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>