---
name: google-stitch-integration
description: Integration protocol for Google Stitch. Sync designs, extract design tokens, and apply design systems to the codebase.
---

# Google Stitch Integration Protocol

## 0. Active Design Context (MANDATORY)
- **Primary Design Source**: `projects/105516963869461134` (Nexus Multi-Entity Dashboard).
- **Protocol**: Whenever the user mentions "Stitch", "Design", or requests UI updates, the Agent MUST automatically consider this project as the "Source of Truth".
- **Auto-Sync**: Use `mcp_stitch_get_project` on this ID to refresh design tokens whenever a structural UI change is requested.

## I. Discovery & Synchronization

When a user mentions a project name or requests a UI update based on a design:
1.  **Project Search**: Use `mcp_stitch_list_projects` if the source is unknown. Otherwise, default to Project `105516963869461134`.
2.  **Design Extraction**: Use `mcp_stitch_get_project` to retrieve:
    - **`designTheme`**: Primary colors, fonts, and roundness.
    - **`designMd`**: Detailed design documentation.
    - **Screenshots**: View the intended layout from `thumbnailScreenshot`.

## II. Mapping Stitch to Code

The AI must map Stitch tokens to the project's CSS variables:
- `primary`: Map to `--primary`.
- `surface-container-lowest`: Map to card background.
- `roundness`: Map to `--radius-lg/md/sm`.
- `font`: Import and set in `:root`.

## III. Layout Interpretation

When building a new module:
1.  Check the "Master Screen" (e.g., Nexus Multi-Entity Dashboard) in Stitch.
2.  Analyze the **Editorial Layout** (Asymmetry, Spacing, Typography hierarchy).
3.  Replicate the exact design tokens into the HTML/CSS of the current Django project.

## IV. UI Editing Workflow

If requested to "edit screen like Nexus":
1.  Analyze the target screen in Stitch.
2.  Update the corresponding local template (e.g., `user_list.html`).
3.  Verify that the local implementation matches the Stitch `designMd` (e.g., "No-Line Rule").
