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
             ('Fecho Convexo', 'fecho', 0),
             ('Triangulação de Delauney', 'delauney', 0),
             ('Triangulação de Polígonos', 'delauney', 1),
             ('Interseção de Segmentos', 'inter_segs', 2),
             ('Interseção de Círculos', 'inter_circs', 3)]

# Pra cada problema, uma lista de algortimos
# Um algoritmo é uma tupla (arquivo, apelido, função principal do arquivo)
# O índices das listas de algoritmos devem ser os mesmo da lista de problemas
algoritmos = []
# Algoritmos do par mais próximo
algoritmos.append ([('forca_bruta', 'Força Bruta', 'brute_force'),
                    ('shamos', 'Divisão e Conquista', 'shamos')
                   ])

# Algoritmos para fecho convexo
algoritmos.append ([('quick_hull', 'QuickHull', 'quick_hull'),
                    ('merge_hull', 'MergeHull', 'merge_hull')
                   ])

# Algoritmos para triangulação de Delauney
algoritmos.append ([('incremental', 'Incremental', 'incremental')
                   ])

# Algoritmos para triangulação de polígonos
algoritmos.append ([('orelhas', 'Remoção de Orelhas', 'orelhas'),
                    ('monotonos', 'Monótonos', 'monotonos'),
                    ('lee_preparata', 'Lee & Preparata', 'lee_preparata')
                    ])

# Algoritmos para detectar todas as interseções de segmentos
algoritmos.append ([('forca_bruta', 'Força Bruta', 'brute_force'),
                    ('bentley_ottmann', 'Bentley & Ottmann', 'bentley_ottmann')
                   ])

# Algoritmos para detectar todas as interseções entre circulos
algoritmos.append ([('forca_bruta', 'Força Bruta', 'brute_force'),
                    ('bentley_ottmann', 'Bentley & Ottmann\nModificado', 'bentley_ottmann')
                   ])