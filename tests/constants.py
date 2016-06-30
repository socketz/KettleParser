TRANSFORMATION_1_FILE = "transformation_1/transformation_1.ktr"

TRANSFORMATION_1_STEPS = {'Text file output': {'type': 'TextFileOutput'}, 'Filter rows': {'type': 'FilterRows'},
                          'Dummy (do nothing)': {'type': 'Dummy'},
                          'Text file input': {'type': 'TextFileInput'},
                          'Select values': {'type': 'SelectValues'}}

TRANSFORMATION_1_HOPS = [{'to': 'Select values', 'from': 'Text file input', 'enabled': True, 'error': False},
                         {'to': 'Filter rows', 'from': 'Select values', 'enabled': True, 'error': False},
                         {'to': 'Dummy (do nothing)', 'from': 'Filter rows', 'enabled': True, 'error': False},
                         {'to': 'Text file output', 'from': 'Filter rows', 'enabled': True, 'error': False}]

TRANSFORMATION_1_GRAPH = {'Text file input': ['Select values'],
                          'Filter rows': ['Dummy (do nothing)', 'Text file output'],
                          'Select values': ['Filter rows']}

TRANSFORMATION_1_PATHS = [['Text file input', 'Select values', 'Filter rows', 'Text file output']]
