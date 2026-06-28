import pandas as pd
import requests
from clean_u import clean_u
from clean_s import clean_s
from clean_a import clean_a
from scrapper import scrapper
from df_info import df_info


pd.set_option('display.width', 1000)

palavritas_sessions = "https://docs.google.com/spreadsheets/d/104R-o0zIQz4PHkzsIaRajoL4WuGs2poTfTAGV55TPzU/export?format=csv&gid=16000988"
palavritas_attempts = "https://docs.google.com/spreadsheets/d/104R-o0zIQz4PHkzsIaRajoL4WuGs2poTfTAGV55TPzU/export?format=csv&gid=1923226155"
user_profile = "https://docs.google.com/spreadsheets/d/104R-o0zIQz4PHkzsIaRajoL4WuGs2poTfTAGV55TPzU/export?format=csv&gid=60060837"


df_s = scrapper(palavritas_sessions) #criando o dataframe de sessions
df_a = scrapper(palavritas_attempts) #criando o dataframe de attempts
df_u = scrapper(user_profile) #criando o dataframe de user

df_info(df_u) 
#df_info(df_u)



# Foi identificado que a coluna result tem alguns registros em branco. 
# Foi usada essa função para limpar os valores
df_s = clean_s(df_s) 


#Foi identificado pelo describe que todos 
df_u = clean_u(df_u)
df_info(df_u) 
print(df_u)