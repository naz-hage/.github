---
name: nb-test
description: "Run tests using the custom Nbuild test system. Use when: user says 'run tests', 'test', 'execute tests', or needs to verify that code works correctly. Works for any project with nbuild test configuration."
---

# NB Test

Use `nb test` to run all unit tests in a C# project with the custom Nbuild test system.

## When to Use

- User says "run tests", "test the code", or "execute tests"
- Need to verify that recent code changes work correctly
- Want to check test coverage and results
- Working with ntools, ntools-launcher, or any nbuild-enabled project
- Before submitting code for review

## How to Run

Run the following command in the terminal from the project directory:

```bash
nb test
```

This command:
- Executes all unit tests in the project
- Uses the custom Nbuild test system
- Reports test results (passed/failed counts)
- Collects code coverage metrics
- Logs results to `nbuild.log`

## Test File Locations

Tests are typically located in folders matching these patterns:
- `*Tests/` or `*Test/` directories
- Files named `*Tests.cs`
- Test projects following convention: `*Tests.csproj` or `*Test.csproj`

## Checking Test Results

After running `nb test`, check the results in `nbuild.log`:

```bash
Get-Content nbuild.log | Select-String "Test Run|Passed|Failed|Total tests" -Context 1
```

Or view the full log:

```bash
cat nbuild.log
```

Look for:
- **Test Summary**: "Test Run Passed" or "Test Run Failed"
- **Test Count**: "Total tests:", "Passed:", "Failed:", "Skipped:"
- **Pass Rate**: Total passed vs. failed count
- **Coverage Report**: Code coverage percentage and location
- **Failures**: Details of any failed tests with error messages
- **Duration**: Total test execution time

## Test Results Interpretation

- ✅ **All Passed**: All tests passed, no failures
- ⚠️ **Skipped Tests**: Tests skipped (usually for platform-specific or optional scenarios)
- ❌ **Failures**: Some tests failed - review error details in log
- 📊 **Coverage**: Code coverage percentage (target usually 70%+)

## What It Does

- Discovers all test projects in the solution
- Executes tests using MSTest, xUnit, NUnit, or configured test framework
- Captures detailed test output
- Aggregates coverage metrics
- Reports summary and failures
- Logs complete results for review

## Common Issues

- **Location**: Must run from a project directory that has `unit-tests.targets` or `e2e-tests.targets`
- **Log File**: Always check `nbuild.log` in the project directory for detailed output
- **Skipped Tests**: Check test code for skip reasons (e.g., `[Ignore]`, platform-specific)
- **Failures**: Review failure message and stack trace in log

## Project Support

Works with:
- ✅ ntools-launcher (130+ tests)
- ✅ ntools (Python + C# tests)
- ✅ Any C# project with nbuild test configuration
