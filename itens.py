# -*- coding: utf-8 -*-

# Tipos de Input  (nome, diretorio)
# 0 - Pontos
# 1 - Polígonos
# 2 - Segmentos
# 3 - Círculos
tipos_input = [("Pontos", "input/pontos"),
               ("Polígonos", "input/poligonos"),
               ("Segmentos", "input/segmentos"),
               ("Círculos", "input/circulos")]

# Lista de tuplas de problemas, cada problema vira um botão na tela inicial
# O formato das tuplas é (problema, diretório na pasta algoritmos, tipo de input)
# Por exemplo: ('Par mais Próximo', 'par_proximo', 1)
problemas = [('Par mais Próximo', 'par_proximo', 0),
             ('Fecho Convexo', 'fecho_convexo', 0),
             ('Triangulação de Delauney', 'delauney', 0),
             ('Triangulação de Polígonos', 'triangulacao', 1),
             ('Interseção de Segmentos', 'inter_segs', 2),
             ('Interseção de Círculos', 'inter_circs', 3)]

# Pra cada problema, uma lista de algortimos
# Um algoritmo é uma tupla (arquivo, apelido, função principal do arquivo)
# O índices das listas de algoritmos devem ser os mesmo da lista de problemas
algoritmos = []
# Algoritmos do par mais próximo
algoritmos.append ([('forca_bruta', 'Força Bruta', 'forca_bruta'),
                    ('shamos', 'Divisão e Conquista', 'shamos'),
                    ('varredura', 'Linha de Varredura', 'varre')
                   ])

# Algoritmos para fecho convexo
algoritmos.append ([('embrulho_presente', 'Embrulho de Presente', 'embrulho'),
                    ('graham', 'Graham', 'graham'),
                    ('incremental', 'Incremental Aleatório', 'incremental'),
                    ('quickhull', 'QuickHull', 'quickhull'),
                    ('mergehull', 'MergeHull', 'mergehull')
                   ])

# Algoritmos para triangulação de Delauney
algoritmos.append ([('incremental', 'Incremental', 'incremental'),
                    ('incremental_dag', 'Incremental\nmostrando DAG', 'incremental')
                   ])

# Algoritmos para triangulação de polígonos
algoritmos.append ([('orelhas', 'Remoção de Orelhas', 'orelhas'),
                    ('monotono', 'Monótonos', 'monotono'),
                    ('lee_preparata', 'Lee & Preparata', 'lee_preparata')
                    ])

# Algoritmos para detectar todas as interseções de segmentos
algoritmos.append ([('forca_bruta', 'Força Bruta', 'forca_bruta'),
                    ('bentley_ottmann', 'Bentley & Ottmann', 'bentley_ottmann')
                   ])

# Algoritmos para detectar todas as interseções entre circulos
algoritmos.append ([('forca_bruta', 'Força Bruta', 'forca_bruta'),
                    ('bent_ott_mod', 'Bentley & Ottmann\nModificado', 'bentley_ottmann_mod')
                   ])