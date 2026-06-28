def scrapper(link): #função para retornar o scrapper da página
    import pandas as pd
    url = link
    df = pd.read_csv(url)
    return df