# Sources and licensing

## Setup reference

The initial scripts were prepared after reading the user-provided
[`myabdur2121-cpu/manim-env-setup`](https://github.com/myabdur2121-cpu/manim-env-setup)
repository at revision
`d6028e41b3df4085382610d259d6753240cd8817`:

- [`sandbox/manimce/setup_manim.sh`](https://github.com/myabdur2121-cpu/manim-env-setup/blob/d6028e41b3df4085382610d259d6753240cd8817/sandbox/manimce/setup_manim.sh)
- [`sandbox/manimce/font.sh`](https://github.com/myabdur2121-cpu/manim-env-setup/blob/d6028e41b3df4085382610d259d6753240cd8817/sandbox/manimce/font.sh)
- [`sandbox/manimgl/manimgl-e2b-sandbox.md`](https://github.com/myabdur2121-cpu/manim-env-setup/blob/d6028e41b3df4085382610d259d6753240cd8817/sandbox/manimgl/manimgl-e2b-sandbox.md)
- [`sandbox/latex-pdf/README.md`](https://github.com/myabdur2121-cpu/manim-env-setup/blob/d6028e41b3df4085382610d259d6753240cd8817/sandbox/latex-pdf/README.md)

The step-by-step documentation format was inspired by the supplied
[ManimGL Colab guide](https://github.com/myabdur212121-afk/manimgl-colab/blob/main/docs/colab-guide.md).
This repository does **not** include that package's notebook magics, managed GPU
switching, warm mode, or performance guarantees.

Changes from the reference include:

- independent engine and optional LaTeX installers;
- persistent font files with archive integrity checks and repeat-run reuse;
- isolated engine environments and tested compatibility pins;
- an Xvfb-based headless wrapper for stable ManimGL;
- a basic GL template profile for slim TeX;
- real distro `tipa` rather than a dummy `.sty` file;
- offline tests and explicit reports of tested versus untested behavior.

## Engines and system software

- [ManimGL / 3b1b Manim](https://github.com/3b1b/manim) — default PyPI package
  `manimgl==1.7.2`.
- [Manim Community](https://github.com/ManimCommunity/manim) — default PyPI package
  `manim==0.21.0`.
- TeX Live, FFmpeg, Xvfb, Fontconfig and development libraries are installed from
  the configured Debian/Ubuntu package repositories.

These projects keep their own licenses and trademarks. This is an independent
setup repository, not an official distribution of either engine. Engine and
system-package binaries are not committed here.

## Downloaded fonts

Font binaries are deliberately **not stored in this Git repository**. The helper
fetches these pinned upstream archives when a workspace first needs them:

| Family | Upstream archive | Saved files |
|---|---|---|
| CMU Serif 0.7.0 | [Computer Modern Unicode release](https://downloads.sourceforge.net/project/cm-unicode/cm-unicode/0.7.0/cm-unicode-0.7.0-ttf.tar.xz) | Four serif TTF faces + `OFL.txt` |
| Noto Serif Bengali 3.000 | [notofonts/bengali release](https://github.com/notofonts/bengali/releases/download/NotoSerifBengali-v3.000/NotoSerifBengali-v3.000.zip) | Nine normal-width TTF weights + `OFL.txt` |

`font.sh` contains the expected archive SHA-256 values and creates checksums for
the saved font files. It retains the upstream OFL text beside each font family.
Refer to those license files and upstream sources for the applicable font terms;
do not assume that the setup scripts relicense the fonts.

## Repository-wide license

No repository-wide open-source license has been selected for this publication.
Public visibility is not, by itself, a general license to redistribute or
relicense upstream-derived material. Contact the repository owner about licensing
before redistribution beyond the rights supplied by the applicable upstream
terms. A future license selection must preserve third-party attribution and terms.
