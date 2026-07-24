# Agent Settings 收藏

這個資料夾收錄 `emmc_offload` 專案中實際生效的 Claude Code agent 設定,
資料夾結構刻意鏡射真實路徑,所以要套用到新專案時,直接把對應檔案複製到新
repo 的相同位置即可,不需要轉換路徑。

```
agent_settings/
├── README.md              本檔案
├── CLAUDE.md              專案規則(repo root 原檔的副本)
├── AGENTS.md              懶人開發準則(repo root 原檔的副本)
└── .claude/
    └── skills/
        ├── google-python-style/   Python 專案內建 skill
        ├── google-cpp-style/      C++ 專案內建 skill
        └── han-lab-plot-style/    論文圖表風格 skill
```

> 這個資料夾只是「收藏 + 說明」,不是自動套用機制。複製檔案後,Claude Code
> 才會依下面說明的規則去讀它們。

---

## 1. CLAUDE.md — 專案規則(自動載入)

Claude Code 啟動時會自動讀取 repo root 的 `CLAUDE.md`。這份規則檔定義了
「思考先於編碼」「簡單優先」「外科手術式修改」等行為準則,以及本專案的
硬性限制(`uv run python`、C++23、共用 root `.venv`)與 skill 使用時機。

**套用方式:** 把 `agent_settings/CLAUDE.md` 複製到新專案的 repo root,
依新專案情況調整「Hard Constraints」章節即可,其餘行為準則可以直接沿用。

## 2. AGENTS.md — 懶人開發準則(由 CLAUDE.md 指定讀取)

這份檔案的內容其實是 **ponytail plugin 自己的 `AGENTS.md` 逐字複製**
(diff 完全一致)。ponytail 是一套「懶人資深工程師模式」的行為準則
(YAGNI、優先用標準函式庫、拒絕不必要的抽象化)。

重點:**AGENTS.md 本身不是 Claude Code 原生會自動讀取的檔案。** 它能生效
是因為 `CLAUDE.md` 第一行寫了「Read AGENTS.md first.」,靠 CLAUDE.md 這個
真正的入口去指示 Claude 主動讀取它。這個機制的好處是:即使某台機器沒裝
ponytail plugin,或該次 session 是 headless/CI 執行、plugin hooks 沒有
生效,懶人開發準則依然會透過這份 AGENTS.md 文字生效。

**套用方式:** 把 `agent_settings/AGENTS.md` 複製到新專案 repo root,並確保
新專案的 CLAUDE.md 也有一行「Read AGENTS.md first.」。

## 3. .claude/skills/ — 專案內建 Skills(自動掃描)

Claude Code 會自動掃描 repo root 的 `.claude/skills/*/SKILL.md`,不需要
額外註冊或安裝,只要檔案在正確路徑就會被列進可用 skills。本專案有三個:

| Skill | 用途 | CLAUDE.md 中的觸發規則 |
|---|---|---|
| `google-python-style` | Google Python 風格規範 + code review checklist | 寫/改 Python 時套用 |
| `google-cpp-style` | Google C++ 風格規範 + code review checklist | 寫/改 C++ 時套用(python skill 的姊妹 skill) |
| `han-lab-plot-style` | MIT Han Lab(Song Han)論文圖表風格 | 畫圖/產生 figure 時套用 |

**套用方式:** 把 `agent_settings/.claude/skills/` 底下三個資料夾整個複製到
新專案的 `.claude/skills/` 下(路徑必須是 `<repo-root>/.claude/skills/<name>/SKILL.md`)。

---

## 4. 需要另外下載的 Plugin:ponytail

本專案唯一依賴的外部 plugin 是 **ponytail**(懶人開發模式的完整實作,
提供 `ponytail`/`ponytail-audit`/`ponytail-debt`/`ponytail-help`/
`ponytail-review` 等 skills 與 hooks)。它**不在這個 repo 裡**,原始檔案
存在使用者全域目錄 `~/.claude/plugins/`,必須額外安裝:

```
# 在 Claude Code 互動模式下執行
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

安裝後 plugin 是**綁在你的使用者帳號(全域),不是綁在這個 repo**。也就是
說,同一台機器上的其他專案也會共用同一份 ponytail;但別人 clone 這個 repo
到別的機器時,不會自動拿到 ponytail,需要照上面指令自己裝一次。

> 目前這個機制沒有寫進 repo 的 `.claude/settings.json`(專案本身也沒有這個
> 檔案,只有 `.claude/settings.local.json` 記錄本機的 permission 白名單,
> 屬於本機狀態,故意不收錄進本資料夾)。如果希望 team 成員 clone 專案時,
> Claude Code 能自動提示安裝 ponytail,可以在專案的 `.claude/settings.json`
> 加上 `enabledPlugins` / `extraKnownMarketplaces` 設定 —— 這是可選的加強,
> 目前專案尚未這樣做。

## 5. 不需要下載的內建 Skills

Claude Code CLI 本身內建一批 skill(如 `dataviz`、`artifact-design`、
`update-config`、`simplify`、`init`、`review`、`security-review`、
`loop`、`schedule` 等),這些是編譯進 CLI 本體的功能,**不是檔案、不需要
安裝任何 plugin**,只要 Claude Code 版本夠新就會出現在可用 skills 清單裡。
不要把它們跟本資料夾收錄的「專案 skills」或「ponytail plugin skills」搞混。

---

## 6. 在新專案套用的完整步驟

```bash
# 1. 專案規則
cp agent_settings/CLAUDE.md   <new-repo>/CLAUDE.md
cp agent_settings/AGENTS.md   <new-repo>/AGENTS.md

# 2. 專案內建 skills
mkdir -p <new-repo>/.claude/skills
cp -r agent_settings/.claude/skills/* <new-repo>/.claude/skills/

# 3. 安裝外部 plugin(每台機器 / 每個使用者只需一次,與 repo 無關)
#    在 Claude Code 互動模式下執行:
#    /plugin marketplace add DietrichGebert/ponytail
#    /plugin install ponytail@ponytail
```

完成後,打開 Claude Code 進到新專案時就會:
1. 自動讀 `CLAUDE.md` → 依指示去讀 `AGENTS.md`
2. 自動掃到 `.claude/skills/` 下的三個 skill
3. 若已裝好 ponytail plugin,`ponytail` 系列 skills 也會出現在可用清單中
