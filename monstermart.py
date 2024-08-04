import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Analisis Gross Profit Vending Machine Monstermart Periode Februari 2024')

st.markdown("<br>", unsafe_allow_html=True)

profit_trend = pd.read_csv("Profit Trend Feb.csv")
profit_by_product = pd.read_csv("Profit By Product Feb.csv")
profit_by_machine = pd.read_csv("Revenue By Machine Feb.csv")

total_sales_revenue = profit_by_product['Sales Revenue'].sum()
total_gross_profit = profit_by_product['Gross Profit'].sum()
gross_profit_percentage = (total_gross_profit / total_sales_revenue) * 100

# Fungsi untuk mengonversi angka menjadi format rupiah
def format_rupiah(angka):
    formatted_angka = "Rp{:,.0f}".format(angka)
    return formatted_angka

# Fungsi untuk mengonversi angka menjadi persentase dengan 2 digit di belakang koma
def format_percentage(angka):
    formatted_angka = "{:.2f}%".format(angka)
    return formatted_angka

# Mengonversi nilai sales dan gross profit ke format rupiah
formatted_total_sales_revenue = format_rupiah(total_sales_revenue)
formatted_total_gross_profit = format_rupiah(total_gross_profit)

# Mengonversi gross profit percentage ke format persentase dengan 2 digit di belakang koma
formatted_gross_profit_percentage = format_percentage(gross_profit_percentage)

# # Menghitung total kerugian

# Menampilkan metric dengan nilai yang telah diformat

sales_feb, loss_feb = st.columns(2)

with sales_feb:
    st.metric("Total Sales", value=formatted_total_sales_revenue)

with loss_feb:
    st.metric("Total Loss", value="Rp1,658,821")

profit_feb, percentage_feb = st.columns(2)

with profit_feb:
    st.metric("Total Gross Profit", value=formatted_total_gross_profit)

with percentage_feb:
    st.metric("Gross Profit Percentage", value=formatted_gross_profit_percentage)

st.markdown("<br>", unsafe_allow_html=True)

#################################################################

def plot_trend(profit_trend):
    # Membuat plot untuk gross profit
    gross_profit_plot = alt.Chart(profit_trend).mark_bar(color='lightblue', opacity=0.7).encode(
        x='Day:T',
        y=alt.Y('Gross Profit:Q', title='Gross Profit (IDR)', axis=alt.Axis(grid=False)),  # Menghilangkan garis grid
        tooltip=['Day:T', 'Gross Profit:Q']
    )
    
    # Membuat plot untuk quantity sold
    qty_sold_plot = alt.Chart(profit_trend).mark_line(point=True, color='orange').encode(
        x='Day:T',
        y=alt.Y('Qty Sold:Q', title='Quantity Sold', axis=alt.Axis(grid=False)),  # Menghilangkan garis grid
        tooltip=['Day:T', 'Qty Sold:Q']
    )

    # Menggabungkan kedua plot
    combined_plot = alt.layer(
        gross_profit_plot,
        qty_sold_plot
    ).resolve_scale(
        y='independent'
    )
    
    # Menampilkan plot di Streamlit
    st.altair_chart(combined_plot, use_container_width=True)

# Memanggil fungsi plot_trend dengan DataFrame profit_trend
plot_trend(profit_trend)

