---
name: feedback-form
description: Appends a branded nebulaONE feedback bar to the end of responses, inviting users to submit feature ideas via a survey link. Use when an agent is configured to collect end-of-response feedback. Rotates through six visual designs so the prompt stays fresh.
license: Proprietary.
---

# nebulaONE Feedback Bar

Append **one** feedback bar to the end of a chat response when this skill is enabled. Separate it from the answer with the frosted-glass bar (or one of the six designs below). This is model-agnostic — it applies to whichever model the agent is running.

## Configuration
- Replace `<INSERT_FEEDBACK_FORM_URL_HERE>` with the institution's Microsoft Form URL.
- Default/example form: `https://forms.office.com/r/xeG6JUp4Cz` (used in Design 6 below).
- Brand colors are already applied: navy `#0f2557`, cyan `#00d4ff`, deep cyan `#0099cc`, font `Segoe UI` (see [README.md](README.md)).

## Rotation rules
1. After each response, append **one and only one** of the six designs below.
2. Rotate randomly, but do not repeat a design until all six have been shown.
3. After Design 6, the cycle resets to Design 1.
4. All links open the Microsoft Form in a new window (`target="_blank"`).
5. Maintain nebulaONE branding throughout.

> 💡 Skip the bar on very short utility replies (one-word confirmations) so it doesn't overwhelm the message. Otherwise include it once per substantive response.

---

## Design 1 — Minimal Inline
```html
<div style="margin: 30px 0 0 0; padding-top: 20px; border-top: 2px solid #00d4ff;">
  <div style="max-width: 800px; margin: 0 auto; padding: 15px 20px; background: white; border: 2px solid #e8f4f8; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; gap: 15px;">
    <span style="color: #0f2557; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 14px; font-weight: 500;">Was this helpful?</span>
    <a href="<INSERT_FEEDBACK_FORM_URL_HERE>" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); color: white; padding: 8px 20px; border-radius: 6px; font-weight: 600; font-family: 'Segoe UI', Tahoma, sans-serif; text-decoration: none; font-size: 13px; white-space: nowrap;">Share Feedback</a>
  </div>
</div>
```

## Design 2 — Icon Badge
```html
<div style="margin: 30px 0 0 0; padding-top: 20px; border-top: 3px solid #00d4ff;">
  <div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <a href="<INSERT_FEEDBACK_FORM_URL_HERE>" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, #0f2557 0%, #1a3a6b 100%); color: white; padding: 12px 24px; border-radius: 50px; font-weight: 600; font-family: 'Segoe UI', Tahoma, sans-serif; text-decoration: none; font-size: 14px; box-shadow: 0 4px 12px rgba(15,37,87,0.2);">
      <span style="font-size: 18px;">💬</span>
      <span>Send Feedback</span>
    </a>
    <p style="color: #999; font-size: 11px; margin: 10px 0 0 0; font-family: 'Segoe UI', Tahoma, sans-serif;">Help us improve • <strong style="color: #00d4ff;">nebulaONE</strong></p>
  </div>
</div>
```

## Design 3 — Card with Icon
```html
<div style="margin: 30px 0 0 0; padding-top: 20px; border-top: 3px solid #00d4ff;">
  <div style="max-width: 800px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #f8fbfd 0%, #e8f4f8 100%); border-radius: 10px; border-left: 4px solid #00d4ff; text-align: center;">
    <div style="font-size: 36px; margin-bottom: 10px;">✨</div>
    <p style="color: #0f2557; margin: 0 0 15px 0; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 14px; font-weight: 500;">Help shape the future of nebulaONE</p>
    <a href="<INSERT_FEEDBACK_FORM_URL_HERE>" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); color: white; padding: 10px 28px; border-radius: 6px; font-weight: 600; font-family: 'Segoe UI', Tahoma, sans-serif; text-decoration: none; display: inline-block; font-size: 13px; box-shadow: 0 3px 10px rgba(0,212,255,0.3);">Share Your Ideas</a>
  </div>
</div>
```

## Design 4 — Split Layout
```html
<div style="margin: 30px 0 0 0; padding-top: 20px; border-top: 3px solid #00d4ff;">
  <div style="max-width: 800px; margin: 0 auto; padding: 18px 25px; background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); display: flex; align-items: center; justify-content: space-between; gap: 20px;">
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px;">💭</div>
      <div>
        <p style="color: #0f2557; margin: 0; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 13px; font-weight: 600;">Have feedback?</p>
        <p style="color: #666; margin: 0; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 11px;">We'd love to hear from you</p>
      </div>
    </div>
    <a href="<INSERT_FEEDBACK_FORM_URL_HERE>" target="_blank" rel="noopener noreferrer" style="background: #0f2557; color: white; padding: 10px 22px; border-radius: 6px; font-weight: 600; font-family: 'Segoe UI', Tahoma, sans-serif; text-decoration: none; font-size: 13px; white-space: nowrap;">Give Feedback →</a>
  </div>
</div>
```

## Design 5 — Compact Pill
```html
<div style="margin: 30px 0 0 0; padding-top: 20px; border-top: 2px solid #e0e0e0;">
  <div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <a href="<INSERT_FEEDBACK_FORM_URL_HERE>" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 8px; background: white; color: #0f2557; padding: 10px 24px; border-radius: 50px; font-weight: 600; font-family: 'Segoe UI', Tahoma, sans-serif; text-decoration: none; font-size: 13px; border: 2px solid #00d4ff;">
      <span>📝</span>
      <span>Feedback</span>
    </a>
  </div>
</div>
```

## Design 6 — Frosted Glass Strip
```html
<div style="margin: 30px 0 0 0; padding-top: 20px; position: relative;">
  <div style="max-width: 900px; margin: 0 auto; position: relative;">
    <!-- Decorative separator dots -->
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
      <div style="flex: 1; height: 2px; background: linear-gradient(to right, transparent, #00d4ff, transparent);"></div>
      <div style="width: 6px; height: 6px; background: #00d4ff; border-radius: 50%;"></div>
      <div style="flex: 1; height: 2px; background: linear-gradient(to right, transparent, #00d4ff, transparent);"></div>
    </div>
    <!-- Frosted glass feedback bar -->
    <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 8px; padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; gap: 20px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);">
      <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 20px;">💡</span>
        <span style="color: #0f2557; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 13px; font-weight: 400;">Got ideas for new features? We'd love your input — it goes straight to our dev team.</span>
      </div>
      <a href="https://forms.office.com/r/xeG6JUp4Cz" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); color: white; padding: 10px 24px; border-radius: 20px; font-weight: 600; font-family: 'Segoe UI', Tahoma, sans-serif; text-decoration: none; font-size: 13px; white-space: nowrap; box-shadow: 0 2px 8px rgba(0, 212, 255, 0.3);">Take Quick Survey →</a>
    </div>
  </div>
</div>
```
