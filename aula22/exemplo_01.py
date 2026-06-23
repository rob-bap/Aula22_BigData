import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    print("Obtendo os dados...")
    ENDEREÇO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv" # é possivel importar dados de bancos com links pela internet

    df_ocorrenciais = pd.read_csv(ENDEREÇO_DADOS, sep = ';', encoding = 'iso-8859-1') # outros tipos de codificação de dados: utf-8, latin1, cp1252

    # delimitando variaveis, para que não ocorra a obtenção de todos os dados que não serão necessarios
    df_roubo_veiculos = df_ocorrenciais[['munic', 'roubo_veiculo']]

    # totalizando as ocorrencias pelos municipios
    df_roubo_veiculos = df_roubo_veiculos.groupby('munic', as_index = False)['roubo_veiculo'].sum() # agrupa dados pelos que se repetem ex.: Rio de Janeiro que aparece em várias partes

    # ordenando dataframe por ordem decrescente
    df_roubo_veiculos = df_roubo_veiculos.sort_values(by = 'roubo_veiculo', ascending = False)

    # print(df_roubo_veiculos.head(20))

except Exception as e:
    print(f"Erro na importção de dados: {e}")

# obtendo as medidas
try:
    print('Calculando as medidas...')
    array_roubo_veiculo = np.array(df_roubo_veiculos['roubo_veiculo']) # criand array para facilitar calculos futuros com os dados

    media_roubo_veiculo = np.mean(array_roubo_veiculo) # calculando media
    mediana_roubo_veiculo = np.median(array_roubo_veiculo) # calculando mediana
    distancia = abs(media_roubo_veiculo - mediana_roubo_veiculo / mediana_roubo_veiculo * 100) # abs = obtendo valor absoluto, transformando numero negativo em positivo.

    print('\nMedidas de Tendência Central')
    print(30 * '=')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância: {distancia}')

except Exception as e:
    print(f'Erro ao obter medidas: {e}')

# obtendo a distribuição, calculando quarti baseado no array criado pelos roubos de veiculos
try:
    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)
    
    print('\nQuartis')
    print(30 * '=')
    print(f'Q1: {q1}')
    print(f'Q2: {mediana_roubo_veiculo}')
    print(f'Q3: {q3}')

    # municipios com menos roubos
    df_roubo_veiculos_menores = df_roubo_veiculos[df_roubo_veiculos['roubo_veiculo'] < q1]

    # municipios com mais roubos
    df_roubo_veiculos_maiores = df_roubo_veiculos[df_roubo_veiculos['roubo_veiculo'] > q3]

    print('\nMunicipios com menos casos de roubos: ')
    print(30 * '=')
    print(df_roubo_veiculos_menores.sort_values(by = 'roubo_veiculo', ascending = True))

    print('\nMunicipios com mais casos de roubos: ')
    print(30 * '=')
    print(df_roubo_veiculos_maiores)

except Exception as e:
    print(f'Erro ao obter distribuição: {e}')

# obtendo medidas de dispersão
try:
    # Amplitude total
    # amplitude = maior valor - valor minimo
    # resultado: mais proximo de minimo, baixa dispersão
    # se for 0, significa que todos os dados são iguais
    # se mais proximo do maior valor, alta dispersão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(30 * '=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')


except Exception as e:
    print(f'Erro ao obter medidas de dispersão: {e}')

# calculando outliers
try:
    # IQR (Intervalo Interquartil) = Amplitude dos 50% dos dados mais centrais
    # iqr = Q3 - Q1
    # ele ignora os valores extremos. Max e Min estão fora do IQR
    # não sofre interferencia dos valores extremos 
    # quanto mais proximo do zero, mais homogenio são os dados
    # quanto mais proximo do Q3, menos homogenio são os dados
    iqr = q3 - q1

    # limite inferior: vai identificar os outliners abaixo dele
    limite_inferior = q1 - (1.5 * iqr)

    # limite superior: vai identificar os outliners acima dele
    limite_superior = q3 + (1.5 * iqr)

    print('\nMedidas')
    print(30 * '=')
    print(f'Mínimo: {maximo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}') # q2
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')

except Exception as e:
    print(f"Erro ao calcular Outliers: {e}")

