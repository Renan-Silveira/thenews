def clean_a(df):
    import pandas as pd
    for coluna in df.select_dtypes(include="str").columns:
        df[coluna] = df[coluna].str.upper() #colocando as colunas texto em maiúscula
        df[coluna] = df[coluna].str.rstrip() #removendo espaços em branco na direita
        df[coluna] = df[coluna].str.lstrip() #removendo espaços em branco na esquerda
        df = df.drop_duplicates(subset='session_id', keep='first')
    return df