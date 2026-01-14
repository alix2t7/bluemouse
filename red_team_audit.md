# 🛡️ BlueMouse 紅隊審計：端到端使用者旅程擬真

本文檔詳細記錄了開發者與終端使用者接觸「藍圖小老鼠」系統的兩條主要路徑，並作為紅隊攻擊測試的基礎場景。

---

## 🚪 正門：GitHub 開發者實戰旅程 (The Main Entrance)

此情境模擬一名軟體工程師 (DevOps) 如何整合 BlueMouse 核心。

1.  **Repo 探索**：使用者克隆倉庫後，查閱 `README.md` 與 `BlueMouse_v6.1_MASTER_ARCH.md`。
2.  **環境初始化**：執行 `setup_mcp.py` 並建立 `venv`。
3.  **核心調度**：執行 `run_standalone.py` 啟動 CLI 模式。
4.  **需求碰撞**：使用者輸入需求（例如：`建立一個電商後台`）。
5.  **蘇格拉底攻防**：系統識別場景，跳出關鍵問題（如：如何處理超賣？）。使用者在此階段透過選擇方案與系統達成「架構共識」。
6.  **代碼具現化**：系統啟動 `antigravity_code_generator`，經過 17 層 AST 物理驗證後產出安全代碼。

## 🚪 側門：MCP AI 代理生態旅程 (The Side Entrance)

此情境模擬使用者透過 Cursor, Windsurf 或 Antigravity 使用 BlueMouse 提供的 MCP 工具。

1.  **MCP 接入**：使用者在 Cursor/Windsurf 的 `mcp_config.json` 中添加 BlueMouse MCP Server 路徑。
2.  **自然語言召喚**：使用者在聊天視窗輸入：`@BlueMouse 幫我分析並驗證這段 Django 代碼的安全性`。
3.  **工具觸發**：AI 代理自動調用 `mmla_validate_code` 或 `generate_socratic_questions`。
4.  **秘密掃描**：BlueMouse 透過 `validation_17_layers.py` 對使用者工作區代碼進行靜態掃描，檢出寫死的密鑰並回傳給 AI 代理。
5.  **修復循環**：AI 代理根據 BlueMouse 的報錯與建議，自動修正代碼。

---

## 🚩 紅隊測試場景 (攻擊向量)

| 攻擊目標 | 測試動作 (Attack Vector) | 預期防禦行為 |
| :--- | :--- | :--- |
| **輸入層** | 輸入完全無關的垃圾字串（如：`asdfghjkl`）或超長 Payload。 | 觸發 Layer 4 保底規則或拒絕服務。 |
| **邏輯層** | 輸入惡意指令（指令注入或敏感字眼需求）。 | 安全掃描層 (L16) 自動攔截危險語法。 |
| **穩定層** | 在 MCP 環境中發起 100+ 併發工具調用。 | 多層 AI 降級機制確保系統不崩潰。 |
| **欺騙層** | 對蘇格拉底問題給出邏輯矛盾的答案。 | 系統應能識別並持續追問或給出風險警告。 |