# exibindo os outliners
try:
    # outliers superiores
    df_roubo_veiculos_outliers_superiores = df_roubo_veiculos[df_roubo_veiculos['roubo_veiculo'] > limite_superior]

    # outliers inferiores
    df_roubo_veiculos_outliers_inferiores = df_roubo_veiculos[df_roubo_veiculos['roubo_veiculo'] < limite_inferior]

    print('\nMunicípios com Outliers Inferiores')
    print(30 * '=')
    
    if len(df_roubo_veiculos_outliers_inferiores) == 0:
        print('Não existe outliers inferiores.')

    else:
        print(df_roubo_veiculos_outliers_inferiores.sort_values(by = 'roubo_veiculo', ascending = True))
    
    print('\nMunicípios com Outliers Supeiores')
    print(30 * '=')
    
    if len(df_roubo_veiculos_outliers_superiores) == 0:
        print('Não existe outliers superiores.')

    else:
        print(df_roubo_veiculos_outliers_superiores.sort_values(by = 'roubo_veiculo', ascending = False))

except Exception as e:
    print(f"Erro ao calcular os outliers: {e}")

try:

# Assimetria
# Indica como os dados estão distribuidos em torno de um valor central
# Usada para decrever o grau de assimetria de distribuição
# Os valores estão equilibrados?
# Existe uma maior quantidade de observação de registros maiores ou menores?
# O peso da distribuição está mais pra qual lado? 'p/ os mais baixos ou os mais altos?'


# Interpretação
# Resultado da Assimetria > 1 = Assimetria positiva alta
# Calda longa à direita
# Existem valores muito altos puxando média pra cima
# A tendência de que a média seja maior que a mediana
    

# Resultado da Assimetria entre 0.5 e 1 = Assimetria positiva moderada
# Calda à direita 
# Existem valores altos puxando média pra cima, mas é menos acentuada
# A tendência de que a média seja muito proxima da mediana


# Resultado da Assimetria entre -0.5 e 0.5 = Disribuição aproximadamente simetrica
# Os dados estão equilibrados em torno da média
    

# Resultado da Assimetria entre -0.5 e -1 = Assimetria negativa moderada
# Calda à esquerda 
# Existem valores baixos puxando a média para baixo, mas é menos acentuado
# A tendência de que a média seja menor que a mediana
    

# Resultado da Assimetria < -1 = Assimetria negativa alta
# Calda longa à esquerda 
# Existem valores muito baixos puxando a média para baixo
# A tendência de que a média seja muito menor que a mediana

    assimatria = df_roubo_veiculos['roubo_veiculo'].skew()

# Curtose
# Medida que descreve o formato da distribuição
# Nos ajuda a entender, se os valores estão espalhados ou mais proximos da média
# Ajuda a entender se existem ourliers

# Interpretação
# Curtose Alta
# Geralemnte temos muitos valores distribuidos em torno da média e alguns outros, muito distante delas
    
# Curtose Baixa
# Os dados tendem a estar distribuidos ao longo do conjunto
    

# Interpretação segundo Fisher (Obs.: No Pandas o padrão é Fisher)
# Resultado da curtose = 0 ------> (Mesocúrtica)  pearson 3
# Distribuição normal
# Concentração moderada no centro
# Outliers são raros
    
# Resultado da curtose < 1 ------> (Platicúrtica)  pearson < 3
# Pico achatado
# Dados mais afastados
# Poucos Extremos, podendo haver outliers

# Resultado da curtose > 1 ------> (Leptocúrtica)  pearson > 3
# Pico mais alto
# Muitos valores próximos da média
# Outliers mais fortes
# Caldas mais pesadas
    
    curtose = df_roubo_veiculos['roubo_veiculo'].kurtosis()


    print('\nMedidas de Distrbuição')
    print(30 * '=')
    print(f'Assimetria: {assimatria}')
    print(f'Curtose: {curtose}')


except Exception as e:
    print(f'Erro ao calcular distribuição: {e}')

try:
    print('Calculando a variabilidade dos dados')
    # Variância
    # É uma medida para verificar a dispersão dos dados
    # Observa-se em relação à média
    # É a média dos quadrados das diferenças entre cada valor e média
    # Obs.: O resultado da variancia está elevado ao quadrado

    # Interpretação
    # Quanto maior a variancia, maior é o afastamento dos valores em relação à média
    # Quanto mnenor a variancia, menor é o afastamento dos valores em relação à média

    variancia = np.var(array_roubo_veiculo)

    # Distancia entre Média e Variancia
    # até 10% = baixa dispersão em relação à média
    # entre 10% e 25%= dispersão moderada em relação à média
    # maior 25% = alta dispersão em relação à média

    distancia_var_media = variancia / (media_roubo_veiculo ** 2) * 100

    # Desvio Padrão
    # É a raiz quadrada da variancia
    # É a normalização da variância
    # Apresenta o quanto os dados podem estar afastados em relação à média
    # (tanto para mais, quanto para menos)

    desvio_padrao = np.std(array_roubo_veiculo)

    # Coeficiente de Variação
    # É a magnitude do desvio padrão em relação a média
    coef_variação = desvio_padrao / media_roubo_veiculo * 100

    print('\nMedidas de Variabilidade')
    print(30 * '=')
    print(f'Variância: {variancia}')
    print(f'Distância entre Variancia e a Média: {distancia_var_media}%')
    print(f'Desvio Padrão: {desvio_padrao}')
    print(f'Coeficiente de Variação: {coef_variação}%')


