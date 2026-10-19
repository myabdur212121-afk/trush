# Contributing

Keep this repository small, explicit and safe to run in a disposable sandbox.
Read [AGENTS.md](AGENTS.md) and [the guide](docs/sandbox-guide.md) before changes.

## Preserve the contract

- Exactly five entry-point installers: two independent engines, two optional
  LaTeX profiles, and one shared font helper.
- Neither engine installs the other engine or LaTeX implicitly.
- Both engines always use the helper; valid local fonts must not download again.
- Missing runtime packages must be detected from real state after a reset.
- Use isolated venvs, non-interactive APT, quoted paths, and fail on real errors.
- Keep `--help`, side-effect-free `--dry-run`, and font `--check` working.
- Slim must not install `texlive-full` or `texlive-fonts-extra`; it must use a
  compatible GL template. Full must mean the actual full distro package.
- Documentation is English; Bengali text in font-render examples is intentional.

## Offline checks

These require Bash and Python, not a Manim installation or font download:

```bash
python3 -m unittest discover -s tests -v
```

Run lint as well (install ShellCheck separately if your environment lacks it):

```bash
shellcheck *.sh
```

Do not describe these checks as an actual successful installation or render.

## Integration checks

Use a disposable Debian/Ubuntu environment with suitable privileges. Install one
engine at a time, confirm it did not install the other engine/LaTeX, and render
`FontsOnly`. If testing slim, run `latex_slim.sh` and render `FontsAndMath`.
Follow [the guide](docs/sandbox-guide.md) for exact commands and output paths.

Use separate workspaces if proving engine-only behavior on a clean system.
Re-running a script on an already populated system does not prove what a fresh
installation would pull in. Full TeX Live is a separate, expensive test: run it
only when explicitly authorized, and clearly distinguish dependency simulation
from a real installation.

Check font reuse both in the current registration state and with a fresh
Fontconfig configuration. Network-blocked repeat runs should leave font contents
and modification times unchanged. Never commit test downloads or font binaries.

## Before a pull request

1. Run offline tests and ShellCheck.
2. Run relevant integration tests, or state which were not run and why.
3. Update guide/troubleshooting/validation notes to match changed behavior.
4. Review `git status --short` and `git diff --cached`.
5. Check for credentials and accidentally staged fonts, runtimes, videos or logs.
6. Explain the change, compatibility impact and test evidence in the PR.

Do not put credentials in shell arguments or remote URLs, and never request a
real PAT in an issue. See [SECURITY.md](SECURITY.md). No repository-wide license
has yet been chosen; see [sources and licensing](docs/sources-and-licensing.md).
