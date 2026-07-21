activate:
	source .venv/bin/activate

run:
	uv run main.py

run-calc-test:
	uv run calculator/tests.py