# -*- coding: utf-8 -*-
"""Algoritmos para o problema da Triangulação de Polígonos:

Dado um polígono P, determinar uma triangulação (conjunto maximal de diagonais)

Algoritmos disponveis:
- Remoção de Orelhas
"""
from . import orelhas
from . import monotono

children = [
	[ 'orelhas', 'Orelhas', 'Remoção de Orelhas' ],
    [ 'monotono', 'Monotono', 'Monótonos']
]

__all__ = [a[0] for a in children]
