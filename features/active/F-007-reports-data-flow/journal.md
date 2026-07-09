# F-007 reports-data-flow

## LOOP 日志

### Iteration 0

1. 这轮做什么？
   - 创建 Feature Workspace。
2. 改了什么？
   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。
3. 怎么验证？
   - 关闭前运行 gpcf_check_evidence.py。
4. 发现什么问题？
   - none
5. 是否可以提交？
   - 否，Evidence Gate 仍待验证。

### Iteration 1

1. 这轮做什么？
   - Planner 执行 runtime 调度。
2. 改了什么？
   - Planner -> Builder；status=implement
3. 怎么验证？
   - runtime/queue.json 与 runtime/state.json。
4. 发现什么问题？
   - 未发现调度阻塞项。
5. 是否可以提交？
   - 否，commit/push 仍需明确授权。

### Iteration 2

1. 这轮做什么？
   - 采集本地可回放证据。
2. 改了什么？
   - 更新 evidence 文件和 feature.yaml 证据状态。
3. 怎么验证？
   - 运行工作区 validator、py_compile、git diff --check 和范围证据门禁。
4. 发现什么问题？
   - 未发现阻塞项。
5. 是否可以提交？
   - 是，前提是 close gate 通过。

### Iteration 3

1. 这轮做什么？
   - Recorder 执行 runtime 调度。
2. 改了什么？
   - Recorder -> Recorder；status=commit
3. 怎么验证？
   - tests=pass build=pass screenshots=waived api=waived summary=pass
4. 发现什么问题？
   - 未发现调度阻塞项。
5. 是否可以提交？
   - 否，commit/push 仍需明确授权。
