import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def define_color(val):
    if val < 0:
        color = 'red'
    elif val > 0:
        color = 'green'
    else:
        color = 'gray'
    return 'color: %s' % color

def set_color_patrim(val):
    return 'color: %s' % 'olive'


def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: green' if v else '' for v in is_max]

def highlight_min(s):
    is_min = s == s.min()
    return ['background-color: red' if v else '' for v in is_min]


@st.cache_data
def getFile(f):
    return pd.read_csv(f, sep=';', thousands='.', decimal=',', encoding='Latin-1')

st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon='app.jpg',
    page_title='Ligalito')


f = 'https://raw.githubusercontent.com/renatosts/Ligalito/master/cartola.csv'
#f = 'cartola.csv'

cart = getFile(f)

cart = cart.sort_values(['cart_nome', 'cart_rodada'])

cart['cart_acum'] = round(cart.groupby(['cart_nome'])['cart_pontos'].cumsum(), 2)

ult_rodada = cart.cart_rodada.max()

patr = cart[cart.cart_rodada == ult_rodada][['cart_nome', 'cart_patr']]

df = cart[cart.cart_rodada != 0].pivot(values='cart_pontos', index='cart_nome', columns='cart_rodada').reset_index()

colunas = [i for i in range(1, ult_rodada + 1)]
colunas.sort(reverse=True)

df['Total'] = df[colunas].sum(axis=1)

df = df.sort_values(['Total', 'cart_nome'], ascending=[False, True])

df = df.merge(patr, on='cart_nome')

df = df[['cart_nome', 'Total', 'cart_patr'] + colunas]

df.columns = ['Nome', 'Total', 'Patrim'] + [str(i) for i in colunas]

df = df.set_index('Nome')

df_aux = df

df_aux = df_aux.style.format(thousands='.',
                             decimal = ',',
                             precision=2,
                            ).map(define_color, subset=['Total']).map(set_color_patrim, subset=['Patrim']).apply(highlight_max, subset=[str(i) for i in colunas]).apply(highlight_min, subset=[str(i) for i in colunas])

st.dataframe(df_aux)


fig1 = go.Figure()

fig2 = go.Figure()

for nome in cart.cart_nome.drop_duplicates():

    df = cart[cart.cart_nome == nome].tail(10)

    fig1.add_trace(
        go.Scatter(x=df.cart_rodada, y=df.cart_acum, name=nome))

    fig2.add_trace(
        go.Scatter(x=df.cart_rodada, y=df.cart_patr, name=nome))

fig1.update_layout(title='Pontuação')
fig2.update_layout(title='Patrimônio')

fig1.update_layout(legend=dict(
    orientation='h',
    yanchor='bottom',
    y=1.02,
    xanchor='right',
    x=1))

fig2.update_layout(legend=dict(
    orientation='h',
    yanchor='bottom',
    y=1.02,
    xanchor='right',
    x=1))

fig1.update_xaxes(scaleratio = 1)
fig2.update_xaxes(scaleratio = 1)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

for nome in cart.cart_nome.drop_duplicates():
    df = cart[(cart.cart_nome == nome) & (cart.cart_rodada != 0)]

    media = df.cart_pontos.mean()

    fig = go.Figure()
    fig.update_layout(title=f'{nome} (Média: {media:.2f})')
    fig.add_trace(go.Bar(x=df.cart_rodada, y=df.cart_pontos, name=nome))
    fig.add_hline(y=media, line_width=3, line_color='red', name='Media')
    st.plotly_chart(fig, use_container_width=True)
