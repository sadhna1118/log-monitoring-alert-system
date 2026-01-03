# Contributing to Log Monitoring & Alert System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/log-monitoring-system.git
   cd log-monitoring-system
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python setup.py
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Code Formatting

```bash
# Format code with black
black src/

# Check with flake8
flake8 src/

# Type checking
mypy src/
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new threat detection pattern`
- `fix: Correct SQL injection regex pattern`
- `docs: Update setup instructions`
- `test: Add tests for log parser`

## Types of Contributions

### 🐛 Bug Reports
- Use the issue tracker
- Describe the bug clearly
- Include steps to reproduce
- Provide error messages/logs

### 💡 Feature Requests
- Describe the feature and its benefits
- Explain the use case
- Discuss implementation approach

### 📝 Documentation
- Fix typos or unclear instructions
- Add examples and tutorials
- Improve API documentation

### 🔧 Code Contributions

#### Adding New Threat Patterns

Add patterns to `src/patterns.py`:

```python
# In SecurityPatterns class
NEW_THREAT_PATTERNS = [
    r'your-regex-pattern-here',
    r'another-pattern',
]
```

Update detection in `src/log_parser.py`:

```python
def analyze_log_entry(self, entry: LogEntry) -> LogEntry:
    # Add your new threat detection
    if self.patterns.detect_new_threat(entry.message):
        entry.add_threat("New Threat Type", "pattern")
    return entry
```

#### Adding New Integrations

1. Create new module in `src/`
2. Follow existing patterns (see `webhook_notifier.py`)
3. Update documentation
4. Add tests

#### Improving ML Models

Contributions to ML accuracy are welcome:
- Better feature extraction
- Alternative algorithms
- Hyperparameter tuning
- Training data improvements

## Pull Request Process

1. **Update documentation** for any new features
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Submit PR** with clear description

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commits are meaningful
- [ ] No merge conflicts
- [ ] CHANGELOG.md updated

## Code Review

- Be respectful and constructive
- Address review comments
- Update PR based on feedback

## Areas for Contribution

### High Priority
- [ ] Add more threat detection patterns
- [ ] Improve ML model accuracy
- [ ] Add more integration options (PagerDuty, Datadog, etc.)
- [ ] Performance optimizations
- [ ] Better error handling

### Medium Priority
- [ ] Add more visualizations to dashboard
- [ ] Implement user authentication
- [ ] Add API rate limiting
- [ ] Support for more log formats
- [ ] Mobile-responsive dashboard

### Nice to Have
- [ ] Kubernetes deployment templates
- [ ] Grafana dashboards
- [ ] Advanced ML models (LSTM, Transformers)
- [ ] Real-time streaming with Kafka
- [ ] Multi-language support

## Questions?

Feel free to:
- Open an issue for questions
- Reach out to maintainers
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