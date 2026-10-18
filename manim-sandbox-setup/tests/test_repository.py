"""Offline repository checks; no package installation or external requests."""
import ast
from pathlib import Path
import re
import shutil
import subprocess
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
INSTALLERS = {"manimgl.sh", "manimce.sh", "latex_full.sh", "latex_slim.sh", "font.sh"}


def source_files():
    roots = [ROOT, ROOT / "docs", ROOT / "examples", ROOT / "tests"]
    for directory in roots:
        if directory.is_dir():
            yield from (p for p in directory.iterdir() if p.is_file())
    if (ROOT / ".github").is_dir():
        yield from (p for p in (ROOT / ".github").rglob("*") if p.is_file())


class RepositoryTests(unittest.TestCase):
    def test_exactly_five_root_installers(self):
        self.assertEqual({p.name for p in ROOT.glob("*.sh")}, INSTALLERS)

    def test_python_examples_parse_without_importing_engines(self):
        for path in (ROOT / "examples").glob("*.py"):
            with self.subTest(file=path.name):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_internal_document_links_exist(self):
        pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for path in source_files():
            if path.suffix != ".md":
                continue
            for match in pattern.finditer(path.read_text(encoding="utf-8")):
                link = match.group(1).strip().split()[0]
                if link.startswith(("http:", "https:", "mailto:", "#")):
                    continue
                local = unquote(link.split("#", 1)[0])
                if not local:
                    continue
                destination = (path.parent / local).resolve()
                with self.subTest(document=str(path.relative_to(ROOT)), link=link):
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.is_file(), f"Broken local link: {link}")

    def test_sources_use_lf_and_are_not_binaries(self):
        for path in source_files():
            with self.subTest(file=str(path.relative_to(ROOT))):
                data = path.read_bytes()
                self.assertFalse(b"\r\n" in data, "Use LF line endings; file contents not shown")
                self.assertFalse(b"\x00" in data, "Unexpected binary data; file contents not shown")
                self.assertTrue(data.endswith(b"\n"))

    def test_no_credential_values_in_source(self):
        # This intentionally detects values, not harmless names such as token.md.
        patterns = (
            rb"gh[pousr]_[A-Za-z0-9]{36,}",
            rb"github_pat_[A-Za-z0-9_]{30,}",
            rb"https://[^\s/]+:[^\s/]+@(?:github\.com|api\.github\.com)",
        )
        for path in source_files():
            data = path.read_bytes()
            for pattern in patterns:
                with self.subTest(file=str(path.relative_to(ROOT))):
                    self.assertFalse(bool(re.search(pattern, data)), "Potential credential found; value not shown")

    @unittest.skipUnless(shutil.which("git"), "Git is needed to verify ignore rules")
    def test_ignore_rules_protect_local_state(self):
        if not (ROOT / ".git").exists():
            self.skipTest("Archive checkout has no Git metadata")
        examples = [
            "token.md", "nested/token.md", "TOKEN.md", ".env", ".env.production",
            "credentials.json", ".git-credentials", ".netrc", "private.key",
            "fonts/cmu-serif/cmunrm.ttf", ".venv/manimgl/bin/python",
            ".cache/render.log", "bin/manimgl", "configs/manimgl-tex.yml",
            "videos/example.mp4", "media/partial.mp4", "bundle.zip",
        ]
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--stdin"], cwd=ROOT,
            input="\n".join(examples) + "\n", capture_output=True, text=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(result.stdout.splitlines()), set(examples))

    @unittest.skipUnless(shutil.which("git"), "Git is needed to verify staged/tracked files")
    def test_git_index_excludes_secrets_and_runtime_assets(self):
        if not (ROOT / ".git").exists():
            self.skipTest("Archive checkout has no Git metadata")
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True,
            text=True, check=True, timeout=15,
        )
        paths = [Path(name) for name in result.stdout.split("\0") if name]
        forbidden_dirs = {".venv", ".cache", "fonts", "bin", "media", "videos", "__pycache__"}
        forbidden_suffixes = {".ttf", ".otf", ".woff", ".woff2", ".mp4", ".zip", ".pdf", ".key", ".pem"}
        for path in paths:
            with self.subTest(file=str(path)):
                self.assertFalse(forbidden_dirs.intersection(path.parts))
                self.assertNotIn(path.suffix.lower(), forbidden_suffixes)
                self.assertNotEqual(path.name.lower(), "token.md")
                self.assertFalse(path.name.startswith(".env"))
                self.assertNotEqual(str(path), "configs/manimgl-tex.yml")


if __name__ == "__main__":
    unittest.main()
