import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="TheNews - Palavritas", layout="wide") #usando a tela toda no wide

@st.cache_data #usando o decorator para melhorar a performance com cache
def load_data(file_path):
    df = pd.read_parquet(file_path)
    
    # convertendo os booleanos
    bool_cols = [
        'played_next_day', 'active_d30', 'newsletter_open_before_game', 
        'orders_food_delivery', 'plays_other_word_games', 'newsletter_subscriber'
    ]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)
            
    # criando uma coluna para mapear se houve retorno ou não
    df['retornou_d1'] = df['played_next_day'].map({1: 'Retornou', 0: 'Não Retornou'})
    
    return df


df = load_data(os.path.join('data', 'df_cleaned.parquet'))

st.title("Palavritas: Análise Comportamental")
st.markdown("""
Este relatório apresenta a distribuição de todo o comportamento. 
O objetivo é responder **o que faz o usuário voltar no dia seguinte (D+1) e se manter ativo (D30)**, analisando o perfil, a rotina e o engajamento.
""")
st.divider()

# horários do jogo e atividade
st.header("1. Horário de Jogo e Relação Tempo Jogado")
col1, col2 = st.columns(2)


with col1:
    st.subheader("Distribuição de Sessões por Horário")
    
    fig_hour = px.histogram(
        df, 
        x="session_hour", 
        color="retornou_d1",
        barmode="group",
        histnorm='percent',
        nbins=24,
        title="Percentual de Sessões ao longo do dia",
        labels={'session_hour': 'Hora do Dia', 'retornou_d1': 'Retenção D+1', 'percent': 'Percentual'},
        color_discrete_sequence=['#EF553B', '#00CC96']
    )
    st.plotly_chart(fig_hour, use_container_width=True)

with col2:
    st.subheader("Tempo para Encontrar a Palavra vs Retenção")
    fig_box = px.box(
        df, 
        x="retornou_d1", 
        y="time_to_complete_sec", 
        color="retornou_d1",
        title="Tempo para Encontrar a Palavra por Grupo",
        labels={'time_to_complete_sec': 'Tempo para Finalizar', 'retornou_d1': 'Status'},
        color_discrete_sequence=['#EF553B', '#00CC96']
    )
    st.plotly_chart(fig_box, use_container_width=True)


st.info("""
**Insights:**
* Podemos observar que há pouca diferença entre quem retornou ou não em números, mas observamos que quem voltou, foi principalmente durante os primeiros dias do mês.
* Também podemos ver uma pequena diferença no tempo de jogo, mostrando que pessoas que retornam tem mais tempo de tela.
""")

st.divider()

st.header("2. Impacto do Perfil (Setor, Salário, Device) e Newsletter")
st.markdown("Abaixo vemos a **Taxa de Conversão** (probabilidade de retornar) para cada segmento específico.")

def plot_conversion_bar(
    df,
    feature,
    target_col='played_next_day',
    title="",
    y_label=None
):
    agg = df.groupby(feature)[target_col].agg(['mean', 'size']).reset_index()
    agg = agg.sort_values(by='mean', ascending=True)

    fig = px.bar(
        agg,
        y=feature,
        x='mean',
        orientation='h',
        text='mean',
        title=title,
        labels={
            'mean': 'Taxa de Retenção',
            feature: y_label if y_label else feature
        },
        color='mean',
        color_continuous_scale="Blues"
    )

    fig.update_traces(texttemplate='%{text:.1%}', textposition='auto')
    fig.update_layout(coloraxis_showscale=False)

    return fig

col3, col4, col5 = st.columns(3)

with col3:
    st.plotly_chart(plot_conversion_bar(df, 'salary_range', title="Retenção por Faixa Salarial", y_label='Salário'), use_container_width=True)
    st.plotly_chart(plot_conversion_bar(df, 'primary_device', title="Retenção por Device", y_label='Dispositivo'), use_container_width=True)

with col4:
    st.plotly_chart(plot_conversion_bar(df, 'sector', title="Retenção por Setor de Atuação", y_label='Atuação'), use_container_width=True)
    st.plotly_chart(plot_conversion_bar(df, 'age_range', title="Retenção por Faixa Etária", y_label='Faixa Etária'), use_container_width=True)

with col5:
    st.plotly_chart(plot_conversion_bar(df, 'newsletter_open_before_game', title="Abriu Newsletter Antes? (0=Não, 1=Sim)", y_label="Abre a newsletter antes de jogar?"), use_container_width=True)
    st.plotly_chart(plot_conversion_bar(df, 'typical_play_time', title="Período Típico de Jogo", y_label='Quando costuma jogar?'), use_container_width=True)

