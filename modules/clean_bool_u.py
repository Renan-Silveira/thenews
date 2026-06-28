def clean_bool_u(df):
    import pandas as pd
    colunas_booleanas = [
        'plays_other_word_games',
        'newsletter_subscriber',
        'orders_food_delivery'
    ]
    validos = ['True', 'False']

    for coluna in colunas_booleanas:
        invalidos = df.loc[~df[coluna].isin(validos), coluna]

        if not invalidos.empty:
            print(f'\nColuna: {coluna}')
            print(invalidos.value_counts(dropna=False))