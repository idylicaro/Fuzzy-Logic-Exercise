import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#  T(x1) = {PS (pouca sujeira), MS(m´edia sujeira), GS(grande sujeira)}
#  T(x2) = {SM(sem mancha), MM(m´edia mancha), GM(grande mancha)}
#  T(y) = {MC(muito curto), C(curto), M(m´edio), L(longo), ML(muito longo)}


# Variáveis Linguísticas
x1 = ctrl.Antecedent(np.arange(0, 101, 1), 'Sujeira')
x2 = ctrl.Antecedent(np.arange(0, 101, 1), 'Mancha')
y = ctrl.Consequent(np.arange(0, 61, 1), 'Tempo')

# Conjuntos de Termos Linguísticos (triangular fuzzy membership function)
x1['POUCA SUJEIRA'] = fuzz.trimf(x1.universe, [0, 25, 50])
x1['MÉDIA SUJEIRA'] = fuzz.trimf(x1.universe, [0, 50, 100])
x1['GRANDE SUJEIRA'] = fuzz.trimf(x1.universe, [50, 75, 100])

x2['SEM MANCHA'] = fuzz.trimf(x2.universe, [0, 25, 50])
x2['MÉDIA MANCHA'] = fuzz.trimf(x2.universe, [0, 50, 100])
x2['GRANDE MANCHA'] = fuzz.trimf(x2.universe, [50, 75, 100])

y['MUITO CURTO'] = fuzz.trimf(y.universe, [0, 5, 10])
y['CURTO'] = fuzz.trimf(y.universe, [0, 10, 25])
y['MÉDIO'] = fuzz.trimf(y.universe, [10, 25, 40])
y['LONGO'] = fuzz.trimf(y.universe, [25, 40, 60])
y['MUITO LONGO'] = fuzz.trimf(y.universe, [40, 50, 60])

# x1.view()
# x2.view()
# y.view()

# PS + SM
rule1 = ctrl.Rule(x1['POUCA SUJEIRA'] & x2['SEM MANCHA'], y['MUITO CURTO'])
rule2 = ctrl.Rule(x1['POUCA SUJEIRA'] & x2['MÉDIA MANCHA'], y['MÉDIO'])
rule3 = ctrl.Rule(x1['POUCA SUJEIRA'] & x2['GRANDE MANCHA'], y['LONGO'])
rule4 = ctrl.Rule(x1['MÉDIA SUJEIRA'] & x2['SEM MANCHA'], y['CURTO'])
rule5 = ctrl.Rule(x1['MÉDIA SUJEIRA'] & x2['MÉDIA MANCHA'], y['MÉDIO'])
rule6 = ctrl.Rule(x1['MÉDIA SUJEIRA'] & x2['GRANDE MANCHA'], y['LONGO'])
rule7 = ctrl.Rule(x1['GRANDE SUJEIRA'] & x2['SEM MANCHA'], y['MÉDIO'])
rule8 = ctrl.Rule(x1['GRANDE SUJEIRA'] & x2['MÉDIA MANCHA'], y['LONGO'])
rule9 = ctrl.Rule(x1['GRANDE SUJEIRA'] & x2['GRANDE MANCHA'], y['MUITO LONGO'])

tempo_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
tempo_simulador = ctrl.ControlSystemSimulation(tempo_ctrl)

# Entrando com alguns valores para qualidade da dinheiro e do pessoal
tempo_simulador.input['Sujeira'] = 30
tempo_simulador.input['Mancha'] = 1

# Computando o resultado
tempo_simulador.compute()

x1.view(sim=tempo_simulador)
x2.view(sim=tempo_simulador)
y.view(sim=tempo_simulador)
print("O tempo da lavagem será de", tempo_simulador.output['Tempo'], "%")