except Exception as e:
    print(f'Erro ao calcular a variabilidade dos dados: {e}')


try:
    plt.subplots(3, 2, figsize=(18, 10))
    plt.suptitle('Roubo de Veículos por Municípios', fontsize=16, fontweight='bold', color='darkblue')

    plt.subplot(3, 2, 1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans = True)
    plt.title('Boxplot da Distribuição')

    plt.subplot(3, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}', fontsize=9)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_veiculo}', fontsize=9)
    plt.text(0.1, 0.7, f'Distancia : {distancia}', fontsize=9)
    plt.text(0.1, 0.6, f'Q1: {q1}', fontsize=9)
    plt.text(0.1, 0.5, f'Q3: {q3}', fontsize=9)
    plt.text(0.1, 0.4, f'Máximo: {maximo}', fontsize=9)
    plt.text(0.1, 0.3, f'Minimo: {minimo}', fontsize=9)
    plt.text(0.1, 0.2, f'IQR: {iqr}', fontsize=9)
    plt.text(0.1, 0.1, f'Limite Inferior: {limite_inferior}', fontsize=9)
    plt.text(0.1, 0.0, f'Limite Superior: {limite_superior}', fontsize=9)
    plt.axis('off')
    plt.title('Medidas de Distribuição')

    plt.subplot(3 , 2, 3)
    df_roubo_veiculos_outliers_superiores = (df_roubo_veiculos_outliers_superiores.head(10).sort_values(by='roubo_veiculo', ascending=False))
    plt.bar(df_roubo_veiculos_outliers_superiores['munic'], df_roubo_veiculos_outliers_superiores['roubo_veiculo'], color='darkblue')

    deslocamento = max(df_roubo_veiculos_outliers_superiores['roubo_veiculo']) * 0.03 # variavel que define o deslocamento do texto
    for i, valor in enumerate(df_roubo_veiculos_outliers_superiores['roubo_veiculo']):
        plt.text(i, valor + deslocamento, f'{valor}', ha='center') # valor + 0.5 = posição x, i = posição y

    plt.title('Municipios com Outliers Superiores')
    plt.xticks(rotation=45, ha='right') # .xticks(rotation=45, ha='right') = rotation define rotação do texto, ha define direção

    plt.subplot(3, 2, 4)
    if len(df_roubo_veiculos_outliers_inferiores) > 0:
        df_roubo_veiculos_outliers_inferiores = df_roubo_veiculos_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True)
        plt.barh(df_roubo_veiculos_outliers_inferiores['munic'], df_roubo_veiculos_outliers_inferiores['roubo_veiculo'], color='darkblue')

        deslocamento = max(df_roubo_veiculos_outliers_inferiores['roubo_veiculo']) * 0.03
        for i, valor in enumerate(df_roubo_veiculos_outliers_inferiores['roubo_veiculo']):
            plt.text(valor + deslocamento, i, f'{valor}', ha='center') # valor + 0.5 = posição x, i = posição y
            
        plt.title('Municipios com Ouliers Inferiores')

    else:
        df_roubo_veiculos_menores = (df_roubo_veiculos_menores.sort_values(by='roubo_veiculo', ascending=True).head(10)) 
        plt.barh(df_roubo_veiculos_menores['munic'], df_roubo_veiculos_menores['roubo_veiculo'], color='darkblue') # .str.slice(0, 10) = define o tamanho do texto mostrado no gráfico

        deslocamento = max(df_roubo_veiculos_menores['roubo_veiculo']) * 0.03
        for i, valor in enumerate(df_roubo_veiculos_menores['roubo_veiculo']):
            plt.text(valor + deslocamento, i, f'{valor}', ha='center') # valor + 0.5 = posição x, i = posição y

        plt.title('Municipios com Menores Roubos')
        plt.xticks(rotation=45, ha='right')

    plt.subplot(3, 2, 5)
    plt.hist(array_roubo_veiculo, bins=100)
    plt.axvline(media_roubo_veiculo, color='darkblue', linewidth=1)
    plt.axvline(mediana_roubo_veiculo, color='darkgreen', linewidth=1)

    plt.tight_layout()  # ajusta completamente o layout do gráfico
    plt.show()

except Exception as e:
    print(f'Erro ao criar gráfico: {e}')