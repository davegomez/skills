# UI framework

Use clap for every CLI, ratatui for full-screen TUIs, and GPUI for desktop apps.

**Desktop: GPUI**

GPUI is a hybrid immediate-mode and retained-mode, GPU-accelerated UI framework from Zed Industries. It works well for Zed. It is not a stable general-purpose framework: it has frequent breaking changes, and it needs the latest stable Rust.

The Zed repository is the official GPUI project and the source of truth: the `crates/gpui` crate in `zed-industries/zed`, its README, and gpui.rs. Take each fact about the API from the source at the tag that you pin. Where gpui.rs and the source at the tag do not agree, the source is correct.

| Package | Maintainer | Use |
| --- | --- | --- |
| `gpui` and `gpui_platform` from git | Zed Industries | Always. Pin the tag in the workspace manifest (see [architecture](architecture.md)). |
| `gpui` on crates.io | Zed Industries | Do not use. Use the git dependency at the pinned tag. |
| `gpui-pre` and GPUI Kit on crates.io | Longbridge | Reference only. `gpui-pre` is a copy of Zed `main`. GPUI Kit depends on `gpui-pre`, not on Zed's `gpui`, so it does not work with the git dependency. |

- **Platforms:** macOS (Metal), Linux (wgpu, on X11 and Wayland), and Windows (Direct3D 11). This skill does not cover the `gpui_web` (WebAssembly) and `gpui_ios` crates.
- **Components:** The `gpui` crate has elements such as `div`, `img`, `svg`, `canvas`, `list`, `uniform_list`, and text. It has no ready button, text input, or checkbox. Write these components on the GPUI elements. GPUI Kit has ready components, but only for `gpui-pre`.

**GPUI accessibility**

- GPUI uses AccessKit, which maps to UI Automation (Windows), NSAccessibility (macOS), and AT-SPI (Linux).
- Accessibility is opt-in per element. Screen readers see an element only if the app gives it an `id` and a `role`. A text child gives the node no name. Set the name with `.aria_label(...)`.
- Before you build a rich text or hypertext view, check in the AccessKit README that its adapters support rich text and hypertext.
- Budget for manual screen-reader tests on all 3 desktop platforms. The rules per need are in [accessibility](accessibility.md).

**CLI and terminal UX**

- Use `clap` with the derive API.
- Use `ratatui` only for interactive full-screen tools. Always give a non-interactive subcommand for the same task.
- If `NO_COLOR` is set and not empty, print no ANSI color.
- Disable color and animation when stdout is not a terminal.
- Give `--json` output for every command that prints data.
