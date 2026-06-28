# Case | Analista de Dados
**the news | Palavritas**

---

## Sobre o desafio

O objetivo foi analisar o comportamento dos usuários no jogo **Palavritas**, uma funcionalidade gamificada do app, para entender:

> O que determina se um usuário volta a jogar e como aumentar o engajamento (retenção D1 e D30)?


---

## Objetivo

Investigar os principais fatores que influenciam:

- Retenção D1 (voltar no dia seguinte)
- Retenção D30 (usuário ativo no longo prazo)

E responder:

> O que diferencia usuários que continuam jogando daqueles que abandonam?

---

## 1. Limpeza e diagnóstico dos dados

### Problemas encontrados

- Inconsistência em colunas booleanas (`"True"`, `"FALSE"`, `"sim"`, `"não"`)
- Tipos incorretos (strings representando booleanos e datas)
- Valores ausentes em variáveis de perfil

### Tratamentos aplicados

- Padronização de booleanos para `True/False`
- Conversão de tipos (`datetime`, `int`, `category`)
- Remoção de registros inválidos ou incompletos
- Normalização de categorias (device, setor, etc.)

### Decisões importantes

- Realizei a limpeza dos dados para evitar problemas classificatórios
- Realizei o tratamento das colunas string para padronização
- Investiguei sobre os dados não categóricos

---

## 2. Análise exploratória

### Variáveis analisadas

- Horário do jogo  
- Palavra do dia  
- Perfil do usuário (setor, salário, device)  
- Frequência de food delivery  
- Relação com newsletter  
- Frequência de uso do app  

---

## Estrutura do projeto
```
│
├── modules/
│ ├── clean_a.py
│ ├── clean_bool_u.py
│ ├── clean_s.py
│ ├── clean_u.py
│ ├── df_info.py
│ ├── scrapper.py
├── main.ipynb
```

---

## Ferramentas utilizadas

- Python (Pandas, NumPy, Seaborn)   
- Jupyter Notebook  
- Google Sheets  

---

## Conclusão

Este projeto responde à pergunta central de produto e growth:

> Como transformar um jogo diário em um hábito contínuo de longo prazo?
