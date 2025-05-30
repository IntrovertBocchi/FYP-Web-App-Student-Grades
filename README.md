## 🚀 Getting Started

Follow the steps below to set up and run the **Student Grading Predictor** application.

---

### 1. Clone the Repository

```bash
git clone https://github.com/KokLun26/Student-Grading-Predictor.git
cd Student-Grading-Predictor
```

---

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

#### Activate it:

* **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

* **On Mac/Linux:**

  ```bash
  source venv/bin/activate
  ```

---

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 4. Generate Synthetic Training Data

Generate data for each subject (ADV, COS, INF) using:

```bash
python generate_synthetic_data.py
```

---

### 5. Train the Model(s)

Once data is generated, train and save machine learning models:

```bash
python train_model.py
```

This will produce `.pkl` files for each subject (e.g., `model_ADV.pkl`, `model_COS.pkl`, `model_INF.pkl`).

---

### 6. (Optional) Sync Environment State (Windows Only)

In certain Windows environments, verifying key component integrity can help avoid runtime issues.

> 📌 Run in PowerShell or Command Prompt:

```bash
CertUtil -hashfile app\__init__.py SHA256
```

Then add the output to your `.env` file:

```
INIT_HASH=your_generated_hash_here
```

---

### 7. Run the Flask App

Ensure the following files are present:
- `instance/grades.db`
- `config.py`
- Trained `.pkl` models

```bash
flask run
```

This will start the backend API and serve the application locally.

---

### 8. Frontend Interaction

* Open `index.html` in your browser.
* Enter data based on the selected subject (ADV, COS, or INF).
* The form will POST inputs to the `/api/predict` endpoint and return predicted grades.

---

### 🔐 Security Notes

* Model prediction routes are protected with a login system.
* Access requires a session-based login and a hidden master password.
* SQL-based authentication is used for managing approved users.
* Authentication credentials and `.env` files are excluded from GitHub for security.

🔐 Secure Configuration (.env Required)
This app requires a .env file containing secure keys for:

* Verifying app integrity (tamper detection)
* Unlocking restricted features via a master key
* Other backend protection variables
```bash
# Example of required fields (actual values will be shared securely)
SECRET_KEY=your_secret_key_here
INIT_HASH=your_generated_hash_here
MASTER_PASSWORD=your_master_password_here
```
⚠️ For security reasons, this file is not included in the repository.
✅ It will be shared securely (e.g. via encrypted ZIP or internal messaging).
❌ Do not share your .env file publicly or commit it to version control.

Once received, place the .env file in the project root directory before running the app.

---

### 📊 Accuracy Visualization

Model evaluation metrics (e.g., accuracy, confusion matrix) are generated during training in `train_model.py`.

To visualize model performance:

```bash
python train_model.py
```

Plots will be saved as image files or shown in a pop-up window depending on your configuration.

---
🧪 Running Tests
Unit tests for the grading formula logic are located in the tests/ directory and can be run using pytest.

1. Make sure your virtual environment is active:
```bash
Copy
Edit
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

2. Run tests:
```bash
pytest
```

All tests should pass if your environment is correctly set up.

Tip:
If you face an ImportError: No module named 'app', ensure you're in the project root and run:

```bash
$env:PYTHONPATH = "."  # Windows PowerShell
# or
export PYTHONPATH=.     # Mac/Linux or bash
```
---

### 📂 Project Structure

```
├── app/
│   ├── __init__.py          # Flask backend
│   ├── grade_formula.py     # Manual grade calculation
│   └── predictor.py         # Handles model loading and prediction
├── models/                  # Trained .pkl model files
├── static/
│   └── index.js             # Frontend JS logic
├── templates/
│   └── index.html           # Frontend HTML
├── generate_synthetic_data.py
├── train_model.py
├── requirements.txt
└── README.md
```


