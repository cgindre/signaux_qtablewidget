# -*- coding: utf-8 -*-

from scipy.constants import Avogadro
from numpy import format_float_scientific

print("Avogadro = ", Avogadro)

qtte = 10 #mol
nb_atomes = qtte * Avogadro

print("qtte = ", qtte)
print("nb_atomes = ", nb_atomes)
inv_avogadro = 1.0 / Avogadro
print("inv_avogadro = ", inv_avogadro)

# Pour C14,
Am = 1.66e+11 # Bq.g-1

Activite = 10 # Bq
m_C14 = Activite / Am
coef = (14 * Am) / Avogadro
print("coef = ", coef)
N = Activite * coef
print("N = ", format_float_scientific(N) )

m_C12 = 10.0
N_C12 = m_C12 * Avogadro / 12
coef = 12 /Avogadro
print("coef = ", coef)
print("N_C12 = ", N_C12)