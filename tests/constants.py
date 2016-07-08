import os

TRANSFORMATION_1_FILE = os.path.join(os.path.dirname(__file__), "transformation_1/transformation_1.ktr")

TRANSFORMATION_1_STEPS = {'Dummy (do nothing)': {'type': 'Dummy'}, 'Select values': {'type': 'SelectValues'},
                          'Text file output': {'type': 'TextFileOutput'}, 'Filter rows': {'type': 'FilterRows'},
                          'Text file input': {'type': 'TextFileInput'}, 'Dummy (do nothing) 2': {'type': 'Dummy'}}

TRANSFORMATION_1_HOPS = [{'to': 'Select values', 'from': 'Text file input', 'enabled': 'Y'},
                         {'to': 'Filter rows', 'from': 'Select values', 'enabled': 'Y'},
                         {'to': 'Dummy (do nothing)', 'from': 'Filter rows', 'enabled': 'Y'},
                         {'to': 'Text file output', 'from': 'Filter rows', 'enabled': 'Y'},
                         {'to': 'Dummy (do nothing) 2', 'from': 'Select values', 'enabled': 'Y'}]

TRANSFORMATION_1_GRAPH = {'Text file input': ['Select values'],
                          'Filter rows': ['Dummy (do nothing)', 'Text file output'],
                          'Select values': ['Filter rows', 'Dummy (do nothing) 2']}

TRANSFORMATION_1_PATHS = [['Text file input', 'Select values', 'Filter rows', 'Text file output']]
