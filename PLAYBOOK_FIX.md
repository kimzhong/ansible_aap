# Playbook 修复记录

## 问题描述
前端页面显示 "Failed to load playbooks" 错误，playbooks 显示为单个长字符串。

## 修复内容
1. 修复 frontend/src/views/Playbook.vue 中的数据处理逻辑
2. 更新相关文档

## 修复详情
- 后端 API 返回格式: `{"playbooks": ["backup", "documentation", ...]}`
- 前端需要提取 `response.playbooks` 数组而不是整个响应对象

## 修复代码
```javascript
// 修改前
playbooks.value = await playbookService.getPlaybooks();

// 修改后  
const response = await playbookService.getPlaybooks();
playbooks.value = response.playbooks || [];
```