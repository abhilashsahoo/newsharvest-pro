# Contributing to NewsHarvest Pro 🤝

Thank you for your interest in contributing to NewsHarvest Pro! We welcome contributions from the community and are excited to collaborate with you.

## 🎯 How to Contribute

### Types of Contributions

- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new functionality
- 🔧 **Code Contributions**: Submit bug fixes and improvements
- 📚 **Documentation**: Improve guides, examples, and explanations
- 🧪 **Testing**: Add test cases and improve test coverage
- 🌐 **Website Support**: Add support for new news websites
- 🎨 **UI/UX**: Improve the web interface design

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/newsharvest-pro.git
cd newsharvest-pro

# Add the upstream repository
git remote add upstream https://github.com/abhilashsahoo/newsharvest-pro.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 pre-commit
```

### 3. Create a Branch

```bash
# Create a new branch for your contribution
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

## 📋 Development Guidelines

### Code Style

We follow Python best practices and PEP 8:

```bash
# Format code with Black
black .

# Check code style with flake8
flake8 .

# Sort imports
isort .
```

### Commit Messages

Use clear, descriptive commit messages:

```
✅ Good:
feat: add support for Reuters news extraction
fix: resolve encoding issues in article titles
docs: update installation instructions

❌ Avoid:
update code
fix bug
misc changes
```

### Code Quality

- **Follow PEP 8**: Use consistent formatting and naming
- **Add docstrings**: Document functions and classes
- **Include type hints**: Use Python type annotations where helpful
- **Handle errors gracefully**: Add appropriate exception handling
- **Write tests**: Include test cases for new functionality

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=newsharvest_pro

# Run specific test file
pytest tests/test_harvester.py
```

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_new_feature.py
import pytest
from newsharvest_simple import SimpleNewsHarvester

def test_new_feature():
    harvester = SimpleNewsHarvester()
    result = harvester.new_feature()
    assert result is not None
    assert len(result) > 0
```

## 🌐 Adding Website Support

### Website Compatibility Checklist

When adding support for a new website:

- [ ] **Test URL patterns**: Ensure article discovery works
- [ ] **Test content extraction**: Verify title, content, author extraction
- [ ] **Handle edge cases**: Test with different article formats
- [ ] **Document selectors**: Add CSS selectors to extraction logic
- [ ] **Update README**: Add website to compatibility list
- [ ] **Add example URL**: Include test URL in documentation

### Website Support Template

```python
def extract_from_new_site(self, soup, url):
    """Extract content from NewSite articles"""
    
    # Title extraction
    title_selectors = [
        'h1.article-headline',      # Primary selector
        '.entry-title',             # Fallback
        'h1'                        # Generic fallback
    ]
    
    # Content extraction
    content_selectors = [
        '.article-body p',          # Primary selector
        '.entry-content p',         # Fallback
        'article p'                 # Generic fallback
    ]
    
    # Author extraction
    author_selectors = [
        '.author-name',             # Primary selector
        '.byline',                  # Fallback
        '[rel="author"]'            # Generic fallback
    ]
    
    # Add extraction logic here
    return {
        'title': extracted_title,
        'content': extracted_content,
        'author': extracted_author
    }
```

## 🐛 Bug Reports

### Before Submitting a Bug Report

