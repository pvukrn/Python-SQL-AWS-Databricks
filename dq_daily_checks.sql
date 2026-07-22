-- daily view to catch bad records before downstream pipelines pick them up.
-- acts as a simple dq gate.

CREATE OR REPLACE VIEW dq_checks.daily_anomalies AS
WITH flagged_data AS (
    SELECT 
        txn_id,
        acct_id,
        amount,
        txn_date,
        
        -- amount shouldn't be negative or null
        CASE WHEN amount IS NULL OR amount < 0 THEN 1 ELSE 0 END AS bad_amount_flag,
        
        -- missing account mapping
        CASE WHEN acct_id IS NULL THEN 1 ELSE 0 END AS missing_acct_flag,
        
        -- catch exact dupes on the same day
        ROW_NUMBER() OVER (
            PARTITION BY acct_id, amount, txn_date 
            ORDER BY txn_id
        ) AS dupe_row_num
        
    FROM raw_data.transactions
    WHERE txn_date >= current_date - interval '1' day
)

SELECT 
    txn_id,
    acct_id,
    bad_amount_flag,
    missing_acct_flag
FROM flagged_data
WHERE bad_amount_flag = 1 
   OR missing_acct_flag = 1 
   OR dupe_row_num > 1;
