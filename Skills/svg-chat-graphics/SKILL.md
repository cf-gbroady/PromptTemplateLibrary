---
name: svg-chat-graphics
summary: Create accessible, secure SVG graphics and present them reliably in chat with attachment-based rendering and fallbacks.
description: Use when a user asks to create, improve, validate, attach, or display an SVG graphic inline in chat, including banners, diagrams, cards, infographics, or troubleshooting visuals.
---

# SVG Chat Graphics

## Purpose

Create polished, self-contained SVG graphics using current SVG and accessibility practices, then present them in chat through the most reliable rendering path available. Treat successful inline display as a client capability, not something the SVG author can absolutely guarantee.

## When to Use

- The user asks for an SVG banner, infographic, diagram, card, icon, flow, timeline, or technical visual.
- The user asks to display an existing SVG inline in chat.
- The user asks why an SVG is not rendering or how to improve SVG compatibility.
- The user wants an SVG that is accessible, responsive, secure, portable, or easy to share.

## Do Not Use When

- The user primarily needs a photograph, photorealistic illustration, or raster image editing.
- The requested output is mainly an interactive web application; use HTML instead.
- The user explicitly requires PNG, JPEG, WebP, or another non-SVG format only.
- The SVG would include untrusted code or markup that cannot be sanitized.

## Inputs to Consider

- The visual's purpose, audience, dimensions, aspect ratio, and destination.
- Required text, branding, colors, logo assets, and accessibility description.
- Whether the SVG is new or an existing file that must be revised.
- Available tools for text-artifact creation, file attachment, code execution, validation, rasterization, or image preview.
- Whether the chat client supports SVG attachments as inline Markdown images.

## Research and Grounding

Use these sources when standards or platform behavior need verification:

- W3C SVG 2: https://www.w3.org/TR/SVG2/ and https://svgwg.org/svg2-draft/
- W3C SVG accessibility support: https://w3c.github.io/svgwg/svg2-draft/access.html
- MDN SVG `<title>`: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/title
- MDN ARIA `img` role: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/img_role
- Anthropic Agent Skills examples and specification: https://github.com/anthropics/skills
- OpenAI file and data-analysis capabilities, when relevant to the host product: https://help.openai.com/en/articles/8437071-chatgpt-code-interpreter and https://help.openai.com/en/articles/8555545-file-uploads-with-gpts-and-advanced-data-analysis-in-chatgpt

Research findings that govern this skill:

- A skill should be self-contained, narrowly triggered, and operational rather than explanatory.
- SVG 2 is the current standards direction, but broad chat compatibility improves when graphics use a conservative, static subset supported by SVG 1.1-era renderers.
- Meaningful SVGs need an accessible name; complex graphics benefit from a longer description.
- SVG is XML-based active content, so generated chat graphics must exclude scripts, event handlers, `foreignObject`, unsafe links, and external dependencies.
- A file-generation or attachment capability improves reliable chat display, but code execution is not inherently required to author SVG markup.

## Workflow

1. **Interpret the request**
   - Determine the visual type, message hierarchy, audience, target size, and intended chat or document surface.
   - Ask one consolidated clarification only when missing information would materially change the result.

2. **Inspect capabilities before generating**
   - Identify whether a text-artifact/file tool can create and attach an `.svg` file.
   - Identify whether code execution is available for XML validation, raster preview, or PNG fallback.
   - Do not claim inline display is guaranteed. Rendering ultimately depends on the chat client, content sanitizer, MIME handling, and attachment URL.

3. **Choose the delivery path**
   - Preferred: create a real `.svg` attachment with a text-artifact or file tool, then embed the exact returned attachment URL using Markdown image syntax.
   - Alternate: if the platform explicitly supports raw inline SVG, include sanitized SVG markup only when requested and safe.
   - Fallback: if SVG preview is unsupported, provide the `.svg` download and, when rasterization is available, create a PNG preview for inline display.
   - Never invent an attachment path, generated-image URL, or file identifier.

4. **Design the composition**
   - Use a clear visual hierarchy: headline, short explanatory line, primary content, and optional footer.
   - Keep text concise and readable at the intended display size.
   - Use grids, alignment, spacing, and restrained color consistently.
   - Do not rely on color alone to communicate status or meaning.