1. **Check existing issues**: Search for similar problems
2. **Test with latest version**: Ensure you're using the current release
3. **Test with multiple sites**: Verify if issue is site-specific
4. **Gather information**: Collect relevant details

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. Use URL '...'
3. Set parameters '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- NewsHarvest Pro version: [e.g., 1.0.0]
- Website URL: [e.g., https://example.com]

**Error Messages**
```
Paste any error messages here
```

**Additional Context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Describe the problem this feature would solve or the workflow it would improve.

**Proposed Solution**
Describe how you envision this feature working.

**Alternatives Considered**
Any alternative solutions or workarounds you've considered.

**Additional Context**
Any other context, mockups, or examples.
```

## 📚 Documentation Contributions

### Documentation Guidelines

- **Be clear and concise**: Use simple, direct language
- **Include examples**: Show practical usage
- **Update related files**: Keep all documentation consistent
- **Test instructions**: Verify that examples work
- **Consider all users**: Write for beginners and experts

### Documentation Structure

```
docs/
├── installation.md     # Installation instructions
├── quickstart.md      # Getting started guide
├── api-reference.md   # API documentation
├── examples/          # Usage examples
├── troubleshooting.md # Common issues and solutions
└── contributing.md    # This file
```

## 🔍 Code Review Process

### Submitting Pull Requests

1. **Ensure tests pass**: Run full test suite
2. **Update documentation**: Include relevant docs updates
3. **Add changelog entry**: Document your changes
4. **Request review**: Assign reviewers when ready

### Pull Request Template

```markdown
**Description**
Brief description of changes made.

**Type of Change**
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

**Testing**
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

**Checklist**
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changelog updated
```

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag release

## 🤔 Questions and Support

### Getting Help

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Create a GitHub Issue
- **Feature requests**: Create a GitHub Issue with feature label
- **Security issues**: Email abhilashsahoo@gmail.com

### Community Guidelines

- **Be respectful**: Treat all contributors with respect
- **Be constructive**: Provide helpful feedback
- **Be patient**: Maintainers are volunteers
- **Be collaborative**: Work together toward common goals

## 🎉 Recognition

### Contributors

All contributors will be:
- Added to the CONTRIBUTORS.md file
- Mentioned in release notes for significant contributions
- Credited in documentation they help improve

### Types of Recognition

- **Code Contributors**: Listed in main contributors section
- **Documentation Contributors**: Listed in documentation section
- **Bug Reporters**: Credited in issue resolution
- **Feature Requesters**: Credited in feature implementation

## 📈 Contribution Ideas

### Easy First Contributions

- **Documentation improvements**: Fix typos, clarify instructions
- **Website testing**: Test with new news websites
- **Bug reports**: Report issues you encounter
- **Example improvements**: Enhance usage examples

### Medium Difficulty

- **New website support**: Add extraction logic for new sites
- **UI improvements**: Enhance web interface
- **Performance optimization**: Improve collection speed
- **Error handling**: Add better error messages

### Advanced Contributions

- **New features**: Implement major new functionality
- **Architecture improvements**: Enhance system design
- **Machine learning integration**: Add ML-based quality scoring
- **API development**: Create REST API endpoints

## 🔧 Development Setup Details

### Project Structure

```
newsharvest-pro/
├── app.py                    # Flask web application
├── newsharvest_simple.py     # Command-line interface
├── requirements.txt          # Python dependencies
├── README.md                # Main documentation
├── CONTRIBUTING.md          # This file
├── LICENSE                  # MIT License
├── tests/                   # Test files
│   ├── test_harvester.py
│   ├── test_bias_analysis.py
│   └── test_quality_scoring.py
├── docs/                    # Documentation
│   ├── examples/
│   └── guides/
└── examples/                # Usage examples
    ├── basic_usage.py
    ├── advanced_analysis.py
    └── custom_extraction.py
```

### Environment Variables

```bash
# Optional configuration
export NEWSHARVEST_DEBUG=true           # Enable debug mode
export NEWSHARVEST_DELAY=2              # Custom delay between requests
export NEWSHARVEST_TIMEOUT=15           # Request timeout
export NEWSHARVEST_USER_AGENT="Custom"  # Custom user agent
```

### Development Commands

```bash
# Run development server
python app.py

# Run tests with verbose output
pytest -v

# Generate test coverage report
pytest --cov=. --cov-report=html

# Check code quality
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Format code
black . --line-length=88

# Sort imports
isort . --profile=black
```

## 📝 Changelog Guidelines

### Changelog Format

```markdown
## [1.2.0] - 2025-07-15

### Added
- Support for Reuters news extraction
- Advanced bias detection for economic terminology
- Export to XML format

### Changed
- Improved quality scoring algorithm
- Updated web interface design
- Enhanced error messages

### Fixed
- Character encoding issues with special characters
- Duplicate detection false positives
- Memory usage optimization

### Deprecated
- Legacy bias analysis methods (will be removed in 2.0.0)

### Removed
- Support for Python 3.7 (now requires 3.8+)

### Security
- Updated dependencies to address security vulnerabilities
```

## 🚀 Thank You!

Your contributions make NewsHarvest Pro better for everyone. Whether you're fixing a typo, adding a feature, or helping other users, every contribution is valuable and appreciated.

**Happy contributing!** 🎉

---

*For questions about contributing, please open a GitHub Discussion or reach out to the maintainers.*