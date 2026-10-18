# AI agent instructions

This repository sets up Manim in a headless Linux sandbox. Start with
[`docs/sandbox-guide.md`](docs/sandbox-guide.md), not the Colab notebook commands
in the reference project. Keep documentation in English.

## Selection contract

1. Identify the requested engine: **ManimGL** or **ManimCE**. Ask if unclear.
2. Install only that engine. Do not install both unless the user asks for both.
3. LaTeX is optional. If the user says only “LaTeX”, ask **slim or full** before
   running either extension. Do not silently install full TeX Live.
4. Both engine installers must call the sibling `font.sh` helper. Never remove
   this behavior or replace it with a success marker.
5. Keep font binaries local: cached fonts, licenses and checksums belong in
   `<workspace>/fonts/`, which is ignored by Git but kept in the workspace.

| User intent | Run from the repository directory |
|---|---|
| ManimGL only | `bash manimgl.sh` |
| ManimCE only | `bash manimce.sh` |
| ManimGL + slim LaTeX | `bash manimgl.sh && bash latex_slim.sh` |
| ManimGL + full LaTeX | `bash manimgl.sh && bash latex_full.sh` |
| ManimCE + slim LaTeX | `bash manimce.sh && bash latex_slim.sh` |
| ManimCE + full LaTeX | `bash manimce.sh && bash latex_full.sh` |

## Before execution

- Check OS, Python version, privilege availability and free disk space. These
  installers target Debian/Ubuntu and Python 3.11+; only Debian 13 has been
  verified here. Do not pretend the same commands support macOS, Windows,
  Termux or a Colab notebook API.
- Keep all five scripts together. Use an existing persistent checkout instead
  of cloning repeatedly into new folders and losing access to the font cache.
- Default workspace = installer directory. If reusing another workspace, pass
  the same absolute `MANIM_WORKSPACE` value to every installer/helper.
- In agent tools, working directories and exported variables may not survive
  between calls. Set `cwd` for each call or use absolute paths and explicit env.
- Review `--dry-run` when needed. A dry-run shows intent, not proof of a working
  installation. No credentials are needed for this public setup repository.

## Install and restore

- Use the provided scripts. Do not bypass the isolated virtual environments
  with global pip or `--break-system-packages`.
- Run APT-using installers sequentially. Do not launch full TeX Live as part of
  routine tests; it is a multi-GB optional action.
- Recheck actual runtime state after a sandbox reset. APT packages and `.venv/`
  may disappear even when source files and the fonts remain.
- Never delete `fonts/` just to “clean up”. Do not use `git clean -fdx`.
- The helper verifies local files and registration; repeated calls are safe.
  Missing registration is repaired from disk. Only a missing/corrupt font family
  needs another download.
- Store persistent work under the provider's supported workspace root. On
  Arena/E2B that is `/home/user`; do not assume `/tmp`, `.cache` or `.venv` persist.

## Render correctly

- GL import: `from manimlib import *`. CE import: `from manim import *`.
- GL: use generated `bin/manimgl` and **`-w`** for file rendering. The wrapper
  starts Xvfb if `DISPLAY` is absent; software OpenGL is the tested default.
- CE: use generated `bin/manim` (alias `bin/manimce`), normally `-ql`.
- Do not claim GPU acceleration from the presence of a flag. Hardware rendering
  must be verified separately. No GPU or Colab warm-mode implementation is bundled.
- GL slim TeX requires `basic`, which `bin/manimgl` selects via the generated
  profile. A custom `--config_file` replaces that selection; ensure it also uses
  a compatible template. Direct GL calls should set `template="basic"`.
- Use `Text(..., font="CMU Serif")` for Computer Modern Unicode Serif and
  `Text(..., font="Noto Serif Bengali")` for Bengali. These names do not select
  the font used inside `MathTex`/`Tex` automatically.
- In GL, use `Group`, not `VGroup`, when combining GlowDot/DotCloud objects with
  other objects. Use `Tex` for math, `TexText` for mixed text/math.

## Verify before saying “ready”

Run the selected CLI's `--version`, that environment's `python -m pip check`, and
`bash font.sh --check` with the same workspace. Render the selected engine's
`FontsOnly` example. If LaTeX was requested, also render `FontsAndMath` and check
that an actual non-empty MP4 exists. See the guide for exact commands.

Report:

- selected engine and version;
- LaTeX selection, or “not requested” (do not remove an existing TeX installation);
- whether fonts were downloaded, reused or re-registered;
- checks actually run, their outcome and the output path;
- any errors or untested features, without inventing successful results.

## Repository changes

- Preserve the five-script separation, `--help`, side-effect-free `--dry-run`,
  automatic fonts and isolated environments.
- Run `python3 -m unittest discover -s tests -v` and `shellcheck *.sh` after edits.
- Never commit `token.md`, PATs, `.env`, credentials, font binaries, virtual
  environments, caches, generated wrappers/profiles or rendered videos.
- Review the staged file list and diff before commits. `.gitignore` is not a
  substitute for a secret scan and does not remove already-tracked secrets.
- Push only when the user authorizes it. Never place credentials in remote URLs,
  example commands, documentation, Git history or public issue logs.
- Do not invent a project-wide license for upstream-derived material. Licensing
  and attribution are described in `docs/sources-and-licensing.md`.
