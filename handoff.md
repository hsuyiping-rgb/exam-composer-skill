# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（若有 L3）。

## ⏯️ 目前做到哪

2026-09-07 在**第三台電腦** `DESKTOP-HJA3024`（`C:\Users\user`）開工。做了三件事：

1. **補環境**：這台原本三處全域 skills 目錄都沒有 `exam-composer`，已從 repo `skills/exam-composer/SKILL.md` 複製到 `~/.claude`／`~/.codex`／`~/.agents`，四份 SHA-256 均為 `63634399BDEAAE1A0019814517D8F943F48D8D506B519B71FF3CA708E786BB92`。
2. **推上次未推的 commit**：9/4 有兩個 commit（`370ee58` SKILL.md 兩版合併、`ef2cd68` Step 5 LibreOffice 說明）留在本地沒推，已補推。上一份 handoff 寫「Git push ✅」其實只涵蓋到 `eb22685`。
3. **五年級數學任務 Step 4 查重完成並結案**（本次主要工作，見下）。

**Step 4 查重結果**：108-1~114-1 共 7 個學年度全數取得，**逐份實際開啟、逐頁截圖判讀**。27 題中 18 題與歷屆相似——★ 接近原題重複 10 題、▲ 命題框架高度相似 8 題、△ 部分相似 9 題，**沒有一題是「未發現相似」**。經命題教師確認，採「只改 ★ 的 10 題，改寫時換命題角度而非只換數字」。第 2、3、4、6、7、8、16、19、21、23 題全數重寫，並再與 7 份逐題比對一次（第二輪查重）全部通過。

**同步更新的產出**：`查重報告.md`（新建）、`試題草稿.md`（10 題改寫＋逐題附改寫紀錄）、`正式試題卷.docx`／`教師解答卷.docx`（以 python-docx 就地編輯，保留原排版）、第 19 題圖重繪為 `images/q19_平行四邊形內角.png`（原不規則四邊形圖已刪）、`設定摘要.md` 流程狀態回填。**`雙向細目表.docx` 無須修改**——10 題改寫全部守住原題型／Bloom／單元格位。

## 🚦 目前狀態

- **`命題成果/115上_五年級_數學_第一次定期考察/` 已完成 Step 0～Step 5**，只剩**功能六 NotebookLM 歸檔**未做。
- ⚠️ **接手前必知**：`命題成果/` 在 `.gitignore` 內（校內試卷不進版控），所以**本次所有命題產出都不在 GitHub 上，只存在 GDrive**。換電腦接手時靠 GDrive 同步，不要以為 clone repo 就會有。
- ⚠️ **視覺渲染 QA 仍未完成**：DESKTOP-31QBU95、kfes、DESKTOP-HJA3024 **三台電腦都沒有 LibreOffice**。已改用 python-docx 做結構性 QA 並通過（10 個選擇題空白括號、7 幅圖齊備、答案列正確、無亂碼），但排版需請命題教師用 Word 實際開啟確認，特別是第 22 題作圖區與新的第 19 題平行四邊形圖。
- **Step 4 前的備份**留在任務資料夾：`試題草稿_Step4前備份.md`、`正式試題卷_Step4前備份.docx`、`教師解答卷_Step4前備份.docx`。確認新版無誤後可刪。
- **技能本體單一真實來源仍是 repo 的 `skills/exam-composer/SKILL.md`**，換電腦一律從這裡同步到三處全域目錄。
- NotebookLM 目前有 4 本任務專屬筆記本（六年級國語／數學／自然／社會），五年級數學這本**尚未建立**。
- `光復108課綱歷年定期試題/` 維持空的，這是正常狀態（Step 4 用即時 blob 讀取，不存檔）。

## ➡️ 下一步

1. **功能六 NotebookLM 歸檔**：建立獨立筆記本 `115上_五年級_數學_第一次定期考察_命題成果`，加入本次教材、正式試題卷、教師解答卷、雙向細目表、查重報告與通用參考資料。**避免呼叫 `label list`**（會觸發 NotebookLM 自動分類副作用）。
2. **把本次 Step 4 的三條經驗寫進 `skills/exam-composer/SKILL.md`**（改 repo 版再同步三處、比對 SHA-256 後 commit）：
   - Step 3 撰寫時就預先避開光復高頻命題框架（見 `agents.md` 測試發現第 16 點清單），不要等 Step 4 才大量重寫；
   - Step 4 的 ▲ 類判準明文化為「★ 必改、▲ 由命題教師決定並在報告中逐題記錄」；
   - Step 4 重寫的硬約束：**必須守住原題型／Bloom／單元格位**，如此雙向細目表無須重做。
3. **把 ESA 操作要點補進 SKILL.md 或 esa-exam-review**（完整版在 `查重報告.md` 第七節）：div-based 版面、POST 一次取整年清單、`no` 屬性藏檔名、**不可直接導航模組 JSP（會作廢 session）**、`.doc` 年度改讀解答卷。
4. 若要正式讓某位命題教師使用**國語**科，Step 1 需把其餘六課也逐頁精讀（舊的未完成項目）。
5. 考慮在常用電腦安裝 LibreOffice，否則 Step 5 視覺渲染 QA 永遠做不了。

