#!/usr/bin/env python3
"""
Hardcoded Values Checker

Scans template files for hardcoded project-specific values that should be
replaced with configuration placeholders.
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Set


class HardcodedValuesChecker:
    """Checks for hardcoded values in template files."""

    def __init__(self, template_dir: str = ".temp", patterns_file: str = None):
        self.template_dir = Path(template_dir)
        self.issues: List[Dict[str, str]] = []
        self.checked_files: int = 0
        self.patterns_file = patterns_file or str(Path(__file__).parent / "hardcoded_patterns.txt")
        self.patterns_file = patterns_file or str(Path(__file__).parent / "hardcoded_patterns.txt")
        self.hardcoded_patterns = self._load_patterns()

    def _load_patterns(self) -> List[tuple]:
        """Load hardcoded patterns from file."""
        patterns = []
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse pattern|description|severity
                    parts = line.split('|')
                    if len(parts) == 3:
                        pattern, description, severity = parts
                        patterns.append((pattern.strip(), description.strip(), severity.strip()))
        except FileNotFoundError:
            print(f"⚠️  Patterns file not found: {self.patterns_file}")
            print("Using default patterns instead.")
            # Fallback to minimal default patterns
            patterns = [
                (r'\b(?:Proto|proto)\b', 'project name', 'warning'),
                (r'\b(?:nazh|naz-hage)\b', 'organization/user name', 'warning'),
            ]
        except Exception as e:
            print(f"⚠️  Error loading patterns file: {e}")
            print("Using default patterns instead.")
            patterns = [
                (r'\b(?:Proto|proto)\b', 'project name', 'warning'),
                (r'\b(?:nazh|naz-hage)\b', 'organization/user name', 'warning'),
            ]
        
        return patterns

    def check_all_files(self) -> bool:
        """Check all template files for hardcoded values."""
        if not self.template_dir.exists():
            print(f"❌ Template directory not found: {self.template_dir}")
            return False

        # Find all markdown and yaml files
        pattern = "**/*.{md,yaml,yml}"
        files = list(self.template_dir.glob(pattern))

        for file_path in files:
            self._check_file(file_path)

        self.checked_files = len(files)
        return len(self.issues) == 0

    def _check_file(self, file_path: Path) -> None:
        """Check a single file for hardcoded values."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except (UnicodeDecodeError, IOError) as e:
            self.issues.append({
                'file': str(file_path),
                'line': '1',
                'issue': f'Could not read file: {e}',
                'severity': 'error'
            })
            return

        for line_num, line in enumerate(lines, 1):
            self._check_line(file_path, line_num, line)

    def _check_line(self, file_path: Path, line_num: int, line: str) -> None:
        """Check a single line for hardcoded values."""

        # Skip lines that are already using placeholders
        if any(placeholder in line for placeholder in ['[PROJECT_NAME]', '[ORG_NAME]', '[TOOL_COMMAND]']):
            return

        # Use patterns loaded from file
        for pattern, description, severity in self.hardcoded_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                # Skip if it's in a code block or comment that explains it's an example
                if self._is_in_example_context(line, match.start()):
                    continue

                self.issues.append({
                    'file': str(file_path),
                    'line': str(line_num),
                    'issue': f'Potential hardcoded {description}: "{match.group()}"',
                    'severity': severity,
                    'context': line.strip()
                })

    def _is_in_example_context(self, line: str, match_pos: int) -> bool:
        """Check if a match is in an example context where hardcoded values are expected."""
        line_lower = line.lower()

        # Check for example indicators
        example_indicators = [
            'example',
            'e.g.',
            'for instance',
            'such as',
            'like',
            'sample',
            'demo',
            'test',
            'placeholder',
            'your-',
            'my-',
            'company-',
            'org-'
        ]

        # Check if any indicator is in the line
        if any(indicator in line_lower for indicator in example_indicators):
            return True

        # Check if it's in a code comment explaining it's an example
        if '#' in line and any(indicator in line_lower[line.find('#'):] for indicator in example_indicators):
            return True

        return False

    def print_results(self) -> None:
        """Print the results of the check."""
        if not self.issues:
            print("✅ No hardcoded values found!")
            print(f"Checked {self.checked_files} files.")
            return

        # Group issues by severity
        errors = [i for i in self.issues if i['severity'] == 'error']
        warnings = [i for i in self.issues if i['severity'] == 'warning']
        infos = [i for i in self.issues if i['severity'] == 'info']

        if errors:
            print("❌ Errors:")
            for issue in errors:
                print(f"  {issue['file']}:{issue['line']} - {issue['issue']}")
                if 'context' in issue:
                    print(f"    Context: {issue['context']}")
            print()

        if warnings:
            print("⚠️  Warnings:")
            for issue in warnings:
                print(f"  {issue['file']}:{issue['line']} - {issue['issue']}")
                if 'context' in issue:
                    print(f"    Context: {issue['context']}")
            print()

        if infos:
            print("ℹ️  Informational:")
            for issue in infos:
                print(f"  {issue['file']}:{issue['line']} - {issue['issue']}")
                if 'context' in issue:
                    print(f"    Context: {issue['context']}")
            print()

        print(f"Checked {self.checked_files} files.")
        print(f"Found {len(self.issues)} issues ({len(errors)} errors, {len(warnings)} warnings, {len(infos)} info)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check for hardcoded values in template files")
    parser.add_argument("template_dir", nargs="?", default=".temp",
                       help="Template directory to check (default: .temp)")
    parser.add_argument("--patterns-file", 
                       help="Path to patterns file (default: validation/hardcoded_patterns.txt)")
    parser.add_argument("--fix", action="store_true",
                       help="Attempt to fix some issues automatically")
    parser.add_argument("--exclude-patterns", nargs="*",
                       help="Additional regex patterns to exclude")

    args = parser.parse_args()

    checker = HardcodedValuesChecker(args.template_dir, args.patterns_file)

    if checker.check_all_files():
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        checker.print_results()

        # Count errors vs warnings
        errors = sum(1 for i in checker.issues if i['severity'] == 'error')
        if errors > 0:
            print("❌ Found errors that need to be addressed!")
            sys.exit(1)
        else:
            print("⚠️  Only warnings found. Review and fix as appropriate.")
            sys.exit(0)


if __name__ == "__main__":
    main()