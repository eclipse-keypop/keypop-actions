# Eclipse Keypop GitHub Actions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Collection of GitHub Actions for automating various tasks in Eclipse Keypop libraries and projects.

## Available Actions

### Doxygen Documentation
Action for generating and publishing C++ API reference documentation. [See detailed documentation](docs/doxygen-action.md)

## Using Actions

Actions in this repository can be referenced using Git tags. When referencing an action, you must specify a tag to ensure workflow stability and reproducibility.

```yaml
# Reference format:
- uses: eclipse-keypop/actions/{action-name}@{tag}

# Example with specific version:
- uses: eclipse-keypop/actions/doxygen@v1.0.0

# Example with major version only (automatically uses latest minor/patch):
- uses: eclipse-keypop/actions/doxygen@v1
```

We follow semantic versioning for our actions:
- Major version tags (e.g., `v1`): Point to the latest stable release within that major version
- Specific version tags (e.g., `v1.0.0`): Point to exact versions
- Using specific versions is recommended for production workflows
- Using major version tags is acceptable for development workflows

**Note**: Avoid using `@main` or branch references as they may contain breaking changes.

## Contributing

Please read our [contribution guidelines](https://keypop.org/community/contributing/) before submitting any changes.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.