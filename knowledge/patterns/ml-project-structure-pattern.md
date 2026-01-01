---
title: "ML Project Structure Pattern"
type: "architecture"
category: "ml-projects"
tags: [ml, project-structure, modularity, production, dvc, mlflow, docker]
confidence: 95
source: "KalyanM45/AI-Project-Gallery Analysis (5 projects)"
created: 2025-12-23
---

# ML Project Structure Pattern

**Source**: Analysis of KalyanM45 portfolio (Airbnb Price, Flight Fare, Gold Price, E-Commerce, Article Scraper)
**Confidence**: 95% (Production-proven across 5 projects)
**Best For**: Regression, Classification, Time Series, Web Scraping, BI Projects

---

## Core Principle

**Separation of Concerns:**
- **Notebooks**: Exploration & Experimentation (rapid iteration)
- **src/**: Production code (modular, testable, reusable)
- **Artifacts/**: Trained models & preprocessors (versioned)
- **Web Interface**: Flask/FastAPI for predictions (deployment)
- **Infrastructure**: Docker & DVC (reproducibility)

---

## Directory Structure

```
project/
├── Notebook_Experiments/        # Jupyter exploration
│   ├── 01_EDA.ipynb            # Data exploration
│   ├── 02_Feature_Engineering.ipynb
│   ├── 03_Model_Training.ipynb
│   ├── 04_Model_Evaluation.ipynb
│   ├── 05_Hyperparameter_Tuning.ipynb
│   └── ...
│
├── src/project_name/            # Production code
│   ├── __init__.py
│   ├── config/
│   │   └── config.yaml          # Hyperparameters, settings
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_loader.py       # Load from CSV/SQL/API
│   │   └── data_processor.py    # Cleaning, validation, normalization
│   ├── features/
│   │   ├── __init__.py
│   │   ├── feature_engineering.py
│   │   └── feature_scaler.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluator.py
│   │   └── forecast_generator.py (time series)
│   └── utils/
│       ├── __init__.py
│       ├── logging_utils.py
│       └── data_utils.py
│
├── Artifacts/                   # Trained models
│   ├── model.pkl
│   ├── preprocessor.pkl
│   ├── scaler.pkl
│   └── model_metadata.json
│
├── templates/                   # Flask HTML
│   ├── index.html
│   ├── prediction.html
│   └── results.html
│
├── static/                      # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── .github/workflows/           # CI/CD
│   ├── tests.yml
│   └── deployment.yml
│
├── .dvc/                        # Data Version Control
├── dvc.yaml                     # Pipeline definition
├── dvc.lock                     # Reproducibility lock file
├── mlruns/                      # MLFlow experiments (optional)
├── logs/                        # Application logs
│
├── app.py                       # Flask/FastAPI entry point
├── setup.py                     # Package configuration
├── template.py                  # Project scaffolding generator
├── requirements.txt             # Python dependencies (pinned!)
├── Dockerfile                   # Containerization
├── .gitignore
├── README.md
└── LICENSE
```

---

## Key Files & Patterns

### 1. **Notebooks → Production Conversion**

| Stage | Location | Purpose |
|-------|----------|---------|
| Exploration | `Notebook_Experiments/` | Rapid iteration, visualization, analysis |
| Development | Extract → `src/` modules | Modular, testable code |
| Production | `app.py` loads from `src/` | API endpoints, web interface |

**Pattern**: Notebooks are TEMPORARY, src/ is PERMANENT

### 2. **Configuration Management**

**File**: `src/project_name/config/config.yaml`

```yaml
model:
  type: "xgboost"
  hyperparameters:
    learning_rate: 0.01
    max_depth: 5
    n_estimators: 100

data:
  train_size: 0.7
  validation_size: 0.2
  test_size: 0.1

preprocessing:
  normalize: true
  outlier_method: "iqr"
```

**Why?**: Never hardcode hyperparameters. Enable quick experimentation without code changes.

### 3. **Data Processing Pipeline**

**File**: `src/project_name/data/data_processor.py`

```python
class DataProcessor:
    def load(self, path): ...
    def validate(self): ...
    def clean(self): ...
    def normalize(self): ...
    def split(self, train/val/test): ...
```

**Pattern**: Method chaining for composability
```python
processor = DataProcessor()
train, val, test = processor.load(path).validate().clean().normalize().split()
```

### 4. **Model Interface Standardization**

**All Models Implement**:
```python
class BaseModel:
    def train(self, X_train, y_train): ...
    def predict(self, X): ...
    def evaluate(self, X_test, y_test): ...
    def save(self, path): ...
    def load(self, path): ...
```

**Why?**: Interchangeable model implementations (XGBoost → CatBoost swap easily)

### 5. **Web Interface Pattern**

**File**: `app.py`

```python
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    preprocessed = preprocessor.transform(data)
    prediction = model.predict(preprocessed)
    return {
        'prediction': prediction,
        'confidence': confidence_score
    }

@app.route('/model-info')
def model_info():
    return {
        'model_type': 'XGBoost Regression',
        'accuracy': 0.92,
        'features': feature_names
    }
```

---

## MLOps Stack Integration

### DVC (Data Version Control)

**File**: `dvc.yaml`

```yaml
stages:
  data_load:
    cmd: python -m src.data.data_loader
    deps:
      - raw_data.csv
    outs:
      - data/loaded_data.pkl

  preprocess:
    cmd: python -m src.data.data_processor
    deps:
      - data/loaded_data.pkl
    outs:
      - data/processed_data.pkl

  train:
    cmd: python -m src.models.model_trainer
    deps:
      - data/processed_data.pkl
    outs:
      - Artifacts/model.pkl
    metrics:
      - metrics.json
```

**Benefits**:
- `dvc repro` = automated full pipeline
- `dvc.lock` = reproducible experiments
- Tracked data versions (not in Git)

### MLFlow (Experiment Tracking)

```python
import mlflow

mlflow.start_run()
mlflow.log_param('learning_rate', 0.01)
mlflow.log_metric('rmse', 0.45)
mlflow.log_artifact('model.pkl')
mlflow.end_run()
```

**View Results**: `mlflow ui`

### Docker (Containerization)

**File**: `Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t project:latest .
docker run -p 5000:5000 project:latest
```

---

## Development Workflow

### Phase 1: Exploration (Notebooks)
1. Load data → visualize distributions
2. Feature engineering experiments
3. Model training & evaluation (multiple attempts)
4. Document learnings

### Phase 2: Modularization (src/)
1. Extract `DataProcessor` from notebooks
2. Extract feature engineering functions
3. Create `ModelTrainer` class
4. Create `ModelEvaluator` class

### Phase 3: Pipeline (DVC)
1. Define `dvc.yaml` stages
2. Track Artifacts/ with DVC
3. Run `dvc repro` for reproducibility
4. Commit `dvc.lock` to git

### Phase 4: Web Interface (Flask)
1. Load model from Artifacts/
2. Create prediction endpoint
3. Add model info endpoint
4. Test with postman/curl

### Phase 5: Deployment (Docker)
1. Create Dockerfile
2. Build & test locally
3. Push to registry (optional)
4. Deploy to production

---

## Best Practices

1. **Notebooks are Exploration, Not Production**
   - Notebooks for "why & how"
   - src/ modules for "what & where"
   - Never import from notebooks in production code

2. **Pin Everything**
   - `requirements.txt`: exact versions
   - `dvc.lock`: exact data/model versions
   - `setup.py`: exact package dependencies

3. **Separate Data, Code, Models**
   - Data: `data/` (tracked with DVC)
   - Code: `src/` (tracked with Git)
   - Models: `Artifacts/` (tracked with DVC)
   - This prevents Git bloat

4. **Configuration Over Hardcoding**
   - All hyperparameters in `config.yaml`
   - All paths in `config.yaml`
   - Change behavior without code modifications

5. **Temporal Data Handling (Time Series)**
   - NEVER shuffle time series data
   - Use temporal train/test split (70/20/10 by date)
   - Test on different time periods for robustness

6. **Standardize Model Interfaces**
   - All models have same methods: `train()`, `predict()`, `evaluate()`
   - Enable easy model swapping
   - Simplify comparison & testing

7. **Document Assumptions**
   - What preprocessing was applied?
   - What features were engineered?
   - What are the model's limitations?
   - → Store in `model_metadata.json`

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Hardcoded hyperparameters | Hard to experiment | Move to `config.yaml` |
| No data versioning | Reproductibility breaks | Use DVC to track data |
| Preprocessing in notebook only | Can't reproduce in production | Extract to `data_processor.py` |
| Random seed not set | Results not reproducible | Set seed in `config.yaml` |
| No train/test split | Overfitting undetected | Use proper splits |
| Model in Git | Repo becomes huge | Use DVC for models |
| No logging | Debugging impossible | Add `logging_utils.py` |

---

## When to Use This Pattern

✓ **Use This Pattern For**:
- Regression problems (house price, sales forecast)
- Classification problems (customer churn, fraud detection)
- Time series forecasting (stock price, demand)
- Web scraping projects (data collection)
- Business intelligence projects (exploratory analysis)

✗ **Don't Use For**:
- One-off scripts (use simpler structure)
- Research prototypes (notebooks are fine)
- Real-time streaming (different architecture)

---

## Related Blueprints

- **end-to-end-ml-project**: Full implementation of this pattern
- **timeseries-prediction-project**: Time series specific variant
- **web-scraping-project**: Simplified variant for data collection

---

## Implementation Checklist

- [ ] Create directory structure from template
- [ ] Move notebook code to src/ modules
- [ ] Create config.yaml with all hyperparameters
- [ ] Implement BaseModel interface
- [ ] Write data_processor.py
- [ ] Write model_trainer.py
- [ ] Set up DVC with dvc.yaml
- [ ] Create Flask app.py with endpoints
- [ ] Write Dockerfile
- [ ] Test with `dvc repro` and `docker run`
- [ ] Commit dvc.lock to git
- [ ] Document in README.md

---

**Last Updated**: 2025-12-23
**Source Projects**: 5 (Airbnb, Flight Fare, Gold Price, E-Commerce, Article Scraper)
**Production Status**: ✓ Proven in 5+ projects
