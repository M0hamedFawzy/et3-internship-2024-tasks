import sys
sys.path.append(r'C:\Users\Mohamad Fawzy\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from django.db import connections, models
from .models import DimUser, DimWallet, FactTransaction, DimDate
import os
import pickle
from AI_Models.work import get_users_future, get_profits_future, get_transactions_future
from django.http import JsonResponse




def abbreviate_number(value):
    """
    Format the number into a more readable format, e.g., 240K, 2M, etc.
    """
    try:
        value = float(value)
        if value >= 1_000_000:
            return f'{value / 1_000_000:.0f}M'  # Millions
        elif value >= 1_000:
            return f'{value / 1_000:.0f}K'  # Thousands
        else:
            return str(value)
    except (ValueError, TypeError):
        return value


def execute_dw_sql(query, params=None):
    with connections['datawarehouse'].cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


@staff_member_required
def dashboard(request):
    # USERS SECTION
    # Card for all active users
    active_users_count = DimUser.objects.using('datawarehouse').filter(is_active=True).count()

    # Card for all non-null green users
    green_users_count = DimUser.objects.using('datawarehouse').exclude(green_user_status_id__isnull=True).count()

    # Doughnut chart: active vs non-active users
    active_vs_non_active_users = {
        "active": active_users_count,
        "non_active": DimUser.objects.using('datawarehouse').filter(is_active=False).count()
    }

    # Polar area chart: Subscription plans
    subscription_plans = DimUser.objects.using('datawarehouse').values('subscription_plan_id').annotate(count=models.Count('user_id'))

    # Radar chart: Green vs non-green users
    green_vs_non_green = {
        "green_users": green_users_count,
        "non_green_users": DimUser.objects.using('datawarehouse').filter(green_user_status_id__isnull=True).count()
    }

    # Bar chart for green users distribution
    green_distribution = DimUser.objects.using('datawarehouse').raw("""
        SELECT green_user_status_id, COUNT(user_id) as user_count
        FROM DimUser u
        WHERE u.green_user_status_id IN (1, 2, 3)  -- 1 = Leaf, 2 = Tree, 3 = Forest
        GROUP BY green_user_status_id
        ORDER BY green_user_status_id;
    """)

    leaf = DimUser.objects.using('datawarehouse').filter(green_user_status_id=1).count()
    tree = DimUser.objects.using('datawarehouse').filter(green_user_status_id=2).count()
    forest = DimUser.objects.using('datawarehouse').filter(green_user_status_id=3).count()



    # WALLETS SECTION
    # Card for all active wallets
    active_wallets_count = DimWallet.objects.using('datawarehouse').filter(is_active=True).count()

    # Doughnut chart: active vs non-active wallets
    active_vs_non_active_wallets = {
        "active_wallets": active_wallets_count,
        "non_active_wallets": DimWallet.objects.using('datawarehouse').filter(is_active=False).count()
    }

    # Bar chart: Average wallet balance by month/year
    avg_balance_query = """
        SELECT TO_CHAR(transaction_date, 'YYYY-MM') as month_year, AVG(balance_after)
        FROM facttransaction
        GROUP BY month_year
        ORDER BY month_year;
    """
    avg_wallet_balances = execute_dw_sql(avg_balance_query)

    # Bar chart for created wallets
    query = """SELECT 
  EXTRACT(YEAR FROM registration_date) AS reg_year,
  COUNT(*) AS total_wallets
FROM 
  dimuser
GROUP BY 
  EXTRACT(YEAR FROM registration_date)
ORDER BY 
  reg_year"""
    created_wallets = execute_dw_sql(query)




    # TRANSACTIONS SECTION
    # Card for total number of transactions
    total_transactions_count = FactTransaction.objects.using('datawarehouse').count()

    # Card for total profit from transactions
    total_transactions_profit = FactTransaction.objects.aggregate(total_profit=Sum('fees'))

    # Bar chart: Transactions per year (2022-2024)
    transactions_per_year_query = """
           SELECT year, COUNT(*) as transaction_count
FROM facttransaction f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY year 
ORDER BY year;
    """
    transactions_per_year = execute_dw_sql(transactions_per_year_query)

    # Doughnut chart: Service types
    service_types_query = """
        SELECT s.service_name, COUNT(f.transaction_id)
        FROM facttransaction f
        JOIN DimServiceType s ON f.service_type_id = s.service_type_id
        GROUP BY s.service_name
        ORDER BY COUNT(f.transaction_id) DESC;
    """
    service_types_distribution = execute_dw_sql(service_types_query)

    # Line chart: Peak transaction times per month
    peak_transactions_query = """
        SELECT EXTRACT(MONTH FROM transaction_date) as month, COUNT(transaction_id) as transactions
        FROM facttransaction
        WHERE EXTRACT(YEAR FROM transaction_date) = 2024
        GROUP BY month
        ORDER BY month;
    """
    peak_transactions = execute_dw_sql(peak_transactions_query)



    # TRENDS SECTION
    # user registration trend
    # future = get_users_future()
    # future_dict = future.to_dict('list')
    # dates = future_dict["ds"]
    # predictions = future_dict["yhat"]


    # Combine data for rendering
    context = {
        "cards": {
            "active_users": abbreviate_number(active_users_count),
            "green_users": abbreviate_number(green_users_count),
            "active_wallets": abbreviate_number(active_wallets_count),
            "total_transactions": abbreviate_number(total_transactions_count),
            "total_transactions_profit": abbreviate_number(total_transactions_profit['total_profit'])
        },
        "charts": {
            "users": {
                "active_vs_non_active": active_vs_non_active_users,
                "subscription_plans": subscription_plans,
                "green_vs_non_green": green_vs_non_green,
                "green_distribution": green_distribution,
                "leaf": leaf,
                "tree": tree,
                "forest": forest,
            },
            "wallets": {
                "average_balances": avg_wallet_balances,
                "active_vs_non_active": active_vs_non_active_wallets,
                "created_wallets": created_wallets
            },
            "transactions": {
                "per_year": transactions_per_year,
                "service_types": service_types_distribution,
                "peak_transactions": peak_transactions
            },
        }
    }

    return render(request, 'dwbi_dashboard/dashboard.html', context)


# def generate_chart(request):
#     if request.method == 'POST':
#         # Get the period and frequency from the form data
#         period = int(request.POST.get('period'))
#         freq = request.POST.get('freq')
#         # users forecast
#         users_dates, users_future = get_users_future(period=period, freq=freq)
#         # transactions forecast
#         trans_dates, trans_future = get_transactions_future(period=period, freq=freq)
#         # profits forecast
#         profits_dates, profits_future = get_profits_future(period=period, freq=freq)
#
#         context = {
#             "trends": {
#                 "users": {
#                     "dates": users_dates,
#                     "predictions": users_future,
#                 },
#                 "transactions": {
#                     "dates": trans_dates,
#                     "predictions": trans_future,
#                 },
#                 "profits": {
#                     "dates": profits_dates,
#                     "predictions": profits_future,
#                 },
#             }
#         }
#         return render(request, 'dwbi_dashboard/dashboard.html', context)

def generate_chart(request):
    if request.method == 'POST':
        period = int(request.POST.get('period'))
        freq = request.POST.get('freq')

        # Generate forecasts
        users_dates, users_future = get_users_future(period=period, freq=freq)
        trans_dates, trans_future = get_transactions_future(period=period, freq=freq)
        profits_dates, profits_future = get_profits_future(period=period, freq=freq)

        data = {
            "users": {
                "dates": users_dates,
                "predictions": users_future,
            },
            "transactions": {
                "dates": trans_dates,
                "predictions": trans_future,
            },
            "profits": {
                "dates": profits_dates,
                "predictions": profits_future,
            },
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request"}, status=400)