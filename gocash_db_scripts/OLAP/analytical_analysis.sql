-- Examples for using the OLAP DB for Analytical purposes


-- 1. Monthly Transaction Totals: Analyze transaction amounts by month and year to detect seasonal trends.
SELECT 
    D.year, 
    D.month, 
    SUM(F.amount) AS total_amount
FROM 
    FactTransaction F
JOIN DimDate D ON F.date_id = D.date_id
GROUP BY D.year, D.month
ORDER BY D.year, D.month;


-- 2. User Segmentation by Subscription Plan: Understand how transaction activity varies by subscription type.
SELECT 
    SP.name AS subscription_plan, 
    COUNT(DISTINCT F.user_id) AS user_count,
    SUM(F.amount) AS total_transactions
FROM 
    FactTransaction F
JOIN DimUser U ON F.user_id = U.user_id
JOIN DimSubscriptionPlan SP ON U.subscription_plan_id = SP.subscription_plan_id
GROUP BY SP.name;


-- 3. Average Transaction Size by Service Type: Evaluate which services have the largest transaction sizes.
SELECT 
    S.service_name,
    AVG(F.amount) AS avg_transaction_amount
FROM 
    FactTransaction F
JOIN DimServiceType S ON F.service_type_id = S.service_type_id
GROUP BY S.service_name
ORDER BY avg_transaction_amount DESC;


-- 4. Retention Analysis by Registration Date: Track activity over time for users who registered in a specific period.
SELECT 
    D.year, 
    D.month,
    COUNT(DISTINCT F.user_id) AS active_users
FROM 
    FactTransaction F
JOIN DimUser U ON F.user_id = U.user_id
JOIN DimDate D ON F.date_id = D.date_id
WHERE U.registration_date BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY D.year, D.month
ORDER BY D.year, D.month;


-- 5. Balance Change Analysis: Measure how the total balance changes over time across all wallets.
SELECT 
    D.year,
    D.month,
    SUM(F.balance_after - F.balance_before) AS net_balance_change
FROM 
    FactTransaction F
JOIN DimDate D ON F.date_id = D.date_id
GROUP BY D.year, D.month
ORDER BY D.year, D.month;
