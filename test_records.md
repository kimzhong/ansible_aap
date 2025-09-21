# Ansible AAP 测试记录

## 测试用例 1: 执行一个简单的 Ansible playbook

**ID:** TC-001
**描述:** 验证 `/api/v1/tasks` 端点是否可以成功接收一个简单的 playbook 和 inventory，执行它，并返回一个成功的 JSON 响应。

**前置条件:**
- FastAPI 服务器正在运行。
- WSL 已安装并配置了 `ansible` 和 `ansible-runner`。

**测试步骤:**
1.  向 `http://127.0.0.1:8000/api/v1/tasks` 发送一个 `POST` 请求。
2.  请求体应包含以下 JSON 数据：
    ```json
    {
        "inventory": "localhost ansible_connection=local",
        "playbook": "- hosts: localhost\n  tasks:\n    - name: Ping\n      ansible.builtin.ping:"
    }
    ```
3.  执行以下 PowerShell 命令来发送请求并保存响应：
    ```powershell
    $body = @{
        inventory = "localhost ansible_connection=local"
        playbook = "- hosts: localhost`n  tasks:`n    - name: Ping`n      ansible.builtin.ping:"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/tasks -Method Post -Body $body -ContentType "application/json" -Verbose

    $response | ConvertTo-Json -Depth 100 | Out-File -FilePath d:\ansible_aap\test_result.json

    Get-Content d:\ansible_aap\test_result.json
    ```

**预期结果:**
- 命令成功执行，退出码为 0。
- `test_result.json` 文件包含一个 JSON 对象。
- JSON 对象中的 `status` 字段为 `success`。
- JSON 对象中的 `data` 字段包含一个 `ping` 值为 `pong` 的响应。

**实际结果 (2025-09-20):**
- 测试通过。API 返回了预期的成功响应。

--- 

## 测试用例 2: 异步执行 Ansible playbook 并检索结果

**ID:** TC-002
**描述:** 验证 `/api/v1/tasks` 端点是否可以异步启动一个任务，并能通过 `/api/v1/tasks/{task_id}` 端点成功检索其结果。

**前置条件:**
- FastAPI 服务器正在运行。
- WSL 已安装并配置了 `ansible` 和 `ansible-runner`。

**测试步骤:**
1.  向 `http://127.0.0.1:8000/api/v1/tasks` 发送一个 `POST` 请求以启动一个新任务。
2.  从响应中获取 `task_id`。
3.  等待一段足够长的时间（例如 15 秒），以确保任务有足够的时间执行完成。
4.  使用 `task_id` 向 `http://127.0.0.1:8000/api/v1/tasks/{task_id}` 发送一个 `GET` 请求。
5.  执行以下 PowerShell 命令来发送请求并保存响应：
    ```powershell
    $body = @{
        inventory = "localhost ansible_connection=local"
        playbook = "- hosts: localhost`n  tasks:`n    - name: Ping`n      ansible.builtin.ping:"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/tasks -Method Post -Body $body -ContentType "application/json"

    $taskId = $response.task_id

    Start-Sleep -Seconds 15

    $result = Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/tasks/$taskId

    $result | ConvertTo-Json -Depth 100 | Out-File -FilePath d:\ansible_aap\test_result.json

    Get-Content d:\ansible_aap\test_result.json
    ```

**预期结果:**
- 第一个请求成功返回一个 `task_id`。
- 第二个请求成功返回一个 JSON 对象。
- JSON 对象中的 `status` 字段为 `success`。
- JSON 对象中的 `data` 字段包含一个 `ping` 值为 `pong` 的响应。

**实际结果 (2025-09-20):**
- 测试通过。API 成功地异步执行了任务并返回了预期的结果。

---

## 测试用例 3: 前端 Playbooks 加载和显示

**ID:** TC-003
**描述:** 验证前端应用是否能正确加载和显示可用的 Ansible playbooks。

**前置条件:**
- FastAPI 后端服务器正在运行 (http://localhost:8000)。
- Vue.js 前端应用正在运行 (http://localhost:5173)。
- ansible/ 目录包含多个 .yml playbook 文件。

**测试步骤:**
1. 打开浏览器访问 http://localhost:5173
2. 导航到 Playbook 页面
3. 观察 playbooks 下拉选择框的内容

**预期结果:**
- 页面成功加载，无错误信息
- playbooks 下拉选择框显示所有可用的 playbook 选项
- 每个 playbook 作为独立的选项显示（如：backup, documentation, logging 等）

**问题记录 (2025-01-22):**
- **问题:** 前端显示 "Failed to load playbooks" 错误
- **问题:** playbooks 显示为单个长字符串而不是独立选项

**问题分析:**
1. 后端 API `/api/v1/playbooks` 返回格式: `{"playbooks": ["backup", "documentation", ...]}`
2. 前端代码错误地将整个响应对象赋值给 `playbooks.value`
3. 应该提取 `response.playbooks` 数组

**解决方案:**
修改 `frontend/src/views/Playbook.vue` 中的 `onMounted` 函数:
```javascript
// 修改前 (错误)
playbooks.value = await playbookService.getPlaybooks();

// 修改后 (正确)
const response = await playbookService.getPlaybooks();
playbooks.value = response.playbooks || [];
```

**实际结果 (2025-01-22):**
- 问题已修复。前端现在正确显示所有可用的 playbook 选项。
- 每个 playbook 作为独立的下拉选项显示。
- 不再出现 "Failed to load playbooks" 错误。

---