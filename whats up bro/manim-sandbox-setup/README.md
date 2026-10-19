# Manim Sandbox Setup

**Choose an engine. Add LaTeX only when needed. Download fonts once.**

Independent Bash installers for **ManimGL** and **Manim Community**, built for
headless Debian/Ubuntu sandboxes. Includes persistent **CMU Serif** and
**Noto Serif Bengali** font caching, isolated Python environments, small render
examples, and a step-by-step guide for people and AI agents.

**[Sandbox guide](docs/sandbox-guide.md)** · **[AI instructions](AGENTS.md)** ·
**[Troubleshooting](docs/troubleshooting.md)** · **[Validation](docs/validation.md)**

> **For AI agents:** read [`AGENTS.md`](AGENTS.md), then follow the
> [sandbox guide](docs/sandbox-guide.md). Install only the engine and LaTeX profile
> requested by the user. If the request just says “LaTeX”, ask **slim or full**.

## Five scripts, independent choices

| Script | Responsibility |
|---|---|
| [`manimgl.sh`](manimgl.sh) | **ManimGL only**, its dependencies, shared fonts, and a headless OpenGL wrapper |
| [`manimce.sh`](manimce.sh) | **Manim Community only**, its dependencies, shared fonts, and a Cairo-rendering CLI wrapper |
| [`latex_slim.sh`](latex_slim.sh) | Optional Manim-focused TeX, XeLaTeX, dvisvgm, common math packages and real `tipa` |
| [`latex_full.sh`](latex_full.sh) | Optional **actual `texlive-full`**, dvisvgm and real `tipa` |
| [`font.sh`](font.sh) | Shared download-once helper: **CMU Serif + Noto Serif Bengali** |

Neither engine installer installs the other engine or LaTeX. Both call `font.sh`
automatically, and refuse to proceed if the helper is missing. Keep the five
scripts together.

## Quick start

Clone into a persistent directory. On Arena/E2B, use a directory under `/home/user`.
This is a public repository: **no GitHub token is needed to clone or install**.

```bash
git clone https://github.com/myabdur212121-afk/manim-sandbox-setup.git
cd manim-sandbox-setup
```

**Choose one setup; do not run all of these just to get started.**

```bash
# ManimGL + slim LaTeX
bash manimgl.sh && bash latex_slim.sh
```

```bash
# ManimCE + slim LaTeX
bash manimce.sh && bash latex_slim.sh
```

Other combinations:

| Request | Command |
|---|---|
| ManimGL only | `bash manimgl.sh` |
| ManimCE only | `bash manimce.sh` |
| ManimGL + full LaTeX | `bash manimgl.sh && bash latex_full.sh` |
| ManimCE + full LaTeX | `bash manimce.sh && bash latex_full.sh` |

**Full TeX Live is large:** allow several GB of disk space and a longer download.
For text/shapes without `Tex` or `MathTex`, no LaTeX extension is needed.

## First render

Run only the command for your installed engine, from the repository directory:

```bash
# ManimGL: headless file output, low quality, black background
./bin/manimgl examples/check_manimgl.py FontsOnly -w -l -c '#000000' --video_dir videos/gl
```

```bash
# ManimCE: Cairo renderer, low quality
./bin/manim -ql --media_dir videos/ce examples/check_manimce.py FontsOnly
```

After installing a LaTeX extension, replace `FontsOnly` with `FontsAndMath`.
The examples exercise both English and Bengali fonts. `bin/manimce` is an alias
for `bin/manim`. See the [complete guide](docs/sandbox-guide.md) for verification,
output locations and restart instructions.

## Fonts: local cache, not repository assets

Font binaries are **not committed to this repository**. On first setup, the
helper downloads and verifies the upstream archives, saves the extracted fonts
and OFL licenses in `<workspace>/fonts/`, then registers that directory with
Fontconfig for the current user.

- **CMU Serif 0.7.0:** regular, bold, italic and bold italic.
- **Noto Serif Bengali 3.000:** nine normal-width weights, Thin through Black.
- Saved files take about **5.2 MiB**; source archives are discarded.
- Repeat setup reuses the files. Missing registration is restored without a
  download; a missing/corrupt family is downloaded again.

```python
Text("Hello", font="CMU Serif")
Text("বাংলা লেখা", font="Noto Serif Bengali")
```

These are text fonts, not an automatic replacement for LaTeX's math fonts.
`.gitignore` keeps the cache out of commits; it does **not** delete it from the
workspace. Do not use `git clean -fdx` on an installed workspace.

## Slim vs full

| | Slim | Full |
|---|---|---|
| ManimCE default `Tex` / `MathTex` | Yes | Yes |
| ManimGL template selected by wrapper | `basic` | `default` |
| XeLaTeX | Included | Included |
| `texlive-fonts-extra` / full font preamble | Not included | Included through `texlive-full` |
| Installs a Manim engine | No | No |

Each extension writes `configs/manimgl-tex.yml`. The generated `bin/manimgl`
wrapper loads it automatically; a user-provided `--config_file` takes precedence.
For direct GL invocations outside the wrapper, use `Tex(..., template="basic")`
with slim TeX. See [the guide](docs/sandbox-guide.md#step-3--optional-latex) for details.

## Requirements and persistence

- Debian/Ubuntu with Bash and `apt-get`; **validated on Debian 13**. Ubuntu is a
  target platform, not a separately verified test result.
- Python **3.11+**, Internet access for missing packages, and root or passwordless
  `sudo` for system dependencies. Run as your normal user where possible.
- Current defaults: **ManimGL 1.7.2**, **ManimCE 0.21.0**, **IPython 8.21.0**.
- Separate `.venv/manimgl` and `.venv/manimce`; no global pip installs or shell
  startup edits. Generated commands live in `bin/`.
- Software OpenGL via Xvfb is the tested GL headless path. This project does not
  implement Colab notebook magics, warm mode or a managed GPU-switching API.

**After an Arena sandbox reset**, rerun the selected engine installer and selected
LaTeX extension. System packages and `.venv/` do not persist. Scripts, scenes and
`fonts/` can persist inside the supported workspace, subject to provider limits.

Use `MANIM_WORKSPACE=/absolute/path` consistently across scripts to share an
existing cache/runtime location. Additional settings and safe update instructions
are in the [guide](docs/sandbox-guide.md#step-8--custom-workspace-and-version-settings).

## Inspect and test

```bash
bash manimgl.sh --dry-run       # no downloads or filesystem changes
bash latex_full.sh --dry-run
bash font.sh --check            # quiet; exit 0 means cache intact + registered
python3 -m unittest discover -s tests -v
shellcheck *.sh
```

**Validation is reported honestly:** both engines, fonts, headless renders and
slim TeX were exercised. Full TeX received syntax/dry-run/dependency checks, but
was **not installed or render-tested**. These are local test results, not a claim
of a GitHub Actions run. Read the [validation record](docs/validation.md).

## Project layout

```text
manim-sandbox-setup/
├── manimgl.sh / manimce.sh
├── latex_slim.sh / latex_full.sh / font.sh
├── README.md / AGENTS.md
├── docs/           # Guide, troubleshooting, validation, sources
├── examples/       # GL and CE font / math scenes
├── tests/          # Offline contract and repository checks
├── CONTRIBUTING.md / SECURITY.md
└── .gitignore      # Excludes secrets, fonts, runtimes and rendered outputs
```

See [contributing](CONTRIBUTING.md) and [security](SECURITY.md) before opening a PR.
Source attribution and third-party font licenses are documented in
[sources and licensing](docs/sources-and-licensing.md). No repository-wide
open-source license has been selected; public visibility alone is not a license.
