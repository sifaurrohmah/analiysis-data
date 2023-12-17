import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

sns.set(style='dark')

data = pd.read_csv("https://raw.githubusercontent.com/sifaurrohmah/analiysis-data/main/all_data3.csv")
data['dateday'] = pd.to_datetime(data['dateday'])

#satu
def create_cuaca_df(df):
    cuaca_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    cuaca_df= cuaca_df.reset_index()
    cuaca_df.rename(columns={
        "count": "totalpengguna",
        "casual": "casualpengguna",
        "registered": "registeredpengguna"
    }, inplace=True)
    
    cuaca_df = pd.melt(cuaca_df,
                        id_vars=['season'],
                        value_vars=['casualpengguna', 'registeredpengguna'],
                        var_name='type_of_pengguna',
                        value_name='count_pengguna')
    
    cuaca_df['season'] = pd.Categorical(cuaca_df['season'],
                        categories=['Fall', 'Winter','Spring', 'Summer'])
    
    cuaca_df = cuaca_df.sort_values('season')
    
    return cuaca_df

#dua
def create_user(df):
    user = df.resample(rule='M', on='dateday').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    user.index = user.index.strftime('%b-%y')
    user = user.reset_index()
    user.rename(columns={
        "dateday": "yearmonth",
        "count": "totalpengguna",
        "casual": "casualpengguna",
        "registered": "registeredpengguna"
    }, inplace=True)
    
    return user

#tiga
def create_minggu_df(df):
    minggu_df = df.groupby("hour").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    }) 
    minggu_df = minggu_df.reset_index()
    minggu_df.rename(columns={
        "count": "totalpengguna",
        "casual": "casualpengguna",
        "registered": "registeredpengguna"
    }, inplace=True)
    
    return minggu_df

#empat

def create_data_weekday(df):
    data_weekday = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    data_weekday = data_weekday.reset_index()
    data_weekday.rename(columns={
        "count": "totalpengguna",
        "casual": "casualpengguna",
        "registered": "registeredpengguna"
    }, inplace=True)
    
    data_weekday = pd.melt(data_weekday,
                            id_vars=['weekday'],
                            value_vars=['casualpengguna', 'registeredpengguna'],
                            var_name='type_of_pengguna',
                            value_name='count_pengguna')
    
    data_weekday['weekday'] = pd.Categorical(data_weekday['weekday'],
                            categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    data_weekday = data_weekday.sort_values('weekday')
    
    return data_weekday



# Membuat komponen filter

min_date = data["dateday"].min()
max_date = data["dateday"].max()

# Sidebar
with st.sidebar:
    # menambahkan image
    st.image("https://raw.githubusercontent.com/sifaurrohmah/analiysis-data/main/bike.jpg"
                , width=100)

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# hubungkan filter dengan main

main_df = data[
    (data["dateday"] >= str(start_date)) &
    (data["dateday"] <= str(end_date))
]

#menyiapkan dataframe
cuaca_df = create_cuaca_df(main_df)
user = create_user(main_df)
minggu_df = create_minggu_df(main_df)
data_weekday = create_data_weekday(main_df)

#membuat Judul
st.header("Bike Sharing Dasboard :) ")

st.subheader('Daily Bike')

col1, col2, col3 = st.columns(3)
with col1:
    totalpengguna = main_df['count'].sum()
    st.metric("Total Pengguna", value=totalpengguna)
with col2:
    casualpengguna = main_df['casual'].sum()
    st.metric("Total Pengguna Sepeda Biasa ", value=casualpengguna)
with col3:
    registeredpengguna = main_df['registered'].sum()
    st.metric("Total Pengguna Sepeda terdaftar ", value=registeredpengguna)

#.....................Membuat Chart..................
st.subheader('Penggunaan Sepeda dari tahun 2011-2012')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=user,
    x="yearmonth",
    y="totalpengguna",
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

fig1 = px.bar(cuaca_df,
        x='season',
        y=['count_pengguna'],
        color='type_of_pengguna',
        color_discrete_sequence=["skyblue", "green", "red"],
        title='Penggunaan Sepeda Berdasarkan Cuaca').update_layout(xaxis_title='', yaxis_title='Total Pengguna')
st.plotly_chart(fig1, use_container_width=True)


