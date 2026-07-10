# Runtime Setup

1. Call `codex_app__load_workspace_dependencies` before running presentation scripts.
2. Use the returned bundled Node and Python binaries. Do not assume `/usr/bin/python3`, `/usr/local/bin/python3`, or the shell-default `node` contains presentation dependencies.
3. Initialize an Artifact Tool workspace with the Presentations skill setup script. Run `create_base_deck.mjs`, `inspect_pptx.mjs`, and `render_compare.mjs` with that workspace as the current working directory so their `createRequire(process.cwd())` resolution finds `@oai/artifact-tool` and `sharp`.
4. Run `render_slides.py` and `slides_test.py` with the bundled Python returned by workspace dependency discovery. Do not install `pdf2image`, Pillow, or other packages globally as a first response to an import error.
5. Use the bundled LibreOffice/soffice path for headless compatibility checks.
6. Use Computer Use for the final Microsoft PowerPoint open/save/close/reopen test. Do not use AppleScript or shell `open` as a substitute for UI confirmation.

If a module cannot be resolved, first verify the current workspace and runtime binary. Only add a local workspace dependency after confirming it is genuinely absent from the bundled runtime.
