-- create user
CREATE OR REPLACE PROCEDURE create_user(username VARCHAR, phone_number VARCHAR)
LANGUAGE plpgsql
AS 
$$
BEGIN
    INSERT INTO Users (username, phone_number, subscription_plan_id)
    VALUES (username, phone_number, 1);  -- Standard plan has id = 1
END;
$$;
-- example: call create_user('ABDO', '01154577714')




-- create wallet
CREATE OR REPLACE PROCEDURE create_wallet(user_phone VARCHAR, wallet_pass CHAR(6))
LANGUAGE plpgsql
AS 
$$
DECLARE
    user_id INT;
BEGIN
    SELECT user_id INTO user_id FROM Users WHERE phone_number = user_phone;
    IF user_id IS NOT NULL THEN
        INSERT INTO Wallet (wallet_pass, user_id, is_active) VALUES (wallet_pass, user_id, TRUE);
    END IF;
END;
$$;
-- example: call create_wallet('01154577714', '3333')




-- toggle wallet status
CREATE OR REPLACE PROCEDURE toggle_wallet_status(user_phone VARCHAR, user_action VARCHAR)
LANGUAGE plpgsql
AS 
$$
DECLARE
    v_user_id INT;
    new_status BOOLEAN;
BEGIN
    new_status := (lower(user_action) = 'activate');  -- If 'activate', new_status = TRUE; if 'deactivate', new_status = FALSE
    SELECT user_id INTO v_user_id FROM Users WHERE phone_number = user_phone;

    IF v_user_id IS NOT NULL THEN
        UPDATE Wallet SET is_active = new_status WHERE user_id = v_user_id;
    END IF;
END;
$$;
-- example: call toggle_wallet_status('01126008231', 'deactivate')




-- charge wallet (Deposite)
CREATE OR REPLACE PROCEDURE charge_wallet(user_phone VARCHAR, amount DECIMAL)
LANGUAGE plpgsql
AS 
$$
DECLARE
    v_user_id INT;
    v_wallet_id INT;
    v_balance_before DECIMAL;
    v_balance_after DECIMAL;
BEGIN
    SELECT user_id INTO v_user_id FROM Users WHERE phone_number = user_phone;
    SELECT wallet_id, balance INTO v_wallet_id, v_balance_before FROM Wallet WHERE user_id = v_user_id;

    IF v_wallet_id IS NOT NULL THEN
        v_balance_after := v_balance_before + amount;
        UPDATE Wallet SET balance = v_balance_after WHERE wallet_id = v-wallet_id;

        INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after)
        VALUES (v_user_id, user_phone, v_wallet_id, amount, 0, 'Deposite', 'Charge Wallet', v_balance_before, v_balance_after);
    END IF;
END;
$$;
-- example: call charge_wallet('01126008231', 5000)




-- withdraw money
CREATE OR REPLACE PROCEDURE withdraw_money(user_phone VARCHAR, amount DECIMAL, service_name VARCHAR)
LANGUAGE plpgsql
AS 
$$
DECLARE
    v_user_id INT;
    v_wallet_id INT;
    v_balance_before DECIMAL;
    v_balance_after DECIMAL;
    v_fees DECIMAL := amount * 0.04; -- tax = 4 %
BEGIN
    SELECT user_id INTO v_user_id FROM Users WHERE phone_number = user_phone;
    SELECT wallet_id, balance INTO v_wallet_id, v_balance_before FROM Wallet WHERE user_id = v_user_id;

    IF v_wallet_id IS NOT NULL THEN
        v_balance_after := v_balance_before - (amount + v_fees);
        UPDATE Wallet SET balance = v_balance_after WHERE wallet_id = v_wallet_id;

        INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after)
        VALUES (v_user_id, user_phone, v_wallet_id, amount, v_fees, 'Withdrawal', service_name, v_balance_before, v_balance_after);
    END IF;
END;
$$;
-- example: call withdraw_money('01126008231', 800, 'ATM')




-- send money
CREATE OR REPLACE PROCEDURE send_money(sender_phone VARCHAR, receiver_phone VARCHAR, amount DECIMAL)
LANGUAGE plpgsql
AS 
$$
DECLARE
    sender_id INT;
    receiver_id INT;
    sender_wallet_id INT;
    receiver_wallet_id INT;
    sender_balance_before DECIMAL;
    sender_balance_after DECIMAL;
    receiver_balance_before DECIMAL;
    receiver_balance_after DECIMAL;
    fees DECIMAL := 0;
BEGIN
    -- Get sender details
    SELECT user_id INTO sender_id FROM Users WHERE phone_number = sender_phone;
    SELECT wallet_id, balance INTO sender_wallet_id, sender_balance_before FROM Wallet WHERE user_id = sender_id;

    -- Check if receiver exists in the database
    SELECT user_id INTO receiver_id FROM Users WHERE phone_number = receiver_phone;

    IF receiver_id IS NULL THEN
        -- Non-application user: add fees
        fees := amount * 0.01;
        sender_balance_after := sender_balance_before - (amount + fees);

        -- Transaction for sender only
        INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after)
        VALUES (sender_id, receiver_phone, sender_wallet_id, amount, fees, 'Transaction', 'Non Subscribed User', sender_balance_before, sender_balance_after);
    ELSE
        -- Application user: no fees
        SELECT wallet_id, balance INTO receiver_wallet_id, receiver_balance_before FROM Wallet WHERE user_id = receiver_id;

        sender_balance_after := sender_balance_before - amount;
        receiver_balance_after := receiver_balance_before + amount;

        -- Transaction for sender
        INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after)
        VALUES (sender_id, receiver_phone, sender_wallet_id, amount, 0, 'Transaction', 'GoCash User', sender_balance_before, sender_balance_after);

        -- Transaction for receiver
        INSERT INTO Transaction (sender_id, receiver, user_wallet_id, amount, fees, service_type, service_name, balance_before, balance_after)
        VALUES (sender_id, receiver_phone, receiver_wallet_id, amount, 0, 'Transaction', 'GoCash User', receiver_balance_before, receiver_balance_after);
    END IF;

    -- Update balances
    UPDATE Wallet SET balance = sender_balance_after WHERE wallet_id = sender_wallet_id;
    IF receiver_id IS NOT NULL THEN
        UPDATE Wallet SET balance = receiver_balance_after WHERE wallet_id = receiver_wallet_id;
    END IF;
END;
$$;
-- example: call send_money('01126008231', '01143874955', 500)




