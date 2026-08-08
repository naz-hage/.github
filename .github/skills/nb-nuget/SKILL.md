---
name: nb-nuget
description: Build and publish NuGet packages locally using the custom Nbuild system
triggers:
  - build nuget
  - publish nuget
  - nuget add
  - nuget package
  - pack nuget
---

# NuGet Package Build Skill

## Purpose
Builds a C# project as a NuGet package and publishes it to a local NuGet feed for testing. Uses the custom Nbuild system to ensure consistent builds.

## When to Use
- User says "build nuget", "publish nuget", "pack nuget", or "nuget add"
- Need to create a local NuGet package for testing before publishing to public feed
- Rebuilding ntools-launcher or other packages after code changes
- Testing package dependencies before publishing to NuGet.org

## How to Use

### Build and Publish Locally
```powershell
nb nuget_add
```

This command:
1. Compiles the project
2. Creates a NuGet package (.nupkg file)
3. Publishes to local NuGet feed for testing

### Verify Package Published
After publishing, verify the package is available:
```powershell
dotnet nuget search <package-name> --source <local-feed-path>
```

## Common Workflows

### ntools-launcher Package
```powershell
cd c:\source\ntools-launcher
nb nuget_add
```

Result: Package published to local feed, ready for testing in sdo-e2e-test or other consumers.

### Update Consumer Project
After publishing ntools-launcher locally:
```powershell
cd c:\source\ntools
dotnet build .\sdo-e2e-test\sdo-e2e-test.csproj
```

The project will use the updated local package.

## Package Metadata

When rebuilding packages, verify:
- ✅ Version incremented in .csproj or .nuspec
- ✅ Dependencies properly declared (especially transitive ones like YamlDotNet)
- ✅ Package metadata complete (authors, description, license)
- ✅ Build succeeds with 0 errors

## Local NuGet Feed

Packages are typically published to:
- Windows: `%USERPROFILE%\.nuget\packages` or custom local folder
- Configuration: Stored in `NuGet.config`

## Troubleshooting

**Package not found after publishing:**
- Check NuGet.config for local feed path
- Verify package file exists in feed directory
- Clear NuGet cache: `dotnet nuget locals all --clear`

**Dependency resolution issues:**
- Ensure dependencies are declared in .nuspec or .csproj
- Transitive dependencies (like YamlDotNet for ntools-launcher) must be explicit
- Rebuild and republish after dependency changes

**Version conflicts:**
- Increment package version before republishing
- Remove old version from local feed if needed
- Clear NuGet cache before rebuilding

## ⚠️ WINDOWS ONLY - DO NOT USE UNIX COMMANDS

**CRITICAL**: This workspace runs on Windows PowerShell. DO NOT use Unix/Linux commands:

❌ **NEVER use**:
- `tail` - does not exist on Windows
- `grep` - use `Select-String` instead
- `cat` - use `Get-Content` instead
- `head` - use `Select-Object -First` instead
- Any pipe to `tail` like `| tail -20` - use `| Select-Object -Last 20` instead

✅ **ALWAYS use PowerShell equivalents**:
- View end of file: `Get-Content file.log | Select-Object -Last 20`
- Search file: `Get-Content file.log | Select-String "pattern"`
- View beginning: `Get-Content file.log | Select-Object -First 20`
