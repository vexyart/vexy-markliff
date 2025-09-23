#!/usr/bin/env python3
"""Quality Dashboard Generator for Vexy Markliff."""
# this_file: scripts/quality_dashboard.py

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class QualityDashboard:
    """Generate comprehensive quality dashboard combining all monitoring systems."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.dashboard_dir = project_root / "quality_dashboard"
        self.dashboard_dir.mkdir(exist_ok=True)

        # Import monitoring components
        self.metrics_dir = project_root / "quality_metrics"
        self.perf_dir = project_root / "performance_data"
        self.security_dir = project_root / "security_reports"

    def generate_dashboard(self) -> dict[str, Any]:
        """Generate comprehensive quality dashboard."""

        dashboard_data = {
            "generated_at": datetime.now().isoformat(),
            "project_info": self._get_project_info(),
            "overall_health": {},
            "quality_metrics": self._load_latest_quality_metrics(),
            "performance_metrics": self._load_latest_performance_metrics(),
            "security_status": self._load_latest_security_status(),
            "trends": self._analyze_trends(),
            "recommendations": self._generate_recommendations(),
        }

        # Calculate overall health score
        dashboard_data["overall_health"] = self._calculate_overall_health(dashboard_data)

        return dashboard_data

    def _get_project_info(self) -> dict[str, Any]:
        """Get basic project information."""
        info = {
            "name": "vexy-markliff",
            "description": "Bidirectional Markdown/HTML to XLIFF 2.1 converter",
        }

        # Try to get version
        try:
            result = subprocess.run(
                ["python", "-c", "import vexy_markliff; print(vexy_markliff.__version__)"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            info["version"] = result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            info["version"] = "unknown"

        # Git information
        try:
            # Get commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True, cwd=self.project_root
            )
            info["commit"] = result.stdout.strip()[:8] if result.returncode == 0 else "unknown"

            # Get branch
            result = subprocess.run(
                ["git", "branch", "--show-current"], check=False, capture_output=True, text=True, cwd=self.project_root
            )
            info["branch"] = result.stdout.strip() if result.returncode == 0 else "unknown"

        except Exception:
            info["commit"] = "unknown"
            info["branch"] = "unknown"

        return info

    def _load_latest_quality_metrics(self) -> dict[str, Any]:
        """Load the most recent quality metrics."""
        if not self.metrics_dir.exists():
            return {"available": False, "reason": "No metrics directory found"}

        # Find the most recent metrics file
        metrics_files = list(self.metrics_dir.glob("metrics_*.json"))
        if not metrics_files:
            return {"available": False, "reason": "No metrics files found"}

        latest_file = max(metrics_files, key=lambda f: f.stat().st_mtime)

        try:
            with open(latest_file) as f:
                data = json.load(f)
            data["available"] = True
            data["file"] = str(latest_file.name)
            return data
        except Exception as e:
            return {"available": False, "reason": f"Error loading metrics: {e}"}

    def _load_latest_performance_metrics(self) -> dict[str, Any]:
        """Load the most recent performance metrics."""
        if not self.perf_dir.exists():
            return {"available": False, "reason": "No performance directory found"}

        history_file = self.perf_dir / "history.json"
        if not history_file.exists():
            return {"available": False, "reason": "No performance history found"}

        try:
            with open(history_file) as f:
                history = json.load(f)

            if not history:
                return {"available": False, "reason": "Empty performance history"}

            latest = history[-1]
            latest["available"] = True
            latest["history_length"] = len(history)
            return latest
        except Exception as e:
            return {"available": False, "reason": f"Error loading performance data: {e}"}

    def _load_latest_security_status(self) -> dict[str, Any]:
        """Load the most recent security scan results."""
        if not self.security_dir.exists():
            return {"available": False, "reason": "No security directory found"}

        # Find the most recent security scan file
        security_files = list(self.security_dir.glob("security_scan_*.json"))
        if not security_files:
            return {"available": False, "reason": "No security scan files found"}

        latest_file = max(security_files, key=lambda f: f.stat().st_mtime)

        try:
            with open(latest_file) as f:
                data = json.load(f)
            data["available"] = True
            data["file"] = str(latest_file.name)
            return data
        except Exception as e:
            return {"available": False, "reason": f"Error loading security data: {e}"}

    def _analyze_trends(self) -> dict[str, Any]:
        """Analyze trends across historical data."""
        return {
            "performance": self._analyze_performance_trends(),
            "quality": self._analyze_quality_trends(),
            "security": self._analyze_security_trends(),
        }

    def _analyze_performance_trends(self) -> dict[str, Any]:
        """Analyze performance trends over time."""
        history_file = self.perf_dir / "history.json"
        if not history_file.exists():
            return {"available": False, "reason": "No performance history"}

        try:
            with open(history_file) as f:
                history = json.load(f)

            if len(history) < 2:
                return {"available": False, "reason": "Insufficient data for trend analysis"}

            # Analyze last 10 runs
            recent_data = history[-10:]

            # Extract key metrics over time
            import_times = []
            conversion_times = []

            for entry in recent_data:
                if "tests" in entry:
                    if "import_performance" in entry["tests"]:
                        test = entry["tests"]["import_performance"]
                        if test.get("success") and "mean_seconds" in test:
                            import_times.append(test["mean_seconds"])

                    if "small_conversion" in entry["tests"]:
                        test = entry["tests"]["small_conversion"]
                        if test.get("success") and "mean_seconds" in test:
                            conversion_times.append(test["mean_seconds"])

            trends = {}
            if len(import_times) >= 2:
                trends["import_time"] = self._calculate_trend(import_times)
            if len(conversion_times) >= 2:
                trends["conversion_time"] = self._calculate_trend(conversion_times)

            return {"available": True, "data_points": len(recent_data), "trends": trends}

        except Exception as e:
            return {"available": False, "reason": f"Error analyzing performance trends: {e}"}

    def _analyze_quality_trends(self) -> dict[str, Any]:
        """Analyze quality trends over time."""
        if not self.metrics_dir.exists():
            return {"available": False, "reason": "No quality metrics available"}

        # Get recent metrics files
        metrics_files = sorted(self.metrics_dir.glob("metrics_*.json"), key=lambda f: f.stat().st_mtime)[
            -5:
        ]  # Last 5 files

        if len(metrics_files) < 2:
            return {"available": False, "reason": "Insufficient data for trend analysis"}

        try:
            coverage_data = []
            test_success_data = []

            for file in metrics_files:
                with open(file) as f:
                    data = json.load(f)

                # Extract coverage data
                if "code_coverage" in data and "total_coverage" in data["code_coverage"]:
                    coverage_data.append(data["code_coverage"]["total_coverage"])

                # Extract test success data
                if "test_results" in data and "exit_code" in data["test_results"]:
                    test_success_data.append(1 if data["test_results"]["exit_code"] == 0 else 0)

            trends = {}
            if len(coverage_data) >= 2:
                trends["coverage"] = self._calculate_trend(coverage_data)
            if len(test_success_data) >= 2:
                success_rate = sum(test_success_data) / len(test_success_data)
                trends["test_success_rate"] = success_rate

            return {"available": True, "data_points": len(metrics_files), "trends": trends}

        except Exception as e:
            return {"available": False, "reason": f"Error analyzing quality trends: {e}"}

    def _analyze_security_trends(self) -> dict[str, Any]:
        """Analyze security trends over time."""
        if not self.security_dir.exists():
            return {"available": False, "reason": "No security data available"}

        # Get recent security files
        security_files = sorted(self.security_dir.glob("security_scan_*.json"), key=lambda f: f.stat().st_mtime)[
            -5:
        ]  # Last 5 files

        if len(security_files) < 2:
            return {"available": False, "reason": "Insufficient data for trend analysis"}

        try:
            vulnerability_counts = []

            for file in security_files:
                with open(file) as f:
                    data = json.load(f)

                # Count total vulnerabilities
                total_vulns = 0
                if "scans" in data:
                    for scan_name, scan_result in data["scans"].items():
                        if scan_name == "dependency_vulnerabilities":
                            if "safety" in scan_result and scan_result["safety"].get("success"):
                                total_vulns += scan_result["safety"].get("total_vulnerabilities", 0)

                vulnerability_counts.append(total_vulns)

            trends = {}
            if len(vulnerability_counts) >= 2:
                trends["vulnerabilities"] = self._calculate_trend(vulnerability_counts, reverse=True)

            return {"available": True, "data_points": len(security_files), "trends": trends}

        except Exception as e:
            return {"available": False, "reason": f"Error analyzing security trends: {e}"}

    def _calculate_trend(self, values: list[float], reverse: bool = False) -> dict[str, Any]:
        """Calculate trend direction and magnitude."""
        if len(values) < 2:
            return {"direction": "unknown", "magnitude": 0}

        # Simple trend calculation using first vs last value
        first_val = values[0]
        last_val = values[-1]

        if first_val == 0:
            return {"direction": "unknown", "magnitude": 0}

        percent_change = ((last_val - first_val) / first_val) * 100

        # For reverse metrics (like vulnerabilities), improvement means decrease
        if reverse:
            percent_change = -percent_change

        if percent_change > 5:
            direction = "improving"
        elif percent_change < -5:
            direction = "degrading"
        else:
            direction = "stable"

        return {"direction": direction, "magnitude": abs(percent_change), "percent_change": percent_change}

    def _calculate_overall_health(self, dashboard_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate overall project health score."""
        score = 100
        issues = []
        strengths = []

        # Quality metrics assessment
        quality_metrics = dashboard_data.get("quality_metrics", {})
        if quality_metrics.get("available"):
            # Code coverage
            if "code_coverage" in quality_metrics and "total_coverage" in quality_metrics["code_coverage"]:
                coverage = quality_metrics["code_coverage"]["total_coverage"]
                if coverage >= 90:
                    strengths.append(f"Excellent code coverage ({coverage:.1f}%)")
                elif coverage >= 80:
                    strengths.append(f"Good code coverage ({coverage:.1f}%)")
                elif coverage >= 70:
                    score -= 10
                    issues.append(f"Code coverage needs improvement ({coverage:.1f}%)")
                else:
                    score -= 20
                    issues.append(f"Low code coverage ({coverage:.1f}%)")

            # Test results
            if "test_results" in quality_metrics and "exit_code" in quality_metrics["test_results"]:
                if quality_metrics["test_results"]["exit_code"] == 0:
                    strengths.append("All tests passing")
                else:
                    score -= 15
                    issues.append("Some tests failing")

        # Performance assessment
        performance = dashboard_data.get("performance_metrics", {})
        if performance.get("available"):
            # Import performance
            if "tests" in performance and "import_performance" in performance["tests"]:
                import_test = performance["tests"]["import_performance"]
                if import_test.get("success") and "mean_seconds" in import_test:
                    import_time = import_test["mean_seconds"]
                    if import_time < 0.1:
                        strengths.append("Fast import performance")
                    elif import_time > 2.0:
                        score -= 10
                        issues.append("Slow import performance")

        # Security assessment
        security = dashboard_data.get("security_status", {})
        if security.get("available"):
            critical_issues = 0
            if "scans" in security:
                for scan_result in security["scans"].values():
                    if "safety" in scan_result and scan_result["safety"].get("success"):
                        critical_issues += scan_result["safety"].get("total_vulnerabilities", 0)

            if critical_issues == 0:
                strengths.append("No security vulnerabilities detected")
            else:
                score -= critical_issues * 5  # 5 points per vulnerability
                issues.append(f"{critical_issues} security vulnerabilities found")

        # Trend assessment
        trends = dashboard_data.get("trends", {})
        for trend_category, trend_data in trends.items():
            if trend_data.get("available") and "trends" in trend_data:
                for metric, trend_info in trend_data["trends"].items():
                    # Handle cases where trend_info might be a number instead of dict
                    if isinstance(trend_info, dict):
                        direction = trend_info.get("direction")
                        magnitude = trend_info.get("magnitude", 0)

                        if direction == "degrading" and magnitude > 10:
                            score -= 5
                            issues.append(f"{trend_category} {metric} is degrading")
                        elif direction == "improving" and magnitude > 10:
                            strengths.append(f"{trend_category} {metric} is improving")
                    else:
                        # trend_info is a scalar value, skip trend analysis
                        continue

        # Ensure score doesn't go below 0
        score = max(0, score)

        # Determine health status
        if score >= 90:
            status = "excellent"
            status_icon = "🟢"
        elif score >= 80:
            status = "good"
            status_icon = "🟡"
        elif score >= 70:
            status = "fair"
            status_icon = "🟠"
        else:
            status = "poor"
            status_icon = "🔴"

        return {
            "score": score,
            "status": status,
            "status_icon": status_icon,
            "issues": issues,
            "strengths": strengths,
            "assessment": f"Project health is {status} with a score of {score}/100",
        }

    def _generate_recommendations(self) -> list[dict[str, Any]]:
        """Generate actionable recommendations based on current metrics."""
        recommendations = []

        # Load current data to make recommendations
        quality_metrics = self._load_latest_quality_metrics()
        performance_metrics = self._load_latest_performance_metrics()
        security_status = self._load_latest_security_status()

        # Quality recommendations
        if quality_metrics.get("available"):
            if "code_coverage" in quality_metrics and "total_coverage" in quality_metrics["code_coverage"]:
                coverage = quality_metrics["code_coverage"]["total_coverage"]
                if coverage < 80:
                    recommendations.append(
                        {
                            "category": "quality",
                            "priority": "high",
                            "title": "Improve Code Coverage",
                            "description": f"Current coverage is {coverage:.1f}%. Target should be >80%.",
                            "action": "Add unit tests for uncovered modules",
                            "effort": "medium",
                        }
                    )

        # Performance recommendations
        if performance_metrics.get("available"):
            if "tests" in performance_metrics:
                for test_name, test_result in performance_metrics["tests"].items():
                    if test_result.get("success"):
                        if "import_performance" in test_name and "mean_seconds" in test_result:
                            if test_result["mean_seconds"] > 1.0:
                                recommendations.append(
                                    {
                                        "category": "performance",
                                        "priority": "medium",
                                        "title": "Optimize Import Performance",
                                        "description": f"Import time is {test_result['mean_seconds']:.2f}s",
                                        "action": "Review and optimize import dependencies",
                                        "effort": "low",
                                    }
                                )

        # Security recommendations
        if security_status.get("available"):
            if "scans" in security_status:
                total_vulns = 0
                for scan_result in security_status["scans"].values():
                    if "safety" in scan_result and scan_result["safety"].get("success"):
                        total_vulns += scan_result["safety"].get("total_vulnerabilities", 0)

                if total_vulns > 0:
                    recommendations.append(
                        {
                            "category": "security",
                            "priority": "high",
                            "title": "Address Security Vulnerabilities",
                            "description": f"{total_vulns} vulnerabilities found in dependencies",
                            "action": "Update vulnerable dependencies to secure versions",
                            "effort": "low",
                        }
                    )

        # General recommendations
        if not recommendations:
            recommendations.append(
                {
                    "category": "maintenance",
                    "priority": "low",
                    "title": "Maintain Current Quality",
                    "description": "Project metrics look good. Keep up the current practices.",
                    "action": "Continue regular monitoring and maintenance",
                    "effort": "low",
                }
            )

        return recommendations

    def generate_html_dashboard(self, dashboard_data: dict[str, Any]) -> str:
        """Generate HTML dashboard."""
        overall_health = dashboard_data["overall_health"]

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vexy Markliff Quality Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .health-score {{ font-size: 48px; color: #2563eb; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .card h3 {{ margin-top: 0; color: #1f2937; }}
        .metric {{ display: flex; justify-content: space-between; margin: 10px 0; }}
        .metric-value {{ font-weight: bold; }}
        .status-good {{ color: #059669; }}
        .status-warning {{ color: #d97706; }}
        .status-error {{ color: #dc2626; }}
        .trend-up {{ color: #059669; }}
        .trend-down {{ color: #dc2626; }}
        .trend-stable {{ color: #6b7280; }}
        .recommendations {{ margin-top: 20px; }}
        .recommendation {{ background: #f9fafb; padding: 15px; border-left: 4px solid #3b82f6; margin: 10px 0; }}
        .priority-high {{ border-left-color: #dc2626; }}
        .priority-medium {{ border-left-color: #d97706; }}
        .priority-low {{ border-left-color: #059669; }}
        .timestamp {{ color: #6b7280; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{overall_health["status_icon"]} Vexy Markliff Quality Dashboard</h1>
            <div class="health-score">{overall_health["score"]}/100</div>
            <p><strong>Status:</strong> {overall_health["assessment"]}</p>
            <p class="timestamp">Generated: {dashboard_data["generated_at"]}</p>
        </div>

        <div class="grid">
"""

        # Quality Metrics Card
        quality_metrics = dashboard_data.get("quality_metrics", {})
        html += """
            <div class="card">
                <h3>📊 Quality Metrics</h3>
"""
        if quality_metrics.get("available"):
            if "code_coverage" in quality_metrics and "total_coverage" in quality_metrics["code_coverage"]:
                coverage = quality_metrics["code_coverage"]["total_coverage"]
                status_class = (
                    "status-good" if coverage >= 80 else "status-warning" if coverage >= 70 else "status-error"
                )
                html += f"""
                <div class="metric">
                    <span>Code Coverage</span>
                    <span class="metric-value {status_class}">{coverage:.1f}%</span>
                </div>
"""
            if "test_results" in quality_metrics and "exit_code" in quality_metrics["test_results"]:
                test_status = "Passing" if quality_metrics["test_results"]["exit_code"] == 0 else "Failing"
                status_class = "status-good" if test_status == "Passing" else "status-error"
                html += f"""
                <div class="metric">
                    <span>Tests</span>
                    <span class="metric-value {status_class}">{test_status}</span>
                </div>
"""
        else:
            html += "<p>Quality metrics not available</p>"

        html += "</div>"

        # Performance Metrics Card
        performance = dashboard_data.get("performance_metrics", {})
        html += """
            <div class="card">
                <h3>⚡ Performance</h3>
"""
        if performance.get("available") and "tests" in performance:
            for test_name, test_result in performance["tests"].items():
                if test_result.get("success") and "mean_seconds" in test_result:
                    display_name = test_name.replace("_", " ").title()
                    time_val = test_result["mean_seconds"]
                    time_display = f"{time_val:.3f}s" if time_val >= 0.001 else f"{time_val * 1000:.1f}ms"

                    status_class = "status-good"
                    if ("import" in test_name and time_val > 1.0) or ("conversion" in test_name and time_val > 5.0):
                        status_class = "status-warning"

                    html += f"""
                <div class="metric">
                    <span>{display_name}</span>
                    <span class="metric-value {status_class}">{time_display}</span>
                </div>
"""
        else:
            html += "<p>Performance metrics not available</p>"

        html += "</div>"

        # Security Status Card
        security = dashboard_data.get("security_status", {})
        html += """
            <div class="card">
                <h3>🔒 Security</h3>
"""
        if security.get("available") and "scans" in security:
            total_vulns = 0
            for scan_result in security["scans"].values():
                if "safety" in scan_result and scan_result["safety"].get("success"):
                    total_vulns += scan_result["safety"].get("total_vulnerabilities", 0)

            status_class = "status-good" if total_vulns == 0 else "status-error"
            vuln_text = "No vulnerabilities" if total_vulns == 0 else f"{total_vulns} vulnerabilities"

            html += f"""
                <div class="metric">
                    <span>Vulnerabilities</span>
                    <span class="metric-value {status_class}">{vuln_text}</span>
                </div>
"""
        else:
            html += "<p>Security status not available</p>"

        html += "</div>"

        # Recommendations Card
        recommendations = dashboard_data.get("recommendations", [])
        html += """
            <div class="card">
                <h3>💡 Recommendations</h3>
                <div class="recommendations">
"""
        for rec in recommendations[:5]:  # Show top 5 recommendations
            priority_class = f"priority-{rec['priority']}"
            html += f"""
                <div class="recommendation {priority_class}">
                    <strong>{rec["title"]}</strong> ({rec["priority"]} priority)
                    <p>{rec["description"]}</p>
                    <p><em>Action:</em> {rec["action"]}</p>
                </div>
"""

        html += """
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html

    def save_dashboard(self, dashboard_data: dict[str, Any], save_html: bool = True) -> Path:
        """Save dashboard data and optionally generate HTML."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON data
        json_file = self.dashboard_dir / f"dashboard_{timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(dashboard_data, f, indent=2)

        # Save HTML dashboard
        if save_html:
            html_content = self.generate_html_dashboard(dashboard_data)
            html_file = self.dashboard_dir / f"dashboard_{timestamp}.html"
            with open(html_file, "w") as f:
                f.write(html_content)

            # Also save as latest.html for easy access
            latest_file = self.dashboard_dir / "latest.html"
            with open(latest_file, "w") as f:
                f.write(html_content)

            return html_file

        return json_file


def main():
    """Main entry point for quality dashboard generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate quality dashboard for Vexy Markliff")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML generation")
    parser.add_argument("--open", action="store_true", help="Open dashboard in browser")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    dashboard = QualityDashboard(project_root)

    # Generate dashboard
    dashboard_data = dashboard.generate_dashboard()

    # Display summary
    overall_health = dashboard_data["overall_health"]

    if overall_health["strengths"]:
        for _strength in overall_health["strengths"][:3]:
            pass

    if overall_health["issues"]:
        for _issue in overall_health["issues"][:3]:
            pass

    # Save dashboard
    dashboard.save_dashboard(dashboard_data, save_html=not args.no_html)

    # Open in browser if requested
    if args.open and not args.no_html:
        import webbrowser

        latest_file = dashboard.dashboard_dir / "latest.html"
        if latest_file.exists():
            webbrowser.open(f"file://{latest_file.absolute()}")


if __name__ == "__main__":
    main()
