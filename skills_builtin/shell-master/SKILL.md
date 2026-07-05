# shell-master

## Description
Shell脚本自动化——安全执行系统管理任务、生成跨平台脚本、批量操作。

## Instructions

1. 分析任务需求，确认无安全风险
2. 生成跨平台Shell脚本（Bash/PowerShell兼容）
3. 自动添加安全检查和错误处理：
   - 前置条件检查
   - 失败时回滚
   - 操作日志记录
4. 提供dry-run模式预览影响
5. 对批量操作添加进度条

## Safety Rules
- 禁止 `rm -rf /` 等破坏性命令
- 禁止修改系统关键文件
- 所有操作默认先在临时目录测试
- 危险操作必须添加 `--confirm` 参数

## Compatible Agents
- claude-code
