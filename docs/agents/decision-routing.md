# 決策文件路由規則

本專案採用 Matt Pocock skills 的 spec/ticket/ADR 慣例，適用於研究實驗而非產品功能。任何「這個決策該記在哪」的判斷都套用下表，不論是否透過 `/to-spec`、`/to-tickets`、`/domain-modeling` 等 slash command 觸發。

## 路由表

| 決策性質 | 去處 |
|---|---|
| 純詞彙定義，不含實作細節 | `CONTEXT.md`（glossary） |
| 只影響單一實驗、寫 spec 當下拍板 | `experiments/<name>/SPEC.md` 的 Implementation Decisions 段落 |
| 通過下方 ADR 三條件測試，且只影響單一實驗的架構 | `experiments/<name>/docs/adr/NNNN-slug.md` |
| 通過 ADR 三條件測試，且影響跨實驗/整個專案（框架、環境、共用機制） | `docs/adr/NNNN-slug.md`（根層級） |
| 純過程紀錄、debug 發現、當天做了什麼 | `logs/YYYY-MM-DD.md`；若冒出真正決策，log 只留一句連結，內容搬去上面三類之一 |

## ADR 三條件測試

只有同時符合以下三點才寫 ADR，缺一則不寫：

1. **難以逆轉** — 改變主意的成本很高
2. **沒有上下文會讓未來的人意外** — 讀 code 的人會問「為什麼當初這樣做？」
3. **真的有取捨** — 有其他選項，選了一個是有理由的

ADR 格式與編號規則見 mattpocock skills 的 `ADR-FORMAT.md`（sequential numbering，`docs/adr/` 目錄下當前最大編號 +1）；每個目錄（根層級、各 `experiments/<name>/`）各自獨立編號。

## Ticket 位置

Ticket（`to-tickets` 產出）放在 `experiments/<name>/tickets/NN-slug.md`，**不是**預設的 `.scratch/<feature>/issues/`——研究實驗需要長期保存 provenance，跟該實驗的 spec/code 放一起比獨立的暫存區更合理。
