import subprocess
import sys
from pathlib import Path

def run_command(args, label):
    print(label)
    result = subprocess.run([sys.executable] + args)
    if result.returncode != 0:
        print(f"\n❌ {label} failed")
        sys.exit(result.returncode)

def main():
    script_dir = Path(__file__).resolve().parent

    run_command(["-m", "unittest", "discover", "-s", str(script_dir / "unit_tests")], "Unit Tests")
    run_command(["-m", "unittest", "discover", "-s", str(script_dir / "system_tests")], "System Tests")
    run_command([str(script_dir / "run_regression_tests.py")], "Regression Tests")

if __name__ == "__main__":
    main()
