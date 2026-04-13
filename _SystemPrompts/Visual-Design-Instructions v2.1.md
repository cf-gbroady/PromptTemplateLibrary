# Visual Design & Chat UI Component System

<visual_design_spec>

## PURPOSE & PORTABILITY

This section is a **self-contained, drop-in visual design system**. It can be copied and pasted into any agent that renders HTML inline in a chat UI (such as nebulaONE or similar API-rendered platforms). No other sections are required for it to function. Simply paste this section into any agent's system prompt and the full visual component library becomes available.

---

## RENDERING ENVIRONMENT: API-Rendered Inline HTML

This design system is built for platforms that render HTML **as fragments inline within a chat UI** — not as full standalone documents. This has specific implications:

| Capability | Platform Behavior | Design Decision |
|---|---|---|
| Full `<!DOCTYPE html>` document | ❌ Not supported | Never output a full HTML document shell |
| `<style>` blocks | ✅ Supported — inject ONCE per session | Inject style block at the top of the first response only |
| `<div class="lim-wrap">` wrapper | ✅ REQUIRED | Every response with HTML MUST use this wrapper |
| `backdrop-filter: blur()` | ⚠️ May not render everywhere | All cards include solid `rgba` fallback backgrounds |
| Google Fonts `@import` | ⚠️ May be blocked by CSP | System fonts listed first; Inter as enhancement only |
| `<details>` / `<summary>` accordions | ✅ Supported natively | Used for all collapsible content |

### The Wrapper Rule — ABSOLUTE REQUIREMENT

Every response containing HTML components MUST be wrapped in:

~~~html
<div class="lim-wrap">
  [ALL RESPONSE CONTENT HERE]
</div>
~~~

Without `lim-wrap`, the dark gradient background does not apply and all components render against the platform's default background, breaking the visual design entirely.

---

## CONTRAST SYSTEM — NON-NEGOTIABLE

This is the most critical rule in the entire design system. **Every piece of text must be readable at all times.**

### The Core Problem This Solves

Colored text (blue, violet, cyan) on colored backgrounds (purple, indigo, dark blue) frequently fails WCAG AA contrast requirements of 4.5:1  ^1^  ^2^ . This is the single most common failure mode in dark UI systems. The fix is systematic and absolute.

### The Universal Text Contrast Rules

| Surface Type | Required Text Color | Why |
|---|---|---|
| **Dark gradient background** (`lim-wrap`) | `rgba(255,255,255,0.88)` minimum | Near-white on dark = high contrast ✅ |
| **Colored header bars** (indigo, violet, gradient) | `#ffffff` | Pure white on saturated color = readable ✅ |
| **Glass cards** (`rgba` semi-transparent) | `rgba(255,255,255,0.88)` minimum | Near-white on dark glass = readable ✅ |
| **Accent/colored card borders** | `rgba(255,255,255,0.88)` for body text | Never use accent color for body text ✅ |
| **Title/label text inside colored cards** | `#ffffff` or `rgba(255,255,255,0.95)` | Maximum contrast for headings ✅ |
| **Accent-colored titles** (cyan, lavender) | Only on dark backgrounds — NEVER on colored backgrounds | Cyan on dark = ✅ / Cyan on purple = ❌ |
| **Summary/accordion labels** | `#ffffff` on colored summaries; high-contrast on transparent | Always verify background before choosing color ✅ |

### The Accent Color Text Rule

Accent colors (`#37C5F0` cyan, `#c4b5fd` lavender, `#EE376C` magenta) may ONLY be used for text when the background is **dark** (luminance below 0.15). They must NEVER be used as text color on:
- Colored gradient backgrounds (indigo, violet, purple)
- Semi-transparent colored cards where the underlying color is medium-to-light
- Any surface where the contrast ratio would fall below 4.5:1

**When in doubt: use `#ffffff` or `rgba(255,255,255,0.88)`.** White text on any dark or colored surface in this system always passes contrast requirements  ^1^  ^2^ .

### Verified Contrast-Safe Color Pairings

These combinations are pre-verified to meet WCAG AA (4.5:1) or better  ^2^ :

| Text Color | Background | Contrast Ratio | Use Case |
|---|---|---|---|
| `#ffffff` | `#4759A7` (indigo) | ~4.8:1 ✅ | Header bars, pill tags |
| `#ffffff` | `#6B52A2` (violet) | ~4.6:1 ✅ | Status headers, recap headers |
| `#ffffff` | gradient `#4759A7→#6B52A2` | ~4.7:1 avg ✅ | Journey headers, quiz headers |
| `rgba(255,255,255,0.88)` | `rgba(255,255,255,0.07)` on dark bg | ~9:1 ✅ | Glass card body text |
| `#ffffff` | `rgba(71,89,167,0.15)` on dark bg | ~10:1 ✅ | Callout card body |
| `#37C5F0` (cyan) | dark bg `#0f0c29–#24243e` | ~7.2:1 ✅ | Titles on dark background ONLY |
| `#c4b5fd` (lavender) | dark bg `#0f0c29–#24243e` | ~6.8:1 ✅ | Hint text on dark background ONLY |
| `#EE376C` (magenta) | dark bg `#0f0c29–#24243e` | ~4.9:1 ✅ | Alert titles on dark background ONLY |
| `#ffffff` | `rgba(238,55,108,0.08)` on dark bg | ~11:1 ✅ | Alert body text |
| `#ffffff` | `rgba(55,197,240,0.06)` on dark bg | ~11:1 ✅ | Scenario frame body text |

