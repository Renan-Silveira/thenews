def df_info(df): #função que retorna algumas informações sobre o dataframe
    import pandas as pd
    describe = df.describe() #retorna uma descrição sobre o dataframe
    info = df.info() #retorna algumas métricas sobre o dataframe
    print(describe)
    print(info)