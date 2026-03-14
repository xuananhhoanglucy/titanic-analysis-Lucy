# Titanic Survival Analysis & Statistical Modeling - by Xuan Anh (Lucy) Hoang and Saad Larabi
An end-to-end analysis of Titanic Survival Analysis from data cleaning to analysis and visualization.

## Project Overview:
This project provides an end-to-end data analysis of the Titanic passenger manifest. The goal is to explore the factors that influenced survival rates through data cleaning, feature engineering, and statistical modeling. Unlike standard exploratory notebooks, this project is built with a modular architecture, separating core logic into a reusable Python library to ensure scalability and maintainability.

## Tech Stack:
- Language: Python
- Data Manipulation: Pandas (cleaning, filtering, and renaming complex datasets), NumPy (numerical operations).
- Statistical Analysis: SciPy (specifically stats for linear regression and correlation coefficients).
- Visualization: Matplotlib (generating distribution plots, bar charts for survival rates, and regression lines).
- Environment: Jupyter Notebooks and Python Scripts.

## Key Insights: 
- Socio-Economic Influence: A clear correlation was identified between passenger class and survival probability. The analysis shows that "First Class" passengers had a significantly higher survival rate compared to "Third Class."
- Demographic Factors: The data confirms the "women and children first" protocol, with female passengers and children showing drastically higher survival counts across all embarkation points.
- Statistical Correlation: Using linear regression, the project quantifies the relationship between specific variables (like Fare and Age) and survival, providing an R-value to indicate the strength of these connections.
- Geographic Trends: The visualization of survival by embark town reveals that passengers embarking from Cherbourg had different survival distributions compared to those from Southampton or Queenstown.

## Project Structure:
- Project summary and executive insight
- [SQL file](Xuan%20Anh%20Hoang%20ecommerce%20sql.sql): Contains the queries used to calculate key metrics and reasons behind the delay status in some orders.
- [Power BI Dashboard file](Xuan%20Anh%20Hoang%20ecommerce%20pbi.pdf): Contains visualiztion for key metrics with detailed data. 
- [Operations Performance Report](Xuan%20Anh%20Hoang%20eCommerce%20Operations%20Performance%20Report.pdf): Contains analysis and proposed actions.

## Sample Visualization
![Operations Dashboard Preview](eCommerce%20Dashboard%20preview.png)
1. Operational Efficiency
- **Logistics Bottleneck:** Identified a **48% Delay Delivery Rate**, with Warehouse 1 being the primary contributor (63.64% delay rate).
- **Staff Performance:** Isolated fulfillment outliers; while the average time is **180.40 minutes**, specific staff members (ID 202) exceeded this by 11%.

### 2. Quality & Risk Management
- **Product Vulnerability:** Pinpointed **SKU02** as a high-risk item with a **6.67% damage rate**, necessitating a review of packaging standards.
- **Financial Leakage:** Analyzed a **30% Return Ratio**, discovering that nearly all returns are due to internal process errors (Damaged/Wrong Item) rather than customer change-of-mind.



