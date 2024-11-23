# Parameters
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
ACTIVATE = . $(VENV_DIR)/bin/activate

# Create virtual environment and install dependencies
install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Remove virtual environment
clean:
	rm -rf $(VENV_DIR)

# Run tests
test:
	$(ACTIVATE) && pytest

# Run app
run:
	$(ACTIVATE) && $(PYTHON) main.py
