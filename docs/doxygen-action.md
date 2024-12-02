# Keypop Doxygen Documentation Action

Action for generating and publishing C++ API reference documentation using Doxygen. This action handles versioning,
navigation between versions, and proper organization of documentation artifacts.

#### Features

- **Automatic Version Detection**: Extracts version information from `CMakeLists.txt`
- **Version Management**:
    - Supports Java reference versions (`X.Y.Z`)
    - Handles C++-specific fixes (`X.Y.Z.T`)
    - Manages development versions (`X.Y.Z[.T]-SNAPSHOT`)
- **Documentation Organization**:
    - Creates versioned documentation directories
    - Maintains "latest-stable" symlink
    - Generates version navigation
    - Handles cleanup of SNAPSHOT versions upon release
- **Search Engine Optimization**:
    - Generates appropriate `robots.txt`
    - Maintains clean URLs structure
    - Proper indexing of stable versions

#### Usage

```yaml
- uses: eclipse-keypop/actions/doxygen@v1
  with:
    version: "1.0.0"              # Optional: Version to publish (auto-detected if not provided)
    repo-name: "keypop-example"   # Required: Repository name
```

#### Required Files

1. **Doxygen Configuration**:
    - Location: `.github/doxygen/Doxyfile`
    - Must use `%PROJECT_VERSION%` placeholder for version

2. **CMakeLists.txt Structure**:
```cmake
CMAKE_MINIMUM_REQUIRED(VERSION 3.5)

PROJECT(KeypopExample
        VERSION 2.1.1.1  # X.Y.Z[.T] format
        C CXX)

# Package information
SET(PACKAGE_NAME "keypop-example")
SET(PACKAGE_VERSION ${CMAKE_PROJECT_VERSION})
SET(PACKAGE_STRING "${PACKAGE_NAME} ${PACKAGE_VERSION}")
```

The version is determined as follows:
- Version is taken directly from `PROJECT(VERSION X.Y.Z[.T])`
    - X.Y.Z matches the Java reference version
    - Optional T number indicates C++-specific fixes
- Without explicit version parameter, it becomes `X.Y.Z[.T]-SNAPSHOT` for development builds

#### Documentation Structure

The action generates the following structure in your GitHub Pages:
```
repository-gh-pages/
├── 2.1.1.1-SNAPSHOT/    # Development version with C++ fix
├── latest-stable/       # Symlink to latest stable version
├── 2.1.1.1/             # Stable version with C++ fix
├── 2.1.1/               # Java reference version
├── list_versions.md     # Version listing
└── robots.txt           # Search engine directives
```

### Workflow Examples

#### Publishing Release Documentation

```yaml
name: Publish API documentation (release)
on:
  release:
    types: [published]

jobs:
  publish-doc-release:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Extract repository information
        id: repo-info
        shell: bash
        run: |
          {
            echo "repo_name=${GITHUB_REPOSITORY#*/}"
            echo "version=${GITHUB_REF#refs/tags/}"
          } >> "$GITHUB_OUTPUT"

      - name: Generate and prepare documentation
        uses: eclipse-keypop/keypop-action-docs/doxygen@v1
        with:
          repo-name: ${{ steps.repo-info.outputs.repo_name }}
          version: ${{ steps.repo-info.outputs.version }}

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./${{ github.event.repository.name }}
          enable_jekyll: true
          user_name: 'github-actions[bot]'
          user_email: 'github-actions[bot]@users.noreply.github.com'
          commit_message: 'docs: update ${{ steps.repo-info.outputs.version }} documentation'
```

This workflow is triggered when a release is published. It:
1. Checks out the repository with full history
2. Extracts the repository name and release version from the git tag
3. Generates the documentation using the specified version
4. Deploys the generated documentation to GitHub Pages

#### Publishing Documentation on Release

For release documentation, create a separate workflow triggered by release events. The workflow is similar but includes the version parameter:

```yaml
- uses: eclipse-keypop/actions/doxygen@v1
  with:
    version: ${{ steps.repo-info.outputs.version }}
    repo-name: ${{ steps.repo-info.outputs.repo_name }}
```

## Version Management

The action handles version management through the following rules:

1. **Version Detection**:
    - Reads version from `PROJECT(VERSION X.Y.Z[.T])` in `CMakeLists.txt`
    - Without explicit version parameter, treats as development (SNAPSHOT) version

2. **Version Types**:
    - Base version (`X.Y.Z`): Matches Java reference version
    - Fix version (`X.Y.Z.T`): C++-specific fixes for Java version X.Y.Z
    - SNAPSHOT (`X.Y.Z[.T]-SNAPSHOT`): Development versions

3. **Version Lifecycle**:
    - SNAPSHOT versions are replaced when their corresponding release is published
    - All non-SNAPSHOT versions are considered stable
    - Latest stable version is always accessible via the `latest-stable` symlink
    - The fourth number (T) represents C++-specific fixes for a given Java version
    - A version can't have both released and SNAPSHOT states at the same time