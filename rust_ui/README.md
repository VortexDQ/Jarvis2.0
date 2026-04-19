# Jarvis Rust UI

This folder contains a Rust + Slint UI launcher for the Jarvis interface.

Run from `jarvis_app` with:

```bash
cd rust_ui
cargo run
```

The UI definition is in `rust_ui/src/jarvis.slint` and the Rust entrypoint is `rust_ui/src/main.rs`.

The UI includes:
- neon glass style command cards
- mute and PC-access buttons
- a radial status core
- a CSS-inspired dark theme
