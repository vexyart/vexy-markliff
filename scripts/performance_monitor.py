#!/usr/bin/env python3
"""Performance Regression Monitoring System for Vexy Markliff."""
# this_file: scripts/performance_monitor.py

import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class PerformanceMonitor:
    """Monitor and track performance metrics to detect regressions."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.perf_dir = project_root / "performance_data"
        self.perf_dir.mkdir(exist_ok=True)
        self.baseline_file = self.perf_dir / "baseline.json"
        self.history_file = self.perf_dir / "history.json"

    def run_performance_tests(self) -> dict[str, Any]:
        """Run comprehensive performance tests and return results."""

        results = {"timestamp": datetime.now().isoformat(), "tests": {}}

        # Test 1: Package import performance
        results["tests"]["import_performance"] = self._test_import_performance()

        # Test 2: Converter instantiation performance
        results["tests"]["converter_instantiation"] = self._test_converter_instantiation()

        # Test 3: Small document conversion performance
        results["tests"]["small_conversion"] = self._test_small_conversion()

        # Test 4: Medium document conversion performance
        results["tests"]["medium_conversion"] = self._test_medium_conversion()

        # Test 5: Large document conversion performance
        results["tests"]["large_conversion"] = self._test_large_conversion()

        # Test 6: Memory usage analysis
        results["tests"]["memory_usage"] = self._test_memory_usage()

        return results

    def _test_import_performance(self) -> dict[str, Any]:
        """Test package import performance."""

        times = []
        for _i in range(5):  # Run 5 times for statistical reliability
            start_time = time.perf_counter()

            # Fresh subprocess to avoid caching
            import subprocess

            result = subprocess.run(
                [sys.executable, "-c", "import vexy_markliff; from vexy_markliff.core.converter import VexyMarkliff"],
                check=False,
                capture_output=True,
                cwd=self.project_root,
            )

            end_time = time.perf_counter()
            duration = end_time - start_time

            if result.returncode == 0:
                times.append(duration)

        if times:
            return {
                "mean_seconds": statistics.mean(times),
                "median_seconds": statistics.median(times),
                "min_seconds": min(times),
                "max_seconds": max(times),
                "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
                "sample_count": len(times),
                "success": True,
            }
        return {"success": False, "error": "All import attempts failed"}

    def _test_converter_instantiation(self) -> dict[str, Any]:
        """Test converter instantiation performance."""

        try:
            from vexy_markliff.core.converter import VexyMarkliff

            times = []
            for _ in range(10):
                start_time = time.perf_counter()
                VexyMarkliff()
                end_time = time.perf_counter()
                times.append(end_time - start_time)

            return {
                "mean_seconds": statistics.mean(times),
                "median_seconds": statistics.median(times),
                "min_seconds": min(times),
                "max_seconds": max(times),
                "sample_count": len(times),
                "success": True,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _test_small_conversion(self) -> dict[str, Any]:
        """Test small document conversion performance."""

        small_markdown = """# Small Document

This is a small test document with basic formatting.

- Item 1
- Item 2
- Item 3

Some **bold** and *italic* text."""

        return self._run_conversion_test(small_markdown, "small")

    def _test_medium_conversion(self) -> dict[str, Any]:
        """Test medium document conversion performance."""

        # Generate medium-sized document
        medium_sections = []
        for i in range(20):
            section = f"""
## Section {i + 1}

This is section {i + 1} with multiple paragraphs and formatting.

### Subsection {i + 1}.1

Here's some content with:
- List item {i + 1}.1
- List item {i + 1}.2
- List item {i + 1}.3

### Subsection {i + 1}.2

More content with **bold text** and *italic text* and `inline code`.

```python
def example_function_{i}():
    return "This is code block {i}"
```

