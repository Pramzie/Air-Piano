# Installation Guide

This guide will help you set up and run this Python-based program.

## Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

## Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Program

1. **Activate the Virtual Environment** (if not already activated)
   ```bash
   # Windows
   .\venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the Program**
   ```bash
   python main.py
   ```

## Troubleshooting

If you encounter any issues:

1. Ensure Python is correctly installed and in your PATH
   ```bash
   python --version
   ```

2. Verify pip is installed
   ```bash
   pip --version
   ```

3. Make sure all dependencies are installed
   ```bash
   pip list
   ```

## Additional Notes

- To deactivate the virtual environment when you're done:
  ```bash
  deactivate
  ```
- Keep your dependencies up to date:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

## Support

If you encounter any issues, please:
1. Check the existing issues in the repository
2. Create a new issue with details about your problem
3. Include your OS version and Python version in any bug reports
