def clean_s(df):
    import pandas as pd
    df['result'] = df['result'].fillna("N/I") # N/I | Não Informado
    for coluna in df.select_dtypes(include="str").columns:
        df[coluna] = df[coluna].str.upper() #colocando as colunas texto em maiúscula
        df[coluna] = df[coluna].str.rstrip() #removendo espaços em branco na direita
        df[coluna] = df[coluna].str.lstrip() #removendo espaços em branco na esquerda
    df['word_date'] = pd.to_datetime(df['word_date'], dayfirst=True, errors='coerce')
    df['played_next_day'] = df['played_next_day'].astype(bool)
    df['newsletter_open_before_game'] = df['newsletter_open_before_game'].astype(bool)
    df['active_d30'] = df['active_d30'].astype(bool)
    df = df.dropna()
    df = df.drop_duplicates(subset='session_id', keep='first')
    return df