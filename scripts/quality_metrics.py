#!/usr/bin/env python3
"""Quality Metrics Tracking System for Vexy Markliff."""
# this_file: scripts/quality_metrics.py

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class QualityMetricsCollector:
    """Collect and track various quality metrics for the project."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.metrics_dir = project_root / "quality_metrics"
        self.metrics_dir.mkdir(exist_ok=True)

    def collect_all_metrics(self) -> dict[str, Any]:
        """Collect all available quality metrics."""

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "version": self._get_package_version(),
            "code_coverage": self._collect_code_coverage(),
            "test_results": self._collect_test_results(),
            "code_quality": self._collect_code_quality(),
            "performance": self._collect_performance_metrics(),
            "security": self._collect_security_metrics(),
            "dependencies": self._collect_dependency_info(),
            "git_info": self._collect_git_info(),
        }

        # Save metrics to file
        metrics_file = self.metrics_dir / f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)

        return metrics

    def _get_package_version(self) -> str:
        """Get the current package version."""
        try:
            result = subprocess.run(
                ["python", "-c", "import vexy_markliff; print(vexy_markliff.__version__)"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"

    def _collect_code_coverage(self) -> dict[str, Any]:
        """Collect code coverage metrics."""
        try:
            # Run pytest with coverage
            subprocess.run(
                ["uvx", "hatch", "run", "test:pytest", "--cov=vexy_markliff", "--cov-report=json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    coverage_data = json.load(f)

                return {
                    "total_coverage": coverage_data["totals"]["percent_covered"],
                    "lines_covered": coverage_data["totals"]["covered_lines"],
                    "lines_missing": coverage_data["totals"]["missing_lines"],
                    "files": {
                        file: data["summary"]["percent_covered"] for file, data in coverage_data["files"].items()
                    },
                }
            return {"error": "Coverage file not found"}
        except Exception as e:
            return {"error": str(e)}

    def _collect_test_results(self) -> dict[str, Any]:
        """Collect test execution results."""
        try:
            start_time = time.time()
            result = subprocess.run(
                ["uvx", "hatch", "test", "--json-report", "--json-report-file=test_results.json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            duration = time.time() - start_time

            # Parse pytest output for basic metrics
            output_lines = result.stdout.split("\n")
            summary_line = next((line for line in output_lines if "passed" in line and "failed" in line), "")

            return {
                "exit_code": result.returncode,
                "duration_seconds": duration,
                "summary": summary_line,
                "total_tests_estimated": self._count_test_files(),
            }
        except Exception as e:
            return {"error": str(e)}

    def _count_test_files(self) -> int:
        """Count the number of test files."""
        test_dir = self.project_root / "tests"
        if test_dir.exists():
            return len(list(test_dir.glob("test_*.py")))
        return 0

    def _collect_code_quality(self) -> dict[str, Any]:
        """Collect code quality metrics using various tools."""

        quality_metrics = {}

        # Ruff linting
        try:
            result = subprocess.run(
                ["uvx", "ruff", "check", ".", "--output-format=json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            if result.stdout:
                ruff_issues = json.loads(result.stdout)
                quality_metrics["ruff"] = {
                    "total_issues": len(ruff_issues),
                    "by_severity": self._group_ruff_issues(ruff_issues),
                }
            else:
                quality_metrics["ruff"] = {"total_issues": 0}
        except Exception as e:
            quality_metrics["ruff"] = {"error": str(e)}

        # MyPy type checking
        try:
            result = subprocess.run(
                ["uvx", "mypy", "src/vexy_markliff", "--json-report", "mypy_report"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            quality_metrics["mypy"] = {
                "exit_code": result.returncode,
                "stderr_lines": len(result.stderr.split("\n")) if result.stderr else 0,
            }
        except Exception as e:
            quality_metrics["mypy"] = {"error": str(e)}

        # Line counts
        quality_metrics["code_stats"] = self._collect_code_stats()

        return quality_metrics

    def _group_ruff_issues(self, issues: list[dict]) -> dict[str, int]:
        """Group ruff issues by severity/type."""
        groups = {}
        for issue in issues:
            code = issue.get("code", "unknown")
            if code not in groups:
                groups[code] = 0
            groups[code] += 1
        return groups

    def _collect_code_stats(self) -> dict[str, Any]:
        """Collect basic code statistics."""
        src_dir = self.project_root / "src"
        tests_dir = self.project_root / "tests"

        stats = {
            "src_files": 0,
            "src_lines": 0,
            "test_files": 0,
            "test_lines": 0,
        }

        for py_file in src_dir.rglob("*.py"):
            stats["src_files"] += 1
            stats["src_lines"] += len(py_file.read_text().split("\n"))

        for py_file in tests_dir.rglob("*.py"):
            stats["test_files"] += 1
            stats["test_lines"] += len(py_file.read_text().split("\n"))

        return stats

    def _collect_performance_metrics(self) -> dict[str, Any]:
        """Collect performance-related metrics."""

        try:
            # Test import performance
            start_time = time.time()
            result = subprocess.run(
                [
                    "python",
                    "-c",
                    "import vexy_markliff; from vexy_markliff.core.converter import VexyMarkliff; converter = VexyMarkliff()",
                ],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            import_time = time.time() - start_time

            # Test conversion performance
            start_time = time.time()
            result = subprocess.run(
                [
                    "python",
                    "-c",
                    "import vexy_markliff; converter = vexy_markliff.VexyMarkliff(); converter.markdown_to_xliff('# Test', 'en', 'es')",
                ],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            conversion_time = time.time() - start_time

            return {
                "import_time_seconds": import_time,
                "conversion_time_seconds": conversion_time,
                "import_success": result.returncode == 0,
            }
        except Exception as e:
            return {"error": str(e)}

    def _collect_security_metrics(self) -> dict[str, Any]:
        """Collect security-related metrics."""

        security_metrics = {}

        # Bandit security scan
        try:
            result = subprocess.run(
                ["uvx", "bandit", "-r", "src/", "-f", "json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            if result.stdout:
                bandit_data = json.loads(result.stdout)
                security_metrics["bandit"] = {
                    "total_issues": len(bandit_data.get("results", [])),
                    "by_severity": self._group_bandit_issues(bandit_data.get("results", [])),
                }
            else:
                security_metrics["bandit"] = {"total_issues": 0}
        except Exception as e:
            security_metrics["bandit"] = {"error": str(e)}

        return security_metrics

    def _group_bandit_issues(self, issues: list[dict]) -> dict[str, int]:
        """Group bandit issues by severity."""
        groups = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for issue in issues:
            severity = issue.get("issue_severity", "LOW")
            if severity in groups:
                groups[severity] += 1
        return groups

    def _collect_dependency_info(self) -> dict[str, Any]:
        """Collect dependency information."""

        try:
            # Get dependency list
            result = subprocess.run(
                ["uvx", "pip", "list", "--format=json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            dependencies = json.loads(result.stdout) if result.stdout else []

            return {
                "total_dependencies": len(dependencies),
                "dependencies": {dep["name"]: dep["version"] for dep in dependencies},
            }
        except Exception as e:
            return {"error": str(e)}

    def _collect_git_info(self) -> dict[str, Any]:
        """Collect git repository information."""

        try:
            # Get current commit
            commit_result = subprocess.run(
                ["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True, cwd=self.project_root
            )

            # Get branch name
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"], check=False, capture_output=True, text=True, cwd=self.project_root
            )

            # Get commit count
            count_result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "commit_hash": commit_result.stdout.strip(),
                "branch": branch_result.stdout.strip(),
                "commit_count": int(count_result.stdout.strip()) if count_result.stdout.strip().isdigit() else 0,
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_summary_report(self, metrics: dict[str, Any]) -> str:
        """Generate a human-readable summary report."""
        report = []
        report.append("# Quality Metrics Report")
        report.append(f"**Generated:** {metrics['timestamp']}")
        report.append(f"**Version:** {metrics['version']}")
        report.append("")

        # Code Coverage
        if "total_coverage" in metrics.get("code_coverage", {}):
            coverage = metrics["code_coverage"]["total_coverage"]
            report.append(f"## Code Coverage: {coverage:.1f}%")
            if coverage >= 90:
                report.append("✅ Excellent coverage")
            elif coverage >= 80:
                report.append("✅ Good coverage")
            elif coverage >= 70:
                report.append("⚠️ Adequate coverage")
            else:
                report.append("❌ Needs improvement")
            report.append("")

        # Test Results
        test_info = metrics.get("test_results", {})
        if "exit_code" in test_info:
            status = "✅ Passing" if test_info["exit_code"] == 0 else "❌ Failing"
            report.append(f"## Tests: {status}")
            if "duration_seconds" in test_info:
                report.append(f"Duration: {test_info['duration_seconds']:.1f}s")
            report.append("")

        # Performance
        perf_info = metrics.get("performance", {})
        if "import_time_seconds" in perf_info:
            import_time = perf_info["import_time_seconds"]
            report.append("## Performance")
            report.append(f"Import time: {import_time:.3f}s")
            if import_time < 0.1:
                report.append("✅ Fast import")
            elif import_time < 1.0:
                report.append("⚠️ Moderate import time")
            else:
                report.append("❌ Slow import")
            report.append("")

        # Security
        security_info = metrics.get("security", {})
        if "bandit" in security_info and "total_issues" in security_info["bandit"]:
            issues = security_info["bandit"]["total_issues"]
            report.append(f"## Security: {issues} issues")
            if issues == 0:
                report.append("✅ No security issues found")
            else:
                report.append("⚠️ Security issues detected")
            report.append("")

        return "\n".join(report)


def main():
    """Main entry point for quality metrics collection."""
    project_root = Path(__file__).parent.parent
    collector = QualityMetricsCollector(project_root)

    metrics = collector.collect_all_metrics()
    report = collector.generate_summary_report(metrics)

    # Also save the report
    report_file = collector.metrics_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
