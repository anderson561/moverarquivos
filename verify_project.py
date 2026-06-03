# verify_project.py
"""Automated verification script for the MoverArquivos project.

Features:
- Run unit tests with coverage (coverage report generated).
- Lint source code using ruff.
- Execute the compiled executable in **real mode**.
- Validate build script execution.
- Consolidate results into a Markdown report at `reports/verification_report.md`.
"""
import subprocess
import sys
import os
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent  # project root (c:/python/moverarquivos)
ADV_ORG = BASE_DIR / "advanced-organizer"
REPORTS_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORTS_DIR / "verification_report.md"

def run_cmd(command, cwd=None, shell=False):
    """Run a shell command, capture output, and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr

def write_section(title: str, content: str):
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"## {title}\n\n```\n{content}\n```\n\n")

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    # Clear previous report
    REPORT_FILE.write_text("# MoverArquivos Verification Report\n\nGenerated on " + __import__("datetime").datetime.now().isoformat() + "\n\n", encoding="utf-8")

    # 1. Run tests with coverage
    print("Running tests with coverage...")
    # Determine a valid working directory for pytest/coverage
    # Determine test directory (advanced-organizer/tests)
    test_dir_path = os.path.abspath(str(ADV_ORG / "tests"))
    if os.path.isdir(test_dir_path):
        test_cwd_path = test_dir_path
    else:
        test_cwd_path = os.path.abspath(str(ADV_ORG))
    print(f"[DEBUG] Using test_cwd: {test_cwd_path}")
    rc, out, err = run_cmd([sys.executable, "-m", "coverage", "run", "-m", "pytest"], cwd=test_cwd_path)
    write_section("Test Execution (pytest)", out + "\n" + err)
    if rc == 0:
        # generate coverage report in markdown (run from project root)
        rc_cov, out_cov, err_cov = run_cmd([sys.executable, "-m", "coverage", "report", "-m"], cwd=str(ADV_ORG))
        write_section("Coverage Report", out_cov + "\n" + err_cov)
    else:
        write_section("Test Execution (pytest)", "Tests failed. Skipping coverage.")

    # 2. Lint with ruff
    print("Running ruff linter...")
    rc_lint, out_lint, err_lint = run_cmd([sys.executable, "-m", "ruff", "check", str(ADV_ORG / "src")])
    write_section("Ruff Linting", out_lint + "\n" + err_lint)

    # 3. Execute binary in real mode
    exe_path = ADV_ORG / "dist" / "OrganizadorArquivos.exe"
    if exe_path.is_file():
        print("Executing binary in real mode...")
        # Use the same test_cwd if the binary expects a working directory; otherwise default to ADV_ORG
        exec_cwd = os.path.abspath(str(ADV_ORG))
        print(f"[DEBUG] Using exec_cwd: {exec_cwd}")
        rc_bin, out_bin, err_bin = run_cmd([str(exe_path), "--path", str(BASE_DIR / "test_dummy"), "--real"], cwd=exec_cwd)
        write_section("Executable (real mode)", out_bin + "\n" + err_bin)
    else:
        write_section("Executable (real mode)", "Executable not found at " + str(exe_path))

    # 4. Run build script (build.bat) silently
    build_bat = ADV_ORG / "build.bat"
    if build_bat.is_file():
        print("Running build.bat...")
        rc_build, out_build, err_build = run_cmd(["cmd", "/c", str(build_bat)], cwd=str(ADV_ORG))
        write_section("Build Script Output", out_build + "\n" + err_build)
    else:
        write_section("Build Script Output", "build.bat not found.")

    print(f"Verification report generated at {REPORT_FILE}")

if __name__ == "__main__":
    main()