5. **Create a self-contained SVG**
   - Start with a root element similar to:

     `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="svg-title svg-desc" lang="en" xml:lang="en">`

   - Put `<title>` first for backward compatibility, followed by `<desc>`.
   - Use unique IDs for gradients, masks, clip paths, filters, titles, and descriptions.
   - Include both `viewBox` and explicit `width`/`height`; use `preserveAspectRatio="xMidYMid meet"` when useful.
   - Prefer basic elements: `rect`, `circle`, `ellipse`, `line`, `polyline`, `polygon`, `path`, `text`, `tspan`, `g`, `defs`, gradients, simple clip paths, and restrained filters.
   - Use system font stacks such as `Inter, Arial, sans-serif`; do not depend on downloaded fonts.
   - Position text explicitly. SVG does not provide dependable automatic paragraph wrapping across renderers.
   - Escape XML-sensitive characters such as `&`, `<`, and `>` in text content.
   - Keep all styles inline or in a local `<style>` block. Avoid external stylesheets.
   - Do not reference remote images, fonts, scripts, or styles. If a raster asset is essential, embed it only when the host and size constraints permit.

6. **Apply compatibility rules**
   - Favor static graphics over animation for chat.
   - Avoid `foreignObject`, JavaScript, event attributes, HTML embedding, external `<use>` references, CSS imports, and unsupported experimental features.
   - Avoid dependence on hover, focus, or interaction for essential information.
   - Use moderate filter effects; excessive blur, blend modes, or complex masks may render inconsistently.
   - Keep IDs, URLs, and clipping references internally consistent.

7. **Apply accessibility rules**
   - For meaningful graphics, use `role="img"` with `aria-labelledby` referencing `<title>` and `<desc>`.
   - Make `<title>` a short accessible name and `<desc>` a useful summary of the visual's message.
   - Set `lang` and `xml:lang` when the SVG contains text.
   - Maintain readable contrast and a logical reading order in the source.
   - For purely decorative SVGs, omit misleading descriptions and use `aria-hidden="true"` or a presentation role as appropriate.
   - Do not assume visible SVG text alone supplies a sufficient alternative for every assistive-technology combination.

8. **Apply security rules**
   - Treat SVG as XML/code, not as inert pixels.
   - Never include `<script>`, `foreignObject`, `iframe`, embedded HTML, `on*` event attributes, `javascript:` URLs, DTDs, XML entities, or external resource requests.
   - Do not inline untrusted user-supplied SVG without sanitization.
   - If the host application serves user SVGs, recommend SVG-specific sanitization, restrictive response headers, and image-context or raster previews.

9. **Validate before delivery**
   - Confirm the document is well-formed XML.
   - Confirm the root has the SVG namespace, a valid `viewBox`, and nonzero dimensions.
   - Check for duplicate or unresolved IDs and references.
   - Check that no prohibited active-content elements or attributes are present.
   - Confirm the accessible name and description are present when the image is meaningful.
   - Confirm text fits within its intended boxes and no critical elements are clipped.
   - When code execution is available, parse the XML and optionally render or rasterize a preview.

10. **Create and attach the file**
    - Use a meaningful lowercase filename with underscores or hyphens, such as `project_status_summary.svg`.
    - Create the SVG as a text/code artifact with XML or SVG syntax highlighting when the tool supports it.
    - Use the attachment URL returned by the tool; never assume a local path will display to the user.

11. **Display in chat**
    - Attempt Markdown image embedding with the exact attachment URL:

      `![Concise description of the graphic](ATTACHMENT_URL)`

    - Also provide a normal download link when useful:

      `[Download the SVG](ATTACHMENT_URL)`

    - Use a concise alt string in Markdown even though the SVG also contains `<title>` and `<desc>`.
    - If the client does not render SVG inline, do not repeatedly post identical embeds. Move to the fallback path.

12. **Fallback when inline rendering fails**
    - Keep the SVG as the editable/source-quality deliverable.
    - If rasterization is available, create a PNG from the SVG and display the PNG inline.
    - If rasterization is unavailable, provide the SVG download and briefly explain that the current client does not preview it.
    - Do not claim Code Interpreter, Data Analysis, or file tools force the client to render SVG inline; they only help create, validate, attach, or convert the file.

## Tool Use

### Text-artifact or file-creation tool

Use this whenever available to create a genuine `.svg` attachment. This is the most important capability for reliable chat delivery because it provides a real file object and authoritative attachment URL.

When updating an existing SVG artifact, create a new version through the tool's update/version mechanism rather than creating a confusing duplicate, when the platform supports versioning.

### Code Interpreter or Data Analysis

Code execution is **recommended but not mandatory**.

Use it for:

