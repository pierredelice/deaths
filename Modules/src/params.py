from json import load
from os import makedirs
import glob

def get_params() -> dict:
    """Parametros generales del programa
    """
    params = {
        #Ruta general
        "path": "/Users/pierredelice/Library/CloudStorage/Dropbox/Mac/Documents/GitHub/Defunción/data/defuncion_seed_homologadas/",
        #Ruta de los datos de defunción
        "dataset": "*.txt",
        # Ruta de las graficas
        "path graphics": "../Graphics",
        # Ruta de los resultados
        "path results": "../Results",
        #
        "path models": "../Models", 
    }
    return params


def mkdir(path: str) -> None:
    """
    Documentation
    """
    makedirs(
        path,
        exist_ok=True
        )