## ⚠️ 注意事項

- **🆕 ESA 操作：登入後只用 `fetch` 取資料，絕對不要導航到模組 JSP 網址**（`/jsp/c_exammgt/index.jsp?pid=0261`）。繞過入口框架會讓伺服器回 `index_error.jsp?err=7` 並**作廢整個 session**，必須請使用者重新登入。本次即因此中斷一次。
- **🆕 ESA 試卷清單是 div-based**（`div.row` ＋ `div.column`，不是 `table/tr`）；`POST /jsp/c_exammgt/ExamMgtAction.do` 帶 `method=examMain&mod=examMain&selseyear=<代碼，如 1141>` 可一次取回整個學年期清單；PDF 檔名在 `div[id^=row2_itmfile_]`／`div[id^=row2_ansfile_]` 的 `no` 屬性，下載路徑 `/central/014796/upfile/exammgt/<檔名>`。
- **🆕 部分年度試卷檔是 `.doc`**（本次 110-1），瀏覽器無法渲染，**改讀解答卷 PDF**（掃描版含完整題目）即可正常比對。
- **🆕 瀏覽器工具執行 JS 時，回傳值不要含長檔名或編碼字串**，會被防資料外洩機制擋下（回 `BLOCKED: Cookie/query string data`）。把檔名留在頁面變數內，只回傳狀態碼、大小等短資訊。
- **🆕 修改既有 `.docx` 優先用 python-docx 就地編輯**，不要整份重生：可改段落文字、替換圖片 blob 與 `a:ext`／`wp:extent` 尺寸，完整保留原排版。本機無 Node `docx` 套件，但有 python-docx 1.2.0。
- **🆕 用 Bash heredoc 寫含 Windows 路徑的 Python 時，字串要用 raw（`r"""`）**，否則 `C:\Users` 的 `\U` 會被當成 unicode escape 而語法錯誤。
- **Chrome 側邊面板要打開才會建立 Claude in Chrome 連線**；執行 Step A／Step 4 這類需要登入的階段，Chrome 視窗全程不要關閉。若連線意外中斷，先呼叫 `list_connected_browsers` 確認裝置是否還是原本那個。
- **Agent 絕不輸入帳號密碼**：ESA 與親師生平台登入一律由使用者本人完成，Agent 只等待。
- **Step A（教材下載）**：登入由使用者做，登入後的下載點擊由 Agent 接手並逐檔驗證落地。翰林 PDF 入口在 `edisc3.hle.com.tw` 左側選單「**教材資源／PPT**」（頁面 `gwty_v2023.html`）。Chrome 會靜默封鎖同站第 2 個以後的自動下載，優先用網站的「勾選＋下載已勾選項目」打包成單一 ZIP。
- **翰林教材拆檔邏輯依科目而異**：數學按「課」拆（L01~L10），社會教專按「單元」包裹（CH1=單元1）。一律先下載目次確認，不要憑檔名猜。
- **Step 4 不需要也無法把歷史 PDF 存進資料夾**：用 `fetch` 轉 blob URL ＋頁面內嵌 iframe 顯示，截圖比對，不留檔案。**不要點擊 PDF 內容區**（會造成 tab 凍結），只用 scroll ＋ zoom。
- **Node.js 寫入 GDrive 路徑檔案時一律用 `path.join()`**，不要字串相加＋反斜線（錯誤不會拋例外，極難排查）。
- **題目圖像規則**：需要新圖或改版圖時召喚全域 `draw` 技能，輸出到該次 `命題成果/.../images/`；本次第 19 題圖為 PIL 程式繪製（幾何圖精度需求高，程式繪圖比生圖可靠）。
- **NotebookLM 規則**：每次任務建立單獨 Notebook，不沿用舊的；避免呼叫 `label list`。
- **`exam-composer` 若要修改**：先改 repo 的 `skills/exam-composer/SKILL.md`，再同步到 `~/.claude`／`~/.codex`／`~/.agents` 三處，四份比對 SHA-256 後 commit。

## 📎 本次收工的層級狀態

- ✅ L1 本地：agents.md（新增測試發現第 16 點）、handoff.md 已更新
- ✅ L2 GitHub：已 commit + push
- ⚠️ **L3 Obsidian 未更新**：本機（DESKTOP-HJA3024）**沒有 Obsidian MCP**，無法寫入 `定期考察命題技能/專案工作流程.md`。本次的詳細決策脈絡（為何只改 ★ 10 題、▲ 的取捨理由、ESA 操作踩坑細節）已完整寫進 `agents.md` 測試發現第 16 點與任務資料夾的 `查重報告.md`，**回到有 Obsidian 的電腦時請補寫 L3 筆記**。

## 🕐 最後更新
- 時間：2026-09-07（收工）
- 更新者：Claude @ DESKTOP-HJA3024
- Git push：✅ 已推（commit `85c2283`）
