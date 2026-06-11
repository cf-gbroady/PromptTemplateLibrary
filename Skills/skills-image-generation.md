---
name: image-generation
description: Guides creation of high-quality, on-brand generated images. Trigger when a user asks to make, generate, design, illustrate, or visualize an image, illustration, icon, banner, diagram concept, or graphic. Covers prompt construction, aspect ratios, brand style, text-in-image limits, alt text, and safe/appropriate use.
license: Proprietary.
---

# Image Generation

nebulaONE is multimodal and can generate images. This skill makes generated visuals **useful, on-brand, accessible, and appropriate**. Model-agnostic.

## Before generating
- **Confirm intent** for non-trivial requests: subject, purpose (slide, banner, hero, icon), mood, and aspect ratio. A 10-second clarification beats a wrong render.
- **Choose the right tool:** for **data** (real numbers → charts) use [skills-data.md](skills-data.md) / matplotlib, **not** image generation. Generate images for concepts, scenes, illustrations, and decorative/brand visuals.
- **Don't generate** identifiable real people (especially students/patients), logos you don't own, copyrighted characters, or anything that could mislead in a clinical/academic context. See [skills-compliance-privacy.md](skills-compliance-privacy.md).

## Writing a strong prompt
Layer these elements:
1. **Subject** — what's in frame, concretely.
2. **Composition** — close-up / wide, point of view, focal point, negative space for text.
3. **Style** — photographic, flat vector, isometric, watercolor, 3D render, line art.
4. **Lighting & mood** — soft daylight, studio, dramatic, optimistic, clinical-clean.
5. **Palette** — for brand visuals, specify nebulaONE colors: deep navy `#0f2557`, cyan `#00d4ff`, indigo `#9381ff` on clean white/light backgrounds.
6. **Constraints** — "no text," "lots of headroom for a title," aspect ratio.

**Example:** "Flat-vector illustration of a university campus network, isometric, deep-navy and cyan palette on white, generous empty space top-right for a title, modern and optimistic, no text."

## Aspect ratios (pick to fit the use)
- **16:9** — slide backgrounds, hero banners, video thumbnails.
- **1:1** — avatars, icons, social tiles.
- **4:3 / 3:2** — document figures.
- **9:16** — mobile/story.

## Brand style defaults
- Clean, modern, professional; lots of white space; flat or soft-3D vector for product/edu/health contexts.
- nebulaONE palette as the dominant scheme unless the user asks otherwise.
- Consistent style across a set (don't mix photoreal and cartoon in one deck).

## Text in images
- Generators render text unreliably. **Don't** ask the model to bake in headlines, labels, or data.
- Instead, leave **negative space** and overlay real text in the slide/doc (PowerPoint textbox, HTML caption).

## After generating
- Provide **alt text** describing function and content (see [skills-accessibility.md](skills-accessibility.md)).
- Offer a quick **iteration path**: "Want it wider, lighter background, or more abstract?"
- If placing into a deck/doc, hand off to [skills-pptx.md](skills-pptx.md) / [skills-docx-v2.md](skills-docx-v2.md) for sizing and centering.

## Guardrails
- No depiction of real, identifiable individuals without basis; no sensitive/clinical imagery that could be mistaken for real medical guidance.
- Keep content appropriate for an education/enterprise audience.
