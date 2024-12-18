# import pandas as pd
from joblib import dump, load
# from prophet import Prophet
import sys
sys.path.append(r'C:\Users\Mohamad Fawzy\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')


# users = pd.read_csv('D:/et3_tasks/gocash_db_scripts/AI_&_DataScience/users.csv')
# transactions = pd.read_csv('D:/et3_tasks/gocash_db_scripts/AI_&_DataScience/total_transactions.csv')
# profits = pd.read_csv('D:/et3_tasks/gocash_db_scripts/AI_&_DataScience/total_profit.csv')
#
# users.rename(columns={'reg_year': 'year', 'reg_month': 'month', 'reg_day': 'day', 'total_registered_users': 'y'}, inplace=True)
# profits.rename(columns={'transaction_year': 'year', 'transaction_month': 'month', 'transaction_day': 'day', 'total_profit': 'y'}, inplace=True)
#
# users['ds'] = pd.to_datetime(users[['year', 'month', 'day']])
# transactions['ds'] = pd.to_datetime(transactions[['year', 'month', 'day']])
# profits['ds'] = pd.to_datetime(profits[['year', 'month', 'day']])
#
# users = users[['ds', 'y']]
# profits = profits[['ds', 'y']]
#
# users_model = Prophet()
# transactions_model = Prophet()
# profits_model = Prophet()
#
# users_model.fit(users)
# transactions_model.fit(transactions)
# profits_model.fit(profits)
#
# users_future = users_model.make_future_dataframe(periods=8, freq='M', include_history=False)
# users_prediction = users_model.predict(users_future)
#
# print(users_prediction[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
#
# dump(users_model, 'users_model.joblib')
# dump(transactions_model, 'transactions_model.joblib')
# dump(profits_model, 'profits_model.joblib')
# print("Done")


def get_users_future(period, freq):
    loaded_model = load('AI_Models/users_model.joblib')
    users_future = loaded_model.make_future_dataframe(periods=period, freq=freq, include_history=False)
    users_prediction = loaded_model.predict(users_future)
    users_future_dict = users_prediction.to_dict('list')
    users_dates = users_future_dict["ds"]
    users_dates = [date.strftime('%Y-%m-%d') for date in users_dates]
    users_predictions = users_future_dict["yhat"]

    return users_dates, users_predictions


def get_transactions_future(period, freq):
    loaded_model = load('AI_Models/transactions_model.joblib')
    users_future = loaded_model.make_future_dataframe(periods=period, freq=freq, include_history=False)
    users_prediction = loaded_model.predict(users_future)
    users_future_dict = users_prediction.to_dict('list')
    users_dates = users_future_dict["ds"]
    users_dates = [date.strftime('%Y-%m-%d') for date in users_dates]
    users_predictions = users_future_dict["yhat"]

    return users_dates, users_predictions


def get_profits_future(period, freq):
    loaded_model = load('AI_Models/profits_model.joblib')
    users_future = loaded_model.make_future_dataframe(periods=period, freq=freq, include_history=False)
    users_prediction = loaded_model.predict(users_future)
    users_future_dict = users_prediction.to_dict('list')
    users_dates = users_future_dict["ds"]
    users_dates = [date.strftime('%Y-%m-%d') for date in users_dates]
    users_predictions = users_future_dict["yhat"]

    return users_dates, users_predictions

