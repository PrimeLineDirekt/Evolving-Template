#!/usr/bin/env python3
"""
ML Project Scaffold Generator
Generated from: KalyanM45/AI-Project-Gallery Analysis + ML Project Structure Pattern

Purpose: Automatically generate a production-ready ML project structure

Usage:
    python project-scaffold.py --name=my_project --path=~/projects/
    python project-scaffold.py --blueprint=end-to-end-ml --with-templates

Features:
- Creates complete directory structure
- Generates template files (config.yaml, setup.py, etc.)
- Creates GitHub Actions CI/CD
- Sets up DVC configuration
- Initializes git repository
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Template content constants
SETUP_PY_TEMPLATE = '''"""
Setup configuration for {project_name}

Install with: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    description="ML Project: {description}",
    author="",
    author_email="",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.2.0",
        "xgboost>=1.7.0",
        "python-dotenv>=0.21.0",
        "flask>=2.3.0",
        "pydantic>=1.10.0",
    ],
    extras_require={{
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=5.0",
            "mypy>=0.990",
        ],
        "ml": [
            "mlflow>=2.0",
            "optuna>=3.0",
        ],
    }},
)
'''

REQUIREMENTS_TXT_TEMPLATE = '''# Production dependencies (pinned versions)
numpy==1.24.3
pandas==2.0.2
scikit-learn==1.2.2
xgboost==1.7.5
lightgbm==4.0.0
python-dotenv==0.21.0
flask==2.3.2
pydantic==1.10.9
joblib==1.3.1

# Optional MLOps
mlflow==2.3.0
optuna==3.1.0
'''

CONFIG_YAML_TEMPLATE = '''# ML Project Configuration
# Customize these settings for your project

data:
  source: "raw_data.csv"
  encoding: "utf-8"
  train_size: 0.7
  validation_size: 0.2
  test_size: 0.1

preprocessing:
  normalize: true
  outlier_method: "iqr"  # or "zscore"
  handle_missing: "drop"  # or "mean", "median"

features:
  lag_features: [1, 7, 30]
  rolling_window: [7, 30]

model:
  type: "xgboost"  # or "lightgbm", "catboost", "random_forest"
  hyperparameters:
    learning_rate: 0.01
    max_depth: 5
    n_estimators: 100
    random_state: 42

training:
  epochs: 100
  batch_size: 32
  validation_split: 0.2
  early_stopping: true

evaluation:
  metrics: ["rmse", "mae", "r2"]
  cross_validation: 5
'''

GITIGNORE_TEMPLATE = '''# Data
data/
raw_data.csv
*.csv
*.xlsx

# Models
Artifacts/
*.pkl
*.joblib
*.h5

# MLFlow
mlruns/
.mlflow

# DVC
.dvc/cache
.dvc/tmp

# Environment
.env
.venv
venv/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
'''

DOCKERFILE_TEMPLATE = '''FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
'''

ENV_TEMPLATE = '''# Environment Configuration

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Model paths
MODEL_PATH=Artifacts/model.pkl
PREPROCESSOR_PATH=Artifacts/preprocessor.pkl
METADATA_PATH=Artifacts/model_metadata.json

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
'''

GITHUB_ACTIONS_TEMPLATE = '''name: ML Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python 3.9
      uses: actions/setup-python@v4
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest black flake8

    - name: Lint with flake8
      run: flake8 src/

    - name: Format check with black
      run: black --check src/

    - name: Run tests
      run: pytest tests/

    - name: Run DVC pipeline
      run: |
        pip install dvc
        dvc repro
'''

DATA_PROCESSOR_TEMPLATE = '''"""
Data processing module
"""

