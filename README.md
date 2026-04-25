# 🛍️ E-Commerce Product Recommendation & Customer Segmentation

## 📌 Project Overview

This project combines **Supervised Learning** and **Unsupervised Learning** to analyze e-commerce customer reviews and extract valuable insights.

The main objectives are:

* 🎯 Predict whether a product will be **recommended** or not
* 📊 Identify **customer segments** based on behavior and feedback

---

## 🧠 Machine Learning Approaches

### 🔹 1. Supervised Learning (Classification)

We built classification models to predict if a product is recommended (`1`) or not (`0`).

#### ✔️ Models Used:

* Logistic Regression
* Decision Tree
* Random Forest

#### 📈 Results:

| Model               | Accuracy          |
| ------------------- | ----------------- |
| Logistic Regression | 93.53%            |
| Decision Tree       | 93.43%            |
| Random Forest       | **93.75% (Best)** |

👉 **Random Forest** achieved the best performance after hyperparameter tuning.

---

### 🔹 2. Unsupervised Learning (Clustering)

We applied clustering techniques to discover hidden patterns in customer behavior.

#### ✔️ Methods Used:

* K-Means Clustering
* Hierarchical Clustering
* DBSCAN

#### 📊 Key Insights:

* K-Means provided clear segmentation of customers
* Hierarchical Clustering helped visualize group structures using dendrograms
* DBSCAN detected **outliers and noise points**

---

## ⚙️ Technologies Used

* Python
* Pandas & NumPy
* Scikit-learn
* Matplotlib & Seaborn
* Streamlit (for web app)
* TextBlob (for sentiment analysis)

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecommerce-project.git
cd ecommerce-project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app

```bash
streamlit run app.py
```

👉 The app will open in your browser at:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
ecommerce_project/
│
├── app.py                  # Streamlit application
├── ecommerce_project.ipynb # Supervised learning notebook
├── nonSupervise.ipynb      # Clustering notebook
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

## 🔍 Key Features

* Data cleaning and preprocessing
* Feature engineering (review length, sentiment analysis)
* Model training and evaluation
* Hyperparameter tuning (GridSearch)
* Customer segmentation using clustering
* Interactive dashboard with Streamlit

---

## 💡 Conclusion

This project demonstrates how machine learning can:

* Improve product recommendation systems
* Understand customer behavior
* Identify hidden patterns in data

---

## 👨‍💻 Author

**Ikram Daoubih**

---

## ⭐ Don't forget to star the repository if you like it!
