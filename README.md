# Network Security System (Phishing Detection)

An end-to-end machine learning project to detect phishing network records using a training pipeline, MongoDB data source, and FastAPI-based prediction service.

## Features

- Data ingestion from MongoDB
- Data validation using schema checks and drift reporting
- Data transformation and preprocessing pipeline
- Model training and artifact generation
- Batch prediction from uploaded CSV file
- Optional model/artifact sync to AWS S3

## Tech Stack

- Python
- FastAPI + Uvicorn
- Scikit-learn, Pandas, NumPy
- MongoDB (PyMongo)
- MLflow, DagsHub (experiment tracking)
- Docker

## Project Structure

```text
networksecurity/
	components/         # ingestion, validation, transformation, training
	pipeline/           # orchestration pipeline
	entity/             # config + artifact entities
	utils/              # utility modules
	cloud/              # S3 sync helper
data_schema/          # schema.yaml
Network_Data/         # source csv
final_model/          # saved model artifacts
templates/            # HTML templates for prediction output
app.py                # FastAPI app
main.py               # local training flow entry
push_data.py          # push CSV data into MongoDB
```

## Prerequisites

- Python 3.10+ (recommended)
- MongoDB Atlas/database access
- (Optional) AWS credentials for S3 sync

## Installation

```bash
git clone <your-repository-url>
cd Network-Security-System

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirement.txt
```

## Environment Variables

Create a `.env` file in the project root.

```env
# Used in app.py (training/prediction service)
MONGO_URI=<your_mongodb_connection_string>

# Used in push_data.py
MONDB_URL=<your_mongodb_connection_string>

# Optional for S3 sync in training pipeline
AWS_ACCESS_KEY_ID=<your_key>
AWS_SECRET_ACCESS_KEY=<your_secret>
AWS_DEFAULT_REGION=<your_region>
```

## How to Run

### 1) Push initial dataset to MongoDB

```bash
python push_data.py
```

### 2) Run training pipeline (script)

```bash
python main.py
```

### 3) Start API server

```bash
python app.py
```

Server runs at: `http://localhost:8000`

## API Endpoints

- `GET /` → Redirects to Swagger docs
- `GET /docs` → Interactive API documentation
- `GET /train` → Runs full training pipeline
- `GET /predict` → Prediction upload page
- `POST /predict` → Upload CSV and get prediction table

## Docker

```bash
docker build -t network-security-system .
docker run -p 8000:8000 --env-file .env network-security-system
```

## Artifacts Generated

- Training artifacts under `Artifacts/<timestamp>/`
- Model/preprocessor under `final_model/`

## Notes

- Keep secrets in `.env` and never commit credentials.
- Ensure your MongoDB URI is valid before running ingestion/training.
- If prediction UI template is missing, add `templates/predict.html` for upload form.

## Author

**Aamir**
