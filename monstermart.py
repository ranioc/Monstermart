import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

st.header('Analisis Gross Profit Vending Machine Monstermart Periode Februari 2024')
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

st.subheader("Daily Trend of General Gross Profit and Quantity Sold")

def plot_trend(profit_trend):
    # Membuat plot untuk quantity sold
    qty_sold_plot = alt.Chart(profit_trend).mark_line(color='orange').encode(
        x='Day:T',
        y=alt.Y('Qty Sold:Q', title='Quantity Sold', axis=alt.Axis(grid=False)),  # Menghilangkan garis grid
        tooltip=['Day:T', 'Qty Sold:Q']
    )

    # Membuat plot untuk gross profit
    gross_profit_plot = alt.Chart(profit_trend).mark_bar(color='lightblue', opacity=0.7).encode(
        x='Day:T',
        y=alt.Y('Gross Profit:Q', title='Gross Profit (IDR)', axis=alt.Axis(grid=False)),  # Menghilangkan garis grid
        tooltip=['Day:T', 'Gross Profit:Q']
    )

    # Menggabungkan kedua plot
    combined_plot = alt.layer(
        qty_sold_plot,
        gross_profit_plot
    ).resolve_scale(
        y='independent'
    )

    # Menampilkan plot di Streamlit
    st.altair_chart(combined_plot, use_container_width=True)

# Memanggil fungsi plot_trend dengan DataFrame profit_trend
plot_trend(profit_trend)