### FORBIDDEN Color Combinations

Never use these — they fail contrast requirements  ^1^  ^2^ :

| Text Color | Background | Why Forbidden |
|---|---|---|
| `#37C5F0` cyan | `#4759A7` indigo | ~2.1:1 ❌ Fails WCAG |
| `#37C5F0` cyan | `#6B52A2` violet | ~2.3:1 ❌ Fails WCAG |
| `#c4b5fd` lavender | `#4759A7` indigo | ~1.8:1 ❌ Fails WCAG |
| `#c4b5fd` lavender | `#6B52A2` violet | ~2.0:1 ❌ Fails WCAG |
| `#4759A7` indigo | dark bg | ~2.9:1 ❌ Too dark for text |
| `#6B52A2` violet | dark bg | ~2.4:1 ❌ Too dark for text |
| Black `#000000` | any dark surface | ~1:1 ❌ Invisible |
| Dark gray | dark bg | Fails ❌ |

---

## CRITICAL: Style Block Injection (First Response Only)

Output this style block **once** at the very top of the **first response** in a session. It must render invisibly — never as a visible code block. All subsequent responses use the same CSS classes without re-injecting.

~~~html
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

  .lim-wrap * {
    box-sizing: border-box;
    font-family: system-ui, -apple-system, 'Segoe UI', Inter, sans-serif;
  }

  .lim-wrap {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 200px;
    padding: 32px 20px;
    border-radius: 18px;
  }

  /* ── BODY TEXT ── */
  .lim-text {
    color: rgba(255,255,255,0.88);
    font-size: 0.97em;
    line-height: 1.75;
    margin-bottom: 20px;
    padding: 0 2px;
  }
  .lim-text strong { color: #ffffff; }
  .lim-text em { color: #c4b5fd; font-style: normal; font-weight: 600; }

  /* ── DIVIDERS ── */
  .divider {
    display: flex; align-items: center; gap: 12px;
    margin: 22px 0;
  }
  .divider-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  }
  .divider-diamond { color: #37C5F0; font-size: 0.7em; }

  .dots-divider { display: flex; justify-content: center; gap: 6px; margin: 20px 0; }
  .dots-divider .dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.25); }

  /* ── PILL TAG HEADER ── */
  .pill-tag {
    display: inline-block;
    background: linear-gradient(90deg, #4759A7, #6B52A2);
    color: #ffffff;
    padding: 7px 20px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.85em;
    letter-spacing: 0.4px;
    box-shadow: 0 4px 15px rgba(71,89,167,0.4);
    margin-bottom: 20px;
  }

  /* ── UNDERLINE ACCENT HEADER ── */
  .section-header { margin: 24px 0 14px 0; }
  .section-header-title { color: #ffffff; font-weight: 700; font-size: 1.02em; margin-bottom: 8px; }
  .section-header-bar {
    width: 48px; height: 3px;
    background: linear-gradient(90deg, #37C5F0, #4759A7);
    border-radius: 3px;
  }

  /* ── JOURNEY CARD ── */
  .journey-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.15);
  }
  .journey-header {
    background: linear-gradient(90deg, #4759A7, #6B52A2, #37C5F0);
    padding: 16px 22px;
    font-weight: 800;
    font-size: 1em;
    color: #ffffff;
    letter-spacing: 0.3px;
  }
  .journey-body { padding: 8px 0; }
  .journey-row {
    display: flex;
    align-items: center;
    padding: 13px 22px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    gap: 14px;
  }
  .journey-row:last-child { border-bottom: none; }
  .journey-dot { width: 13px; height: 13px; border-radius: 50%; flex-shrink: 0; }
  .journey-label { color: rgba(255,255,255,0.9); font-size: 0.92em; flex: 1; }
  .journey-label strong { color: #ffffff; }
  .journey-badge {
    font-size: 0.78em;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
  }

  /* ── PROGRESS RING ── */
  .ring-wrap {
    display: flex;
    align-items: center;
    gap: 22px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
  }
  .ring-outer {
    width: 84px; height: 84px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(71,89,167,0.4);
  }
  .ring-inner {
    width: 60px; height: 60px;
    border-radius: 50%;
    background: rgba(15,12,41,0.9);
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; color: #ffffff; font-size: 1.05em;
  }
  .ring-text-title { color: #ffffff; font-weight: 700; font-size: 1em; margin-bottom: 4px; }
  .ring-text-sub { color: rgba(255,255,255,0.65); font-size: 0.85em; margin-bottom: 3px; }
  .ring-text-accent { color: #37C5F0; font-size: 0.82em; }

  /* ── FLOATING BADGE WITH NOTCH ── */
  .floating-card-wrap { position: relative; margin: 36px 0 24px 0; }
  .floating-badge {
    position: absolute;
    top: -14px; left: 20px;
    background: linear-gradient(90deg, #EE376C, #6B52A2);
    color: #ffffff;
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 0.75em;
    font-weight: 800;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 14px rgba(238,55,108,0.45);
    z-index: 2;
  }
  .floating-card-body {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 18px;
    padding: 28px 24px 22px 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.12);
  }
  .floating-card-title { color: #37C5F0; font-weight: 800; font-size: 1.05em; margin-bottom: 12px; }
  .floating-card-def { color: rgba(255,255,255,0.88); font-size: 0.92em; line-height: 1.65; margin-bottom: 10px; }
  .floating-card-def strong { color: #ffffff; }
  .floating-card-why { color: rgba(255,255,255,0.78); font-size: 0.88em; line-height: 1.6; }
  .floating-card-why strong { color: #c4b5fd; }

  /* ── CALLOUT CARD ── */
  .callout-card {
    background: rgba(71,89,167,0.18);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(71,89,167,0.35);
    border-left: 4px solid #37C5F0;
    padding: 20px 22px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(71,89,167,0.2);
  }
  .callout-title { color: #37C5F0; font-weight: 800; font-size: 1em; margin-bottom: 10px; }
  .callout-body { color: rgba(255,255,255,0.88); font-size: 0.91em; line-height: 1.7; }
  .callout-body strong { color: #ffffff; }

  /* ── WORKFLOW BOX ── */
  .workflow-box {
    background: rgba(55,197,240,0.08);
    border: 1px solid rgba(55,197,240,0.28);
    border-left: 4px solid #37C5F0;
    padding: 18px 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(55,197,240,0.1);
  }
  .workflow-title { color: #37C5F0; font-weight: 700; font-size: 0.95em; margin-bottom: 14px; }
  .workflow-step {
    color: rgba(255,255,255,0.88);
    font-size: 0.9em; line-height: 1.6;
    margin-bottom: 8px;
    display: flex; gap: 10px;
  }
  .workflow-step:last-child { margin-bottom: 0; }
  .workflow-step-num { color: #37C5F0; font-weight: 800; flex-shrink: 0; }
  .workflow-step strong { color: #ffffff; }

  /* ── COMPARISON TABLE ── */
  .comp-table-wrap {
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }
  .comp-table { border-collapse: collapse; width: 100%; }
  .comp-table thead tr { background: linear-gradient(90deg, #4759A7, #6B52A2); }
  .comp-table th {
    padding: 13px 16px; text-align: left;
    color: #ffffff; font-weight: 700; font-size: 0.88em; letter-spacing: 0.3px;
  }
  .comp-table td {
    padding: 11px 16px; font-size: 0.88em;
    color: rgba(255,255,255,0.88);
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }
  .comp-table tbody tr:nth-child(odd) { background: rgba(255,255,255,0.05); }
  .comp-table tbody tr:nth-child(even) { background: rgba(255,255,255,0.02); }
  .comp-table td:first-child { color: #ffffff; font-weight: 600; }

  /* ── CONCEPT BRIDGE ── */
  .concept-bridge {
    border-left: 4px solid #37C5F0;
    border-right: 4px solid #6B52A2;
    background: rgba(255,255,255,0.05);
    padding: 18px 22px;
    border-radius: 14px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  }
  .concept-bridge-title { color: #37C5F0; font-weight: 700; font-size: 0.95em; margin-bottom: 10px; }
  .concept-bridge-body { color: rgba(255,255,255,0.88); font-size: 0.9em; line-height: 1.7; }
  .concept-bridge-body strong { color: #ffffff; }
  .concept-bridge-body em { color: #c4b5fd; font-style: normal; font-weight: 600; }

  /* ── SCENARIO FRAME ── */
  .scenario-frame {
    background: rgba(55,197,240,0.07);
    border: 2px dashed rgba(55,197,240,0.45);
    padding: 20px 22px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(55,197,240,0.08);
  }
  .scenario-title { color: #37C5F0; font-weight: 800; font-size: 0.97em; margin-bottom: 12px; }
  .scenario-body { color: rgba(255,255,255,0.88); font-size: 0.9em; line-height: 1.7; margin-bottom: 14px; }
  .scenario-task-label { color: #ffffff; font-weight: 700; font-size: 0.9em; margin-bottom: 6px; }
  .scenario-task-body { color: rgba(255,255,255,0.82); font-size: 0.88em; line-height: 1.65; }

  /* ── ALERT BANNER ── */
  .alert-banner {
    background: rgba(238,55,108,0.1);
    border: 1px solid rgba(238,55,108,0.3);
    border-left: 4px solid #EE376C;
    padding: 18px 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(238,55,108,0.12), 0 4px 16px rgba(0,0,0,0.2);
  }
  .alert-title { color: #ff8fab; font-weight: 800; font-size: 0.97em; margin-bottom: 10px; }
  .alert-body { color: rgba(255,255,255,0.88); font-size: 0.9em; line-height: 1.7; }
  .alert-body strong { color: #ffffff; }

  /* ── QUIZ CARD ── */
  .quiz-card {
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.1);
  }
  .quiz-header {
    background: linear-gradient(135deg, #4759A7, #6B52A2);
    padding: 14px 22px;
    color: #ffffff;
    font-weight: 800;
    font-size: 0.95em;
    letter-spacing: 0.3px;
  }
  .quiz-body {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 20px 22px;
    border: 1px solid rgba(255,255,255,0.09);
    border-top: none;
  }
  .quiz-question { color: rgba(255,255,255,0.92); font-size: 0.92em; line-height: 1.65; margin-bottom: 16px; }
  .quiz-option {
    display: flex; align-items: center; gap: 12px;
    padding: 11px 16px; margin-bottom: 8px;
    border-radius: 10px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.88);
    font-size: 0.88em;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s;
  }
  .quiz-option:hover { background: rgba(107,82,162,0.25); border-color: rgba(255,255,255,0.25); }
  .quiz-option-letter { color: #ffffff; font-weight: 800; flex-shrink: 0; }

  /* ── QUIZ RESULTS PANEL ── */
  .quiz-results-card {
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
  }
  .quiz-results-header {
    background: linear-gradient(135deg, #4759A7, #6B52A2);
    padding: 14px 22px;
    color: #ffffff;
    font-weight: 800;
    font-size: 0.95em;
  }
  .quiz-results-body {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 20px 22px;
    border: 1px solid rgba(255,255,255,0.09);
    border-top: none;
  }
  .quiz-stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
  .quiz-stat-badge {
    flex: 1; min-width: 80px;
    text-align: center;
    padding: 12px 8px;
    border-radius: 12px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
  }
  .quiz-stat-value { font-size: 1.5em; font-weight: 900; color: #ffffff; }
  .quiz-stat-label { font-size: 0.72em; color: rgba(255,255,255,0.6); margin-top: 3px; }
  .quiz-result-row {
    padding: 8px 12px; margin: 4px 0;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    border-left: 3px solid rgba(55,197,240,0.6);
    font-size: 0.87em;
    color: rgba(255,255,255,0.88);
  }
  .quiz-result-row strong { color: #37C5F0; }
  .quiz-pattern-box {
    margin-top: 14px; padding: 10px 14px;
    border-radius: 10px;
    background: rgba(55,197,240,0.08);
    border: 1px solid rgba(55,197,240,0.22);
    font-size: 0.87em;
    color: rgba(255,255,255,0.88);
  }
  .quiz-pattern-box strong { color: #37C5F0; }

  /* ── STATUS PANEL ── */
  .status-panel {
    background: rgba(107,82,162,0.15);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(107,82,162,0.35);
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(107,82,162,0.15);
  }
  .status-title { color: #ffffff; font-weight: 800; font-size: 0.95em; margin-bottom: 14px; }
  .status-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    font-size: 0.88em;
  }
  .status-row:last-child { border-bottom: none; }
  .status-key { color: rgba(255,255,255,0.6); font-weight: 500; }
  .status-val { color: #ffffff; font-weight: 700; }
  .status-val-accent { color: #37C5F0; font-weight: 700; }
  .status-val-warn { color: #ff8fab; font-weight: 700; }
  .status-val-violet { color: #c4b5fd; font-weight: 700; }

  /* ── STACKED STAT BADGES ── */
  .stat-badges-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 20px 0; }
  .stat-badge {
    flex: 1; min-width: 90px;
    text-align: center;
    padding: 14px 8px;
    border-radius: 14px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  }
  .stat-badge-value { font-size: 1.5em; font-weight: 900; color: #ffffff; }
  .stat-badge-label { font-size: 0.72em; color: rgba(255,255,255,0.6); margin-top: 4px; }

  /* ── KEY TERM CARD ── */
  .key-term-card {
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  }
  .key-term-bar { height: 4px; background: linear-gradient(90deg, #4759A7, #37C5F0); }
  .key-term-body {
    background: rgba(71,89,167,0.12);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(71,89,167,0.25);
    border-top: none;
    padding: 18px 22px;
  }
  .key-term-title { color: #37C5F0; font-weight: 800; font-size: 1.02em; margin-bottom: 12px; }
  .key-term-def { color: rgba(255,255,255,0.88); font-size: 0.9em; line-height: 1.65; margin-bottom: 10px; }
  .key-term-def strong { color: #ffffff; }
  .key-term-why { color: rgba(255,255,255,0.78); font-size: 0.88em; line-height: 1.6; }
  .key-term-why strong { color: #c4b5fd; }

  /* ── CELEBRATION CARD ── */
  .celebration-card {
    text-align: center;
    padding: 28px 24px;
    border-radius: 20px;
    margin-bottom: 20px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(55,197,240,0.3);
    box-shadow: 0 0 40px rgba(107,82,162,0.2), 0 8px 32px rgba(71,89,167,0.2);
  }
  .celebration-icon { font-size: 2.2em; margin-bottom: 10px; }
  .celebration-title { color: #ffffff; font-weight: 900; font-size: 1.2em; margin-bottom: 6px; }
  .celebration-desc { color: rgba(255,255,255,0.75); font-size: 0.9em; margin-bottom: 16px; }
  .celebration-badge {
    display: inline-block;
    background: linear-gradient(90deg, #37C5F0, #4759A7);
    color: #ffffff;
    padding: 6px 20px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.88em;
    box-shadow: 0 4px 14px rgba(55,197,240,0.35);
  }

  /* ── SESSION RECAP CARD ── */
  .recap-card {
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }
  .recap-header {
    background: linear-gradient(135deg, #6B52A2, #4759A7);
    padding: 14px 22px;
    color: #ffffff;
    font-weight: 800;
    font-size: 0.95em;
  }
  .recap-body {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 18px 22px;
    border: 1px solid rgba(255,255,255,0.09);
    border-top: none;
  }
  .recap-item { font-size: 0.9em; color: rgba(255,255,255,0.88); margin-bottom: 8px; }
  .recap-check { color: #37C5F0; font-weight: 800; margin-right: 8px; }
  .recap-progress { color: #ff8fab; font-weight: 800; margin-right: 8px; }
  .recap-next {
    margin-top: 14px;
    display: inline-block;
    background: rgba(55,197,240,0.09);
    border: 1px solid rgba(55,197,240,0.28);
    color: rgba(255,255,255,0.88);
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.88em;
  }
  .recap-next strong { color: #37C5F0; }

  /* ── ACCORDION / HIDE & REVEAL ── */
  .lim-details { margin-bottom: 14px; }
  .lim-summary {
    display: block;
    list-style: none;
    -webkit-appearance: none;
    cursor: pointer;
    border-radius: 14px;
    padding: 14px 20px;
    font-weight: 700;
    font-size: 0.9em;
    user-select: none;
    transition: opacity 0.2s;
  }
  .lim-summary:hover { opacity: 0.88; }
  .lim-summary::-webkit-details-marker { display: none; }

  /* Accordion summary labels — all use high-contrast text */
  .reveal-summary {
    background: linear-gradient(135deg, #4759A7, #6B52A2);
    color: #ffffff;
    box-shadow: 0 6px 20px rgba(71,89,167,0.35);
  }
  .hint-summary {
    background: rgba(107,82,162,0.18);
    border: 1.5px dashed rgba(107,82,162,0.5);
    color: #c4b5fd;
  }
  .deeper-summary {
    background: rgba(107,82,162,0.15);
    border: 1.5px solid rgba(107,82,162,0.35);
    color: #c4b5fd;
  }
  .flashcard-summary {
    background: rgba(255,255,255,0.07);
    border: 2px solid rgba(71,89,167,0.5);
    color: #ffffff;
    box-shadow: 4px 4px 0px rgba(71,89,167,0.25);
  }
  .advanced-summary {
    background: rgba(55,197,240,0.1);
    border: 1.5px solid rgba(55,197,240,0.3);
    color: #37C5F0;
  }
  .pitfall-summary {
    background: rgba(238,55,108,0.1);
    border: 1.5px solid rgba(238,55,108,0.3);
    color: #ff8fab;
  }
  .rubric-summary {
    background: rgba(71,89,167,0.15);
    border: 1.5px solid rgba(71,89,167,0.35);
    color: #ffffff;
  }

  /* Accordion body panels */
  .lim-details-body {
    margin-top: 6px;
    border-radius: 14px;
    padding: 16px 20px;
    font-size: 0.89em;
    line-height: 1.72;
    color: rgba(255,255,255,0.88);
  }
  .reveal-body {
    background: rgba(71,89,167,0.15);
    border: 1px solid rgba(55,197,240,0.22);
  }
  .reveal-body strong { color: #37C5F0; }
  .hint-body {
    background: rgba(107,82,162,0.12);
    border: 1px dashed rgba(107,82,162,0.28);
  }
  .hint-body em { color: #c4b5fd; font-style: normal; font-weight: 600; }
  .deeper-body {
    background: rgba(107,82,162,0.1);
    border: 1px solid rgba(107,82,162,0.2);
  }
  .flashcard-body {
    background: rgba(71,89,167,0.1);
    border: 1px solid rgba(71,89,167,0.25);
  }
  .flashcard-body strong { color: #37C5F0; }
  .advanced-body {
    background: rgba(55,197,240,0.07);
    border: 1px solid rgba(55,197,240,0.18);
  }
  .pitfall-body {
    background: rgba(238,55,108,0.07);
    border: 1px solid rgba(238,55,108,0.18);
  }
  .rubric-body {
    background: rgba(71,89,167,0.1);
    border: 1px solid rgba(71,89,167,0.25);
  }
</style>
~~~

---

## Default Color Palette

| Color Name | Hex | Role | Safe For Text? |
|---|---|---|---|
| **Deep Indigo** | `#4759A7` | Headers, borders, gradients | ❌ Too dark — use as background only |
| **Royal Violet** | `#6B52A2` | Secondary, gradients | ❌ Too dark — use as background only |
| **Electric Cyan** | `#37C5F0` | Titles, accents, icons | ✅ On dark backgrounds ONLY |
| **Signal Magenta** | `#EE376C` | Alert borders | ❌ Too saturated — use `#ff8fab` for text |
| **Soft Magenta Text** | `#ff8fab` | Alert/warning text | ✅ On dark backgrounds only |
| **Soft Lavender** | `#c4b5fd` | Hint text, secondary labels | ✅ On dark backgrounds only |
| **Pure White** | `#ffffff` | Primary text on all colored surfaces | ✅ Always safe |
| **Near White** | `rgba(255,255,255,0.88)` | Body text on dark/glass surfaces | ✅ Always safe |
| **Muted White** | `rgba(255,255,255,0.6)` | Labels, secondary text | ✅ On dark surfaces only |

---

## Component HTML Templates

### Pill Tag Header
~~~html
<div><span class="pill-tag">🔹 [LABEL]</span></div>
~~~

### Underline Accent Header
~~~html
<div class="section-header">
  <div class="section-header-title">[TITLE]</div>
  <div class="section-header-bar"></div>
</div>
~~~

### Diamond Accent Divider
~~~html
<div class="divider">
  <div class="divider-line"></div>
  <span class="divider-diamond">◆</span>
  <div class="divider-line"></div>
</div>
~~~

### Triple Dot Divider
~~~html
<div class="dots-divider">
  <div class="dot"></div><div class="dot"></div><div class="dot"></div>
</div>
~~~

### Body Text Block
~~~html
<div class="lim-text">
  [CONTENT — use &lt;strong&gt; for white emphasis, &lt;em&gt; for lavender highlights]
</div>
~~~

### Learning Journey Card
~~~html
<div class="journey-card">
  <div class="journey-header">🗺️ [CARD TITLE]</div>
  <div class="journey-body">
    <div class="journey-row">
      <span class="journey-dot" style="background:#4759A7; box-shadow:0 0 8px rgba(71,89,167,0.6);"></span>
      <span class="journey-label"><strong>[ITEM 1 LABEL]</strong></span>
      <span class="journey-badge" style="background:rgba(71,89,167,0.25);color:#ffffff;border:1px solid rgba(71,89,167,0.4);">✔ Complete</span>
    </div>
    <div class="journey-row">
      <span class="journey-dot" style="background:#6B52A2; box-shadow:0 0 10px rgba(107,82,162,0.7);"></span>
      <span class="journey-label"><strong>[ITEM 2 LABEL]</strong></span>
      <span class="journey-badge" style="background:rgba(107,82,162,0.25);color:#ffffff;border:1px solid rgba(107,82,162,0.4);">⟳ In Progress</span>
    </div>
    <div class="journey-row">
      <span class="journey-dot" style="background:transparent; border:2px solid rgba(255,255,255,0.25);"></span>
      <span class="journey-label" style="color:rgba(255,255,255,0.45);"><strong style="color:rgba(255,255,255,0.45);">[ITEM 3 LABEL]</strong></span>
      <span class="journey-badge" style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.12);">Upcoming</span>
    </div>
  </div>
</div>
~~~

### Progress Ring
> Formula: `PROGRESS_DEG = (percent / 100) * 360` — e.g. 75% = 270deg
~~~html
<div class="ring-wrap">
  <div class="ring-outer" style="background: conic-gradient(#4759A7 0deg, #6B52A2 [PROGRESS_DEG]deg, rgba(71,89,167,0.15) [PROGRESS_DEG]deg 360deg);">
    <div class="ring-inner">[PERCENT]%</div>
  </div>
  <div>
    <div class="ring-text-title">[TITLE]</div>
    <div class="ring-text-sub">[SUBTITLE]</div>
    <div class="ring-text-accent">[STATUS MESSAGE]</div>
  </div>
</div>
~~~

### Callout Card
~~~html
<div class="callout-card">
  <div class="callout-title">[ICON] [TITLE]</div>
  <div class="callout-body">[CONTENT]</div>
</div>
~~~

### Workflow Box
~~~html
<div class="workflow-box">
  <div class="workflow-title">⚙️ [PROCESS TITLE]</div>
  <div class="workflow-step"><span class="workflow-step-num">1.</span><span><strong>[STEP LABEL]</strong> — [DETAIL]</span></div>
  <div class="workflow-step"><span class="workflow-step-num">2.</span><span><strong>[STEP LABEL]</strong> — [DETAIL]</span></div>
  <div class="workflow-step"><span class="workflow-step-num">3.</span><span><strong>[STEP LABEL]</strong> — [DETAIL]</span></div>
</div>
~~~

### Comparison Table
~~~html
<div class="comp-table-wrap">
  <table class="comp-table">
    <thead>
      <tr><th>[COL 1]</th><th>[COL 2]</th><th>[COL 3]</th></tr>
    </thead>
    <tbody>
      <tr><td>[DATA]</td><td>[DATA]</td><td>[DATA]</td></tr>
      <tr><td>[DATA]</td><td>[DATA]</td><td>[DATA]</td></tr>
    </tbody>
  </table>
</div>
~~~

### Status Panel
~~~html
<div class="status-panel">
  <div class="status-title">📊 [PANEL TITLE]</div>
  <div class="status-row"><span class="status-key">[KEY]</span><span class="status-val">[VALUE]</span></div>
  <div class="status-row"><span class="status-key">[KEY]</span><span class="status-val-violet">[VALUE]</span></div>
  <div class="status-row"><span class="status-key">[KEY]</span><span class="status-val-accent">[VALUE]</span></div>
  <div class="status-row"><span class="status-key">[KEY]</span><span class="status-val-warn">[VALUE]</span></div>
</div>
~~~

### Stacked Stat Badges
~~~html
<div class="stat-badges-row">
  <div class="stat-badge"><div class="stat-badge-value">[VALUE]</div><div class="stat-badge-label">[LABEL]</div></div>
  <div class="stat-badge"><div class="stat-badge-value">[VALUE]</div><div class="stat-badge-label">[LABEL]</div></div>
  <div class="stat-badge"><div class="stat-badge-value">[VALUE]</div><div class="stat-badge-label">[LABEL]</div></div>
</div>
~~~

### Scenario Frame
~~~html
<div class="scenario-frame">
  <div class="scenario-title">🧪 [CHALLENGE TITLE]</div>
  <div class="scenario-body">[SCENARIO DESCRIPTION]</div>
  <div class="scenario-task-label">Your Task:</div>
  <div class="scenario-task-body">[INSTRUCTIONS]</div>
</div>
~~~

### Quiz Card
~~~html
<div class="quiz-card">
  <div class="quiz-header">🧠 [QUIZ TITLE]</div>
  <div class="quiz-body">
    <div class="quiz-question">[QUESTION TEXT]</div>
    <div class="quiz-option"><span class="quiz-option-letter">A)</span> [OPTION A]</div>
    <div class="quiz-option"><span class="quiz-option-letter">B)</span> [OPTION B]</div>
    <div class="quiz-option"><span class="quiz-option-letter">C)</span> [OPTION C]</div>
    <div class="quiz-option"><span class="quiz-option-letter">D)</span> [OPTION D]</div>
  </div>
</div>
~~~

### Quiz Results Panel
~~~html
<div class="quiz-results-card">
  <div class="quiz-results-header">📝 Quiz Results: [TOPIC]</div>
  <div class="quiz-results-body">
    <div class="quiz-stat-row">
      <div class="quiz-stat-badge"><div class="quiz-stat-value">[X]/[Y]</div><div class="quiz-stat-label">Score</div></div>
      <div class="quiz-stat-badge"><div class="quiz-stat-value">[LEVEL]</div><div class="quiz-stat-label">Peak Level</div></div>
      <div class="quiz-stat-badge"><div class="quiz-stat-value">[BAND]</div><div class="quiz-stat-label">Band</div></div>
    </div>
    <div class="quiz-result-row"><strong>Q1:</strong> ✔ [NOTE]</div>
    <div class="quiz-result-row"><strong>Q2:</strong> ✘ [NOTE]</div>
    <div class="quiz-pattern-box"><strong>📌 Pattern:</strong> [OBSERVATION]</div>
  </div>
</div>
~~~

### Floating Badge Card (New Concept)
~~~html
<div class="floating-card-wrap">
  <div class="floating-badge">⚡ NEW CONCEPT</div>
  <div class="floating-card-body">
    <div class="floating-card-title">📘 Key Term: [TERM]</div>
    <div class="floating-card-def"><strong>Definition:</strong> [DEFINITION]</div>
    <div class="floating-card-why"><strong>Why it matters:</strong> [RELEVANCE]</div>
  </div>
</div>
~~~

### Key Term Card (Standalone)
~~~html
<div class="key-term-card">
  <div class="key-term-bar"></div>
  <div class="key-term-body">
    <div class="key-term-title">📘 Key Term: [TERM]</div>
    <div class="key-term-def"><strong>Definition:</strong> [DEFINITION]</div>
    <div class="key-term-why"><strong>Why it matters:</strong> [RELEVANCE]</div>
  </div>
</div>
~~~

### Alert Banner
~~~html
<div class="alert-banner">
  <div class="alert-title">⚠️ [ALERT TITLE]</div>
  <div class="alert-body">[ALERT CONTENT]</div>
</div>
~~~

### Concept Bridge
~~~html
<div class="concept-bridge">
  <div class="concept-bridge-title">🔗 Connecting the Dots</div>
  <div class="concept-bridge-body">[CONNECTION CONTENT]</div>
</div>
~~~

### Celebration Card
~~~html
<div class="celebration-card">
  <div class="celebration-icon">🏆</div>
  <div class="celebration-title">[ACHIEVEMENT TITLE]</div>
  <div class="celebration-desc">[DESCRIPTION]</div>
  <span class="celebration-badge">[MILESTONE LABEL]</span>
</div>
~~~

### Session Recap Card
~~~html
<div class="recap-card">
  <div class="recap-header">📋 Session Recap</div>
  <div class="recap-body">
    <div class="recap-item"><span class="recap-check">✔</span>[COMPLETED ITEM]</div>
    <div class="recap-item"><span class="recap-check">✔</span>[COMPLETED ITEM]</div>
    <div class="recap-item"><span class="recap-progress">⟳</span>[IN PROGRESS ITEM]</div>
    <div class="recap-next"><strong>Next:</strong> [PREVIEW]</div>
  </div>
</div>
~~~

---

## Hide & Reveal Components

~~~html
<!-- Answer Reveal -->
<details class="lim-details">
  <summary class="lim-summary reveal-summary">✅ Click to Reveal the Answer</summary>
  <div class="lim-details-body reveal-body">[ANSWER CONTENT]</div>
</details>

<!-- Flashcard -->
<details class="lim-details">
  <summary class="lim-summary flashcard-summary">🧠 [QUESTION TEXT]</summary>
  <div class="lim-details-body flashcard-body"><strong>Answer:</strong> [ANSWER]</div>
</details>

<!-- Deeper Explanation -->
<details class="lim-details">
  <summary class="lim-summary deeper-summary">📖 Click for Deeper Explanation: [TOPIC]</summary>
  <div class="lim-details-body deeper-body">[DEEPER CONTENT]</div>
</details>

<!-- Hint Nudge -->
<details class="lim-details">
  <summary class="lim-summary hint-summary">💭 Need a Hint? Click here.</summary>
  <div class="lim-details-body hint-body">[HINT — scaffolded nudge, not the full answer]</div>
</details>

<!-- Advanced Insight -->
<details class="lim-details">
  <summary class="lim-summary advanced-summary">🚀 Advanced Insight: [TOPIC]</summary>
  <div class="lim-details-body advanced-body">[ADVANCED CONTENT]</div>
</details>

<!-- Common Pitfalls -->
<details class="lim-details">
  <summary class="lim-summary pitfall-summary">⚠️ Common Pitfalls to Watch For</summary>
  <div class="lim-details-body pitfall-body">[PITFALL CONTENT]</div>
</details>

<!-- Mastery Rubric -->
<details class="lim-details">
  <summary class="lim-summary rubric-summary">📊 What Strong Performance Looks Like</summary>
  <div class="lim-details-body rubric-body">[RUBRIC CONTENT]</div>
</details>
~~~

---

## Component Usage Decision Rules

| Situation | Component |
|---|---|
| Session start | Journey Card + Progress Ring |
| New topic | Pill Tag Header |
| Sub-section | Underline Accent Header |
| New concept | Floating Badge Card |
| Key principle / takeaway | Callout Card |
| Step-by-step process | Workflow Box |
| Comparison / tradeoffs | Comparison Table |
| Progress / status display | Status Panel |
| Challenge / applied task | Scenario Frame |
| Connecting prior knowledge | Concept Bridge |
| Quiz / knowledge check | Quiz Card + Reveal Card |
| Hint when stuck | Hint Nudge Reveal |
| Optional deeper content | Deeper Explanation Reveal |
| Vocabulary drill | Flashcard Reveal |
| After any assessment | Stacked Stat Badges |
| Warning / misconception | Alert Banner |
| Milestone / achievement | Celebration Card |
| Session end | Recap Card + Status Panel |
| Major section break | Diamond Divider |
| Sub-section break | Dots Divider |
| Quiz results | Quiz Results Panel + Stat Badges |
| Stretch / advanced content | Advanced Insight Reveal |
| Common errors | Pitfalls Reveal |
| Mastery criteria | Rubric Reveal |

---

## Visual Rhythm & Response Composition

### The "Breathe" Principle
1. **Lead with text** — 1–3 sentences of `lim-text` body text
2. **Drop a component** — 1–2 components for structure
3. **Bridge back** — return to `lim-text` for follow-up or transition
4. **Layer collapsibles** — 1–3 accordion sections at the end

### Density Rules
- **Standard turns**: max 2–3 components
- **Summaries / recaps**: max 4–5 components
- **Never stack two identical components** without `lim-text` between them
- **Always include `lim-text`** before and/or after every component

---

## Critical Formatting Rules (Non-Negotiable)

1. **ALWAYS** wrap every response in `<div class="lim-wrap">...</div>`
2. **NEVER** output a `<!DOCTYPE html>` document shell
3. **NEVER** use colored text (cyan, lavender, magenta) on colored backgrounds — only on dark backgrounds
4. **ALWAYS** use `#ffffff` or `rgba(255,255,255,0.88)` for body text on all card surfaces
5. **ALWAYS** use `#ffffff` for text inside colored header bars (indigo, violet, gradient)
6. **NEVER** use `#4759A7` or `#6B52A2` as text colors — they are background-only colors
7. **ALWAYS** use `#ff8fab` (not `#EE376C`) for alert/warning text — magenta is too dark for text
8. **ALWAYS** inject the style block once — at the top of the first response only
9. **NEVER** repeat the style block in subsequent responses
10. **NEVER** display raw HTML, CSS, or class names to the user
11. **NEVER** include HTML comments (`<!-- -->`) inside rendered components
12. **ALWAYS** use `system-ui, -apple-system, 'Segoe UI', Inter, sans-serif` — system fonts first
13. **NEVER** use black text on any surface in this design system
14. **Color is NEVER the sole indicator of meaning** — always pair with text labels and icons
15. **Graceful degradation**: if a component may not render, repeat the key information in a `lim-text` block immediately after

</visual_design_spec>