- XML parsing and structural validation.
- Programmatic layout calculations.
- Checking IDs and URL references.
- Detecting prohibited elements or attributes.
- Rasterizing SVG to PNG when supported.
- Creating both SVG and PNG deliverables from the same source.

Do not require it merely to write SVG markup when a text-artifact/file tool is available.

If only Code Interpreter can create downloadable files in the host runtime, then it becomes operationally necessary for attachment creation, not for SVG authorship itself.

### Image-generation tool

Do not use image generation by default for diagrams, text-heavy banners, interface-like cards, or technical infographics that can be authored deterministically in SVG.

Use image generation only when the user wants painterly, photorealistic, highly illustrative, or generative artwork. If the final delivery must be SVG, do not falsely label a raster image as vector art.

### Web research

Use current primary sources when the user asks about standards, browser behavior, accessibility, sanitization, MIME configuration, CSP, or product-specific rendering behavior. Prefer W3C, MDN, official platform documentation, and maintained source repositories.

Do not browse merely to invent visual content that the user already supplied.

## Output Requirements

For each SVG creation or update:

- Produce a valid `.svg` file when a file/artifact capability is available.
- Include a short accessible title and useful description inside meaningful SVGs.
- Use a self-contained, static, responsive, and conservative SVG feature set.
- State whether XML validation or rendering validation was performed.
- Attempt inline display using the exact returned attachment URL when the chat client supports Markdown images.
- Provide a download link when inline rendering is uncertain or the user may need the source file.
- Provide or offer a PNG fallback if the SVG does not preview.
- Keep the response concise; do not dump the full SVG source unless the user requests it or no file tool is available.

Recommended response pattern:

```markdown
Created the SVG and validated it as well-formed XML.

![Short description](ACTUAL_ATTACHMENT_URL)

[Download the SVG](ACTUAL_ATTACHMENT_URL)

If your client does not preview SVG, I can also provide a PNG version.
```

Replace placeholders only with real tool-returned URLs.

## Guardrails

- Never promise that SVG will render inline in every chat client.
- Never invent file URLs, attachment IDs, MIME types, or validation results.
- Never include secrets, credentials, private customer data, or unrelated personal data in visible text, metadata, filenames, IDs, or comments.
- Never include active content, executable scripts, unsafe links, or external dependencies in chat-bound SVGs.
- Do not reproduce proprietary logos, copyrighted artwork, or brand assets unless the user supplied them or has the right to use them.
- Preserve user-provided factual text exactly unless asked to edit it.
- Do not overwrite an uploaded SVG; create a new version or output file.
- Do not claim accessibility compliance based solely on the presence of `<title>` and `<desc>`; accessibility also depends on contrast, reading order, semantics, host embedding, and assistive-technology support.
- Do not assume that raw SVG markup pasted into Markdown will render. Prefer attachment-based delivery.
- Do not expose internal local file paths in the user-facing response when a friendly filename or attachment link is available.

## Failure Handling

### No file or artifact tool

- Return SVG source in a fenced `xml` block only if the user needs immediate output.
- Explain that the source must be saved as an `.svg` file before reliable embedding can be attempted.
- Do not invent a download link.

### SVG attachment exists but does not preview

- Provide the download link.
- Create a PNG fallback if code execution and a renderer are available.
- State that the limitation is in the current client or attachment renderer, not necessarily the SVG file.

### SVG is invalid

- Do not attach or embed it as complete.
- Correct XML errors, duplicated IDs, invalid references, overflow, or unsafe elements.
- Revalidate before delivery.

### User supplies untrusted SVG

- Treat it as potentially active content.
- Inspect and sanitize it before inline display.
- If sanitization cannot be performed confidently, offer rasterization or a security review instead.

### Rasterization is unavailable

- Deliver the SVG source file and explain that a PNG fallback could not be generated in the current runtime.
- Do not claim a visual preview was performed.

## Quality Checklist

Before finishing, verify:

- The requested purpose and key message are visually clear.
- The SVG is well-formed XML.
- Root namespace, `viewBox`, dimensions, and aspect ratio are valid.
- Text remains readable at the intended display size.
- `<title>` and `<desc>` are meaningful and correctly referenced, or the SVG is intentionally decorative.
- Contrast and non-color cues are sufficient.
- Fonts and resources are self-contained or safely fall back.
- No scripts, events, `foreignObject`, DTDs, unsafe URLs, or external dependencies are present.
- IDs are unique and every reference resolves.
- A real attachment/file URL was used for Markdown display.
- A download link or PNG fallback is available if inline SVG rendering is unsupported.
- The response does not claim that tools or client behavior can guarantee universal rendering.
