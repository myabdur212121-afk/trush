# Troubleshooting

Return to the [sandbox guide](sandbox-guide.md) for the normal setup order.
Do not respond to one failed render by installing both engines or full TeX Live.

## Installation and Python

| Symptom | Likely cause / action |
|---|---|
| `Required helper font.sh must be beside ...` | Keep all five scripts together; clone the repository rather than copying one engine installer alone. |
| `apt-get` unavailable | This is not a supported Debian/Ubuntu environment. Do not substitute unrelated platform commands blindly. |
| `sudo: a password is required` | Missing packages need root or a non-interactive sudo session. Resolve privileges before continuing. |
| Python 3.11+ required | Select a compatible interpreter with `PYTHON_BIN=/path/to/python3`. An old distro's default Python may be too old. |
| `externally-managed-environment` | Global pip was used instead of the installer. Use the provided isolated venv; do not add `--break-system-packages`. |
| Pango/Cairo wheel build fails | Read the build error. The scripts request compiler, pkg-config, Cairo and Pango development packages; confirm APT completed successfully. |
| APT lock is held | Another package operation is active. Let it finish; run installers sequentially. Do not delete lock files to bypass a running APT process. |
| Generated command says runtime is missing | The sandbox probably reset. Rerun the selected engine installer. |
| `No module named manimlib` / `manim` | Wrong environment or engine. GL uses `.venv/manimgl` and `manimlib`; CE uses `.venv/manimce` and `manim`. |

## ManimGL on a headless machine

Use **`bin/manimgl`**, not just the entry point inside the venv, for the managed
headless path. The wrapper supplies Xvfb when `DISPLAY` is absent. Keep **`-w`**
to write a file; interactive window previews are not part of the sandbox setup.

```bash
./bin/manimgl examples/check_manimgl.py FontsOnly -w -l -c '#000000' --video_dir videos/gl
```

- **`XOpenDisplay`, display, or OpenGL context error:** confirm Xvfb/Mesa were
  installed by `manimgl.sh`. An exported but invalid `DISPLAY` bypasses the
  wrapper's no-display branch; if there is truly no display, run with
  `env -u DISPLAY ./bin/manimgl ...`.
- **Missing `pkg_resources`:** GL 1.7.2 still imports this API. Rerun the installer
  to restore its tested `setuptools==80.9.0` pin.
- **`pkg_resources` deprecation warning:** expected with the pinned stable GL;
  this warning is not the same as a failed import.
- **Missing `audioop` on Python 3.13+:** the installer supplies `audioop-lts` for
  pydub; check that the scene is using the GL environment.
- **No GPU / slow render:** software Mesa is the tested fallback. Setting
  `LIBGL_ALWAYS_SOFTWARE=0` does not create a GPU or prove acceleration. This
  repository does not ship the Colab package's GPU/warm-mode API.
- **Gray background:** add `-c '#000000'` for black.
- **`VGroup` error involving `GlowDot`/`DotCloud`:** use `Group` for heterogeneous
  objects; `VGroup` requires compatible vectorized objects.

## LaTeX and templates

| Symptom | Action |
|---|---|
| `latex`, `xelatex` or `dvisvgm` missing | Run the requested LaTeX extension. Engine-only setup intentionally does not install TeX. |
| `standalone.cls` missing | The selected extension did not finish; it is provided by the extra LaTeX package set, not merely the base engine. |
| `tipa.sty` missing | Rerun the extension; it installs the real distro `tipa` package. Do not create a dummy style file. |
| `dsfont.sty` or `calligra.sty` missing with slim | You are using a full template. Use the GL wrapper's basic profile, explicitly choose `template="basic"`, or request full TeX. |
| Basic profile is ignored | A custom `--config_file` or explicit template in the scene overrides it. Check those settings and use the same `MANIM_WORKSPACE` for engine/TeX scripts. |
| GL `Missing } inserted` with mixed text and `$...$` | `Tex` is math-oriented; use `TexText` for mixed text/math. |
| Bengali characters fail in ordinary TeX | Use `Text(..., font="Noto Serif Bengali")`, or a XeLaTeX/fontspec template. Installing text fonts does not automatically change the TeX compiler/template. |

Full TeX Live is intentionally optional and large. Do not install it as a hidden
repair step. Running slim after full does not remove the larger packages.

For a small Bengali PDF after an engine and LaTeX setup:

```bash
mkdir -p videos/pdf
xelatex -interaction=nonstopmode -halt-on-error -output-directory=videos/pdf examples/bengali.tex
```

## Fonts and persistence

Start with the helper, not an assumption based on `fc-match` fallback output:

```bash
bash font.sh --check
bash font.sh
```

Pass the same `MANIM_WORKSPACE` used by the engine if it is not the default.

- **The helper says “Already saved and registered”:** correct; no download is
  needed. Repeated engine setups call the helper but skip the installation work.
- **Fonts download again:** check that the original `fonts/` directory and its
  checksums still exist, and that a different workspace was not selected. A
  missing/corrupt family is deliberately repaired with a fresh download.
- **A new sandbox lost registration:** saved fonts can be re-registered without
  downloading if Fontconfig is installed. System packages themselves may still
  need APT/network restoration.
- **Archive hash mismatch:** stop. Do not remove the integrity check or silently
  replace the expected hash. Inspect the upstream release and investigate first.
- **An existing system font wins `fc-match`:** the helper verifies registration
  of its saved files without forcibly removing your other fonts. Duplicate
  families may influence Fontconfig selection.
- **Git does not list `fonts/`:** expected; font binaries are intentionally
  ignored by Git. They remain local workspace data.
- **Fonts disappeared after cleanup:** `git clean -fdx`, deleting the checkout,
  or provider snapshot limits may remove them. Do not store the only copies in
  `.cache`, `.local`, `/tmp` or a virtual environment.

## Report a reproducible problem

Include OS, Python version, selected engine/TeX profile, the exact command, and a
small failing scene. Include only sanitized log excerpts. Never attach a PAT,
`.env`, credential file, private repository URL containing credentials, or a
large runtime/cache folder. See [SECURITY.md](../SECURITY.md).
