dry-run:
	@echo "This is a dry run. Tests will run after this"
	python cli.py -t bash -dr
	@echo "Running tests now..."
	pytest tests/ -v
	@echo "Dry run completed."

voiceover-dry-run:
	@echo "This is a dry run with voiceover recording..."
	python cli.py -t bash -dr --voiceover
	@echo "Voiceover dry run completed."

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=html
	open htmlcov/index.html

clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete

help:
	@echo "Available targets:"
	@echo "  dry-run           - Run CLI with bash topic in dry-run mode"
	@echo "  voiceover-dry-run - Run CLI with bash topic in dry-run mode + voiceover recording"
	@echo "  test              - Run all tests"
	@echo "  test-cov          - Run tests with coverage report"
	@echo "  clean             - Clean output directories and cache files"
	@echo "  help              - Show this help message"