Regular paragraph with [links](https://example.com) and other elements.
"""
            medium_sections.append(section)

        medium_markdown = "# Medium Document\n" + "\n".join(medium_sections)
        return self._run_conversion_test(medium_markdown, "medium")

    def _test_large_conversion(self) -> dict[str, Any]:
        """Test large document conversion performance."""

        # Generate large document
        large_sections = []
        for i in range(100):
            section = f"""
## Chapter {i + 1}: Performance Testing

This is chapter {i + 1} of our performance testing document. It contains
multiple paragraphs, formatting elements, and various Markdown constructs
to simulate real-world usage scenarios.

### {i + 1}.1 Introduction

Performance testing is crucial for ensuring that our conversion engine
can handle documents of various sizes efficiently. This section contains
**important information** about *performance characteristics* and
`optimization techniques`.

### {i + 1}.2 Technical Details

Here are some technical details:

1. First technical point about performance
2. Second technical point about scalability
3. Third technical point about optimization

#### Code Example {i + 1}

```python
def performance_test_{i}():
    \"\"\"Performance test function {i}.\"\"\"
    start_time = time.time()
    # Simulate processing
    for j in range(1000):
        process_data(j)
    end_time = time.time()
    return end_time - start_time

def process_data(value):
    return value * 2 + 1
```

### {i + 1}.3 Analysis

The analysis shows that performance scales linearly with document size
when using the optimized conversion pipeline. Key findings include:

- Memory usage remains constant due to streaming processing
- Conversion speed averages 500KB/s for typical documents
- CPU utilization peaks during HTML parsing phase

Regular paragraph text continues here with additional content to increase
the overall document size and test memory efficiency of the conversion
process.
"""
            large_sections.append(section)

        large_markdown = "# Large Document Performance Test\n" + "\n".join(large_sections)
        return self._run_conversion_test(large_markdown, "large")

    def _run_conversion_test(self, markdown_content: str, test_name: str) -> dict[str, Any]:
        """Run conversion performance test for given content."""
        try:
            from vexy_markliff.core.converter import VexyMarkliff

            converter = VexyMarkliff()
            times = []
            content_size = len(markdown_content.encode("utf-8"))

            # Run test multiple times for reliability
            iterations = 5 if test_name == "large" else 10
            for _ in range(iterations):
                start_time = time.perf_counter()
                result = converter.markdown_to_xliff(markdown_content, "en", "es")
                end_time = time.perf_counter()
                times.append(end_time - start_time)

            output_size = len(result.encode("utf-8"))

            return {
                "mean_seconds": statistics.mean(times),
                "median_seconds": statistics.median(times),
                "min_seconds": min(times),
                "max_seconds": max(times),
                "input_size_bytes": content_size,
                "output_size_bytes": output_size,
                "throughput_kb_per_sec": (content_size / 1024) / statistics.mean(times),
                "sample_count": len(times),
                "success": True,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _test_memory_usage(self) -> dict[str, Any]:
        """Test memory usage during conversion."""

        try:
            import os

            import psutil

            # Get initial memory
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss

            from vexy_markliff.core.converter import VexyMarkliff

            after_import_memory = process.memory_info().rss

            converter = VexyMarkliff()
            after_init_memory = process.memory_info().rss

            # Generate test content
            test_content = "# Test\n\nContent here.\n" * 1000

            # Run conversion
            converter.markdown_to_xliff(test_content, "en", "es")
            after_conversion_memory = process.memory_info().rss

            return {
                "initial_memory_mb": initial_memory / 1024 / 1024,
                "after_import_mb": after_import_memory / 1024 / 1024,
                "after_init_mb": after_init_memory / 1024 / 1024,
                "after_conversion_mb": after_conversion_memory / 1024 / 1024,
                "import_overhead_mb": (after_import_memory - initial_memory) / 1024 / 1024,
                "conversion_overhead_mb": (after_conversion_memory - after_init_memory) / 1024 / 1024,
                "success": True,
            }
        except ImportError:
            return {"success": False, "error": "psutil not available for memory monitoring"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def save_results(self, results: dict[str, Any]) -> None:
        """Save performance results to history."""
        # Load existing history
        history = []
        if self.history_file.exists():
            with open(self.history_file) as f:
                history = json.load(f)

        # Add new results
        history.append(results)

        # Keep only last 100 results to prevent file from growing too large
        history = history[-100:]

        # Save updated history
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)

    def detect_regressions(self, current_results: dict[str, Any]) -> list[dict[str, Any]]:
        """Detect performance regressions compared to baseline and recent history."""
        regressions = []

        # Load baseline if it exists
        baseline = None
        if self.baseline_file.exists():
            with open(self.baseline_file) as f:
                baseline = json.load(f)

        # Load recent history
        history = []
        if self.history_file.exists():
            with open(self.history_file) as f:
                history = json.load(f)

        # Check each test for regressions
        for test_name, current_test in current_results["tests"].items():
            if not current_test.get("success", False):
                continue

            # Check against baseline
            if baseline and test_name in baseline["tests"]:
                baseline_test = baseline["tests"][test_name]
                if baseline_test.get("success", False):
                    regression = self._check_regression(current_test, baseline_test, f"{test_name}_vs_baseline")
                    if regression:
                        regressions.append(regression)

            # Check against recent average (last 10 runs)
            recent_history = [
                h for h in history[-10:] if test_name in h["tests"] and h["tests"][test_name].get("success", False)
            ]
            if len(recent_history) >= 3:  # Need at least 3 data points
                recent_means = {}
                for metric in ["mean_seconds", "median_seconds", "throughput_kb_per_sec"]:
                    values = [h["tests"][test_name][metric] for h in recent_history if metric in h["tests"][test_name]]
                    if values:
                        recent_means[metric] = statistics.mean(values)

                if recent_means:
                    regression = self._check_regression(current_test, recent_means, f"{test_name}_vs_recent_average")
                    if regression:
                        regressions.append(regression)

        return regressions

    def _check_regression(
        self, current: dict[str, Any], reference: dict[str, Any], comparison_name: str
    ) -> dict[str, Any] | None:
        """Check if current performance represents a regression."""
        # Define regression thresholds (percentages)
        REGRESSION_THRESHOLDS = {
            "mean_seconds": 20,  # 20% slower is a regression
            "median_seconds": 20,
            "throughput_kb_per_sec": -15,  # 15% throughput reduction is a regression
        }

        for metric, threshold in REGRESSION_THRESHOLDS.items():
            if metric in current and metric in reference:
                current_value = current[metric]
                reference_value = reference[metric]

                if reference_value > 0:  # Avoid division by zero
                    percent_change = ((current_value - reference_value) / reference_value) * 100

                    # For throughput, negative change is bad; for time metrics, positive change is bad
                    is_regression = False
                    if metric == "throughput_kb_per_sec":
                        is_regression = percent_change < threshold
                    else:
                        is_regression = percent_change > threshold

                    if is_regression:
                        return {
                            "comparison": comparison_name,
                            "metric": metric,
                            "current_value": current_value,
                            "reference_value": reference_value,
                            "percent_change": percent_change,
                            "threshold": threshold,
                            "severity": "major" if abs(percent_change) > 50 else "minor",
                        }

        return None

    def check_ci_performance_targets(self, results: dict[str, Any]) -> list[dict[str, str]]:
        """Check CI-specific performance targets."""
        failures = []

        # Define CI performance targets (stricter than regression thresholds)
        CI_TARGETS = {
            "import_performance": {"max_seconds": 0.050, "description": "Import speed"},
            "small_conversion": {"max_seconds": 0.005, "description": "Small document conversion"},
            "medium_conversion": {"max_seconds": 0.050, "description": "Medium document conversion"},
            "large_conversion": {"max_seconds": 0.200, "description": "Large document conversion"},
        }

        # Check memory targets
        MEMORY_TARGETS = {"conversion_overhead_mb": 15.0, "import_overhead_mb": 5.0}

        # Check throughput targets
        THROUGHPUT_TARGETS = {
            "small_conversion": 50,  # KB/s minimum
            "medium_conversion": 100,  # KB/s minimum
            "large_conversion": 200,  # KB/s minimum
        }

        for test_name, test_data in results["tests"].items():
            if not test_data.get("success", False):
                failures.append(
                    {
                        "type": "test_failure",
                        "test": test_name,
                        "message": f"{test_name} failed: {test_data.get('error', 'Unknown error')}",
                    }
                )
                continue

            # Check time-based targets
            if test_name in CI_TARGETS and "mean_seconds" in test_data:
                target = CI_TARGETS[test_name]
                actual = test_data["mean_seconds"]
                if actual > target["max_seconds"]:
                    failures.append(
                        {
                            "type": "performance_target",
                            "test": test_name,
                            "message": f"{target['description']}: {actual:.3f}s > {target['max_seconds']:.3f}s target",
                        }
                    )

            # Check memory targets
            for memory_metric, max_mb in MEMORY_TARGETS.items():
                if memory_metric in test_data and test_data[memory_metric] > max_mb:
                    failures.append(
                        {
                            "type": "memory_target",
                            "test": test_name,
                            "message": f"Memory usage: {test_data[memory_metric]:.1f}MB > {max_mb:.1f}MB target",
                        }
                    )

            # Check throughput targets
            if test_name in THROUGHPUT_TARGETS and "throughput_kb_per_sec" in test_data:
                min_throughput = THROUGHPUT_TARGETS[test_name]
                actual_throughput = test_data["throughput_kb_per_sec"]
                if actual_throughput < min_throughput:
                    failures.append(
                        {
                            "type": "throughput_target",
                            "test": test_name,
                            "message": f"Throughput: {actual_throughput:.1f} KB/s < {min_throughput} KB/s target",
                        }
                    )

        return failures

    def set_baseline(self, results: dict[str, Any]) -> None:
        """Set current results as the performance baseline."""
        with open(self.baseline_file, "w") as f:
            json.dump(results, f, indent=2)

    def generate_performance_report(
        self,
        results: dict[str, Any],
        regressions: list[dict[str, Any]],
        ci_failures: list[dict[str, str]] | None = None,
    ) -> str:
        """Generate a performance report."""
        if ci_failures is None:
            ci_failures = []

        report = []
        report.append("# Performance Report")
        report.append(f"**Generated:** {results['timestamp']}")
        report.append("")

        # Summary
        total_tests = len(results["tests"])
        successful_tests = sum(1 for test in results["tests"].values() if test.get("success", False))
        report.append(f"**Tests:** {successful_tests}/{total_tests} successful")

        if regressions:
            report.append(f"**Regressions:** {len(regressions)} detected ⚠️")
        else:
            report.append("**Regressions:** None detected ✅")

        if ci_failures:
            report.append(f"**CI Target Failures:** {len(ci_failures)} detected ❌")
        else:
            report.append("**CI Targets:** All met ✅")

        report.append("")

        # Performance results
        report.append("## Test Results")
        for test_name, test_result in results["tests"].items():
            if test_result.get("success", False):
                mean_time = test_result.get("mean_seconds", 0)
                throughput = test_result.get("throughput_kb_per_sec")
                memory_overhead = test_result.get("conversion_overhead_mb")

                report.append(f"### {test_name.replace('_', ' ').title()}")
                report.append(f"- Mean time: {mean_time:.3f}s")
                if throughput:
                    report.append(f"- Throughput: {throughput:.1f} KB/s")
                if memory_overhead is not None:
                    report.append(f"- Memory overhead: {memory_overhead:.1f}MB")

                # Performance assessment
                if "import" in test_name:
                    if mean_time < 0.020:
                        report.append("- ✅ Excellent speed")
                    elif mean_time < 0.050:
                        report.append("- ✅ Good speed")
                    else:
                        report.append("- ⚠️ Slow")
                elif "conversion" in test_name:
                    if throughput and throughput > 500:
                        report.append("- ✅ Excellent throughput")
                    elif throughput and throughput > 100:
                        report.append("- ✅ Good throughput")
                    elif throughput and throughput < 50:
                        report.append("- ❌ Poor throughput")
                    else:
                        report.append("- ⚠️ Moderate throughput")

                report.append("")
            else:
                report.append(f"### {test_name.replace('_', ' ').title()}")
                report.append(f"❌ **FAILED:** {test_result.get('error', 'Unknown error')}")
                report.append("")

        # CI Target Failures
        if ci_failures:
            report.append("## ❌ CI Target Failures")
            for failure in ci_failures:
                report.append(f"- **{failure['type']}:** {failure['message']}")
            report.append("")

        # Regressions
        if regressions:
            report.append("## ⚠️ Performance Regressions Detected")
            for regression in regressions:
                report.append(f"### {regression['comparison']}")
                report.append(f"- **Metric:** {regression['metric']}")
                report.append(f"- **Change:** {regression['percent_change']:+.1f}%")
                report.append(f"- **Severity:** {regression['severity']}")
                report.append("")

        return "\n".join(report)


def main():
    """Main entry point for performance monitoring."""
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Performance monitoring for Vexy Markliff")
    parser.add_argument("--set-baseline", action="store_true", help="Set current performance as baseline")
    parser.add_argument("--no-regression-check", action="store_true", help="Skip regression detection")
    parser.add_argument("--ci-mode", action="store_true", help="Run in CI mode (stricter thresholds, exit codes)")
    parser.add_argument("--update-baseline", action="store_true", help="Update baseline if no regressions")
    parser.add_argument("--json-output", help="Save results as JSON to specified file")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    monitor = PerformanceMonitor(project_root)

    # Enhanced CI mode detection
    is_ci = args.ci_mode or os.getenv("CI") == "true"

    if is_ci:
        pass

    # Run performance tests
    results = monitor.run_performance_tests()

    # Save results to history
    monitor.save_results(results)

    # Set baseline if requested
    if args.set_baseline:
        monitor.set_baseline(results)

    # Detect regressions unless disabled
    regressions = []
    if not args.no_regression_check:
        regressions = monitor.detect_regressions(results)

    # CI mode: check additional performance targets
    ci_failures = []
    if is_ci:
        ci_failures = monitor.check_ci_performance_targets(results)

    # Generate and display report
    report = monitor.generate_performance_report(results, regressions, ci_failures if is_ci else [])

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = monitor.perf_dir / f"perf_report_{timestamp}.md"
    with open(report_file, "w") as f:
        f.write(report)

    # Save JSON output if requested
    if args.json_output:
        with open(args.json_output, "w") as f:
            json.dump(results, f, indent=2)

    # Update baseline if requested and no issues found
    if args.update_baseline and not regressions and not ci_failures:
        monitor.set_baseline(results)

    # Determine exit status
    exit_code = 0

    if ci_failures:
        for _failure in ci_failures:
            pass
        exit_code = 1

    if regressions:
        major_regressions = [r for r in regressions if r["severity"] == "major"]
        if major_regressions:
            exit_code = 1
        elif is_ci:
            exit_code = 1  # In CI, treat minor regressions as failures

    if exit_code == 0:
        pass

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
