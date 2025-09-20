```text
+-----------------+
|     Start       |
+--------+--------+
         |
         v
+--------+--------+
| User Login      |
| (Input Creds)   |
+--------+--------+
         |
         v
+--------+--------+
| Authenticate    |
| (Backend)       |
+--------+--------+
    |       |
    |       v
    |  +----+----+
    |  | Auth Fail |
    |  +----+----+
    v
+--------+--------+
| Auth Success    |
| (Get JWT)       |
+--------+--------+
         |
         v
+--------+--------+
| View Projects   |
| (Select Project)|
+--------+--------+
         |
         v
+--------+--------+
| Select Playbook |
| (Configure Task)|
+--------+--------+
         |
         v
+--------+--------+
| Launch Task     |
| (Backend API)   |
+--------+--------+
         |
         v
+--------+--------+
| Task Queued     |
| (Return Task ID)|
+--------+--------+
         |
         v
+--------+--------+
| Task Executor   |
| (Run Ansible)   |
+--------+--------+
         |
         v
+--------+--------+
| Stream Output   |
| (Real-time Log) |
+--------+--------+
         |
         v
+--------+--------+
| Task Complete   |
| (Update Status) |
+--------+--------+
         |
         v
+--------+--------+
| Display Results |
| (Frontend)      |
+--------+--------+
         |
         v
+--------+--------+
|      End        |
+-----------------+
```