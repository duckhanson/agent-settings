# Domain Docs

探索/生成內容前，Claude 應讀取：

- `CONTEXT-MAP.md`（本專案多 context 佈局）
- 相關 `experiments/<name>/CONTEXT.md`（若存在）
- `docs/adr/`（根層級，跨實驗決策）與 `experiments/<name>/docs/adr/`（單一實驗架構決策）

檔案不存在就略過，不需要主動建議先建立——`grill-with-docs`/`domain-modeling` 會在第一個詞彙/決策定案時才 lazily 建立，見 `docs/agents/grill-workflow.md`。

## 使用 glossary 詞彙
輸出（spec、ticket、ADR 標題等）使用該 context `CONTEXT.md` 已定義的詞彙，不要自創同義詞。

## ADR 衝突要明講
若輸出跟既有 ADR 矛盾，直接標出來，不要默默蓋過去。
