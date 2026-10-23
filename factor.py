import json
import re

fd = open('molar_mass.json', mode='r')
molar_mass = json.load(fd)
fd.close()

def parse_formula(compound: str):
    formula = {}

    for element, subscript in re.findall(r'([A-Z][a-z]?)(\d*)', compound):
        formula[element] = formula.get(element, 0) + int(subscript or 1)

    return formula


def calculate_factor(analyte: str, compound: dict, name: str, decimal: int = 3):#name parameter is only for printing
    def subset(analyte: str, compound: dict):
        _subset = parse_formula(analyte)
        print(f'analyte = {analyte}')
        #analyte.keys()
        #print(f'len of {_subset} = {len(_subset)}')
        #print(f'analyte to factor: {_subset}')

        if len(_subset) == 1:
            #_subset = dict(filter(lambda pair: pair[0] in _subset, compound.items()))
            _subset = {analyte: compound[analyte]}
        #else:
            #_subset = parse_formula(analyte)
        print(f'{_subset}')
        return _subset

    def mass(formula: dict):
        for element, subscript in formula.items():
            print(f'{subscript}*{element} = {subscript}*{molar_mass[element]} = {subscript*molar_mass[element]}')
            formula[element] = formula[element]*molar_mass[element]

        return sum(formula.values())

    denominator = subset(analyte, compound)

    print(f'{name}')
    numerator = mass(compound)
    print(f'{name} = {numerator} g/mol')


    #denominator = parse_formula(analyte)
    #denominator = subset(analyte, formula)
    denominator = mass(denominator)

    print(f'{analyte} = {denominator} g/mol')

    factor = numerator / denominator
    factor = round(factor, decimal)
    print(f'{name} = {factor} {analyte}')
    return factor


sentinel = True

while sentinel != 'END':
    formula = input()
    formula, analyte = formula.split(' ')
    print(f'compound = {formula}')
    #print(parse_formula(formula))
    s = parse_formula(compound=formula)
    print(s)
    calculate_factor(analyte=analyte, compound=s, name=formula)
    sentinel = formula
    print()

