#!/usr/bin/env python3
"""Dependency Vulnerability Scanning Automation for Vexy Markliff."""
# this_file: scripts/security_scanner.py

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class SecurityScanner:
    """Automated security and vulnerability scanning for dependencies and code."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.security_dir = project_root / "security_reports"
        self.security_dir.mkdir(exist_ok=True)

    def run_full_security_scan(self) -> dict[str, Any]:
        """Run comprehensive security scan and return results."""

        results = {"timestamp": datetime.now().isoformat(), "scans": {}}

        # Scan 1: Dependency vulnerability scanning with safety
        results["scans"]["dependency_vulnerabilities"] = self._scan_dependency_vulnerabilities()

        # Scan 2: Code security scanning with bandit
        results["scans"]["code_security"] = self._scan_code_security()

        # Scan 3: Dependency license scanning
        results["scans"]["license_compliance"] = self._scan_license_compliance()

        # Scan 4: Supply chain security
        results["scans"]["supply_chain"] = self._scan_supply_chain_security()

        # Scan 5: Configuration security
        results["scans"]["configuration"] = self._scan_configuration_security()

        return results

    def _scan_dependency_vulnerabilities(self) -> dict[str, Any]:
        """Scan dependencies for known vulnerabilities using safety and pip-audit."""

        vulnerabilities = {}

        # Try safety first
        try:
            result = subprocess.run(
                ["uvx", "safety", "check", "--json"], check=False, capture_output=True, text=True, cwd=self.project_root
            )

            if result.stdout:
                safety_data = json.loads(result.stdout)
                vulnerabilities["safety"] = {
                    "total_vulnerabilities": len(safety_data),
                    "vulnerabilities": safety_data,
                    "success": True,
                }
            else:
                vulnerabilities["safety"] = {"total_vulnerabilities": 0, "vulnerabilities": [], "success": True}
        except subprocess.CalledProcessError as e:
            vulnerabilities["safety"] = {"success": False, "error": f"Safety scan failed: {e}"}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            vulnerabilities["safety"] = {"success": False, "error": f"Safety not available or invalid output: {e}"}

        # Try pip-audit as alternative/additional check
        try:
            result = subprocess.run(
                ["uvx", "pip-audit", "--format=json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.stdout:
                audit_data = json.loads(result.stdout)
                vulnerabilities["pip_audit"] = {
                    "total_vulnerabilities": len(audit_data.get("vulnerabilities", [])),
                    "vulnerabilities": audit_data.get("vulnerabilities", []),
                    "success": True,
                }
            else:
                vulnerabilities["pip_audit"] = {"total_vulnerabilities": 0, "vulnerabilities": [], "success": True}
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            vulnerabilities["pip_audit"] = {"success": False, "error": f"pip-audit failed: {e}"}

        # Manual check for known problematic packages
        vulnerabilities["manual_checks"] = self._manual_dependency_checks()

        return vulnerabilities

    def _manual_dependency_checks(self) -> dict[str, Any]:
        """Perform manual checks for known problematic dependencies."""
        problematic_packages = {
            # Known packages with historical security issues
            "requests": {"min_safe_version": "2.31.0", "reason": "CVE fixes"},
            "urllib3": {"min_safe_version": "2.0.7", "reason": "CVE-2023-45803"},
            "pydantic": {"min_safe_version": "2.0.0", "reason": "Security improvements"},
            "lxml": {"min_safe_version": "4.9.1", "reason": "CVE fixes"},
        }

        try:
            # Get current dependency versions
            result = subprocess.run(
                ["uvx", "pip", "list", "--format=json"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            installed_packages = json.loads(result.stdout)
            package_dict = {pkg["name"].lower(): pkg["version"] for pkg in installed_packages}

            warnings = []
            for package, constraints in problematic_packages.items():
                if package in package_dict:
                    current_version = package_dict[package]
                    min_safe = constraints["min_safe_version"]

                    # Simple version comparison (works for most cases)
                    if self._version_is_less_than(current_version, min_safe):
                        warnings.append(
                            {
                                "package": package,
                                "current_version": current_version,
                                "min_safe_version": min_safe,
                                "reason": constraints["reason"],
                                "severity": "medium",
                            }
                        )

            return {"warnings": warnings, "total_warnings": len(warnings), "success": True}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _version_is_less_than(self, current: str, minimum: str) -> bool:
        """Simple version comparison. Returns True if current < minimum."""
        try:
            # Split versions into components and compare
            current_parts = [int(x) for x in current.split(".")]
            minimum_parts = [int(x) for x in minimum.split(".")]

            # Pad to same length
            max_len = max(len(current_parts), len(minimum_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            minimum_parts.extend([0] * (max_len - len(minimum_parts)))

            return current_parts < minimum_parts
        except (ValueError, AttributeError):
            # If version parsing fails, assume it's safe
            return False

    def _scan_code_security(self) -> dict[str, Any]:
        """Scan source code for security issues using bandit."""

        try:
            result = subprocess.run(
                ["uvx", "bandit", "-r", "src/", "-f", "json", "-ll"],  # -ll for low and high severity only
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.stdout:
                bandit_data = json.loads(result.stdout)
                issues = bandit_data.get("results", [])

                return {
                    "total_issues": len(issues),
                    "issues_by_severity": self._group_security_issues(issues),
                    "critical_issues": [issue for issue in issues if issue.get("issue_severity") == "HIGH"],
                    "success": True,
                }
            return {
                "total_issues": 0,
                "issues_by_severity": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
                "critical_issues": [],
                "success": True,
            }

        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            return {"success": False, "error": f"Bandit scan failed: {e}"}

    def _group_security_issues(self, issues: list[dict[str, Any]]) -> dict[str, int]:
        """Group security issues by severity."""
        groups = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for issue in issues:
            severity = issue.get("issue_severity", "LOW")
            if severity in groups:
                groups[severity] += 1
        return groups

    def _scan_license_compliance(self) -> dict[str, Any]:
        """Scan dependency licenses for compliance issues."""

        try:
            # Get package information with licenses
            result = subprocess.run(
                ["uvx", "pip-licenses", "--format=json", "--with-urls"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.stdout:
                license_data = json.loads(result.stdout)

                # Define problematic licenses
                problematic_licenses = {
                    "GPL-3.0": "Strong copyleft license",
                    "AGPL-3.0": "Network copyleft license",
                    "GPL-2.0": "Strong copyleft license",
                    "LGPL-3.0": "Weak copyleft license",
                }

                warnings = []
                license_counts = {}

                for package in license_data:
                    license_name = package.get("License", "Unknown")
                    license_counts[license_name] = license_counts.get(license_name, 0) + 1

                    if license_name in problematic_licenses:
                        warnings.append(
                            {
                                "package": package.get("Name"),
                                "version": package.get("Version"),
                                "license": license_name,
                                "reason": problematic_licenses[license_name],
                                "url": package.get("URL"),
                            }
                        )

                return {
                    "total_packages": len(license_data),
                    "license_distribution": license_counts,
                    "problematic_licenses": warnings,
                    "warnings_count": len(warnings),
                    "success": True,
                }

        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            return {"success": False, "error": f"License scan failed: {e}"}

    def _scan_supply_chain_security(self) -> dict[str, Any]:
        """Scan for supply chain security issues."""

        issues = []
        checks = {
            "pinned_dependencies": self._check_pinned_dependencies(),
            "trusted_sources": self._check_trusted_sources(),
            "lockfile_present": self._check_lockfile_present(),
        }

        for check_name, result in checks.items():
            if not result["secure"]:
                issues.append(
                    {"check": check_name, "issue": result["issue"], "recommendation": result["recommendation"]}
                )

        return {"total_issues": len(issues), "issues": issues, "checks_performed": list(checks.keys()), "success": True}

    def _check_pinned_dependencies(self) -> dict[str, Any]:
        """Check if dependencies are properly pinned."""
        pyproject_file = self.project_root / "pyproject.toml"
        if not pyproject_file.exists():
            return {
                "secure": False,
                "issue": "No pyproject.toml found",
                "recommendation": "Create pyproject.toml with pinned dependencies",
            }

        try:
            content = pyproject_file.read_text()
            # Simple check for version pinning (look for >= or ~ or exact versions)
            unpinned_indicators = ["*", ">=", ">"]
            has_unpinned = any(indicator in content for indicator in unpinned_indicators)

            if has_unpinned:
                return {
                    "secure": False,
                    "issue": "Some dependencies appear to be unpinned",
                    "recommendation": "Pin all production dependencies to specific versions",
                }

            return {"secure": True, "issue": None, "recommendation": None}

        except Exception as e:
            return {
                "secure": False,
                "issue": f"Could not analyze pyproject.toml: {e}",
                "recommendation": "Review dependency pinning manually",
            }

    def _check_trusted_sources(self) -> dict[str, Any]:
        """Check if using trusted package sources."""
        # This is a basic check - in practice you'd want more sophisticated analysis
        pip_conf_locations = [
            Path.home() / ".pip" / "pip.conf",
            Path.home() / ".config" / "pip" / "pip.conf",
            self.project_root / "pip.conf",
        ]

        for conf_file in pip_conf_locations:
            if conf_file.exists():
                try:
                    content = conf_file.read_text()
                    if "extra-index-url" in content or "trusted-host" in content:
                        return {
                            "secure": False,
                            "issue": "Custom package indexes or trusted hosts configured",
                            "recommendation": "Verify all custom package sources are trusted",
                        }
                except Exception:
                    pass

        return {"secure": True, "issue": None, "recommendation": None}

    def _check_lockfile_present(self) -> dict[str, Any]:
        """Check if dependency lockfile is present."""
        lockfiles = ["uv.lock", "poetry.lock", "Pipfile.lock", "requirements.txt"]
        present_lockfiles = [f for f in lockfiles if (self.project_root / f).exists()]

        if not present_lockfiles:
            return {
                "secure": False,
                "issue": "No dependency lockfile found",
                "recommendation": "Use uv.lock or requirements.txt to lock dependency versions",
            }

        return {"secure": True, "issue": None, "recommendation": None}

    def _scan_configuration_security(self) -> dict[str, Any]:
        """Scan configuration files for security issues."""

        issues = []

        # Check for secrets in configuration files
        config_files = [
            self.project_root / "pyproject.toml",
            self.project_root / ".env",
            self.project_root / "config.yml",
            self.project_root / "config.yaml",
        ]

        secret_patterns = [
            r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]+['\"]",
            r"(?i)(secret|token|key)\s*[:=]\s*['\"][^'\"]+['\"]",
            r"(?i)(api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]",
        ]

        for config_file in config_files:
            if config_file.exists():
                try:
                    content = config_file.read_text()
                    for pattern in secret_patterns:
                        import re

                        if re.search(pattern, content):
                            issues.append(
                                {
                                    "file": str(config_file.relative_to(self.project_root)),
                                    "issue": "Potential secret in configuration file",
                                    "severity": "high",
                                    "recommendation": "Move secrets to environment variables",
                                }
                            )
                            break  # One issue per file is enough
                except Exception:
                    pass

        # Check for insecure default configurations
        pyproject_file = self.project_root / "pyproject.toml"
        if pyproject_file.exists():
            try:
                content = pyproject_file.read_text()
                if "debug = true" in content.lower():
                    issues.append(
                        {
                            "file": "pyproject.toml",
                            "issue": "Debug mode enabled",
                            "severity": "medium",
                            "recommendation": "Disable debug mode in production",
                        }
                    )
            except Exception:
                pass

        return {"total_issues": len(issues), "issues": issues, "success": True}

    def generate_security_report(self, results: dict[str, Any]) -> str:
        """Generate a comprehensive security report."""
        report = []
        report.append("# Security Scan Report")
        report.append(f"**Generated:** {results['timestamp']}")
        report.append("")

        # Summary
        total_critical = 0
        total_warnings = 0
        failed_scans = []

        for scan_name, scan_result in results["scans"].items():
            if not scan_result.get("success", True):
                failed_scans.append(scan_name)
                continue

            # Count critical issues across all scans
            if scan_name == "dependency_vulnerabilities":
                if "safety" in scan_result and scan_result["safety"].get("success"):
                    total_critical += scan_result["safety"].get("total_vulnerabilities", 0)
                if "pip_audit" in scan_result and scan_result["pip_audit"].get("success"):
                    total_critical += scan_result["pip_audit"].get("total_vulnerabilities", 0)

            elif scan_name == "code_security" and scan_result.get("success"):
                critical_issues = scan_result.get("critical_issues", [])
                total_critical += len(critical_issues)

            elif scan_name == "license_compliance" and scan_result.get("success"):
                total_warnings += scan_result.get("warnings_count", 0)

            elif scan_name == "supply_chain" and scan_result.get("success"):
                total_warnings += scan_result.get("total_issues", 0)

            elif scan_name == "configuration" and scan_result.get("success"):
                high_severity = [i for i in scan_result.get("issues", []) if i.get("severity") == "high"]
                total_critical += len(high_severity)

        # Security status
        if total_critical > 0:
            report.append(f"🚨 **Security Status: CRITICAL** - {total_critical} critical issues found")
        elif total_warnings > 0:
            report.append(f"⚠️ **Security Status: WARNING** - {total_warnings} warnings found")
        else:
            report.append("✅ **Security Status: GOOD** - No critical issues found")

        if failed_scans:
            report.append(f"❌ **Failed Scans:** {', '.join(failed_scans)}")

        report.append("")

        # Detailed results
        for scan_name, scan_result in results["scans"].items():
            report.append(f"## {scan_name.replace('_', ' ').title()}")

            if not scan_result.get("success", True):
                report.append(f"❌ Scan failed: {scan_result.get('error', 'Unknown error')}")
                report.append("")
                continue

            if scan_name == "dependency_vulnerabilities":
                self._add_vulnerability_details(report, scan_result)
            elif scan_name == "code_security":
                self._add_code_security_details(report, scan_result)
            elif scan_name == "license_compliance":
                self._add_license_details(report, scan_result)
            elif scan_name == "supply_chain":
                self._add_supply_chain_details(report, scan_result)
            elif scan_name == "configuration":
                self._add_config_security_details(report, scan_result)

            report.append("")

        return "\n".join(report)

    def _add_vulnerability_details(self, report: list[str], scan_result: dict[str, Any]) -> None:
        """Add vulnerability scan details to report."""
        total_vulns = 0
        if "safety" in scan_result and scan_result["safety"].get("success"):
            safety_vulns = scan_result["safety"].get("total_vulnerabilities", 0)
            total_vulns += safety_vulns
            report.append(f"- Safety scan: {safety_vulns} vulnerabilities")

        if "pip_audit" in scan_result and scan_result["pip_audit"].get("success"):
            audit_vulns = scan_result["pip_audit"].get("total_vulnerabilities", 0)
            total_vulns += audit_vulns
            report.append(f"- Pip-audit scan: {audit_vulns} vulnerabilities")

        if "manual_checks" in scan_result and scan_result["manual_checks"].get("success"):
            manual_warnings = scan_result["manual_checks"].get("total_warnings", 0)
            report.append(f"- Manual checks: {manual_warnings} warnings")

        if total_vulns == 0:
            report.append("✅ No vulnerabilities detected")

    def _add_code_security_details(self, report: list[str], scan_result: dict[str, Any]) -> None:
        """Add code security details to report."""
        total_issues = scan_result.get("total_issues", 0)
        if total_issues == 0:
            report.append("✅ No code security issues found")
        else:
            severity_breakdown = scan_result.get("issues_by_severity", {})
            report.append(f"- Total issues: {total_issues}")
            for severity, count in severity_breakdown.items():
                if count > 0:
                    icon = "🚨" if severity == "HIGH" else "⚠️" if severity == "MEDIUM" else "ℹ️"
                    report.append(f"  - {icon} {severity}: {count}")

    def _add_license_details(self, report: list[str], scan_result: dict[str, Any]) -> None:
        """Add license compliance details to report."""
        warnings_count = scan_result.get("warnings_count", 0)
        total_packages = scan_result.get("total_packages", 0)

        if warnings_count == 0:
            report.append(f"✅ License compliance OK ({total_packages} packages checked)")
        else:
            report.append(f"⚠️ {warnings_count} license warnings out of {total_packages} packages")

    def _add_supply_chain_details(self, report: list[str], scan_result: dict[str, Any]) -> None:
        """Add supply chain security details to report."""
        total_issues = scan_result.get("total_issues", 0)
        if total_issues == 0:
            report.append("✅ Supply chain security looks good")
        else:
            report.append(f"⚠️ {total_issues} supply chain issues detected")

    def _add_config_security_details(self, report: list[str], scan_result: dict[str, Any]) -> None:
        """Add configuration security details to report."""
        total_issues = scan_result.get("total_issues", 0)
        if total_issues == 0:
            report.append("✅ Configuration security OK")
        else:
            issues = scan_result.get("issues", [])
            high_severity = [i for i in issues if i.get("severity") == "high"]
            medium_severity = [i for i in issues if i.get("severity") == "medium"]

            if high_severity:
                report.append(f"🚨 {len(high_severity)} high-severity configuration issues")
            if medium_severity:
                report.append(f"⚠️ {len(medium_severity)} medium-severity configuration issues")


def main():
    """Main entry point for security scanning."""
    import argparse

    parser = argparse.ArgumentParser(description="Security scanning for Vexy Markliff")
    parser.add_argument("--save-report", action="store_true", help="Save detailed report to file")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    scanner = SecurityScanner(project_root)

    # Run security scans
    results = scanner.run_full_security_scan()

    # Generate and display report
    report = scanner.generate_security_report(results)

    # Save detailed results if requested
    if args.save_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save full JSON results
        results_file = scanner.security_dir / f"security_scan_{timestamp}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)

        # Save human-readable report
        report_file = scanner.security_dir / f"security_report_{timestamp}.md"
        with open(report_file, "w") as f:
            f.write(report)

    # Check for critical issues and exit with appropriate code
    critical_issues = 0

    for scan_result in results["scans"].values():
        if not scan_result.get("success", True):
            continue

        # Count critical vulnerabilities
        if "safety" in scan_result and scan_result["safety"].get("success"):
            critical_issues += scan_result["safety"].get("total_vulnerabilities", 0)

        if "pip_audit" in scan_result and scan_result["pip_audit"].get("success"):
            critical_issues += scan_result["pip_audit"].get("total_vulnerabilities", 0)

        # Count high-severity code issues
        if "critical_issues" in scan_result:
            critical_issues += len(scan_result["critical_issues"])

    if critical_issues > 0:
        sys.exit(1)
    else:
        pass


if __name__ == "__main__":
    main()
