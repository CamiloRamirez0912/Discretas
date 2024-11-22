import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

class MapaTunja:
    def __init__(self):
        self.hospitales = {
            "Clínica Los Andes": (5.537, -73.367),
            "Clínica Medilaser": (5.544, -73.354),
            "Hospital San Rafael": (5.537, -73.361),
            "Hospital Metropolitano Santiago de Tunja": (5.5199296455904, -73.35837279563792)
        }

        print("Descargando datos de Tunja desde OpenStreetMap...")
        self.gdf_edges = self._descargar_mapa()

    def _descargar_mapa(self):
        tunja_graph = ox.graph_from_place("Tunja, Boyacá, Colombia", network_type="drive")
        _, gdf_edges = ox.graph_to_gdfs(tunja_graph)
        return gdf_edges

    def _geocodificar_direccion(self, direccion):
        try:
            print(f"Geocodificando dirección: {direccion}")
            geocode_result = ox.geocode(direccion)
            print(f"Coordenadas obtenidas: {geocode_result}")
            return Point(geocode_result[1], geocode_result[0])  # Longitud, Latitud
        except Exception as e:
            raise ValueError(f"No se pudo geocodificar la dirección. Detalles: {e}")

    def mostrar_mapa(self, direccion):
        try:
            # Crear GeoDataFrame para la dirección
            punto_direccion = self._geocodificar_direccion(direccion)
            direccion_gdf = gpd.GeoDataFrame(
                {"Lugar": ["Dirección ingresada"]},
                geometry=[punto_direccion],
                crs="EPSG:4326"
            ).to_crs(self.gdf_edges.crs)

            # Crear GeoDataFrame para los hospitales
            hospitales_gdf = gpd.GeoDataFrame(
                self.hospitales.keys(),
                geometry=[Point(lon, lat) for lat, lon in self.hospitales.values()],
                crs="EPSG:4326"
            ).to_crs(self.gdf_edges.crs)

            # Crear el mapa
            print("Generando el mapa...")
            fig, ax = plt.subplots(figsize=(10, 10))
            self.gdf_edges.plot(ax=ax, linewidth=0.5, color="gray")  # Dibujar las calles
            hospitales_gdf.plot(ax=ax, color="red", markersize=100, label="Hospitales")
            direccion_gdf.plot(ax=ax, color="blue", markersize=100, label="Dirección ingresada")
            
            # Añadir etiquetas a los hospitales
            for x, y, label in zip(hospitales_gdf.geometry.x, hospitales_gdf.geometry.y, self.hospitales.keys()):
                ax.text(x, y, label, fontsize=10, ha="right")

            # Añadir etiqueta a la dirección
            for x, y, label in zip(direccion_gdf.geometry.x, direccion_gdf.geometry.y, direccion_gdf["Lugar"]):
                ax.text(x, y, label, fontsize=10, color="blue", ha="right")

            plt.title("Mapa de Tunja con Hospitales y Dirección")
            plt.legend()
            plt.show()
        except ValueError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Ha ocurrido un error inesperado: {e}")
