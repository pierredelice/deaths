import pandas as pd
from params import get_params
from dataset import Dataset

params = get_params()
dataset= Dataset(params)
df = dataset._get_data()