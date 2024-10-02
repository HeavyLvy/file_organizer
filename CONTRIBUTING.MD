# How to contribute

## Creating new code

### Branching
- Feature Branches:
    - Create a new branch for each feature you're working  on.
    - Use descriptive names that clearly convey the feature's purpose. For example:
        - `feature/add-improved-config`
        - `feature/improve-cli-functionality`
- Hotfix Branches
    - Use hotfix branches for urgent bug/security fixes
    - Name them descriptively to indicate the issue being addressed. For Example:
        - `hotfix/config-randomly-deletes`
        - `hotfix/critical-config-leak`

### Pull Requests
- Once your feature or fix is implemented on a separate branch, create a pull request to propose these changes to the main  codebase.

## Code Styling
- 1. Use [pyright](https://pypi.org/project/pyright/) for type checking
- 2. Use [ruff](https://github.com/astral-sh/ruff) or [black](https://github.com/psf/black) for code formatting
- 3. Document your functions/classes using [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)

### Suppress Linting Errors

**How to format the suppressed error**
```python
code # suppress method # | reason (in lower case) | message (any case) - from (in lower case)
```
**examples**
```python
bad code # noqa # | false positive | "exceptions" is not a known attribute of module "jsonschema" - python
bad code # type: ignore # | false positive | "int" is not compatible with "str" - pyright
```
**Git commit**
Preferably commit only the single suppressed error.
The commit message should be the same as the comment:
```bash
git add .
git commit -m 'type: ignore # | false positive | "int" is not compatible with "str" - pyright'
```
