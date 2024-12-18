CREATE TABLE SubscriptionPlan (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    price DECIMAL(6, 2) NOT NULL,
    max_balance DECIMAL(20, 2),
    max_transactions DECIMAL(6, 2)
);

CREATE TABLE GreenPlan (
    id SERIAL PRIMARY KEY,
    green_type VARCHAR(6) UNIQUE NOT NULL,
    price DECIMAL(6, 2) NOT NULL
);

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    username VARCHAR(50),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subscription_plan_id INTEGER,
    green_plan_status_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (subscription_plan_id) REFERENCES SubscriptionPlan(id) ON DELETE SET NULL,
    FOREIGN KEY (green_plan_status_id) REFERENCES GreenPlan(id) ON DELETE SET NULL
);

CREATE TABLE Wallet (
    wallet_id SERIAL PRIMARY KEY,
    wallet_pass CHAR(6) NOT NULL,
    user_id INTEGER NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Transaction (
    transaction_id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    receiver VARCHAR(15) NOT NULL,
    user_wallet_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    fees DECIMAL(10, 2),
    service_type VARCHAR(50),
    service_name VARCHAR(50),
    balance_before DECIMAL(10, 2) DEFAULT 0.00,
    balance_after DECIMAL(10, 2) DEFAULT 0.00,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE NO ACTION,
    FOREIGN KEY (user_wallet_id) REFERENCES Wallet(wallet_id) ON DELETE NO ACTION
);
