dry-run:
	@echo "This is a dry run. Tests will run after this"
	python cli.py -t bash -dr
	@echo "Running tests now..."
	pytest tests/ -v
	@echo "Dry run completed."

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=html

clean:
	rm -rf outputs/cheatsheets/*
	rm -rf outputs/transcripts/*
	rm -rf outputs/transcript-audio/*
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete

help:
	@echo "Available targets:"
	@echo "  dry-run    - Run CLI with bash topic in dry-run mode"
	@echo "  test       - Run all tests"
	@echo "  test-cov   - Run tests with coverage report"
	@echo "  clean      - Clean output directories and cache files"
	@echo "  help       - Show this help message"