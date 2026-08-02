# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（若有 L3）。

## ⏯️ 目前做到哪
需求訪談＋技能撰寫已完成，`exam-composer` 技能（`C:\Users\vm\.claude\skills\exam-composer\SKILL.md`）的 Step 0～5、功能五（篩選替換）、功能六（NotebookLM 整合）全部用真實資料端到端測試過一輪，全部測試通過（過程中抓到並修正了好幾個實作落差，見下方注意事項）。

## 🚦 目前狀態
- 技能本體已寫成且經過完整端到端測試，可以視為 MVP 完成。
- NotebookLM 已建立「命題成果筆記本」（https://notebooklm.google.com/notebook/a9f1f443-5ab7-4ac0-b5d9-345a9266863e），已加入通用參考資料 10 份＋這次測試的專屬來源 6 份。這台電腦的 NotebookLM CLI 現在是登入狀態（`auth_status: configured`）。
- `命題範圍三家出版商教材/` 有 4 份真實康軒教材（約183MB，已 gitignore）；`命題成果/115上_六年級_國語_第一次定期評量/` 有測試產出的設定摘要＋Word 試題卷＋教師解答卷（3題測試版，非正式完整考卷）。
- `光復108課綱歷年定期試題/` 資料夾維持空的，這是正常狀態（Step 4 改用即時截圖比對，不存檔）。

## ➡️ 下一步
1. SKILL.md 的 Step 4 文字敘述還沒同步「不需要存 PDF 進資料夾」這個修正，目前只有 agents.md 記錄了這個發現，下次要記得把 SKILL.md 原文也改掉。
2. Step 4 只測過 108-1 一份歷史考卷，正式使用前建議測試涵蓋 108~114 全部年度的比對流程是否順暢。
3. 若要正式讓某位命題教師使用，Step 1 需要把其餘六課（朱子治家格言選、談遇見更好的自己、臺灣美食詩選、最好的味覺禮物、珍珠奶茶、大小剛好的鞋子）也逐頁精讀，測試時只精讀了第一課「跑道」。
4. 若之後要用 Node.js 產生正式的 Word 試題卷/雙向細目表（不是這次的3題測試版），寫腳本時務必用 `path.join()` 組合含中文字元的檔案路徑，不要用字串相加＋反斜線（這次踩過這個坑，浪費不少時間排查）。

## ⚠️ 注意事項
- **Step A（出版社教材下載）是半自動**：Agent 只負責導航到正確頁面＋列出下載清單，實際點擊下載一定要使用者親手做（瀏覽器會限制/攔截非使用者親手觸發的下載）。
- **esa-exam-review 的兩個版本都已修正密碼規則**（`~/.codex/skills/esa-exam-review` 與 Claude Code 外掛版），改成使用者親自登入、Agent 不碰密碼。**這兩個檔案不在本專案 git repo 裡**，若有 chezmoi 同步 `~/.codex/skills` 記得手動 `chezmoi re-add`。
- **Step 4 查重不需要（也無法）把歷史 PDF 存進資料夾**，改用 `fetch` 轉 blob URL＋`window.open`＋截圖讀取內容，直接比對，不留檔案。
- **Node.js 寫入 GDrive 路徑檔案時，字串路徑組合的錯誤不會拋出例外，非常難排查**：這次用 `OUT_DIR + '\中文檔名.docx'`（少打一個反斜線）導致寫入失敗且無任何錯誤訊息，一度誤判成 Word 檔案鎖定或雲端同步問題，浪費不少來回才找到真因。以後一律用 `path.join()`。
- **NotebookLM 的 `label` 工具呼叫 `list` action 會觸發 AI 自動分類副作用**，可能把不相關的來源混進手動建立的標籤裡，且沒有「從標籤移除」的操作可以修正，之後應避免不必要呼叫。
- **`exam-composer` 技能檔在 `~/.claude/skills/exam-composer/`**，若有 chezmoi 同步 `~/.claude/skills` 記得 `chezmoi re-add`。
- 這次測試在 `命題範圍三家出版商教材/` 資料夾放的是真實康軒教材 PDF（有著作權），`.gitignore` 已排除，不會進版控，但確實存在於使用者的 GDrive 裡，不要誤刪。

## 🕐 最後更新
- 時間：2026-08-02
- 更新者：Claude Code @ DESKTOP-31QBU95
- Git push：待推
