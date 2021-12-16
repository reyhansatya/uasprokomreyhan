import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


df = pd.read_csv('minyak bersih1.csv')

st.set_page_config(layout="wide")

header = st.container()
body = st.container()
side = st.container()

with header:
    st.title('Eksplorasi Data Produksi Minyak Dunia')
    st.markdown('Selamat datang di aplikasi Eksplorasi Data Produksi Minyak Dunia! Kalian dapat menggunakan fitur-fitur yang terdapat pada sidebar untuk mendapatkan insight terkait produksi minyak di dunia. Happy exploring!')

with side:

    st.sidebar.title("Fitur yang dapat digunakan")

    st.sidebar.subheader("1. Produksi minyak mentah per negara")
    list_negara = list(df['nama_negara'].unique())
    list_negara.sort()
    negara = st.sidebar.selectbox("Pilih negara", list_negara)

    st.sidebar.subheader("2. Negara dengan produksi terbesar per tahun")
    jml_negara2 = int(st.sidebar.number_input("Masukkan jumlah negara yang ingin ditampilkan", min_value=1, max_value=len(list_negara),value=10))
    tahun = int(st.sidebar.number_input("Pilih tahun produksi", min_value=1971, max_value=2015,value=2015))

    st.sidebar.subheader("3. Negara dengan produksi terbesar kumulatif")
    jml_negara3 = int(st.sidebar.number_input("Masukkan jumlah negara yang ingin ditampilkan", min_value=1, max_value=len(list_negara),value=10, key=1))

    st.sidebar.subheader("4. Ranking produksi minyak")
    tahun1 = int(st.sidebar.number_input("Pilih tahun produksi", min_value=1971, max_value=2015,value=2015, key=1))


with body:
    plt.style.use('bmh')

    # Fitur 1
    st.title("1) Produksi minyak mentah per negara")
    st.write(f"Visualisasi produksi minyak mentah untuk negara {negara}")
    fig, ax = plt.subplots()
    prod = df[df['nama_negara']==negara]['produksi']
    tahun_plot = df[df['nama_negara']==negara]['tahun']
    ax.plot(tahun_plot, prod)
    ax.set_title(f"Produksi minyak per tahun negara {negara}")
    ax.set_ylabel('Produksi Minyak')
    ax.set_xlabel("Tahun")
    fig.set_size_inches(10, 5, forward=True)   
    body.pyplot(fig)

    # Fitur 2
    st.title(f"2) {jml_negara2} negara dengan produksi minyak mentah terbesar pada tahun {tahun}")
    df3 = df[df['tahun']==tahun]
    df3 = df3.nlargest(jml_negara2, 'produksi')
    df3.sort_values('produksi',inplace=True)
    cmap_name = 'tab20c'
    cmap = cm.get_cmap(cmap_name)
    colors = cmap.colors[:jml_negara2]
    fig2, ax = plt.subplots()
    ax.barh(df3['nama_negara'],df3['produksi'], color=colors)
    ax.set_title(f'{jml_negara2} negara dengan produksi minyak mentah terbesar pada tahun {tahun}')
    ax.set_xlabel(f"Produksi Minyak pada tahun {tahun}")
    fig2.set_size_inches(10, 5, forward=True)   
    body.pyplot(fig2)

    # Fitur 3
    st.title(f"3) {jml_negara3} negara dengan produksi minyak mentah kumulatif terbesar")
    cumul = df.groupby('nama_negara')['produksi'].sum()
    cumul = cumul.nlargest(jml_negara3)
    cumul.sort_values(ascending=True, inplace=True)
    fig3, ax = plt.subplots()
    ax.barh(cumul.index,cumul, color=colors)
    body.pyplot(fig3)

    #Fitur 4
    st.title("4) Ranking produksi minyak")
    left_col, right_col = st.columns(2)

    produksi_kumul = df.groupby(['nama_negara','kode_negara','region','sub-region'])['produksi'].sum().reset_index(name ='produksi_kumulatif')
    ranking_kumul = produksi_kumul.nlargest(1,'produksi_kumulatif')
    produksi_kumul[produksi_kumul['produksi_kumulatif']>0].nsmallest(1,'produksi_kumulatif')
    ranking_kumul = ranking_kumul.append(produksi_kumul[produksi_kumul['produksi_kumulatif']>0].nsmallest(1,'produksi_kumulatif'))
    pd.options.display.float_format = '{:.3f}'.format
    ranking = ['Terbesar','Terkecil']
    ranking_kumul['Ranking'] = ranking
    index_order = ['Ranking','nama_negara','kode_negara','region','sub-region','produksi_kumulatif']
    ranking_kumul = ranking_kumul[index_order]
    renaming = {'Ranking':'Ranking',
                'nama_negara': 'Nama Negara',
                'kode_negara': 'Kode Negara',
                'region':'Region',
                'sub-region' : 'Sub Region',
                'produksi_kumulatif':'Produksi Kumulatif'}
    ranking_kumul = ranking_kumul.rename(columns=renaming)
    
    right_col.write("Negara dengan produksi minyak kumulatif terbesar dan terkecil")
    right_col.dataframe(ranking_kumul)

    produksi_nol = produksi_kumul[produksi_kumul['produksi_kumulatif']==0]
    produksi_nol = produksi_nol.drop(columns='produksi_kumulatif')
    index_order1 = ['nama_negara','kode_negara','region','sub-region']
    produksi_nol = produksi_nol[index_order1]
    renaming1 = {'nama_negara': 'Nama Negara',
                'kode_negara': 'Kode Negara',
                'region':'Region',
                'sub-region' : 'Sub Region',}
    produksi_nol = produksi_nol.rename(columns=renaming1)
    right_col.write("    ")
    right_col.write('Negara yang tidak memproduksi minyak pada tahun 1971-2015')
    right_col.dataframe(produksi_nol)


    produksi_tahun = df[df['tahun']==tahun1].drop(columns='alpha-3')
    rank_tahun = produksi_tahun.nlargest(1,'produksi')
    rank_tahun = rank_tahun.append(produksi_tahun[produksi_tahun['produksi']>0].nsmallest(1,'produksi'))
    rank_tahun['Ranking'] = ranking
    index_order2 = ['Ranking','nama_negara','kode_negara','region','sub-region','produksi']
    rank_tahun = rank_tahun[index_order2]
    renaming2 = {'Ranking':'Ranking',
                'nama_negara': 'Nama Negara',
                'kode_negara': 'Kode Negara',
                'region':'Region',
                'sub-region' : 'Sub Region',
                'produksi':'Produksi'}
    rank_tahun = rank_tahun.rename(columns=renaming2)

    left_col.write(f"Negara dengan produksi minyak kumulatif terbesar dan terkecil pada tahun {tahun1}")
    left_col.dataframe(rank_tahun)


    rank_nol = produksi_tahun[produksi_tahun['produksi']==0].drop(columns=['produksi'])
    rank_nol = rank_nol[index_order1]
    rank_nol = rank_nol.rename(columns=renaming)

    left_col.write("    ")
    left_col.write(f"Negara yang tidak memproduksi minyak pada tahun {tahun1}")
    left_col.dataframe(rank_nol)
