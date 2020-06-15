# -*- coding: utf-8 -*-

# Lista de (problema, diretório, tipo de input)
problemas = [('Par mais Próximo', 'algoritmos/par_proximo', 'input/pontos'),
             ('Fecho Convexo', 'algoritmos/fecho', 'input/pontos'),
             ('Triangulação de Delauney', 'algoritmos/delauney', 'input/pontos'),
             ('Triangulação de Polígonos', 'algoritmos/delauney', 'input/poligonos'),
             ('Interseção de Segmentos', 'algoritmos/inter_segs', 'input/segmentos'),
             ('Interseção de Círculos', 'algoritmos/inter_circs', 'input/circulos')]

# Pra cada problema, uma lista de algortimos
# Um algoritmo é uma tupla (arquivo, apelido, função principal)
# O índices das listas de algoritmos devem ser os mesmo da lista de problemas
algoritmos = []
# Algoritmos do par mais próximo
algoritmos.append ([('forca_bruta.py', 'Força Bruta', 'brute_force'),
                    ('shamos.py', 'Divisão e Conquista', 'shamos')
                   ])

# Algoritmos para fecho convexo
algoritmos.append ([('quick_hull.py', 'QuickHull', 'quick_hull'),
                    ('merge_hull.py', 'MergeHull', 'merge_hull')
                   ])

# Algoritmos para triangulação de Delauney
algoritmos.append ([('incremental.py', 'Incremental', 'incremental')
                   ])

# Algoritmos para triangulação de polígonos
algoritmos.append ([('orelhas.py', 'Remoção de Orelhas', 'orelhas'),
                    ('monotonos.py', 'Monótonos', 'monotonos'),
                    ('lee_preparata.py', 'Lee & Preparata', 'lee_preparata')
                    ])

# Algoritmos para detectar todas as interseções de segmentos
algoritmos.append ([('forca_bruta.py', 'Força Bruta', 'brute_force'),
                    ('bentley_ottmann.py', 'Bentley & Ottmann', 'bentley_ottmann')
                   ])

# Algoritmos para detectar todas as interseções entre circulos
algoritmos.append ([('forca_bruta.py', 'Força Bruta', 'brute_force'),
                    ('bentley_ottmann.py', 'Bentley & Ottmann\nModificado', 'bentley_ottmann')
                   ])