#!/usr/bin/env python3
"""Main Quality Monitoring Automation Script for Vexy Markliff."""
# this_file: scripts/run_quality_monitoring.py

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    """Main entry point for quality monitoring automation."""
    parser = argparse.ArgumentParser(
        description="Run comprehensive quality monitoring for Vexy Markliff",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_quality_monitoring.py --all
  python scripts/run_quality_monitoring.py --metrics --performance
  python scripts/run_quality_monitoring.py --dashboard --open
  python scripts/run_quality_monitoring.py --security --save-reports
        """,
    )

    # Component selection
    parser.add_argument("--all", action="store_true", help="Run all monitoring components")
    parser.add_argument("--metrics", action="store_true", help="Run quality metrics collection")
    parser.add_argument("--performance", action="store_true", help="Run performance monitoring")
    parser.add_argument("--security", action="store_true", help="Run security scanning")
    parser.add_argument("--dashboard", action="store_true", help="Generate quality dashboard")

    # Options
    parser.add_argument("--save-reports", action="store_true", help="Save detailed reports to files")
    parser.add_argument("--set-baseline", action="store_true", help="Set performance baseline")
    parser.add_argument("--open", action="store_true", help="Open dashboard in browser")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML dashboard generation")
    parser.add_argument("--exit-on-failure", action="store_true", help="Exit with error code on critical issues")

    args = parser.parse_args()

    # If no specific components selected, default to all
    if not any([args.metrics, args.performance, args.security, args.dashboard]):
        args.all = True

    project_root = Path(__file__).parent.parent
    success = True

    # Run quality metrics collection
    if args.all or args.metrics:
        try:
            cmd = [sys.executable, "scripts/quality_metrics.py"]
            result = subprocess.run(cmd, check=False, cwd=project_root)
            if result.returncode != 0:
                success = False
            else:
                pass
        except Exception:
            success = False

    # Run performance monitoring
    if args.all or args.performance:
        try:
            cmd = [sys.executable, "scripts/performance_monitor.py"]
            if args.set_baseline:
                cmd.append("--set-baseline")
            result = subprocess.run(cmd, check=False, cwd=project_root)
            if result.returncode != 0:
                if args.exit_on_failure:
                    success = False
            else:
                pass
        except Exception:
            success = False

    # Run security scanning
    if args.all or args.security:
        try:
            cmd = [sys.executable, "scripts/security_scanner.py"]
            if args.save_reports:
                cmd.append("--save-report")
            result = subprocess.run(cmd, check=False, cwd=project_root)
            if result.returncode != 0:
                if args.exit_on_failure:
                    success = False
            else:
                pass
        except Exception:
            success = False

    # Generate quality dashboard
    if args.all or args.dashboard:
        try:
            cmd = [sys.executable, "scripts/quality_dashboard.py"]
            if args.no_html:
                cmd.append("--no-html")
            if args.open:
                cmd.append("--open")
            result = subprocess.run(cmd, check=False, cwd=project_root)
            if result.returncode != 0:
                success = False
            else:
                pass
        except Exception:
            success = False

    if success:
        pass
    else:
        pass

    # Exit with appropriate code
    if not success and args.exit_on_failure:
        sys.exit(1)


if __name__ == "__main__":
    main()
