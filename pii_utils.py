import pyspark.sql.functions as F

def mask_pii_data(df, hash_columns=None, email_columns=None):
    """
    helper to mask sensitive columns before writing to the data lake.
    """
    if not hash_columns: hash_columns = []
    if not email_columns: email_columns = []
    
    res_df = df
    
    # security team requested sha256 for identifiers
    for col in hash_columns:
        if col in res_df.columns:
            res_df = res_df.withColumn(col, F.sha2(F.col(col).cast("string"), 256))
            
    # quick email redaction, leaves domain intact
    # example: test@gmail.com -> t***@gmail.com
    for col in email_columns:
        if col in res_df.columns:
            res_df = res_df.withColumn(
                col,
                F.when(
                    F.col(col).isNotNull(),
                    F.concat(
                        F.substring(F.col(col), 1, 1),
                        F.lit("***@"),
                        F.split(F.col(col), "@").getItem(1)
                    )
                ).otherwise(F.col(col))
            )
            
    return res_df
