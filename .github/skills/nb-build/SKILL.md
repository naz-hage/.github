---
name: nb-build
description: "Build a C# project using the custom Nbuild system. Use when: user says 'build project', 'build', 'compile', or needs to compile the C# code. Works for any project with nbuild.targets in the workspace."
---

# NB Build

Use `nb build` to compile C# projects with the custom Nbuild build system.

## When to Use

- User says "build project" or "build the code"
- Code changes need to be compiled
- Need to verify compilation before running tests
- Working with ntools, ntools-launcher, or any nbuild-enabled project

## How to Run

Run the following command in the terminal from the project directory:

```bash
nb build
```

This command:
- Compiles the C# project
- Runs the custom Nbuild system
- Returns build status and any compilation errors
- Logs results to `nbuild.log`

## Checking Build Results

After running `nb build`, check the results in `nbuild.log`:

```bash
Get-Content nbuild.log | Select-String "Build succeeded|Build failed|error|warning" -Context 2
```

Or view the full log:

```bash
cat nbuild.log
```

Look for:
- **Success**: "Build succeeded" or "BUILD_SUCCEEDED"
- **Failures**: Error messages starting with "error" or "ERROR"
- **Warnings**: Warning messages that need addressing
- **Build Summary**: Section showing overall build status

## What It Does

- Compiles all C# projects in the solution
- Validates the build configuration
- Reports compilation errors and warnings
- Generates any necessary artifacts
- Works with MSBuild/Visual Studio projects

## Common Issues

- **Location**: Must run from a project directory that has `nbuild.targets`
- **Log File**: Always check `nbuild.log` in the project directory for detailed output
- **Errors**: Build errors will be listed with file and line number
- **Warnings**: Can indicate potential issues that should be reviewed

## Project Support

Works with:
- ✅ ntools-launcher
- ✅ ntools
- ✅ Any C# project with nbuild.targets configured
