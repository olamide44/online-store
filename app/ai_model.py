# ai_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

class Model:
    def __init__(self):
        self.model = LinearRegression()
        self.trained = False

    def train_model(self, data):
        data['date'] = pd.to_datetime(data['date'])
        data['date_ordinal'] = data['date'].map(pd.Timestamp.toordinal)

        X = data[['date_ordinal']]
        y = data['sales']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        self.trained = True

    def predict_trends(self, future_dates):
        if not self.trained:
            return "Model is not trained yet."

        future_dates = pd.to_datetime(future_dates)
        future_dates_ordinal = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
        predictions = self.model.predict(pd.DataFrame(future_dates_ordinal, columns=['date_ordinal']))

        # Generate reasons for each prediction
        reasons = []
        for i, date in enumerate(future_dates):
            reason = f"Based on historical sales data trends up to {date.strftime('%Y-%m-%d')}, the sales are predicted to follow the observed pattern."
            reasons.append(reason)

        return predictions.clip(min=0), reasons

def perform_data_analytics(orders, users, products, start_date=None, end_date=None):
    if start_date and end_date:
        orders['date_of_order'] = pd.to_datetime(orders['date_of_order'])
        orders = orders[(orders['date_of_order'] >= start_date) & (orders['date_of_order'] <= end_date)]

    total_users = len(users)
    total_products = len(products)
    total_orders = len(orders)
    average_order_value = orders['total_amount'].mean()

    sales_over_time = orders.groupby('date_of_order')['total_amount'].sum().reset_index()
    sales_over_time['date_of_order'] = pd.to_datetime(sales_over_time['date_of_order'])

    analytics_data = {
        "Total Users": total_users,
        "Total Products": total_products,
        "Total Orders": total_orders,
        "Average Order Value": f"${average_order_value:.2f}"
    }

    sales_plot = create_sales_plot(sales_over_time)

    return analytics_data, sales_plot

def create_sales_plot(sales_over_time):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=sales_over_time, x='date_of_order', y='total_amount')
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

data = pd.DataFrame({
    'date': pd.date_range(start='1/1/2020', periods=100, freq='D'),
    'sales': np.random.randint(100, 500, size=100)
})

model = Model()
model.train_model(data)
