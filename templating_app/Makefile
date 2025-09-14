.PHONY: preview
content:
	uv run main.py single content/preview

music:
	uv run main.py single content/theorycardtest

.PHONY: debug
debug:
	pandoc temp_validation.md -o debug.tex --template=templates/styles/custom.latex --standalone
	# @echo -e 'written the latex content generated from runtime to debug.tex'