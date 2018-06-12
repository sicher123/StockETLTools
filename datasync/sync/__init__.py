import numpy as np
import pandas as pd
from copy import copy
from datetime import datetime, timedelta
from jaqs.data.dataview import DataView
import warnings

warnings.filterwarnings("ignore")
from DataSync.datadesk.utils import trans_symbol

def distributed_query(props):
        props = copy(props)
        fields = copy(props['fields'])
        db_config = props.pop('db_config')
        origin = globals()[props.pop('origin')](db_config)
        view = props['view']
        props['view'] = view
        start_date = props['start_date']
        end_date = props['end_date']

        import math
        num = math.floor((end_date - start_date) / 10000)

        for i in range(num):
            p = {}
            p['start_date'] = start_date + i * 10000
            p['end_date'] = start_date + (i + 1) * 10000
            p['view'] = view
            p['fields'] = fields

        return l

def update_by_id(props ,ID_NAME = 'OBJECT_ID'):
    '''
    :param props:
    :param ID_NAME:
    :return: list -> props list
    '''
    try:
        file = db.get_file(ID_NAME)
        _id = db.get_info(ID_NAME)

        if len(file.keys()) > 0:
            data = file['data'][:].astype(str)
            exist_id = list(data.reshape(data.shape[0] * data.shape[1]))
            prop['fields'] = ID_NAME
            df = origin.read(props=v)
            _id = list(set(df[ID_NAME].values) - set(exist_id))
        else:
            _id = []
    except:
        _id = []

        _id = ','.join(_id)
        prop['OBJECT_ID'] = _id
        return p

