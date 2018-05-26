# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import json
try:
    import cPickle as pickle
except ImportError:
    import pickle
    

def trans_symbol(_symbol,dtype = 'standard'):
    assert dtype in  ['standard','exchange','code'] , 'dtype must in [standard, exchange, code]'
    code_list = _symbol.split('.')
    num = _symbol[0]
    
    try:
        int (num)
    except ValueError:
        return _symbol
        
    if len(code_list) == 1:
        if dtype == 'standard':               
            if num == '0' or num == '3':
                symbol = code_list[0] + '.SZ'
            elif num == '6':
                symbol = code_list[0] + '.SH'
                
        elif dtype == 'exchange':
            if num == '0' or num == '3':
                symbol = code_list[0] + '.XSHE'
            elif num == '6':
                symbol = code_list[0] + '.XSHG'
                
    else:
        if dtype == 'standard':                
            if code_list[1] == 'XSHE':
                symbol = code_list[0] + '.SZ'
            elif code_list[1] == 'XSHG':
                symbol = code_list[0] + '.SH'
        
        elif dtype == 'exchange':           
            if code_list[1] == 'SZ' or code_list[1] == 'sz':
                symbol = code_list[0] + '.XSHE'
            elif code_list[1] == 'SH' or code_list[1] == 'sh':
                symbol = code_list[0] + '.XSHG'
                
        elif dtype == 'code':
                symbol = code_list[0]
                
    return symbol

def read_json(fp):
    """
    Read JSON file to dict. Return None if file not found.

    Parameters
    ----------
    fp : str
        Path of the JSON file.

    Returns
    -------
    dict

    """
    content = dict()
    try:
        with codecs.open(fp, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except IOError as e:
        if e.errno not in (errno.ENOENT, errno.EISDIR, errno.EINVAL):
            raise
    return content


def save_json(serializable, file_name):
    """
    Save an serializable object to JSON file.

    Parameters
    ----------
    serializable : object
    file_name : str

    """
    fn = os.path.abspath(file_name)
    create_dir(fn)
    
    with codecs.open(fn, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, separators=(',\n', ': '))


def load_pickle(fp):
    """
    Read Pickle file. Return None if file not found.

    Parameters
    ----------
    fp : str
        Path of the Pickle file.

    Returns
    -------
    object or None

    """
    content = None
    try:
        with open(fp, 'rb') as f:
            content = pickle.load(f)
    except IOError as e:
        if e.errno not in (errno.ENOENT, errno.EISDIR, errno.EINVAL):
            raise
    return content


def save_pickle(obj, file_name):
    """
    Save an object to Pickle file.

    Parameters
    ----------
    obj : object
    file_name : str

    """
    fn = os.path.abspath(file_name)
    create_dir(fn)

    with open(fn, 'wb') as f:
        pickle.dump(obj, f)



