# 研究實驗版 to-spec 模板

`to-spec` skill 內建的模板（Problem Statement/Solution/User Stories/...）是為產品功能設計的，預設有一個從中受益的 persona，且「done」代表功能如預期運作。研究實驗沒有 persona，結論本身允許是否定的——一個假說被推翻、一個設計撞到天花板,是有效的研究結果,不是功能壞掉。

**在本專案執行 `/to-spec` 時，一律用下面這份模板取代 skill 內建模板**，其餘流程（探索 codebase、確認 seam、套用 triage label）不變。

## 模板

```md
## Research Question

這份 spec 支撐論文裡的哪個 claim/figure？目前還不知道什麼？

## Experimental Design

量測什麼、怎麼量、有哪些變因被控制住。

## Predictions

一份詳盡、逐條列出的清單，每條是**可證偽、可檢驗**的敘述：
「若 X 成立，在 C 條件下 metric M 應呈現 P 模式」

這份清單要盡量詳盡、涵蓋各個面向——精神上對應 to-spec 原本 User Stories 的「窮舉」要求，只是用預測取代 benefit。

## Implementation Decisions

跟 to-spec 原模板一樣：要動的模組、介面、架構決策、schema 變更。不放特定檔案路徑或程式碼片段（除非是 prototype 產生、決策本身就是那個片段，例如 state machine/schema）。

## Measurement Validity Decisions

取代原本的 Testing Decisions。內容包括：
- ground truth 怎麼定義（什麼算「對」）
- 已知的 confound 有哪些、怎麼控制
- 樣本數/統計門檻
- 這份量測的 prior art（spec 裡類似的既有量測手法）

## Out of Scope

跟原模板一樣，但範疇是**認知範疇**而非build範疇：不主張的 claim、沒控制的變因、不宣稱的泛化邊界——而不是「這一輪不做的功能」。

## Further Notes

跟 to-spec 原模板一樣。
```

## 對應到既有慣例

- Implementation Decisions 段落裡通過 ADR 三條件測試的決定，依 [[decision-routing]] 路由到 `docs/adr/` 或 `experiments/<name>/docs/adr/`，不要整段複製進 spec。
- Spec 完成後存放於 `experiments/<name>/SPEC.md`（或該實驗已有多份 spec 時用 `experiments/<name>/SPEC_<topic>.md`），不是 `spec/` 目錄——`spec/` 只放論文 draft 與 paper 本身。
