# 部署和使用文档

本文档介绍了如何部署和使用此应用程序，以及如何利用 Ansible playbook 进行自动化管理。

## 1. 先决条件

在开始之前，请确保您的系统上已安装以下软件：

*   **Docker 和 Docker Compose**: 用于容器化和运行应用程序。
*   **Ansible**: 用于执行自动化 playbook。

## 2. 部署应用程序

应用程序的部署通过主 Ansible playbook `ansible/playbook.yml` 完成。

1.  打开终端并导航到项目的根目录 `ansible_aap`。
2.  运行以下命令来部署或更新应用程序：

    ```bash
    ansible-playbook ansible/playbook.yml
    ```

此 playbook 将会：
*   从代码库拉取最新的代码。
*   构建或拉取 Docker 镜像。
*   启动应用程序容器。

## 3. 使用 Ansible Playbooks

项目包含多个用于不同管理任务的 Ansible playbook。所有 playbook 都应从项目根目录运行。

### 3.1 备份应用程序数据

要备份应用程序数据，请运行以下命令：

```bash
ansible-playbook ansible/backup.yml
```

此 playbook 会在 `ansible` 目录下创建一个名为 `backup.tar.gz` 的备份文件。

### 3.2 恢复应用程序数据

要从备份中恢复应用程序数据，请运行以下命令：

```bash
ansible-playbook ansible/restore.yml
```

此 playbook 将使用 `ansible/backup.tar.gz` 文件来恢复数据。

### 3.3 监控应用程序

要检查应用程序容器的运行状态，请运行以下命令：

```bash
ansible-playbook ansible/monitoring.yml
```

如果任何容器未运行，playbook 将会打印一条警报消息。您可以修改此 playbook 以集成真正的警报系统，如电子邮件或 Slack。

### 3.4 扩展应用程序

要手动扩展应用程序的实例数，请运行以下命令：

```bash
ansible-playbook ansible/scaling.yml
```

您可以编辑 `ansible/scaling.yml` 文件中的 `api_replicas` 和 `frontend_replicas` 变量来调整所需的副本数量。为了实现真正的高可用性，您需要在此 playbook 的基础上集成一个负载均衡器。

### 3.5 收集日志

要从所有应用程序容器中收集日志，请运行以下命令：

```bash
ansible-playbook ansible/logging.yml
```

此 playbook 会将日志保存到 `ansible` 目录下的一个文件中。您可以修改此 playbook 以将日志发送到集中式日志记录系统（如 ELK 或 Splunk）。

### 3.6 生成文档

要为已安装的 Ansible 集合生成文档，请运行以下命令：

```bash
ansible-playbook ansible/documentation.yml
```

这将在 `ansible` 目录中创建一个 `documentation.md` 文件。

## 4. CI/CD

项目包含一个位于 `.github/workflows/ci.yml` 的 GitHub Actions 工作流。此工作流会在每次推送到 `main` 分支时自动运行。

该工作流会执行以下操作：

1.  **代码检查**: 检查代码是否存在语法错误。
2.  **运行测试**: （如果配置了测试）运行自动化测试。
3.  **构建镜像**: 构建 Docker 镜像。
4.  **部署**: （如果配置了部署）将应用程序部署到服务器。

---