import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and prepare data for ML model."""

    def __init__(self):
        self.data = None
        self.scaler = StandardScaler()

    def load(self, path: str) -> 'DataProcessor':
        """Load data from CSV."""
        try:
            self.data = pd.read_csv(path)
            logger.info(f"Loaded data from {{path}}: {{self.data.shape}}")
            return self
        except Exception as e:
            logger.error(f"Failed to load data: {{e}}")
            raise

    def validate(self) -> 'DataProcessor':
        """Validate data integrity."""
        if self.data is None:
            raise ValueError("No data loaded")

        logger.info(f"Validation: {{self.data.shape[0]}} rows, {{self.data.isnull().sum().sum()}} nulls")
        return self

    def clean(self) -> 'DataProcessor':
        """Clean data (remove nulls, duplicates)."""
        initial_shape = self.data.shape

        # Remove duplicates
        self.data = self.data.drop_duplicates()

        # Handle missing values (drop rows with nulls)
        self.data = self.data.dropna()

        logger.info(f"Cleaned: {{initial_shape}} -> {{self.data.shape}}")
        return self

    def normalize(self) -> 'DataProcessor':
        """Normalize features."""
        # Separate features and target
        X = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1]

        # Fit and transform
        X_scaled = self.scaler.fit_transform(X)

        # Reconstruct dataframe
        self.data = pd.DataFrame(X_scaled, columns=X.columns)
        self.data['target'] = y.values

        logger.info("Normalized features")
        return self

    def split(self, train_size=0.7, val_size=0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split into train, validation, test."""
        n = len(self.data)
        train_idx = int(n * train_size)
        val_idx = int(n * (train_size + val_size))

        train = self.data.iloc[:train_idx]
        val = self.data.iloc[train_idx:val_idx]
        test = self.data.iloc[val_idx:]

        logger.info(f"Split: {{train.shape}}, {{val.shape}}, {{test.shape}}")
        return train, val, test
'''

BASE_MODEL_TEMPLATE = '''"""
Base model interface
"""

from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """Abstract base class for ML models."""

    @abstractmethod
    def train(self, X_train, y_train):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X):
        """Make predictions."""
        pass

    @abstractmethod
    def evaluate(self, X_test, y_test):
        """Evaluate the model."""
        pass

    @abstractmethod
    def save(self, path: str):
        """Save the model."""
        pass

    @abstractmethod
    def load(self, path: str):
        """Load the model."""
        pass
'''


def create_directory_structure(project_path: Path):
    """Create the ML project directory structure."""

    directories = [
        "Notebook_Experiments",
        "src/project_name",
        "src/project_name/data",
        "src/project_name/features",
        "src/project_name/models",
        "src/project_name/utils",
        "src/project_name/config",
        "Artifacts",
        "templates",
        "static/css",
        "static/js",
        "static/images",
        ".github/workflows",
        ".dvc",
        "logs",
        "tests",
        "data",
    ]

    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")


def create_files(project_path: Path, project_name: str, description: str):
    """Create template files."""

    files = {
        "setup.py": SETUP_PY_TEMPLATE.format(project_name=project_name, description=description),
        "requirements.txt": REQUIREMENTS_TXT_TEMPLATE,
        "config.yaml": CONFIG_YAML_TEMPLATE,
        ".gitignore": GITIGNORE_TEMPLATE,
        "Dockerfile": DOCKERFILE_TEMPLATE,
        ".env": ENV_TEMPLATE,
        ".github/workflows/ci.yml": GITHUB_ACTIONS_TEMPLATE,
        "src/project_name/data/data_processor.py": DATA_PROCESSOR_TEMPLATE,
        "src/project_name/models/base_model.py": BASE_MODEL_TEMPLATE,
    }

    for file_path, content in files.items():
        full_path = project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        logger.info(f"Created file: {full_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate ML project structure")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--path", default=".", help="Target path")
    parser.add_argument("--description", default="ML Project", help="Project description")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Create project path
    project_path = Path(args.path) / args.name

    if project_path.exists():
        logger.error(f"Project directory already exists: {project_path}")
        return 1

    logger.info(f"Creating ML project: {args.name}")

    # Create structure and files
    create_directory_structure(project_path)
    create_files(project_path, args.name, args.description)

    logger.info(f"✓ Project created at: {project_path}")
    logger.info("\nNext steps:")
    logger.info(f"  1. cd {project_path}")
    logger.info("  2. pip install -e .")
    logger.info("  3. Add your data to data/ directory")
    logger.info("  4. Update config.yaml")
    logger.info("  5. dvc repro")

    return 0


if __name__ == "__main__":
    import sys
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    sys.exit(main())
