import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# =========================
# DASHBOARD HEADER
# =========================
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("---")

# =========================
# LOAD DATASET
# =========================
data_file = "main_data.csv"

# Coba baca file dengan delimiter otomatis
try:
    df = pd.read_csv(data_file, sep=None, engine="python")
    st.write("✅ Dataset berhasil dimuat!")
except FileNotFoundError:
    st.error("❌ Dataset tidak ditemukan. Pastikan file `main_data.csv` tersedia.")
    st.stop()
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat membaca CSV: {e}")
    st.stop()

# Debugging: tampilkan nama kolom yang terbaca
st.write("📌 **Kolom dalam dataset:**", list(df.columns))

# Cek apakah nama kolom sesuai
expected_columns = [
    "instant", "dteday", "season", "yr", "mnth", "holiday", "weekday", "workingday", 
    "weathersit", "temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"
]

if not all(col in df.columns for col in expected_columns):
    st.error("❌ Nama kolom dalam dataset tidak sesuai. Cek kembali format CSV.")
    st.stop()

# Ubah format tanggal
df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')

# =========================
# MAPPING NAMA HARI & CUACA
# =========================
weekday_mapping = {
    0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat",
    5: "Sabtu", 6: "Minggu"
}
df["weekday"] = df["weekday"].map(weekday_mapping)

weather_mapping = {
    1: "Cerah 🌞",
    2: "Mendung ☁️",
    3: "Hujan Ringan 🌧️",
    4: "Hujan Lebat ⛈️"
}
df["weathersit"] = df["weathersit"].map(weather_mapping)

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("📅 Filter Rentang Tanggal:")
min_date, max_date = df["dteday"].min(), df["dteday"].max()
start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

# Pastikan nilai tanggal valid
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

st.sidebar.write(f"📆 **Tanggal dipilih:** {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")

filtered_df = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", value=filtered_df['cnt'].sum())
col2.metric("Penyewaan Weekday", value=filtered_df[filtered_df['weekday'].isin(["Senin", "Selasa", "Rabu", "Kamis", "Jumat"])]["cnt"].sum())
col3.metric("Penyewaan Weekend", value=filtered_df[filtered_df['weekday'].isin(["Sabtu", "Minggu"])]["cnt"].sum())
st.markdown("---")

# =========================
# VISUALIZATION
# =========================

# 1️⃣ **Penyewaan sepeda berdasarkan hari dalam seminggu**
weekday_rentals = filtered_df.groupby("weekday")["cnt"].mean().reset_index()
fig_weekday = px.bar(
    weekday_rentals, x='weekday', y='cnt',
    title="📊 Rata-rata Penyewaan Sepeda per Hari dalam Seminggu",
    text_auto=True, color_discrete_sequence=['#007bff']
)
fig_weekday.update_layout(xaxis_title="Hari", yaxis_title="Rata-rata Penyewaan")
st.plotly_chart(fig_weekday, use_container_width=True)

# 2️⃣ **Penyewaan sepeda berdasarkan bulan**
monthly_rentals = filtered_df.groupby("mnth")["cnt"].mean().reset_index()
fig_monthly = px.line(
    monthly_rentals, x='mnth', y='cnt', markers=True,
    title="📆 Rata-rata Penyewaan Sepeda per Bulan",
    color_discrete_sequence=['#28a745']
)
fig_monthly.update_layout(xaxis_title="Bulan", yaxis_title="Rata-rata Penyewaan")
st.plotly_chart(fig_monthly, use_container_width=True)

# 3️⃣ **Pengaruh cuaca terhadap penyewaan sepeda**
weather_rentals = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()
fig_weather = px.bar(
    weather_rentals, x='weathersit', y='cnt',
    title="🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda",
    text_auto=True, color_discrete_sequence=['#dc3545']
)
fig_weather.update_layout(xaxis_title="Cuaca", yaxis_title="Rata-rata Penyewaan")
st.plotly_chart(fig_weather, use_container_width=True)

st.markdown("---")
st.subheader("📌 Kesimpulan:")
st.markdown(
    "- 🚴 **Penyewaan lebih tinggi pada weekday dibandingkan weekend.**\n"
    "- 📈 **Jumlah penyewaan meningkat di pertengahan tahun dan menurun menjelang akhir tahun.**\n"
    "- 🌤️ **Cuaca cerah meningkatkan jumlah penyewaan sepeda.**"
)
