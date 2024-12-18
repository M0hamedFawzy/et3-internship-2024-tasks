-- search transactions based on transaction type
CREATE OR REPLACE FUNCTION display_transactions(input_transaction_type VARCHAR)
RETURNS TABLE (
    transaction_id INTEGER,
    sender_id INTEGER,
    receiver VARCHAR(15),
    user_wallet_id INTEGER,
    amount DECIMAL(10, 2),
    fees DECIMAL(10, 2),
    service_type VARCHAR(50),
    service_name VARCHAR(50),
    balance_before DECIMAL(10, 2),
    balance_after DECIMAL(10, 2),
    transaction_date TIMESTAMP
)
LANGUAGE plpgsql
AS 
$$
BEGIN
    IF lower(input_transaction_type) = 'all' THEN
        RETURN QUERY
            SELECT * FROM Transaction;
    ELSIF input_transaction_type IS NOT NULL THEN
        RETURN QUERY
            SELECT * FROM Transaction AS t
            WHERE lower(t.service_type) = lower(input_transaction_type);
    END IF;
END;
$$;
--example:  SELECT * FROM display_transactions('transaction');



-- search wallets based on active or inactive
CREATE OR REPLACE FUNCTION display_wallets(status VARCHAR)
RETURNS TABLE (
    wallet_id INTEGER,
    user_id INTEGER,
    balance DECIMAL(10, 2),
    is_active BOOLEAN,
    deleted BOOLEAN
)
LANGUAGE plpgsql
AS 
$$
BEGIN
    RETURN QUERY
    SELECT w.wallet_id, w.user_id, w.balance, w.is_active, w.deleted
    FROM Wallet as w
    WHERE (status = 'active' AND w.is_active = TRUE) OR (status = 'inactive' AND w.is_active = FALSE);
END;
$$;
--example: SELECT display_wallets('active')



-- display user transactions
CREATE OR REPLACE FUNCTION display_user_transactions(user_phone VARCHAR)
RETURNS TABLE (
    transaction_id INTEGER,
    sender_id INTEGER,
    receiver VARCHAR(15),
    user_wallet_id INTEGER,
    amount DECIMAL(10, 2),
    fees DECIMAL(10, 2),
    service_type VARCHAR(50),
    service_name VARCHAR(50),
    balance_before DECIMAL(10, 2),
    balance_after DECIMAL(10, 2),
    transaction_date TIMESTAMP
)
LANGUAGE plpgsql
AS 
$$
DECLARE
    v_user_id INTEGER;
    v_wallet_id INTEGER;
BEGIN
    SELECT user_id INTO v_user_id FROM Users WHERE phone_number = user_phone;
    IF v_user_id IS NULL THEN
        RAISE EXCEPTION 'User not found';
    END IF;

    SELECT wallet_id INTO v_wallet_id FROM Wallet WHERE user_id = v_user_id;
    
    RETURN QUERY
    SELECT * FROM Transaction AS t
    WHERE (t.sender_id = v_user_id OR t.receiver = user_phone) AND t.user_wallet_id = v_wallet_id;
END;
$$;
--example: SELECT display_user_transactions('01126008231')










