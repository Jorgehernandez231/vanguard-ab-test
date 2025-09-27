# Vanguard A/B Test Analysis

[![Google Slides](https://docs.google.com/presentation/d/1NcrkhS_k4dqKjvEEDgipdWkyuNUkoTk8YjKrLQhdwn4/edit?slide=id.g383ec90df5c_0_30#slide=id.g383ec90df5c_0_30)]
[![GitHub](https://github.com/Jorgehernandez231/vanguard-ab-test)]

This project analyzes an **A/B test** conducted on Vanguard’s online platform.  
The objective is to evaluate how the new design impacts **completion rates, error rates, and user engagement**, with special attention to **primary clients (top 10% by balance)**.

---

## 📂 Project Structure

vanguard-ab-test/
│── Data/ # Raw and processed datasets
│── Scrap/ # Supporting scripts or collected data
│── 1.Processing_data.ipynb # Data cleaning & preprocessing
│── 2.EDA.ipynb # Exploratory Data Analysis
│── 3.Metrics_test.ipynb # Statistical tests & KPI evaluation
│── Function.py # Helper functions
│── README.md # Project documentation
│── .gitignore


---

## 🚀 Workflow

1. **Data Processing** (`1.Processing_data.ipynb`)  
   - Load raw datasets  
   - Handle missing values & duplicates  
   - Prepare clean dataset for analysis  

2. **Exploratory Data Analysis (EDA)** (`2.EDA.ipynb`)  
   - Client demographics (age, tenure, balance)  
   - Segmentation of primary vs. other clients  
   - Visualizations of engagement and errors  

3. **Metrics & Hypothesis Testing** (`3.Metrics_test.ipynb`)  
   - Define KPIs (completion rate, error rate, time by step)  
   - Compare Control vs Test groups  
   - Run statistical tests (Chi-square, t-test, ANOVA, power analysis)  

---

## 📊 Key KPIs

- **Completion Rate** → % of users completing the full process  
- **Error Rate** → Errors per funnel step  
- **Time Spent** → Average time per step  
- **Primary Clients Analysis** → Top 10% balance vs others  

---

## 📌 Results Summary

- ✅ **Test group** improved completion rates compared to Control  
- ⚠️ **Primary clients** showed slightly higher error rates  
- 👥 **Younger users (<35)** adapted better than older ones  
- 📈 Early funnel steps still present issues  

---

## ⚙️ Requirements

Install the necessary Python packages:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels jupyter