st.info("""
**Insights:**
* Agora podemos traçar um perfil de quem joga. Principalmente pessoas +45 anos, jogando a noite, principalmente em IOS e da área TECH.
* Um perfil bem específico comparando com os demais perfis mapeados.
""")

st.divider()

st.header("3. Dificuldade/Engajamento por 'Palavra do Dia'")
st.markdown("Quais palavras geram mais frustração (churn) ou mais engajamento (retenção)?")

col6, col7 = st.columns([2, 1])

with col6:
    
    word_stats = df.groupby('word').agg(
        Taxa_Retencao=('played_next_day', 'mean'),
        Tentativas_Medias=('attempt_number', 'mean'),
        Volume=('user_id', 'count')
    ).reset_index()
    
    fig_word = px.scatter(
        word_stats, 
        x="Tentativas_Medias", 
        y="Taxa_Retencao", 
        size="Volume", 
        color="Taxa_Retencao",
        hover_name="word",
        title="Palavra do Dia: Tentativas vs Retenção D+1",
        labels={'Tentativas_Medias': 'Média de Tentativas para Acertar', 'Taxa_Retencao': 'Taxa de Retorno (D+1)'},
        color_continuous_scale="RdYlGn"
    )
    fig_word.add_hline(y=word_stats['Taxa_Retencao'].mean(), line_dash="dot", annotation_text="Média Global de Retenção")
    st.plotly_chart(fig_word, use_container_width=True)

with col7:
    st.info("""
    **Como ler este gráfico:**
    * Bolhas no canto superior esquerdo: Palavras fáceis (poucas tentativas) que retêm muito.
    * Bolhas no canto inferior direito: Palavras difíceis que frustram e derrubam o engajamento no dia seguinte.
    * O tamanho da bolha é o volume de jogadas.
    """)

st.divider()


st.header("Insights")
taxa_geral = df['played_next_day'].mean()
taxa_newsletter = df.groupby('newsletter_open_before_game')['played_next_day'].mean()[1]
taxa_food_high = df[df['food_delivery_freq_week'] > df['food_delivery_freq_week'].median()]['played_next_day'].mean()


col_h1, col_h2 = st.columns(2)

with col_h1:
    st.markdown("##### 1. Hipótese de Engajamento por Newsletter")
    if taxa_newsletter > taxa_geral:
        st.success(f"**Confirmada!** Quem abre a Newsletter tem {taxa_newsletter:.1%} de retenção, contra {taxa_geral:.1%} da média.")
        st.write("Sugestão: Segmentar usuários de baixa retenção e disparar 'dicas' da palavra do dia antes do horário de jogo típico.")
    else:
        st.warning("**Inconclusiva.** A abertura da Newsletter não apresenta correlação positiva forte no momento.")
        st.write("Sugestão: Testar novo CTA no assunto do email (ex: 'Não erre a palavra de hoje!').")

with col_h2:
    st.markdown("##### 2. Hipótese de Perfil de 'Delivery' e Rotina")
    if taxa_food_high < taxa_geral:
        st.warning(f"**Observação:** Usuários com alta frequência de pedidos possuem retenção de {taxa_food_high:.1%}.")
        st.write("Sugestão: Vincular gamificação do Palavritas com cupons de parceiros de delivery para reforçar a associação entre o tempo de espera do pedido e o jogo.")
    else:
        st.write("Os dados atuais sugerem que o perfil de 'Food Delivery' não é o principal motor de retenção. Focar em outras variáveis de comportamento.")

col_h3, col_h4 = st.columns(2)

with col_h3:
    st.markdown("""
    ##### 1. Horário de jogo""")
    st.info("""
    - **Hipótese:** *Acredito que usuários que jogam no período da noite apresentam maior retenção porque esse horário faz parte de uma rotina diária mais consistente.*
    - **Ação:** Enviar notificações ou e-mails próximos ao horário habitual de jogo de cada usuário, priorizando quem costuma jogar à noite.
    - **Critério de sucesso:** *Saberei que funcionou quando a taxa de retorno em D+1 e a retenção em D30 aumentarem em relação ao grupo controle.*
    """)

with col_h4:
    st.markdown("""
    ##### 2. Palavra do dia""")
    st.info("""
    - **Hipótese:** *Acredito que palavras excessivamente difíceis reduzem a retenção porque aumentam a frustração do usuário durante a experiência.*
    - **Ação:** Balancear a dificuldade das palavras e testar dicas opcionais para os desafios mais difíceis.
    - **Critério de sucesso:** *Saberei que funcionou quando palavras classificadas como difíceis apresentarem aumento na taxa de retorno sem reduzir significativamente o desafio do jogo.*
    """)






