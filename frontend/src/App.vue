<template>
  <el-container style="height: 100vh;">
    <el-header style="background-color: #409EFF; color: white; display: flex; align-items: center; justify-content: center;">
      <h1>Ansible AAP</h1>
    </el-header>
    <el-main>
      <div v-if="isLoggedIn">
        <AnsibleRunner />
      </div>
      <Login v-else @login-success="handleLoginSuccess" />
    </el-main>
    <el-footer style="background-color: #f2f2f2; text-align: center; padding: 10px;">
      <p>© 2024 Ansible AAP</p>
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref } from 'vue';
import Login from './components/Login.vue';
import AnsibleRunner from './components/AnsibleRunner.vue';

const isLoggedIn = ref(true); // Hardcoded for now

const handleLoginSuccess = () => {
  isLoggedIn.value = true;
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>
