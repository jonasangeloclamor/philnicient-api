import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy import membership as mfs
import pandas as pd
import matplotlib.pyplot as plt

# Define fuzzy variables
score = ctrl.Antecedent(np.arange(0, 8, 1), 'score')
cri = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'cri')
understanding = ctrl.Consequent(np.arange(0, 101, 1), 'understanding')

# Define membership functions for score
score['low'] = fuzz.trapmf(score.universe, [0, 0, 1, 2])
score['medium'] = fuzz.trapmf(score.universe, [2, 2, 5, 5])
score['high'] = fuzz.trapmf(score.universe, [6, 6, 7, 7])

# Define membership functions for cri
cri['low'] = fuzz.trapmf(cri.universe, [0, 0, 2, 2.5])   # Low CRI (0 to 2.5)
cri['med'] = fuzz.trimf(cri.universe, [2.4, 3, 3.6])     # Medium CRI (2.6 to 3.4)
cri['high'] = fuzz.trapmf(cri.universe, [3.5, 3.9, 5, 5])  # High CRI (3.6 to 5)

# Define membership functions for understanding
understanding['does_not_understand'] = fuzz.trimf(understanding.universe, [0, 20, 40])
understanding['misconception'] = fuzz.trimf(understanding.universe, [21, 40, 60])
understanding['guess'] = fuzz.trimf(understanding.universe, [41, 60, 80])
understanding['understand_but_needs_practice'] = fuzz.trimf(understanding.universe, [61, 80, 100])
understanding['understand'] = fuzz.trimf(understanding.universe, [81, 100, 100])

# Define rules
rule1 = ctrl.Rule(score['high'] & cri['high'], understanding['understand'])
rule2 = ctrl.Rule(score['high'] & cri['low'], understanding['guess'])
rule3 = ctrl.Rule(score['medium'] & cri['high'], understanding['misconception'])
rule4 = ctrl.Rule(score['medium'] & cri['low'], understanding['guess'])
rule5 = ctrl.Rule(score['low'] & cri['high'], understanding['misconception'])
rule6 = ctrl.Rule(score['low'] & cri['low'], understanding['does_not_understand'])
rule7 = ctrl.Rule(score['high'] & cri['med'], understanding['understand_but_needs_practice'])
rule8 = ctrl.Rule(score['medium'] & cri['med'], understanding['misconception'])
rule9 = ctrl.Rule(score['low'] & cri['med'], understanding['misconception'])

# Create control system
understanding_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
understanding_sim = ctrl.ControlSystemSimulation(understanding_ctrl)

# Define function to determine understanding level
def determine_understanding(score_val, cri_val):
    understanding_sim.input['score'] = score_val
    understanding_sim.input['cri'] = cri_val
    understanding_sim.compute()
    return understanding_sim.output['understanding']

# Test the function with sample inputs
score_val = 5
cri_val = 1
understanding_level = determine_understanding(score_val, cri_val)
print("Understanding Level:", understanding_level)
