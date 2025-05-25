## 🚀 Getting Started

Follow the steps below to set up and run the Student Grading Predictor application.

---

### 1. Clone the repository

```bash
git clone https://github.com/KokLun26/Student-Grading-Predictor.git
cd Student-Grading-Predictor
```

---

### 2. Create a virtual environment (recommended)

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

### 3. Install required packages

```bash
pip install -r requirements.txt
```

---

### 4. Optional: Sync environment state (Windows only)

In some deployment environments, it's recommended to verify the integrity of key components to ensure full compatibility.

> 📌 Run this command in PowerShell or Command Prompt:

```bash
CertUtil -hashfile app\__init__.py SHA256
```

Take note of the generated hash and add it to your `.env` file:

```
INIT_HASH=your_generated_hash_here
```

This step can help avoid startup inconsistencies in some local runtime environments.

---

### 5. Run the app

```bash
flask run
```

---
