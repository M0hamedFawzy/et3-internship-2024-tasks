CREATE TABLE DimDate (
    date_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    day INT,
    month INT,
    year INT,
    quarter INT,
    weekday VARCHAR(10)
)PARTITION BY RANGE (date_id);


CREATE TABLE DimUser (
    user_id INT PRIMARY KEY,
    phone_number VARCHAR(15),
    username VARCHAR(50),
    registration_date DATE,
    subscription_plan_id INT,
    green_user_status_id INT,
    is_active BOOLEAN,
    is_staff BOOLEAN
);


CREATE TABLE DimSubscriptionPlan (
    subscription_plan_id INT PRIMARY KEY,
    name VARCHAR(10),
    price DECIMAL(6, 2),
    max_balance DECIMAL(20, 2),
    max_transactions DECIMAL(6, 2)
);


CREATE TABLE DimGreenPlan (
    green_plan_status_id INT PRIMARY KEY,
    green_type VARCHAR(6),
    price DECIMAL(6, 2)
);


CREATE TABLE DimServiceType (
    service_type_id SERIAL PRIMARY KEY,
    service_type VARCHAR(50),
    service_name VARCHAR(50)
);


CREATE TABLE DimWallet (
    wallet_id INT PRIMARY KEY,
    user_id INT,
    balance DECIMAL(10, 2),
    is_active BOOLEAN,
    deleted BOOLEAN
);


CREATE TABLE FactTransaction (
    transaction_id SERIAL,
    date_id INT REFERENCES DimDate(date_id),
    user_id INT REFERENCES DimUser(user_id),
    wallet_id INT REFERENCES DimWallet(wallet_id),
    service_type_id INT REFERENCES DimServiceType(service_type_id),
    amount DECIMAL(10, 2),
    fees DECIMAL(10, 2),
    balance_before DECIMAL(10, 2),
    balance_after DECIMAL(10, 2),
    transaction_date TIMESTAMP NOT NULL,
	PRIMARY KEY (transaction_id, date_id)
)PARTITION BY RANGE (date_id);




-- create partiotions for DimDate & FactTransaction
CREATE TABLE DimDate_2022 PARTITION OF DimDate FOR VALUES FROM (1) TO (366);
CREATE TABLE DimDate_2023 PARTITION OF DimDate FOR VALUES FROM (366) TO (731);
CREATE TABLE DimDate_2024 PARTITION OF DimDate FOR VALUES FROM (731) TO (1096);

CREATE TABLE FactTransaction_2022 PARTITION OF FactTransaction FOR VALUES FROM (1) TO (366);
CREATE TABLE FactTransaction_2023 PARTITION OF FactTransaction FOR VALUES FROM (366) TO (731);
CREATE TABLE FactTransaction_2024 PARTITION OF FactTransaction FOR VALUES FROM (731) TO (1096);


-- create indexing for better performance
CREATE INDEX idx_dimuser_phone ON DimUser (phone_number);
CREATE INDEX idx_dimuser_userid ON DimUser (user_id);

CREATE INDEX idx_dimwallet_userid ON DimWallet (user_id);
CREATE INDEX idx_dimwallet_balance ON DimWallet (balance);

-- Index for DimDate_2022
CREATE INDEX idx_dimdate_2022_date ON DimDate_2022 (date);
CREATE INDEX idx_dimdate_2022_year ON DimDate_2022 (year);

-- Index for DimDate_2023
CREATE INDEX idx_dimdate_2023_date ON DimDate_2023 (date);
CREATE INDEX idx_dimdate_2023_year ON DimDate_2023 (year);

-- Index for DimDate_2024
CREATE INDEX idx_dimdate_2024_date ON DimDate_2024 (date);
CREATE INDEX idx_dimdate_2024_year ON DimDate_2024 (year);

-- index the FactTransaction "parent table"
CREATE INDEX idx_facttransaction_parent_date_id ON FactTransaction (date_id);

-- Index for FactTransaction_2022
CREATE INDEX idx_facttransaction_2022_date ON FactTransaction_2022 (transaction_date);
CREATE INDEX idx_facttransaction_2022_userid ON FactTransaction_2022 (user_id);
CREATE INDEX idx_facttransaction_2022_servicetypeid ON FactTransaction_2022 (service_type_id);

-- Index for FactTransaction_2023
CREATE INDEX idx_facttransaction_2023_date ON FactTransaction_2023 (transaction_date);
CREATE INDEX idx_facttransaction_2023_userid ON FactTransaction_2023 (user_id);
CREATE INDEX idx_facttransaction_2023_servicetypeid ON FactTransaction_2023 (service_type_id);

-- Index for FactTransaction_2024
CREATE INDEX idx_facttransaction_2024_date ON FactTransaction_2024 (transaction_date);
CREATE INDEX idx_facttransaction_2024_userid ON FactTransaction_2024 (user_id);
CREATE INDEX idx_facttransaction_2024_servicetypeid ON FactTransaction_2024 (service_type_id);





-- materialized views for frequently aggregated data
CREATE MATERIALIZED VIEW mv_monthly_transaction_summary AS
SELECT 
    date_trunc('month', transaction_date) AS month,
    user_id,
    SUM(amount) AS total_amount,
    COUNT(transaction_id) AS transaction_count
FROM FactTransaction
GROUP BY 1, 2;




-- * DROP ALL THE TABLES *
drop table dimuser, dimwallet, dimdate, dimgreenplan, dimsubscriptionplan, facttransaction, dimservicetype





/*
1- OLTP vs. OLAP:
    OLTP databases handle transactional tasks and are optimized for quick, real-time operations.
    OLAP databases are optimized for complex queries, aggregations, and historical data analysis.

2-Star Schema:
    Fact Table: Central table that stores metrics for analysis.
    Dimension Tables: Surround the fact table and provide descriptive data that allows us to segment and analyze metrics meaningfully.

3- Dimensional Model Design:
    Fact Table (FactTransaction): Captures measurable data points.
    Date Dimension (DimDate): Key for time-based analysis (e.g., transaction trends over time).
    User Dimension (DimUser): Allows segmentation by user attributes.
    Subscription and Green User Dimensions (DimSubscriptionPlan, DimGreenUser): Support analysis by subscription plans and green user types.
    Service Type Dimension (DimServiceType): Enables tracking by service type and service name.
    Wallet Dimension (DimWallet): Links users to wallet metrics, supporting balance analysis.
*/