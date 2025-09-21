<template>
  <div class="home-container">
    <!-- Navigation Header -->
    <nav class="navbar">
      <div class="nav-brand">
        <h1 class="brand-title">🚀 Ansible AAP</h1>
      </div>
      <div class="nav-actions">
        <div class="user-info">
          <span class="welcome-text">Welcome back!</span>
        </div>
        <button @click="handleLogout" class="logout-button">
          <i class="logout-icon">🚪</i>
          Logout
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-menu">
          <div class="menu-item active" @click="activeTab = 'playbooks'">
            <i class="menu-icon">📋</i>
            <span>Playbooks</span>
          </div>
          <div class="menu-item" @click="activeTab = 'projects'">
            <i class="menu-icon">📁</i>
            <span>Projects</span>
          </div>
          <div class="menu-item" @click="activeTab = 'tasks'">
            <i class="menu-icon">⚡</i>
            <span>Tasks</span>
          </div>
        </div>
      </aside>

      <!-- Content Area -->
      <main class="content-area">
        <div class="content-header">
          <h2 class="content-title">
            {{ activeTab === 'playbooks' ? 'Playbook Management' : 
               activeTab === 'projects' ? 'Project Management' : 'Task History' }}
          </h2>
        </div>
        
        <div class="content-body">
          <Playbook v-if="activeTab === 'playbooks'" />
          <Projects v-else-if="activeTab === 'projects'" />
          <div v-else class="coming-soon">
            <h3>Task History</h3>
            <p>Coming soon...</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import Playbook from './Playbook.vue';
import Projects from './Projects.vue';

const authStore = useAuthStore();
const router = useRouter();
const activeTab = ref('playbooks');

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Navigation */
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-brand .brand-title {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info .welcome-text {
  color: #666;
  font-weight: 500;
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(45deg, #ff6b6b, #ee5a52);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.logout-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.logout-icon {
  font-size: 1.2rem;
}

/* Main Content Layout */
.main-content {
  display: flex;
  min-height: calc(100vh - 80px);
}

/* Sidebar */
.sidebar {
  width: 250px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem 0;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0 1rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(5px);
}

.menu-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
}

.menu-icon {
  font-size: 1.2rem;
}

/* Content Area */
.content-area {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.content-header {
  margin-bottom: 2rem;
}

.content-title {
  color: white;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.content-body {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.coming-soon {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.coming-soon h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }
  
  .nav-brand .brand-title {
    font-size: 1.5rem;
  }
  
  .main-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    padding: 1rem 0;
  }
  
  .sidebar-menu {
    flex-direction: row;
    overflow-x: auto;
    padding: 0 1rem;
  }
  
  .menu-item {
    min-width: 120px;
    justify-content: center;
  }
  
  .content-area {
    padding: 1rem;
  }
}
</style>

<script>
export default {
  name: 'Home'
}
</script>