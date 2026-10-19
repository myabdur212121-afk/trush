"""Offline contract tests: python3 -m unittest discover -s tests -v

These tests do not install packages, download fonts or require an engine.
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ("manimgl.sh", "manimce.sh", "latex_full.sh", "latex_slim.sh", "font.sh")


class ScriptTests(unittest.TestCase):
    def run_script(self, name, *args, workspace=None, extra_env=None):
        env = os.environ.copy()
        if workspace is not None:
            env["MANIM_WORKSPACE"] = str(workspace)
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["bash", str(ROOT / name), *args], env=env,
            text=True, capture_output=True, timeout=30,
        )

    def test_bash_syntax(self):
        for name in SCRIPTS:
            with self.subTest(script=name):
                result = subprocess.run(["bash", "-n", str(ROOT / name)], capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr.decode())

    def test_help(self):
        for name in SCRIPTS:
            with self.subTest(script=name):
                result = self.run_script(name, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Usage:", result.stdout)

    def test_unknown_options_fail(self):
        for name in SCRIPTS:
            with self.subTest(script=name):
                result = self.run_script(name, "--not-a-real-option")
                self.assertEqual(result.returncode, 2)

    def test_relative_workspaces_fail(self):
        for name in SCRIPTS:
            with self.subTest(script=name):
                result = self.run_script(name, "--dry-run", workspace="relative/folder")
                self.assertEqual(result.returncode, 2)
                self.assertIn("absolute", result.stderr)

    def test_dry_run_has_no_side_effects_or_network(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            forbidden = base / "forbidden"
            forbidden.mkdir()
            # Fail if a dry-run attempts a download, package install or cache refresh.
            for name in ("curl", "wget", "git", "apt-get", "sudo", "pip", "pip3", "fc-cache"):
                command = forbidden / name
                command.write_text("#!/usr/bin/env bash\necho 'Unexpected mutation/network command' >&2\nexit 99\n")
                command.chmod(0o755)
            workspace = base / "workspace with spaces & unicode বাংলা"
            env = {"PATH": str(forbidden) + os.pathsep + os.environ["PATH"]}
            for name in SCRIPTS:
                with self.subTest(script=name):
                    result = self.run_script(name, "--dry-run", workspace=workspace, extra_env=env)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertFalse(workspace.exists())

    def test_engine_plans_are_separate(self):
        for name, expected, forbidden in (
            ("manimgl.sh", "manimgl==", "manim=="),
            ("manimce.sh", "manim==", "manimgl=="),
        ):
            with self.subTest(script=name):
                result = self.run_script(name, "--dry-run")
                installs = "\n".join(line for line in result.stdout.splitlines()
                                     if "apt packages" in line or "pip install:" in line)
                self.assertIn(expected, installs)
                self.assertNotIn(forbidden, installs)
                self.assertNotIn("texlive", installs)
                self.assertNotIn("dvisvgm", installs)
                self.assertIn("[fonts]", result.stdout)

    def test_helper_is_mandatory(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in ("manimgl.sh", "manimce.sh"):
                with self.subTest(script=name):
                    script = Path(folder) / name
                    shutil.copy2(ROOT / name, script)
                    result = subprocess.run(["bash", str(script), "--dry-run"],
                                            text=True, capture_output=True, timeout=30)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("Required helper font.sh", result.stderr)

    def test_font_check_does_not_trust_an_empty_cache(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder) / "not-created"
            result = self.run_script("font.sh", "--check", workspace=workspace)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(workspace.exists())

    def test_tex_profiles_have_distinct_package_sets(self):
        slim = self.run_script("latex_slim.sh", "--dry-run")
        full = self.run_script("latex_full.sh", "--dry-run")
        slim_packages = next(line for line in slim.stdout.splitlines() if "apt packages" in line)
        full_packages = next(line for line in full.stdout.splitlines() if "apt packages" in line)
        self.assertNotIn("texlive-full", slim_packages)
        self.assertNotIn("texlive-fonts-extra", slim_packages)
        self.assertIn("texlive-full", full_packages)
        self.assertIn("template: basic", slim.stdout)
        self.assertIn("template: default", full.stdout)


if __name__ == "__main__":
    unittest.main()
