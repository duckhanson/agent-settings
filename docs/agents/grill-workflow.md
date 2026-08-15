# grill-with-docs 在本專案的落地

`grill-with-docs` = 跑 `/grilling` 訪談 + 用 `/domain-modeling` 邊做邊寫 glossary/ADR。上游鏈路：

```
grill-with-docs → to-spec → to-tickets → implement
```

## 不需要修改的部分

- **`grilling` 訪談技巧本身**（一次問一句、附建議答案、依賴關係往下問、能從 codebase 查到的就不問）跟 persona/user story 無關，是中性技巧，維持原樣，不需要研究情境的調整。
- **`grill-with-docs` skill 本體**也不需要改——它只是呼叫 `/grilling` + `/domain-modeling`，本身沒有寫死 product 假設，且它判斷要不要寫 ADR 的三條件測試跟 `decision-routing.md` 用的是同一套。

## 靠專案設定（不是改 skill）接住的部分

- `CONTEXT-MAP.md`：宣告 `experiments/<name>/` 為多 context，讓 `domain-modeling`（因此也讓 `grill-with-docs`）原生把 ADR/glossary 寫進 `experiments/<name>/docs/adr/`，而不是全部塞進單一根層級 `docs/adr/`。
- 跑完 grill-with-docs 之後接 `/to-spec`：套用 `docs/agents/research-spec-template.md`（CLAUDE.md 已指標），不需要重新訪談，直接合成剛剛談定的理解。
- 跑 `/to-tickets`：套用 `experiments/<name>/tickets/` 慣例（見 `docs/agents/decision-routing.md` 的 ticket 位置說明）。
