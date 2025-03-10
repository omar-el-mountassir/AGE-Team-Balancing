# Contributing to Age of Empires 2 Team Balancing Bot

Thank you for your interest in contributing to the Age of Empires 2 Team Balancing Bot! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Contributing to Age of Empires 2 Team Balancing Bot](#contributing-to-age-of-empires-2-team-balancing-bot)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Environment](#development-environment)
    - [1. Set up a Python virtual environment](#1-set-up-a-python-virtual-environment)
    - [2. Install development dependencies](#2-install-development-dependencies)
    - [3. Set up pre-commit hooks (if available)](#3-set-up-pre-commit-hooks-if-available)
    - [4. Create a `.env` file for local development](#4-create-a-env-file-for-local-development)
  - [Development Workflow](#development-workflow)
    - [1. Pull the latest changes](#1-pull-the-latest-changes)
    - [2. Create a new branch for your work](#2-create-a-new-branch-for-your-work)
    - [3. Make your changes and commit them with clear, descriptive messages](#3-make-your-changes-and-commit-them-with-clear-descriptive-messages)
    - [4. Push your branch to your fork](#4-push-your-branch-to-your-fork)
    - [5. Submit a pull request through GitHub](#5-submit-a-pull-request-through-github)
  - [Pull Request Process](#pull-request-process)
  - [Coding Standards](#coding-standards)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Issue Reporting](#issue-reporting)
  - [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please be kind and considerate to other contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Set up the development environment** as described below
4. **Create a new branch** for your feature or bugfix
5. **Make your changes** and commit them
6. **Push your branch** to your fork
7. **Submit a pull request** to the main repository

## Development Environment

### 1. Set up a Python virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install development dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

### 3. Set up pre-commit hooks (if available)

```bash
pre-commit install
```

### 4. Create a `.env` file for local development

```bash
cp .env.example .env
```

Edit the `.env` file with your development settings.

## Development Workflow

### 1. Pull the latest changes

Before starting work, make sure you have the latest changes:

```bash
git checkout main
git pull upstream main  # If you've set up an upstream remote
```

### 2. Create a new branch for your work

```bash
git checkout -b feature/your-feature-name
```

### 3. Make your changes and commit them with clear, descriptive messages

```bash
git add .
git commit -m "Add feature X" -m "Detailed description of the changes"
```

### 4. Push your branch to your fork

```bash
git push origin feature/your-feature-name
```

### 5. Submit a pull request through GitHub

## Pull Request Process

1. Ensure your code follows the project's coding standards
2. Update the documentation to reflect any changes
3. Add tests for new functionality
4. Make sure all tests pass before submitting
5. Fill out the pull request template with all required information
6. Respond to any feedback on your pull request

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for function arguments and return values
- Use descriptive variable names and include docstrings
- Keep functions focused on a single responsibility
- Add comments for complex logic

We use `flake8` for linting and `black` for formatting:

```bash
# Check code style
flake8 .

# Format code
black .
```

## Testing

- Write unit tests for all new functionality
- Ensure existing tests continue to pass
- Tests should be placed in the `tests/` directory, following the same structure as the source code

To run tests:

```bash
pytest
```

## Documentation

- Update the README.md if you're changing user-facing features
- Add docstrings to all functions and classes
- Use descriptive commit messages

## Issue Reporting

When reporting issues, please include:

- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots or error logs if applicable
- Information about your environment (OS, Python version, etc.)

## Feature Requests

Feature requests are welcome! Please provide:

- A clear, descriptive title
- A detailed description of the proposed feature
- Any relevant examples or mockups
- An explanation of why the feature would be useful to most users

Thank you for contributing to Age of Empires 2 Team Balancing Bot!
