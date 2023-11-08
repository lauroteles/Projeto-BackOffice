import pandas as pd
import streamlit as st
import openpyxl
import numpy as np
import plotly.graph_objects as pgo
import base64
from io import BytesIO
import io
#####################################
#Box para receber arquivos
df = None
daf = None


upload_file = st.sidebar.file_uploader(
                            label='Solte o arquivo de PL',
                            type=['xlsx'],
                            key='upload1'
                            )


if upload_file  is not None:
        
        print('hello')
        try:
            df = pd.read_excel(upload_file)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')

    ####    arquivo 2


upload_file2 = st.sidebar.file_uploader(
                            label='Solte o arquivo da planilha de Controle ',
                            type=['xlsx'],
                            key='upload2'
                            )

if upload_file2  is not None:
        print('hello')
        try:
            daf = pd.read_excel(upload_file2)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')
    
    ##### arquivo 3 
## Leitura dos arquivos
if df is not None and daf is not None:
    
    pl = df
    controle = daf

    controle    =   controle.iloc[:,[1,2,4,5,12,-1,7]]
    #controle["2023-10-31 00:00:00"] = pd.to_datetime(controle["2023-10-31 00:00:00"])
    '''
    controle = controle[[   
                                    'Nome',
                                        'Conta',
                                        'UF','Assessor',
                                        'Status',
                                        'Carteira',"2023-10-31 00:00:00"

    
    ]]
    '''
    pl['CONTA'] = pl['CONTA'].astype(str)
    pl['CONTA'] = list(map(
        lambda x: x[2:], pl['CONTA']
    ))
    pl = pl.rename(columns={
        'CONTA':'Conta'
    })

    controle['Conta'] = controle['Conta'].astype(str)
    controle['Conta'] = list(map(
        lambda x: x[:-2], controle['Conta']
    ))
    pl = pl.rename(columns={
        'VALOR':'PL',
        'NOME':'Nome do cliente pelo excel PL'
    })
    def juntar_arquivos(x,y):
        df = pd.merge(x,y, on='Conta', how='outer')
        return df


    arquivo_final = juntar_arquivos(controle,pl)
    arquivo_final = arquivo_final.loc[arquivo_final['Status']=='Ativo']
    arquivo_final = arquivo_final.drop(columns=['Nome do cliente pelo excel PL','Status'])
    print(arquivo_final.columns)

    filtro_pl_abaixo_100k = arquivo_final.loc[arquivo_final.PL<1000].reset_index(drop=True)
    filtro_income = arquivo_final.loc[
        (arquivo_final['Carteira']== 'INC') & (arquivo_final.PL<60000)].reset_index(drop=True)

    filtro_abaixo100k = arquivo_final.loc[
        (arquivo_final['Carteira']!='INC')&(arquivo_final['PL']<100000)].reset_index(drop=True)
    filtro_pl_0 = arquivo_final[arquivo_final.iloc[:,-2]<1].reset_index(drop=True)

    filtro_abaixo100k.to_excel('Testearquivo.xlsx')
    ##########################################
    #Juntando filtros



    ###########################################
    #Streamlit para visualização
    st.subheader('Contas com valor de PL abaixo de R$100.000,00')
    st.dataframe(filtro_abaixo100k)
    st.subheader('Contas Income com PL abaixo de R$60.000,00')
    st.dataframe(filtro_income)
    st.subheader('Contas com valor de PL abaixo de R$1000,00')
    st.dataframe(filtro_pl_abaixo_100k)
    st.subheader('Contas zeradas partindo da planilha de controle')
    st.dataframe(filtro_pl_0)

    ###########################################
    #Widgets para download

    # Função para criar link de download
 # Adicione um botão para fazer o download do arquivo final
    
    if arquivo_final is not None:
        
        
        # Use io.BytesIO para criar um buffer de bytes
        output = io.BytesIO()
        st.markdown(" Download excel clientes com Saldo abaixo de R$ 100.000,00")
        # Salve o DataFrame no buffer no formato XLSX
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtro_abaixo100k.to_excel(writer,
                                        sheet_name='abaixo_de_100k.xlsx',
                                          index=False)
        
        # Crie um link para download
        output.seek(0)
        st.download_button(
            label="Clique para fazer o download",
            data=output,
            file_name='Cliente com saldo abaixo de 100k.xlsx',
            key='download_button'
        )
        ######### Arquivo  income PL Abaixo de 60.000
        output1 = io.BytesIO()
        st.markdown(" Download excel clientes income e saldo menor R$ 60.000,00")
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
           filtro_income.to_excel(writer,
                                        sheet_name='income.xlsx',
                                          index=False)
        
    
        output1.seek(0)
        st.download_button(
            label="Clique para fazer o download",
            data=output1,
            file_name='Income_abaixo_60k.xlsx',
            key='download_button1'
        )
        ### Arquivo PL abaixo de 1.000,00

        output2 = io.BytesIO()
        st.markdown(" Download excel clientes com Saldo abaixo de R$ 1000,00")

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtro_pl_abaixo_100k.to_excel(writer,
                                        sheet_name='pl_abaixo_1000k.xlsx',
                                          index=False)

        output2.seek(0)
        st.download_button(
            label="Clique para fazer o download",
            data=output2,
            file_name='Cliente_saldo_1000.xlsx',
            key='download_button2'
        )

         ######### Arquivo PL 0 (Planilha de controle)
        output3 = io.BytesIO()
        st.markdown(" Download excel clientes com Saldo 0,00")
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtro_pl_0.to_excel(writer,
                                        sheet_name='contas_0.xlsx',
                                          index=False)
        
        
        output3.seek(0)
        st.download_button(
            label="Clique para fazer o download",
            data=output3,
            file_name='Contas_zeradas.xlsx',
            key='download_button3'
        )
        


 
    ##############################################



