# Ansible 管理平台设计文档

## 1. 系统架构

本平台采用前后端分离的微服务架构。

-   **前端**: 基于 Vue.js 和 Element-Plus 的单页应用 (SPA)，负责用户交互和数据展示。
-   **后端**: 基于 Python 和 FastAPI 的 RESTful API 服务，负责处理业务逻辑、执行 Ansible 任务和与数据库交互。
-   **数据库**: 使用 MongoDB 存储所有持久化数据，包括用户信息、项目配置、任务历史等。
-   **任务执行器**: 一个独立的模块（或集成在后端服务中），负责异步执行 Ansible Playbook，并通过消息队列或回调将结果返回给后端主服务。
-   **部署**: 整个平台将通过 Docker 和 Docker-Compose进行容器化部署。

```
+-----------------+      +-----------------+      +-----------------+
|   Web Browser   |----->|     Frontend    |----->|     Backend     |
| (Vue.js SPA)    |      | (Nginx)         |      | (FastAPI)       |
+-----------------+      +-----------------+      +-------+---------+
                                                          |
                                                          v
+-----------------+      +-----------------+      +-------+---------+
| Ansible Engine  |<-----| Task Executor   |----->|    MongoDB      |
+-----------------+      +-----------------+      +-----------------+

```

## 2. 模块设计

### 2.1. 后端模块

-   **`main.py`**: FastAPI 应用入口，配置路由和中间件。
-   **`api/`**: 存放所有 API endpoint 的定义。
    -   `auth.py`: 用户认证（登录、注册）。
    -   `users.py`: 用户管理 CRUD。
    -   `projects.py`: 项目管理 CRUD。
    -   `inventories.py`: Inventory 管理 CRUD。
    -   `tasks.py`: 任务执行和结果查询。
-   **`core/`**: 核心业务逻辑。
    -   `config.py`: 应用配置管理。
    -   `security.py`: 密码哈希、JWT令牌生成与验证。
-   **`db/`**: 数据库交互。
    -   `database.py`: 数据库连接和会话管理。
    -   `models.py`: MongoDB 的数据模型定义 (使用 Pydantic 或类似的库)。
    -   `crud.py`: 封装常用的数据库增删改查操作。
-   **`services/`**: 业务服务层。
    -   `ansible_runner.py`: 封装 Ansible 任务的执行逻辑，与 Ansible Engine 交互。

### 2.2. 前端模块

-   **`src/`**
    -   **`api/`**: 封装对后端 API 的请求。
    -   **`assets/`**: 存放静态资源，如图片、样式文件。
    -   **`components/`**: 可复用的 Vue 组件。
    -   **`layouts/`**: 页面布局组件。
    -   **`router/`**: Vue Router 的路由配置。
    -   **`store/`**: Pinia 或 Vuex 的状态管理。
    -   **`views/`**: 页面级组件。
        -   `Login.vue`: 登录页面，包含用户名和密码输入表单。
        -   `Home.vue`: 主页仪表盘，集成登出功能和 Playbook 执行界面。
        -   `Playbook.vue`: Playbook 执行页面，提供 Playbook 选择、运行和状态监控功能。
    -   **`services/`**: API 服务层。
        -   `playbook.js`: 封装 Playbook 相关的 API 调用（列出、运行、获取任务结果）。

## 3. API 设计

遵循 RESTful 设计原则，使用 JSON 作为数据交换格式。

-   **认证**: 使用 JWT (JSON Web Tokens) 进行无状态认证。
    -   `POST /api/v1/login`: 用户登录，成功后返回 JWT。
    -   `POST /api/v1/logout`: 用户登出（前端清除 JWT）。
-   **用户**: ` /api/v1/users`
-   **项目**: ` /api/v1/projects`
-   **Playbooks**: `/api/v1/playbooks`
    -   `GET /api/v1/playbooks`: 获取可用的 Playbook 列表。
    -   `POST /api/v1/playbooks/{playbook_name}/run`: 运行指定的 Playbook。
-   **任务**: ` /api/v1/tasks`
    -   `POST /api/v1/projects/{project_id}/launch`: 启动一个新任务。
    -   `GET /api/v1/tasks/{task_id}`: 获取任务状态和结果。

## 4. 数据库设计 (MongoDB)

使用集合 (Collections) 来存储不同类型的数据。

-   **`users`**: 存储用户信息。
    -   `{ "_id": ObjectId, "username": "admin", "hashed_password": "...", "role": "admin" }`
-   **`projects`**: 存储项目信息。
    -   `{ "_id": ObjectId, "name": "My Project", "git_url": "..." }`
-   **`inventories`**: 存储 Inventory 信息。
-   **`tasks`**: 存储任务执行的历史记录。
    -   `{ "_id": ObjectId, "project_id": ObjectId, "playbook": "site.yml", "status": "running", "output": "...", "start_time": ISODate, "end_time": ISODate }`