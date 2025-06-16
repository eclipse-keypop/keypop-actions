# Eclipse Keypop Reusable Workflows and Composite Actions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains all **GitHub Actions** and **reusable workflows** for the `eclipse-keypop` organization. It’s structured to separate **custom composite actions**, **reusable workflows**, and to clearly mark **deprecated** items.

---

## 🔁 Reusable Workflows

These can be invoked in any org repo via `workflow_call`:

| Name                           | Description                                           | Path                                                           |
|--------------------------------|-------------------------------------------------------|----------------------------------------------------------------|
| Publish Snapshot               | Publish snapshot versions to Maven Central           | `.github/workflows/reusable-publish-snapshot.yml`             |
| Publish Release                | Publish official releases to Maven Central           | `.github/workflows/reusable-publish-release.yml`              |

---

## 🔧 Custom Composite Actions

These live under `actions/`.

| Name             | Description                      | Path                                  | Status        |
|------------------|----------------------------------|---------------------------------------|---------------|
| doxygen          | Run Doxygen to generate API docs | `actions/doxygen/action.yml`          | **Active**    |

---

## 📘 Usage Examples

### 1. Calling a reusable workflow

```yaml
name: Publish Snapshot

on:
  push:
    branches: [ main ]

jobs:
  publish:
    uses: eclipse-keypop/keypop-actions/.github/workflows/reusable-publish-snapshot.yml@publish-snapshot-v1
    with:
      artifact: build/libs/mylib.jar
````

### 2. Using a composite action

```yaml
- name: Generate Doxygen Documentation
  uses: eclipse-keypop/keypop-actions/actions/doxygen@doxygen-v1
```

### 3. (Deprecated) Old Doxygen action

> ⚠️ **Deprecated** — will be removed in a future release

```yaml
- name: Generate Doxygen Documentation
  uses: eclipse-keypop/keypop-actions/doxygen@v2
```

## 📖 Versioning & Tags

This repository contains multiple components. To manage them independently, all release tags follow this naming convention:

**`<component-name>-<version>`**

* **Full Version Tags** (e.g., `publish-release-v1.2.3`, `publish-snapshot-v1.0.0`, ...):
  These represent a specific, immutable release of a component.

* **Major Version Tags** (e.g., `publish-release-v1`, `publish-snapshot-v2`, ...):
  These are floating tags that point to the latest non-breaking release within their major series. They are updated with each new compatible minor or patch release.

* **Branches** (e.g., `main`):
  Branch names are not considered stable versions. They represent ongoing development and their state can change at any time.

## 🚀 Migrating from the old layout

Replace `uses: eclipse-keypop/keypop-actions/doxygen@v2` by `uses: eclipse-keypop/keypop-actions/actions/doxygen@doxygen-v1`

---

## 🤝 Contributing

Please read our [contribution guidelines](https://keypop.org/community/contributing/) before submitting any changes.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.