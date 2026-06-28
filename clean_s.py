def clean_s(df):
    import pandas as pd
    df['result'] = df['result'].fillna("N/I") # N/I | Não Informado
    for coluna in df.select_dtypes(include="str").columns:
        df[coluna] = df[coluna].str.upper() #colocando as colunas texto em maiúscula
        df[coluna] = df[coluna].str.rstrip() #removendo espaços em branco na direita
        df[coluna] = df[coluna].str.lstrip() #removendo espaços em branco na esquerda
    return df