<template>
  <div class="ansible-runner">
    <h2>Ansible Playbook Runner</h2>
    
    <!-- Section to display available playbooks -->
    <div class="playbook-list">
      <h3>Available Playbooks</h3>
      <ul>
        <!-- Loop through the playbooks array and display each one -->
        <li v-for="playbook in playbooks" :key="playbook">
          {{ playbook }}
          <!-- Button to trigger playbook execution -->
          <button @click="runPlaybook(playbook)" :disabled="runningPlaybook === playbook">Run</button>
        </li>
      </ul>
    </div>

    <!-- Section to display the status of a running playbook -->
    <div v-if="runningPlaybook" class="task-status">
      <h3>Running: {{ runningPlaybook }}</h3>
      <p>Status: {{ taskStatus }}</p>
      <!-- Display the task result when available -->
      <pre v-if="taskResult">{{ taskResult }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      playbooks: [], // Holds the list of available playbooks
      runningPlaybook: null, // The name of the playbook currently being executed
      taskStatus: null, // The status of the current task (e.g., 'running', 'success', 'error')
      taskResult: null, // The detailed result of the completed task
      pollingInterval: null, // Holds the interval ID for polling task status
    };
  },
  /**
   * When the component is created, fetch the list of available playbooks.
   */
  created() {
    this.fetchPlaybooks();
  },
  methods: {
    /**
     * Fetches the list of available playbooks from the API.
     */
    async fetchPlaybooks() {
      try {
        const response = await axios.get('/api/v1/playbooks');
        this.playbooks = response.data.playbooks;
      } catch (error) {
        console.error('Error fetching playbooks:', error);
      }
    },
    /**
     * Starts the execution of a selected playbook.
     * @param {string} playbookName - The name of the playbook to run.
     */
    async runPlaybook(playbookName) {
      // Set the UI to a running state
      this.runningPlaybook = playbookName;
      this.taskStatus = 'running';
      this.taskResult = null;

      try {
        // Make the API call to start the playbook execution
        const response = await axios.post(`/api/v1/playbooks/${playbookName}/run`);
        const taskId = response.data.task_id;
        // Start polling for the task status
        this.pollTaskStatus(taskId);
      } catch (error) {
        console.error(`Error running playbook ${playbookName}:`, error);
        this.taskStatus = 'error';
      }
    },
    /**
     * Polls the API for the status of a running task.
     * @param {string} taskId - The ID of the task to poll.
     */
    pollTaskStatus(taskId) {
      // Set up an interval to check the task status every 2 seconds
      this.pollingInterval = setInterval(async () => {
        try {
          const response = await axios.get(`/api/v1/tasks/${taskId}`);
          const task = response.data;
          this.taskStatus = task.status;

          // If the task is complete (success or error), stop polling
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
  /**
   * Before the component is unmounted, clear the polling interval
   * to prevent memory leaks.
   */
  beforeUnmount() {
    clearInterval(this.pollingInterval);
  },
};
</script>

<style scoped>
/* Scoped styles for the AnsibleRunner component */
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