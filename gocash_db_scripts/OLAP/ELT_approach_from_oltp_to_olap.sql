-- Populate DimDate with date ranges, day, month, year, quarter, weekday values
INSERT INTO DimDate (date, day, month, year, quarter, weekday)
SELECT 
    date,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(QUARTER FROM date) AS quarter,
    TO_CHAR(date, 'Day') AS weekday
FROM 
    generate_series('2022-01-01'::date, '2024-12-31'::date, '1 day'::interval) AS date;



-- This dimension will use data from your Users table in the OLTP database.
INSERT INTO DimUser (user_id, phone_number, username, registration_date, subscription_plan_id, green_user_status_id, is_active, is_staff)
SELECT 
    user_id,
    phone_number,
    username,
    DATE(registration_date),
    subscription_plan_id,
    green_user_status_id,
    is_active,
    is_staff
FROM Users;




-- Populate DimServiceType if service types are predefined
INSERT INTO DimServiceType (service_type, service_name)
VALUES
('Deposit', 'Wallet Deposit'),
('Withdrawal', 'Wallet Withdrawal'),
('Transaction', 'Peer-to-Peer Transfer'),
('Bill Payment', 'Utility Bill'),
('Merchant Payment', 'Store Purchase'),
('Account Subscription', 'Standard/Plus/Premium Subscription'),
('Green Subscription', 'Leaf/Tree/Forest Plan');



-- wallet dimention
INSERT INTO DimWallet (wallet_id, user_id, balance, is_active, deleted)
SELECT 
    wallet_id,
    user_id,
    balance,
    is_active,
    deleted
FROM Wallet;



-- populate the fact table (FactTransaction)
INSERT INTO FactTransaction (transaction_id, date_id, user_id, wallet_id, service_type_id, amount, fees, balance_before, balance_after, transaction_date)
SELECT 
    T.transaction_id,
    D.date_id,
    U.user_id,
    W.wallet_id,
    S.service_type_id,
    T.amount,
    T.fees,
    T.balance_before,
    T.balance_after,
    T.transaction_date
FROM 
    Transaction T
JOIN DimDate D ON D.date = DATE(T.transaction_date)
JOIN DimUser U ON U.user_id = T.sender_id
JOIN DimWallet W ON W.wallet_id = T.user_wallet_id
JOIN DimServiceType S ON S.service_type = T.service_type;
