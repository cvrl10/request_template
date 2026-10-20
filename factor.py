import json
import re
from wsgiref.simple_server import demo_app

fd = open('molar_mass.json', mode='r')
molar_mass = json.load(fd)
fd.close()

def parse_formula(compound: str):
    formula = {}

    for element, subscript in re.findall(r'([A-Z][a-z]?)(\d*)', compound):
        formula[element] = formula.get(element, 0) + int(subscript or 1)

    return formula


def calculate_factor(analyte: str, formula: dict, decimal: int = 3):
    def subset(analyte: str, orignal: dict):
        analyte = parse_formula(analyte).keys()
        print(f'analyte to factor: {analyte}')
        _subset = dict(filter(lambda pair: pair[0] in analyte, orignal.items()))
        return _subset

    def mass(formula: dict):
        for element, subscript in formula.items():
            print(f'{subscript}*{element} = {subscript}*{molar_mass[element]} = {subscript*molar_mass[element]}')
            formula[element] = formula[element]*molar_mass[element]

        return sum(formula.values())

    denominator = subset(analyte, formula)
    numerator = mass(formula)
    print(f'{numerator} g/mol')


    #denominator = parse_formula(analyte)
    #denominator = subset(analyte, formula)
    denominator = mass(denominator)

    factor = numerator / denominator
    factor = round(factor, decimal)
    print(f'factor = {factor}')
    return factor


sentinel = True

while sentinel != 'END':
    formula = input()
    formula, analyte = formula.split(' ')
    print(formula)
    #print(parse_formula(formula))
    s = parse_formula(formula)
    print(s)
    calculate_factor(analyte, s)
    sentinel = formula
    print()

