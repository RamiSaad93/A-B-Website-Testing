def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df