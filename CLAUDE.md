# Research and Develop Rules

Read AGENTS.md first.

> 注意：本文件超過 100 行時，Claude 應主動提議瘦身。

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan, one line per step: `[Step] → verify: [check]`.

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Code Style

- Do not add comments explaining *what* code does; names should be self-explanatory.
- Only add comments for non-obvious *why* (edge cases, workarounds, business constraints).

## 6. 每日紀錄規範

**每次 session 開始先讀最新進度，結束前寫下決策脈絡。**

- 開始新 session 時，先讀取最新一份 `logs/*.md`，確認上次的「下一步待辦」再開始工作。
- Session 結束前，在 `logs/YYYY-MM-DD.md`（當天日期，檔案已存在則附加）寫入紀錄，包含：
  - `## 今日進度`：做了什麼（簡述，不逐行複述 code diff）
  - `## 關鍵決策與理由`：任何偏離 spec.md 或 impl-plan.md 的地方，以及為什麼
  - `## 遇到的問題與解法`：踩過的坑、debug 過程的重要發現
  - `## 下一步待辦`：明確列出接下來要做的事，方便下次 session 或其他協作者接手
- 紀錄要精簡，重點是「決策脈絡」而非流水帳；code 層級的變更可參考 git log，不需重複。
- 若該次 session 沒有偏離 spec、也沒有特別決策，只記「今日進度」與「下一步待辦」即可，不用硬湊其他內容。

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Hard Constraints（不可違反）

### 程式執行
- Python: `uv run python`
- C++: C++23
- 所有實驗共用專案根目錄的 `.venv`，不要在子目錄（如 `experiments/*`、`baselines/*`）另建新 venv

### 開發時優先採用的 Skills
- 開發/寫程式前：先套用 `ponytail` skill，檢視是否為最小可行方案，避免過度工程化。
- 寫/改 Python 程式碼時：套用 `google-python-style` skill，作為預設 coding style。
- 畫圖/產生 figure 時：一律套用 `han-lab-plot-style` skill。
