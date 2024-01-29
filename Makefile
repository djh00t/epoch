PROJECT_NAME=epoch

# Define commands
PYTHON=python3
PIP=pip
FLASK=flask

# Define paths
VENV_PATH=./venv

# Default target
all: install

# Install dependencies and setup the project
install:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_PATH)
	@echo "Activating virtual environment..."
	. $(VENV_PATH)/bin/activate
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# Run the Flask application
run:
	@echo "Starting the Flask server..."
	$(FLASK) run

# Clean the project directory
clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf $(VENV_PATH)

# Reset the project to initial state
reset: clean
	@echo "Resetting the project..."
	rm -rf instance/
	rm -rf $(PROJECT_NAME).egg-info

# Help target to display available commands
help:
	@echo "Available commands:"
	@echo "  make install - Install dependencies and setup the project"
	@echo "  make run     - Run the Flask application"
	@echo "  make clean   - Clean the project directory"
	@echo "  make reset   - Reset the project to initial state"
	@echo "  make help    - Display this help message"
