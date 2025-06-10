# Documentation

This directory contains project documentation and our engineering handbook.

## Engineering Handbook

The [engineering handbook](./engineering-handbook/) contains our team's engineering practices, coding standards, workflows, and best practices. It serves as the single source of truth for how we build software.

The handbook is maintained as a separate repository and included here as a git submodule. This allows it to be:
- Updated independently from the project
- Shared across multiple projects
- Version controlled separately

### Updating the Handbook

To get the latest version of the engineering handbook:

```bash
# Pull the latest changes
git submodule update --remote docs/engineering-handbook

# Or if cloning a fresh copy of this repo
git clone --recursive <repository-url>
```

For more details, see the [Engineering Handbook README](./engineering-handbook/README.md).
