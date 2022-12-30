import re
import numpy as np
import string
from pandas import (
    DataFrame, 
    to_datetime,
)
import nltk
#nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize.treebank import (
    TreebankWordDetokenizer, 
    TreebankWordTokenizer,
    )
from nltk.tokenize.util import align_tokens
from nltk.tokenize.api import TokenizerI
from nltk.tokenize import (
    word_tokenize,
    RegexpTokenizer,
    )

class Tweak:
    """
    Class documentation
    """

    def __init__(self,
                 data: DataFrame) -> None:
        self.data = data
        self._int2uint32()
        self._obj2category()
        self._get_fec_nac()
        self._get_fec_def()
        self._get_format_col()
        self.fecha = [
            'nac_dia','nac_mes',
            'nac_anio','def_dia',
            'def_mes','def_anio'
            ]

    def _int2uint32(self) -> None:
        """
        convert integer to uint32
        """
        # type: ignore
        cols = self.data.select_dtypes('int')
        # type: ignore
        self.data = self.data.astype({
            col: "uint32"
            for col in cols
        })

    def _obj2category(self) -> None:
        """
        convert object to category
        """
        # type: ignore
        cols = self.data.select_dtypes('object')
        self.data = self.data.astype({
            col: "category"
            for col in cols
        })

    def _get_fec_nac(self):
        """
        convert (nac_dia, nac_mes, nac_anio) en
        fecha (to_datetime)
        """
        fecha = to_datetime(dict(
            year = self.data['nac_anio'],
            month = self.data['nac_mes'],
            day = self.data['nac_dia']),
            errors='coerce')
        self.data['fec_nac'] = fecha

    def _get_fec_def(self):
        """
        convert (def_dia, def_mes, def_anio) en
        fecha (to_datetime)
        """
        fecha = to_datetime(dict(
            year = self.data['def_anio'],
            month = self.data['def_mes'],
            day = self.data['def_dia']),
            errors = 'coerce')
        self.data['fec_def'] = fecha

    def _get_format_col(self):
        """
        create dummy variable with missing data
        """
        self.punct = "\n\r"+string.punctuation
        self.digit = str.maketrans('', '', string.digits)
        #Remove unnecessary characters
        self.stopword_es = stopwords.words('spanish')
        self.words_to_remove =['seis','desconocido','desconocida',
            'ignora','individuo','cadaver',
            'especificado','especificada',
            'masculino''identificado','numero',
            'identificada','femenino','restos',
            'humanos','xx xx xx','oseos']

        
        self.data['miscol'] = DataFrame(np.where([self.data.isna().any(axis=1)],1,0)).T
        self.data['nom_c'] = (self.data['nom_c']
                                .astype(str).str.lower()
                                )
        self.data['nom_c'] = (self.data['nom_c'].str.translate(
                                    str.maketrans('','',self.punct)
                                    )
                            )
        self.data['nom_c'] = [w.translate(self.digit) for w in self.data['nom_c']]
        self.data['nombre'] = (
            self.data['nom_c']
            .str.split(" ",expand=False)
            .str.join(" ")
            .str.replace(r".desconocido.","", regex=True)
            .str.replace(r"desconocidos*","", regex=True)
            .str.replace(r"desconoci...*","", regex=True)
            .str.replace(r".desconocidos*","", regex=True)
            .str.replace(r"identificado","", regex=True)
            .str.replace(r"^masculino$","", regex=True)
            .str.replace(r"masculino","", regex=True)
            .str.replace(r"^nan$","", regex=True)
            .str.replace(r"xx xx xx","", regex=True))
        
        self.data['nombre'] = (
            self.data['nombre'].apply(word_tokenize)
            #.apply(lambda x: [word for word in x if not word in self.stopword_es])
            .apply(lambda x: [word for word in x if not word in self.words_to_remove])
            .apply(TreebankWordDetokenizer().detokenize)
            )


    def get_data(self) -> DataFrame:
        """
    Read data after transformation
        """
        data = self.data.drop(self.fecha, axis=1)
        self.data = data
        return self.data.copy()
