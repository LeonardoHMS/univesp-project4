import pandas as pd

dataframe = pd.read_csv('csv/acidentes2025.csv', encoding='latin1', sep=';')
dataframe.drop(['id', 'pesid', 'id_veiculo', 'latitude', 'longitude', 'regional', 'delegacia', 'uop'], axis=1, inplace=True)
dataframe['data_inversa'] = pd.to_datetime(dataframe['data_inversa'])
dataframe['hora'] = pd.to_datetime(dataframe['horario'], format='%H:%M:%S').dt.hour
dataframe['idade'] = pd.to_numeric(dataframe['idade'], errors='coerce')

dataframe.groupby('hora')['mortos'].count().plot(kind='bar')
top_municipios = dataframe['municipio'].value_counts().head(10)
dataframe['tipo_acidente'].value_counts().head(10)
dataframe['estado_fisico'].value_counts(normalize=True)
dataframe['sexo'].value_counts(normalize=True)