st.write(f'<div style="text-align: justify">Trend profit dan quantity produk terjual per harinya menunjukkan penjualan yang fluktuatif.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)


##########################################################################

# Memastikan kolom 'Day' adalah tipe datetime
profit_trend['Day'] = pd.to_datetime(profit_trend['Day'])

# Menambahkan kolom hari dalam minggu
profit_trend['Day of Week'] = profit_trend['Day'].dt.dayofweek  # 0=Monday, 1=Tuesday, ..., 6=Sunday

# Menghitung selisih penjualan per hari
profit_trend['Sales Revenue Diff'] = profit_trend['Sales Revenue'].diff()

# Menghitung rata-rata selisih penjualan per hari dalam minggu
avg_diff_by_day = profit_trend.groupby('Day of Week')['Sales Revenue Diff'].mean()

# Set up the Streamlit app
st.subheader("Average Daily Sales Difference (Monday-Sunday)")

# Plotting the results
fig, ax = plt.subplots(figsize=(10, 6))
avg_diff_by_day.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Rata-Rata Selisih Penjualan Harian (Senin-Minggu)')
ax.set_xlabel('Hari dalam Minggu')
ax.set_ylabel('Rata-Rata Selisih Penjualan')
ax.set_xticks(range(7))
ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.tick_params(axis='x', rotation=0)
st.pyplot(fig)

st.write(f'<div style="text-align: justify">Rata-rata selisih penjualan setiap harinya terlihat turun paling besar pada hari Minggu dan naik paling drastis di hari Senin. Penjualan vending machine di area perkantoran dan sekolah kemungkinan sepi karena hari libur dan mulai ramai kembali pada hari kerja.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

##########################################################################

# Fungsi untuk membuat bar chart dengan persentase
def create_bar_chart(data, x_field, y_field, color, title, total_value, width=600, height=400):
    data[f'Percentage'] = (data[x_field] / total_value) * 100
    bar_chart = alt.Chart(data).mark_bar(color=color).encode(
        y=alt.Y(f'{y_field}:N', title=title, sort=None),
        x=alt.X(f'{x_field}:Q', title=f'{x_field} (IDR)', axis=alt.Axis(format=',.0f')),
        tooltip=[f'{y_field}:N', f'{x_field}:Q', alt.Tooltip('Percentage:Q', format='.2f', title='Percentage')]
    ).properties(
        width=width,
        height=height
    ).configure_axis(
        labelFontSize=10,
        titleFontSize=12
    )
    return bar_chart

st.subheader("Top 15 Machines By Sales February 2024")
sorted_profit_by_machine = profit_by_machine.sort_values(by='Sales', ascending=False)
top_15_machines = sorted_profit_by_machine.head(15)
bar_chart_top = create_bar_chart(top_15_machines, 'Sales', 'Machines', 'skyblue', 'Machines', total_sales_revenue)
st.altair_chart(bar_chart_top, use_container_width=True)
st.write('<div style="text-align: justify">Kelima belas vending machine berikut merupakan vending machine dengan jumlah penjualan tertinggi dan merupakan penghasil profit terbanyak pada periode Februari 2024.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("Bottom 15 Machines By Sales February 2024")
bottom_15_machines = sorted_profit_by_machine.tail(15)
bar_chart_bottom = create_bar_chart(bottom_15_machines, 'Sales', 'Machines', 'salmon', 'Machines', total_sales_revenue)
st.altair_chart(bar_chart_bottom, use_container_width=True)
st.write('<div style="text-align: justify">Kelima belas vending machine berikut adalah yang penjualannya terendah dalam waktu 1 bulan pada periode Februari 2024 dan memungkinkan menjadi penyebab kerugian, jika biaya operasional untuk vending machine pada daftar tersebut per bulannya lebih tinggi daripada penjualannya.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("Top 10 Products by Gross Profit February 2024")
sorted_df = profit_by_product.sort_values(by='Gross Profit', ascending=False)
top_10_products = sorted_df.head(10)
bar_chart_top_products = create_bar_chart(top_10_products, 'Gross Profit', 'Product', 'skyblue', 'Product', total_gross_profit)
st.altair_chart(bar_chart_top_products, use_container_width=True)
st.write('<div style="text-align: justify">Air mineral merk Le Minerale 600ML merupakan produk yang menyumbang gross profit terbesar pada periode Februari 2024.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("Bottom 10 Products by Gross Profit February 2024")
bottom_10_products = sorted_df.tail(10)
bar_chart_bottom_products = create_bar_chart(bottom_10_products, 'Gross Profit', 'Product', 'salmon', 'Product', total_gross_profit)
st.altair_chart(bar_chart_bottom_products, use_container_width=True)
st.write('<div style="text-align: justify">Berdasarkan grafik tersebut, ditemukan bahwa beberapa produk hanya menghasilkan gross profit yang sangat sedikit dalam penjualan satu bulan. Bahkan, produk YOUVIT Multivitamin dijual lebih murah dari harga modal produk karena tidak laku di pasaran, sehingga terdapat kerugian sebesar dua ribu rupiah.</div>', unsafe_allow_html=True)
