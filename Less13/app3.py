import streamlit as st
import pandas as pd
import numpy as np
import io

def convert_to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="data",index=False)
    # see: https://xlsxwriter.readthedocs.io/working_with_pandas.html
    writer.close()
    return output.getvalue()

def main():
    st.title("Caricamento File CSV/XLSX")
    uploaded_file = st.file_uploader("Scegli un file CSV o XLSX", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        # Verifica l'estensione del file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.success("File CSV caricato con successo!")
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            st.success("File XLSX caricato con successo!")
        else:
            st.error("Formato file non supportato!")

        st.dataframe(df)
        if st.button('Start Processing', help="Process Dataframe"):
            #df_copia= df.fillna(df.median(), inplace=True)
            df_copia2=df[df['Price']!='Ask For Price'].reset_index(drop=True)
            df_copia2['Price'] = df_copia2['Price'].astype(str).str.replace(',', '', regex=False)
            df_copia2['Price'].astype(int)
            df_copia2['Price'] = df_copia2['Price'].apply(lambda x: str(x)[:-2]).astype(int)
            df_copia2['fuel_type'] = df_copia2.apply(lambda row:row['kms_driven'] if row['kms_driven'] == 'Petrol' else row['fuel_type'], axis=1)
            df_copia2['kms_driven']=df_copia2['kms_driven'].replace('Petrol', np.nan).copy()
            df_copia2['kms_driven'] = df_copia2['kms_driven'].astype(str).str.replace(',', '', regex=False)
            df_copia2['kms_driven'] = df_copia2['kms_driven'].astype(str).str.replace(' kms', '', regex=False)
            df_copia2=df_copia2[df_copia2['fuel_type'].isna()!=True].reset_index(drop=True)
            df_copia2['kms_driven']=df_copia2['kms_driven'].replace('nan', np.nan).copy()
            df_copia2=df_copia2[df_copia2['kms_driven'].isna()!=True].reset_index(drop=True)
            df_copia2['kms_driven']=df_copia2['kms_driven'].astype(int)
            df_copia2['year']=df_copia2['year'].astype(int)
            df_copia2['brand'] = df_copia2['name']
            df_copia2['brand'] = df_copia2.name.str.split().str.get(0)
            df_copia2=pd.get_dummies(df_copia2, columns=['brand', 'fuel_type'], drop_first=True,  dtype=int)
            df_copia2=df_copia2.drop(columns='name')


            st.download_button(
                                label="download Excel",
                                data=convert_to_excel(df_copia2),
                                file_name="result.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="excel_download",
                                )


if __name__ == "__main__":
    main()