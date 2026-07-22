-- merging upstream events into the silver customer dimension
-- handling scd type 2 so we don't lose the old status history

MERGE INTO silver.dim_customers target
USING bronze.customer_events source
ON target.cust_id = source.cust_id 
AND target.is_active = true

-- close out the old record if status changed
WHEN MATCHED AND target.status != source.status THEN
  UPDATE SET 
    target.is_active = false,
    target.end_date = source.event_timestamp

-- insert the new version
-- databricks needs a separate insert statement to handle the new row for scd2
WHEN NOT MATCHED THEN
  INSERT (
    cust_id, 
    status, 
    start_date, 
    end_date, 
    is_active
  )
  VALUES (
    source.cust_id,
    source.status,
    source.event_timestamp,
    '9999-12-31', -- default future date for active records
    true
  );
