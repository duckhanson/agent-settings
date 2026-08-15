# Context Map

本專案採多 context 佈局：`experiments/<name>/` 底下每個實驗都是獨立 context。`domain-modeling`（因此也包括 `grill-with-docs`）讀到這份檔案就會知道要往每個實驗自己的目錄寫，而不是全部塞進根層級。

- 系統/跨實驗層級的 glossary 與架構決策：根層級 `CONTEXT.md`（尚未建立，lazily 建立）、`docs/adr/`
- 個別實驗的 glossary 與架構決策：`experiments/<name>/CONTEXT.md`（尚未建立）、`experiments/<name>/docs/adr/`

現有 context：`experiments/pass_offload/`、`experiments/background/`、`experiments/api_verification/`、`experiments/batch_size_vs_throughput/`、`experiments/kv_budget_vs_throughput/`、`experiments/param_sweep_vs_speedup/`——新增實驗目錄時自動視為新 context，不需要更新這份清單。

`spec/` 不是 context，只放論文 draft 與 paper，不建立 `CONTEXT.md`/`docs/adr/`。
