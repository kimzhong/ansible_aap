<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>Login</span>
        </div>
      </template>
      <el-form ref="loginForm" :model="loginData" :rules="loginRules" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="loginData.username" placeholder="Username" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginData.password" type="password" placeholder="Password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" style="width: 100%;">Login</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const loginData = ref({
  username: '',
  password: ''
});

const loginRules = {
  username: [{ required: true, message: 'Please input username', trigger: 'blur' }],
  password: [{ required: true, message: 'Please input password', trigger: 'blur' }]
};

const handleLogin = () => {
  console.log('Login attempt with:', loginData.value);
  // Here you would typically handle the login logic, e.g., call an API.
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.login-card {
  width: 400px;
}

.card-header {
  text-align: center;
  font-size: 20px;
}
</style>