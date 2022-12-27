import numpy as np
from os.path import join
import glob
import pandas as pd
from tweak import Tweak
from pandas import (
    DataFrame, 
    read_csv,
    to_datetime,
    )

class Dataset:
    def __init__(self,
            params: dict) -> None:
        self.params = params
        self.data = None
        self.cols = [
            #Identidad del fallecido
            'nom_c','sexo','edad_c',
            'edad','nac_dia','nac_mes',
            'nac_anio','res_ent','res_mun', 
            'res_loc','curp','afiliacion',
            'edo_civil','escolar', 'ocupacion',
            #Datos de la defunción
            'def_dia','def_mes', 
            'def_anio','def_ent',
            'def_mun','def_loc',
            #'def_sitio','des_situa', 
            #Datos del certificante
            #'cert_por','cert_ced',
            #'cert_nom','informante',
            #'cert_dia','cert_mes',
            #'cert_anio',
            #Causa de defunción
            'causa_bas','base'
            ]
        self._read()
        self._format() 
    
    def _get_file(self) -> str:
        file = glob.glob(
                join(self.params['path'],
                    self.params['dataset']
                    )
                )
        return file # type: ignore

    def _read(self) -> DataFrame: # type: ignore
        file = self._get_file() 
        data =  pd.concat([pd.read_csv(
            idx,sep='|',
            usecols= self.cols,
            low_memory=False) for idx in file]
            )
        self.data = data[
                self.cols
           ]
        #return data

    def _format(self) -> DataFrame:
        tweak = Tweak(self.data)
        self.data = tweak.get_data()

    def get_data(self) -> DataFrame:
        """
        Documentation
        """
        return self.data.copy() # type: ignore
        