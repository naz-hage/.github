# Validation Scripts

This directory contains validation scripts to ensure the `.temp` templates are properly genericized and ready for distribution.

## Scripts

### `check_hardcoded_values.py`

Scans template files for hardcoded project-specific values that should be replaced with configuration placeholders.

**Usage:**
```bash
# Check the default .temp directory
python validation/check_hardcoded_values.py

# Check a specific directory
python validation/check_hardcoded_values.py /path/to/templates

# Use a custom patterns file
python validation/check_hardcoded_values.py --patterns-file custom_patterns.txt
```

**Exit Codes:**
- `0`: All checks passed or only warnings found
- `1`: Errors found that must be addressed

### `validate_configs.py`

Validates YAML configuration files to ensure they have the correct structure and required fields.

**Usage:**
```bash
# Validate all config files in .temp
python validation/validate_configs.py

# Validate a specific config file
python validation/validate_configs.py .temp/project-config.yaml
```

## Pattern File Format

The `hardcoded_patterns.txt` file contains patterns to check for hardcoded values. Each line follows this format:

```
pattern|description|severity
```

- **pattern**: Regular expression pattern to match
- **description**: Human-readable description of what the pattern matches
- **severity**: One of `error`, `warning`, or `info`

**Example:**
```
\b(?:Proto|proto)\b|project name|warning
https?://[^\s"]*nazh[^\s"]*|hardcoded URL|warning
```

Lines starting with `#` are treated as comments and ignored.

### Adding New Patterns

To add checks for new hardcoded values:

1. Open `validation/hardcoded_patterns.txt`
2. Add a new line with the pattern, description, and severity
3. Run the checker to verify: `python validation/check_hardcoded_values.py`

**Example - Adding a new project name:**
```
\b(?:myproject|MyProject)\b|project name|warning
```

## Integration with CI/CD

These scripts can be integrated into your CI/CD pipeline to automatically validate templates:

```yaml
# Example GitHub Actions workflow
- name: Validate Templates
  run: |
    python validation/check_hardcoded_values.py
    python validation/validate_configs.py
```

## Common Issues

### False Positives

If the checker reports false positives for values that are intentionally used as examples:

1. Add context indicators like "example", "e.g.", or "sample" near the value
2. The checker automatically skips values in example contexts
3. Alternatively, add the value to the patterns file with `info` severity

### Missing Patterns

If you find hardcoded values that aren't being detected:

1. Add the pattern to `hardcoded_patterns.txt`
2. Test with: `python validation/check_hardcoded_values.py`
3. Commit the updated patterns file

## Best Practices

1. **Run Before Commits**: Always run validation before committing changes to templates
2. **Update Patterns**: Keep the patterns file updated with project-specific names
3. **Review Warnings**: Don't ignore warnings - they often indicate real issues
4. **Test Changes**: After updating templates, verify they still pass validation
