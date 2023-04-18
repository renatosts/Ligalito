import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def define_color(val):
    if val < 0:
        color = 'red'
    elif val > 0:
        color = 'green'
    else:
        color = 'gray'
    return 'color: %s' % color


st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon='app.jpg',
    page_title='Ligalito')

#@st.cache(persist=True)
def getFile(f):
    return pd.read_csv(f, sep=';', thousands='.', decimal=',', encoding='Latin-1')


f = 'https://raw.githubusercontent.com/renatosts/Ligalito/master/cartola.csv'
#f = 'cartola.csv'

cart = getFile(f)
cart = cart.sort_values(['cart_nome', 'cart_rodada'])

cart['cart_acum'] = round(cart.groupby(['cart_nome'])['cart_pontos'].cumsum(), 2)

df = cart[cart.cart_rodada > 0].pivot(values='cart_pontos', index='cart_nome', columns='cart_rodada')
df = df.rename(columns={'cart_rodada': 'index'})

df['Total'] = df.sum(axis=1)
df = df.sort_values(['Total', 'cart_nome'], ascending=[False, True])
df_aux = df

df_aux = df_aux.style.format(thousands=".",
                             decimal = ",",
                             precision=2)
st.dataframe(df_aux)


fig1 = go.Figure()

fig2 = go.Figure()

for nome in cart.cart_nome.drop_duplicates():
    df = cart[cart.cart_nome == nome]


    fig1.add_trace(
        go.Scatter(x=df.cart_rodada, y=df.cart_acum, name=nome))

    fig2.add_trace(
        go.Scatter(x=df.cart_rodada, y=df.cart_patr, name=nome))

fig1.update_layout(title='Pontos')
fig2.update_layout(title='Patrimônio')

fig1.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1))

fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1))

fig1.update_xaxes(scaleratio = 1)
fig2.update_xaxes(scaleratio = 1)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
