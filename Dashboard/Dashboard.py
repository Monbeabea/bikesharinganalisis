import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# DASHBOARD HEADER
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("---")

# LOAD DATASET
data_file = "main_data.csv"

try:
    df = pd.read_csv(data_file, delimiter=";")  # Update delimiter sesuai CSV
except FileNotFoundError:
    st.error("Dataset tidak ditemukan. Pastikan file tersedia.")
    st.stop()

# Cek apakah nama kolom sesuai
expected_columns = [
    "instant", "dteday", "season", "yr", "mnth", "holiday", "weekday", "workingday", 
    "weathersit", "temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"
]

if list(df.columns) != expected_columns:
    st.error("Nama kolom tidak sesuai. Cek kembali format CSV.")
    st.stop()

# Ubah format tanggal
df['dteday'] = pd.to_datetime(df['dteday'], format="%d/%m/%Y")

# SIDEBAR FILTER
st.sidebar.header("Filter Rentang Tanggal:")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", [df["dteday"].min(), df["dteday"].max()], 
    min_value=df["dteday"].min(), 
    max_value=df["dteday"].max()
)

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", value=filtered_df['cnt'].sum())
col2.metric("Total Penyewaan Weekday", value=filtered_df[filtered_df['weekday'] < 5]['cnt'].sum())
col3.metric("Total Penyewaan Weekend", value=filtered_df[filtered_df['weekday'] >= 5]['cnt'].sum())
st.markdown("---")

# VISUALIZATION
# Penyewaan sepeda berdasarkan hari dalam seminggu
weekday_rentals = filtered_df.groupby("weekday")["cnt"].mean().reset_index()
fig_weekday = px.bar(
    weekday_rentals, x='weekday', y='cnt',
    title="Rata-rata Penyewaan Sepeda per Hari dalam Seminggu",
    color_discrete_sequence=['blue']
)
fig_weekday.update_layout(xaxis_title='Hari', yaxis_title='Rata-rata Penyewaan')
st.plotly_chart(fig_weekday, use_container_width=True)

# Penyewaan sepeda berdasarkan bulan
monthly_rentals = filtered_df.groupby("mnth")["cnt"].mean().reset_index()
fig_monthly = px.line(
    monthly_rentals, x='mnth', y='cnt', markers=True,
    title="Rata-rata Penyewaan Sepeda per Bulan",
    color_discrete_sequence=['green']
)
fig_monthly.update_layout(xaxis_title='Bulan", yaxis_title="Rata-rata Penyewaan')
st.plotly_chart(fig_monthly, use_container_width=True)

# Pengaruh cuaca terhadap penyewaan sepeda
weather_rentals = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()
fig_weather = px.bar(
    weather_rentals, x='weathersit', y='cnt',
    title="Pengaruh Cuaca terhadap Penyewaan Sepeda",
    color_discrete_sequence=['red']
)
fig_weather.update_layout(xaxis_title='Cuaca', yaxis_title='Rata-rata Penyewaan')
st.plotly_chart(fig_weather, use_container_width=True)

st.markdown("---")
st.subheader("Kesimpulan:")
st.markdown(
    "1️⃣ **Penyewaan lebih tinggi pada weekday dibandingkan weekend.**\n"
    "2️⃣ **Jumlah penyewaan meningkat di pertengahan tahun dan menurun menjelang akhir tahun.**\n"
    "3️⃣ **Cuaca yang lebih cerah berkontribusi pada peningkatan jumlah penyewaan sepeda.**"
)
