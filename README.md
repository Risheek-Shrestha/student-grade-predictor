# 🎓 Student Grade Predictor — Machine Learning

A machine learning project that predicts student final grades (G3) using academic and personal features. Trained and compared three ML models to find the best predictor.

## 🛠️ Tech Stack

Python 3 · Jupyter Notebook · Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn · Joblib

## 📊 Dataset

- **Source:** UCI Student Performance Dataset (Kaggle)
- **Size:** 395 students, 33 features
- **Target:** G3 (final grade, 0–20)
- **Key features:** studytime, failures, absences, G1, G2, parental education

## 🤖 Models Trained

- Linear Regression — baseline model
- Random Forest — ensemble, best performer
- K-Nearest Neighbors (KNN) — distance based

## 📈 Results

| Model | MAE | R² Score |
|---|---|---|
| Linear Regression | 1.50 | 0.75 |
| Random Forest | 1.11 | 0.83 |
| KNN | 1.41 | 0.78 |

**Best Model: Random Forest (MAE: 1.11, R²: 0.83)**

## 🔍 Key Findings

- G2 (second period grade) is the strongest predictor of final grade
- Higher failures = significantly lower final grade
- Study time has moderate positive impact
- Random Forest outperformed all models with 83% variance explained

## 📁 Project Structure
student-price-predictor/
├── analysis.ipynb       # Main notebook — EDA, training, evaluation
├── student_model.pkl    # Saved Random Forest model
├── archive/
│   └── student-mat.csv  # Dataset
└── README.md

## ⚙️ How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/Risheek-Shrestha/student-price-predictor.git
```

2. Install dependencies
```bash
pip install pandas scikit-learn matplotlib seaborn joblib notebook
```

3. Open the notebook
```bash
jupyter notebook analysis.ipynb
```

4. Run all cells

## 👨‍💻 Author

**Risheek Shrestha**
- GitHub: [@Risheek-Shrestha](https://github.com/Risheek-Shrestha)
- Email: shrestharisheek@gmail.com
