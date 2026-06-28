def clean_u(df):
    import pandas as pd
    df['city'] = df['city'].fillna("N/I") # N/I | Não Informado
    df['age_range'] = df['age_range'].fillna("N/I") # N/I | Não Informado
    df['salary_range'] = df['salary_range'].fillna("N/I") # N/I | Não Informado
    for coluna in df.select_dtypes(include="str").columns:
        df[coluna] = df[coluna].str.upper() #colocando as colunas texto em maiúscula
        df[coluna] = df[coluna].str.rstrip() #removendo espaços em branco na direita
        df[coluna] = df[coluna].str.lstrip() #removendo espaços em branco na esquerda
        
    df['orders_food_delivery'] = df['orders_food_delivery'].str.replace('SIM', 'True')
    df['orders_food_delivery'] = df['orders_food_delivery'].str.replace('NÃO', 'False')
    df['orders_food_delivery'] = df['orders_food_delivery'].str.replace('NAO', 'False')
    df['orders_food_delivery'] = df['orders_food_delivery'].str.replace('TRUE', 'True')
    df['orders_food_delivery'] = df['orders_food_delivery'].str.replace('FALSE', 'False')
    df['orders_food_delivery'] = df['orders_food_delivery'].astype(bool)

    df['plays_other_word_games'] = df['plays_other_word_games'].astype(bool)

    df['newsletter_subscriber'] = df['newsletter_subscriber'].astype(bool)
    return df