st.write(f'<div style="text-align: justify">Trend profit dan quantity produk terjual per harinya menunjukkan penjualan yang fluktuatif dan cenderung rendah pada hari minggu. Hal ini kemungkinan menandakan penjualan vending machine di area perkantoran dan sekolah yang sepi karena hari libur.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

##########################################################################

st.subheader("Top 15 Machines By Sales February 2024")

# Mengurutkan data berdasarkan profit secara descending
sorted_profit_by_machine = profit_by_machine.sort_values(by='Sales', ascending=False)

# Mengambil top 15 mesin dengan penjualan tertinggi
top_15_machines = sorted_profit_by_machine.head(15)

# Membuat visualisasi dengan Altair
bar_chart_top = alt.Chart(top_15_machines).mark_bar(color='skyblue').encode(
    y=alt.Y('Machines:N', title='Machines', sort=None),  # Tidak mengurutkan label sumbu y
    x=alt.X('Sales:Q', title='Sales (IDR)', axis=alt.Axis(format=',.0f')),  # Format sumbu x sebagai rupiah
    tooltip=['Machines:N', 'Sales:Q']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,  # Ukuran font label sumbu
    titleFontSize=12  # Ukuran font judul sumbu
)

# Menampilkan plot di Streamlit
st.altair_chart(bar_chart_top, use_container_width=True)

st.write(f'<div style="text-align: justify">Kelima belas vending machine berikut merupakan vending machine dengan jumlah penjualan tertinggi dan merupakan penghasil profit terbanyak pada periode Februari 2024.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

####################################################################################

st.subheader("Bottom 15 Machines By Sales February 2024")

# Mengambil bottom 15 mesin dengan penjualan terendah
bottom_15_machines = sorted_profit_by_machine.tail(15)

# Membuat visualisasi dengan Altair
bar_chart_bottom = alt.Chart(bottom_15_machines).mark_bar(color='salmon').encode(
    y=alt.Y('Machines:N', title='Machines', sort=None),  # Tidak mengurutkan label sumbu y
    x=alt.X('Sales:Q', title='Sales (IDR)', axis=alt.Axis(format=',.0f')),  # Format sumbu x sebagai rupiah
    tooltip=['Machines:N', 'Sales:Q']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,  # Ukuran font label sumbu
    titleFontSize=12  # Ukuran font judul sumbu
)

# Menampilkan plot di Streamlit
st.altair_chart(bar_chart_bottom, use_container_width=True)

st.write(f'<div style="text-align: justify">Kelima belas vending machine berikut adalah yang penjualannya terendah dalam waktu 1 bulan pada periode Februari 2024 dan memungkinkan menjadi penyebab kerugian, jika biaya operasional untuk vending machine pada daftar tersebut per bulannya lebih tinggi daripada penjualannya.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

##################################################################################################

st.subheader("Top 15 Machines By Quantity Sold February 2024")

# Mengurutkan data berdasarkan jumlah terjual secara descending
sorted_profit_by_machine = profit_by_machine.sort_values(by='Qty Sold', ascending=False)

# Mengambil 15 mesin dengan jumlah terjual tertinggi
top_15_machines_qty_sold = sorted_profit_by_machine.head(15)

# Membuat visualisasi dengan Altair untuk top 15 machines by quantity sold
bar_chart_top_qty_sold = alt.Chart(top_15_machines_qty_sold).mark_bar(color='skyblue').encode(
    y=alt.Y('Machines:N', title='Machines', sort=None),  # Tidak mengurutkan label sumbu y
    x=alt.X('Qty Sold:Q', title='Quantity Sold'),
    tooltip=['Machines:N', 'Qty Sold:Q']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,  # Ukuran font label sumbu
    titleFontSize=12  # Ukuran font judul sumbu
)

# Menampilkan plot di Streamlit
st.altair_chart(bar_chart_top_qty_sold, use_container_width=True)

st.write(f'<div style="text-align: justify">Grafik di atas menandakan bahwa beberapa vending machine dengan penjualan tertinggi juga merupakan yang tertinggi dalam kuantitas terjual.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

##################################################################################################

st.subheader("Bottom 15 Machines By Quantity Sold February 2024")

# Mengambil 15 mesin dengan jumlah terjual terendah
bottom_15_machines_qty_sold = sorted_profit_by_machine.tail(15)

# Membuat visualisasi dengan Altair untuk bottom 15 machines by quantity sold
bar_chart_bottom_qty_sold = alt.Chart(bottom_15_machines_qty_sold).mark_bar(color='salmon').encode(
    y=alt.Y('Machines:N', title='Machines', sort=None),  # Tidak mengurutkan label sumbu y
    x=alt.X('Qty Sold:Q', title='Quantity Sold'),
    tooltip=['Machines:N', 'Qty Sold:Q']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,  # Ukuran font label sumbu
    titleFontSize=12  # Ukuran font judul sumbu
)

# Menampilkan plot di Streamlit
st.altair_chart(bar_chart_bottom_qty_sold, use_container_width=True)

st.write(f'<div style="text-align: justify">Grafik di atas menunjukkan 15 vending machine dengan kuantitas produk terjual paling sedikit dan berpotensi menjadi sumber kerugian, jika harus terus me-mantain biaya operasional dengan penjualan yang tidak banyak.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

##################################################################################################

st.subheader("Top 10 Products by Gross Profit February 2024")

# Mengurutkan data berdasarkan profit secara descending
sorted_df = profit_by_product.sort_values(by='Gross Profit', ascending=False)

# Mengambil 10 produk dengan profit tertinggi
top_10_products = sorted_df.head(10)

# Membuat visualisasi dengan Altair untuk top 10 products by gross profit
bar_chart_top_products = alt.Chart(top_10_products).mark_bar(color='skyblue').encode(
    y=alt.Y('Product:N', title='Product', sort=None),  # Tidak mengurutkan label sumbu y
    x=alt.X('Gross Profit:Q', title='Gross Profit'),
    tooltip=['Product:N', 'Gross Profit:Q']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,  # Ukuran font label sumbu
    titleFontSize=12  # Ukuran font judul sumbu
)

# Menampilkan plot di Streamlit
st.altair_chart(bar_chart_top_products, use_container_width=True)

st.write(f'<div style="text-align: justify">Air mineral merk Le Minerale 600ML merupakan produk yang menyumbang gross profit terbesar pada periode Februari 2024.</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

##################################################################################################

st.subheader("Bottom 10 Products by Gross Profit February 2024")

# Mengambil 10 produk dengan profit terendah
bottom_10_products = sorted_df.tail(10)

# Membuat visualisasi dengan Altair untuk bottom 10 products by gross profit
bar_chart_bottom_products = alt.Chart(bottom_10_products).mark_bar(color='salmon').encode(
    y=alt.Y('Product:N', title='Product', sort=None),  # Tidak mengurutkan label sumbu y
    x=alt.X('Gross Profit:Q', title='Gross Profit'),
    tooltip=['Product:N', 'Gross Profit:Q']
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,  # Ukuran font label sumbu
    titleFontSize=12  # Ukuran font judul sumbu
)

# Menampilkan plot di Streamlit
st.altair_chart(bar_chart_bottom_products, use_container_width=True)

st.write(f'<div style="text-align: justify">Berdasarkan grafik tersebut, ditemukan bahwa beberapa produk hanya menghasilkan gross profit yang sangat sedikit dalam penjualan satu bulan. Bahkan, produk YOUVIT Multivitamin dijual lebih murah dari harga modal produk karena tidak laku di pasaran, sehingga terdapat kerugian sebesar dua ribu rupiah.</div>', unsafe_allow_html=True)
