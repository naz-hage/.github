#!/usr/bin/env python3
"""
Configuration Validation Script

Validates project-config.yaml files for the generic template system.
Checks for required fields, data types, and configuration consistency.
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple


class ConfigValidator:
    """Validates project configuration files."""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.config: Dict[str, Any] = {}

    def validate(self) -> bool:
        """Run all validation checks."""
        try:
            self._load_config()
            self._validate_required_fields()
            self._validate_data_types()
            self._validate_platform_config()
            self._validate_language_config()
            self._validate_tool_config()
            self._validate_consistency()
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(f"Failed to validate config: {e}")
            return False

    def _load_config(self) -> None:
        """Load and parse the configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML syntax: {e}")

    def _validate_required_fields(self) -> None:
        """Validate that all required fields are present."""
        required_fields = [
            'project.name',
            'project.organization',
            'platforms',
            'language'
        ]

        for field_path in required_fields:
            if not self._get_nested_value(field_path):
                self.errors.append(f"Required field missing: {field_path}")

    def _validate_data_types(self) -> None:
        """Validate data types of configuration values."""
        # String fields
        string_fields = [
            'project.name',
            'project.organization',
            'project.description',
            'language',
            'framework',
            'tools.cli',
            'tools.test_runner',
            'tools.linter'
        ]

        for field_path in string_fields:
            value = self._get_nested_value(field_path)
            if value is not None and not isinstance(value, str):
                self.errors.append(f"Field {field_path} must be a string, got {type(value)}")

        # Boolean fields
        boolean_fields = [
            'platforms.azure_devops',
            'platforms.github',
            'platforms.jira'
        ]

        for field_path in boolean_fields:
            value = self._get_nested_value(field_path)
            if value is not None and not isinstance(value, bool):
                self.errors.append(f"Field {field_path} must be a boolean, got {type(value)}")

    def _validate_platform_config(self) -> None:
        """Validate platform configuration."""
        platforms = self.config.get('platforms', {})

        # At least one platform should be enabled
        enabled_platforms = [k for k, v in platforms.items() if v is True]
        if not enabled_platforms:
            self.warnings.append("No platforms are enabled. Consider enabling at least one platform.")

        # Validate platform-specific configurations
        if platforms.get('azure_devops'):
            self._validate_azure_devops_config()

        if platforms.get('github'):
            self._validate_github_config()

        if platforms.get('jira'):
            self._validate_jira_config()

    def _validate_azure_devops_config(self) -> None:
        """Validate Azure DevOps specific configuration."""
        azure_config = self.config.get('azure_devops', {})
        if not azure_config:
            self.warnings.append("Azure DevOps is enabled but no specific configuration provided")

    def _validate_github_config(self) -> None:
        """Validate GitHub specific configuration."""
        github_config = self.config.get('github', {})
        if not github_config:
            self.warnings.append("GitHub is enabled but no specific configuration provided")

    def _validate_jira_config(self) -> None:
        """Validate Jira specific configuration."""
        jira_config = self.config.get('jira', {})
        if not jira_config:
            self.warnings.append("Jira is enabled but no specific configuration provided")

    def _validate_language_config(self) -> None:
        """Validate language and framework configuration."""
        language = self.config.get('language', '').lower()
        framework = self.config.get('framework', '').lower()

        supported_languages = ['python', 'javascript', 'java', 'dotnet']
        if language and language not in supported_languages:
            self.warnings.append(f"Language '{language}' is not in the list of well-supported languages: {supported_languages}")

        # Language-specific validations
        if language == 'python':
            self._validate_python_config()
        elif language == 'javascript':
            self._validate_javascript_config()
        elif language == 'java':
            self._validate_java_config()
        elif language == 'dotnet':
            self._validate_dotnet_config()

    def _validate_python_config(self) -> None:
        """Validate Python-specific configuration."""
        python_config = self.config.get('python', {})
        if python_config.get('version'):
            version = python_config['version']
            if not self._is_valid_python_version(version):
                self.warnings.append(f"Python version '{version}' may not be supported")

    def _validate_javascript_config(self) -> None:
        """Validate JavaScript-specific configuration."""
        js_config = self.config.get('javascript', {})
        if js_config.get('runtime') not in ['node', 'bun', None]:
            self.warnings.append("JavaScript runtime should be 'node' or 'bun'")

    def _validate_java_config(self) -> None:
        """Validate Java-specific configuration."""
        java_config = self.config.get('java', {})
        if java_config.get('version'):
            version = java_config['version']
            if not self._is_valid_java_version(version):
                self.warnings.append(f"Java version '{version}' may not be LTS")

    def _validate_dotnet_config(self) -> None:
        """Validate .NET-specific configuration."""
        dotnet_config = self.config.get('dotnet', {})
        if dotnet_config.get('version'):
            version = dotnet_config['version']
            if not self._is_valid_dotnet_version(version):
                self.warnings.append(f".NET version '{version}' may not be supported")

    def _validate_tool_config(self) -> None:
        """Validate tool configuration."""
        tools = self.config.get('tools', {})

        # SAZ should be the primary CLI tool
        cli_tool = tools.get('cli', '').lower()
        if cli_tool != 'saz':
            self.warnings.append("Consider using 'saz' as the primary CLI tool for consistency")

        # Validate test runners based on language
        language = self.config.get('language', '').lower()
        test_runner = tools.get('test_runner', '').lower()

        if language == 'python' and test_runner not in ['pytest', 'unittest', '']:
            self.warnings.append("For Python, consider using 'pytest' or 'unittest' as test runner")

        if language == 'javascript' and test_runner not in ['jest', 'mocha', 'jasmine', '']:
            self.warnings.append("For JavaScript, consider using 'jest', 'mocha', or 'jasmine' as test runner")

        if language == 'java' and test_runner not in ['junit', 'testng', '']:
            self.warnings.append("For Java, consider using 'junit' or 'testng' as test runner")

        if language == 'dotnet' and test_runner not in ['xunit', 'nunit', 'mstest', '']:
            self.warnings.append("For .NET, consider using 'xunit', 'nunit', or 'mstest' as test runner")

    def _validate_consistency(self) -> None:
        """Validate configuration consistency."""
        # Check for conflicting platform configurations
        platforms = self.config.get('platforms', {})
        enabled_count = sum(1 for v in platforms.values() if v is True)

        if enabled_count > 1:
            self.warnings.append(f"Multiple platforms enabled ({enabled_count}). Ensure SAZ is configured correctly for all platforms.")

    def _get_nested_value(self, field_path: str) -> Any:
        """Get a nested value from the configuration using dot notation."""
        keys = field_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None

        return value

    def _is_valid_python_version(self, version: str) -> bool:
        """Check if Python version is reasonable."""
        try:
            major, minor = map(int, version.split('.')[:2])
            return major == 3 and minor >= 8
        except (ValueError, AttributeError):
            return False

    def _is_valid_java_version(self, version: str) -> bool:
        """Check if Java version is LTS."""
        lts_versions = ['8', '11', '17', '21']
        return version in lts_versions or version.startswith(('8.', '11.', '17.', '21.'))

    def _is_valid_dotnet_version(self, version: str) -> bool:
        """Check if .NET version is supported."""
        try:
            major, minor = map(int, version.split('.')[:2])
            return (major == 6 and minor >= 0) or (major == 7 and minor >= 0) or (major == 8 and minor >= 0)
        except (ValueError, AttributeError):
            return False

    def print_results(self) -> None:
        """Print validation results."""
        if self.errors:
            print("❌ Validation Errors:")
            for error in self.errors:
                print(f"  - {error}")
            print()

        if self.warnings:
            print("⚠️  Validation Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ Configuration is valid!")
            print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate project configuration files")
    parser.add_argument("config_path", nargs="?", default=".github/project-config.yaml",
                       help="Path to configuration file (default: .github/project-config.yaml)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")

    args = parser.parse_args()

    # Check if we're in a project directory
    if not Path(args.config_path).exists():
        # Try to find config in current directory or parent
        possible_paths = [
            ".github/project-config.yaml",
            "project-config.yaml",
            ".github/project-config.yml",
            "project-config.yml"
        ]

        for path in possible_paths:
            if Path(path).exists():
                args.config_path = path
                break
        else:
            print(f"❌ Configuration file not found. Tried: {', '.join(possible_paths)}")
            sys.exit(1)

    if args.verbose:
        print(f"Validating configuration: {args.config_path}")
        print()

    validator = ConfigValidator(args.config_path)

    if validator.validate():
        validator.print_results()
        print("🎉 Configuration validation successful!")
        sys.exit(0)
    else:
        validator.print_results()
        print("❌ Configuration validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()