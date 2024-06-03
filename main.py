import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import random
import math
import shapely.geometry
import tkinter as tk
from tkinter import messagebox

def calcula_distancia(lat1, lon1, lat2, lon2):
    '''Calcula a distância euclidiana (ou "distância em linha reta") entre dois pontos em um plano bidimensional'''
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)


def verifica_distancia(lat1, lon1, lat2, lon2, distancia_minima_sensores):
    '''Verifica distancia entre um novo sensor e sensores que ja estavam previamente na lista, evitando desperdicio de sensores'''
    if not lat2 and not lon2:
        # Se não há mais pontos para verificar, retorna True 
        return True
    if calcula_distancia(lat1, lon1, lat2[0], lon2[0]) < distancia_minima_sensores:
        # Se estiver dentro da distância mínima, retorna False
        return False
    # Caso contrário, continua verificando os próximos pontos recursivamente
    return verifica_distancia(lat1, lon1, lat2[1:], lon2[1:], distancia_minima_sensores)


def esta_no_oceano(latitude, longitude):
    """Verifica se uma determinada latitude e longitude estão localizadas no oceano."""
    # Cria um polígono Shapely representando a área do oceano
    ocean_polygons = cfeature.OCEAN.geometries()
    ocean_polygon = shapely.geometry.MultiPolygon(ocean_polygons)
    
    # Cria um ponto Shapely com as coordenadas fornecidas
    ponto = shapely.geometry.Point(longitude, latitude)
    
    # Verifica se o ponto está dentro do polígono do oceano
    return ocean_polygon.contains(ponto)


def define_sensores(distancia_minima_sensores, sensores_disponiveis, locais):
        '''Define a posição dos sensores.'''
        # Listas para armazenar as coordenadas dos sensores em áreas prioritárias
        latitude_sensores = []
        longitude_sensores = []

        # Listas para armazenar as coordenadas dos sensores em áreas aleatórias no oceano
        latitudes_aleatorias = []
        longitudes_aleatorias = []

        while sensores_disponiveis > 0:
            # Para cada tentativa de posicionar um sensor no oceano, tenta colocar sensores novamente nas áreas de prioridade.
            for local in locais.values():
                for coordenadas in local.values():
                    if sensores_disponiveis > 0:
                        # Gerar coordenadas aleatórias dentro dos limites especificados para as áreas prioritárias
                        sensor_lat = random.uniform(coordenadas[0][0], coordenadas[0][1])
                        sensor_lon = random.uniform(coordenadas[1][0], coordenadas[1][1])

                        # Verificar se a posição é válida (distância mínima entre sensores e estar no oceano)
                        if verifica_distancia(sensor_lat, sensor_lon, latitude_sensores, longitude_sensores, distancia_minima_sensores) and esta_no_oceano(sensor_lat, sensor_lon):
                            latitude_sensores.append(sensor_lat)
                            longitude_sensores.append(sensor_lon)
                            sensores_disponiveis -= 1
                    else:
                        break
                                
                # Se ainda houver sensores disponíveis, colocar em áreas aleatórias no oceano
            if sensores_disponiveis > 0:
                lat_aleatoria = random.uniform(-90, 90)
                lon_aleatoria = random.uniform(-180, 180)
                if verifica_distancia(lat_aleatoria, lon_aleatoria, latitude_sensores, longitude_sensores, distancia_minima_sensores) and esta_no_oceano(lat_aleatoria, lon_aleatoria):
                    latitudes_aleatorias.append(lat_aleatoria)
                    longitudes_aleatorias.append(lon_aleatoria)
                    sensores_disponiveis -= 1
            else:
                break
        # Informar a quantidade de sensores colocados em áreas prioritárias
        print("Quantidade de sensores em areas prioridade: ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(len(latitude_sensores))

        # Informar a quantidade de sensores colocados em áreas aleatórias no oceano
        print("Quantidade de sensores em alto mar:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(len(latitudes_aleatorias))

        # Unir as listas de sensores de áreas prioritárias e aleatórias
        latitude_sensores.extend(latitudes_aleatorias)
        longitude_sensores.extend(longitudes_aleatorias)

        # Informar o total de sensores posicionados
        print("Total de sensores: ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(len(latitude_sensores))

        return latitude_sensores, longitude_sensores

def gerar_grafico():
    try:
        # Obter valores de verba e preço do sensor das entradas
        verba = float(entry_verba.get())
        preco_sensor = float(entry_preco_sensor.get())
        area_coberta_sensor = 5

        distancia_minima_sensores = area_coberta_sensor
        sensores_disponiveis = int(verba // preco_sensor)

        # Mostrar mensagem informando a quantidade de sensores adquiridos
        messagebox.showinfo("Informação", f"Com {verba} reais, foi possível adquirir {sensores_disponiveis} sensores de {preco_sensor} reais.")

        # Definir a posição dos sensores
        latitude_sensores, longitude_sensores = define_sensores(distancia_minima_sensores, sensores_disponiveis, locais)

        # Criar um gráfico de mapa global usando projeção Mollweide
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mollweide())
        ax.set_global()
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        # Plotar as posições dos sensores no mapa
        ax.plot(longitude_sensores, latitude_sensores, 'ro', transform=ccrs.PlateCarree())
        plt.show() # Mostrar o gráfico

    except ValueError:
        # Mensagem de erro se os valores inseridos não forem válidos
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos. (Use .(ponto) ao em vez de ,(vírgula) para números decimais)")


# Áreas de prioridade
locais = {
    'prioridade1': {
        'Grande Barreira de Coral, Austrália': [(-10, -23), (144, 154)],
        'Triângulo dos Corais': [(13, -10),  (95, 150)],
        'Golfo do México': [(24, 29), (-83, -97)],
        'Mar Báltico': [(54, 66),(9, 29)],
        'Mar Mediterrâneo': [(30, 46),(-5, 36)],
        'Delta do Rio Ganges, Índia': [(21, 22),(89, 90)],
        'Arquipélago de Galápagos': [(0, -1.6667), (-90, -92)],
        'Afloramento da Costa Oeste da África': [(10, 25), (-17,-23)],
        'Afloramento da Califórnia:': [(33, 40), (-120, -123)],
        'Mar do Peru': [(-13, -18) , (-75, -82)]
    },
    'prioridade2': {
        'Everglades da Flórida': [(25, 26), (-80, -82)],
        'Sundarbans:': [(21, 23),(88, 90)],
        'Baía de Chesapeake': [(36, 39) ,(-76, -77)],
        'Ártico': [(66.5628, 90), (0, 360)],
        'Antártida': [(-60, -90), (0, 360)]
    }
}


# Criar a janela principal da interface gráfica
root = tk.Tk()
root.title("Configuração de Sensores Oceânicos")

tk.Label(root, text="Verba disponível:").grid(row=0, column=0)
entry_verba = tk.Entry(root)
entry_verba.grid(row=0, column=1)

tk.Label(root, text="Preço do Sensor:").grid(row=1, column=0)
entry_preco_sensor = tk.Entry(root)
entry_preco_sensor.grid(row=1, column=1)

tk.Button(root, text="Gerar Mapeamento", command=gerar_grafico).grid(row=3, columnspan=2)

# Iniciar o loop principal da interface gráfica
root.mainloop()