# -*- coding: utf-8 -*-
"""
Physical properties

(c) 2018 Frank Roemer; see http://wgserve.de/pyilt2
Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""

import requests

prop2abr = {'Activity': 'a',
 'Adiabatic compressibility': 'kS',
 'Apparent enthalpy': 'Hap',
 'Apparent molar heat capacity': 'capm',
 'Apparent molar volume': 'Vapm',
 'Composition at phase equilibrium': 'Xpeq',
 'Critical pressure': 'Pc',
 'Critical temperature': 'Tc',
 'Density': 'dens',
 'Electrical conductivity': 'econd',
 'Enthalpy': 'H',
 'Enthalpy function {H(T)-H(0)}/T': 'HvT',
 'Enthalpy of dilution': 'Hdil',
 'Enthalpy of mixing of a binary solvent with component': 'Hmix',
 'Enthalpy of transition or fusion': 'Hfus',
 'Enthalpy of vaporization or sublimation': 'Hvap',
 'Entropy': 'S',
 'Equilibrium pressure': 'Peq',
 'Equilibrium temperature': 'Teq',
 'Eutectic composition': 'Xeut',
 'Eutectic temperature': 'Teut',
 'Excess enthalpy': 'Hex',
 'Excess volume': 'Vex',
 'Heat capacity at constant pressure': 'cp',
 'Heat capacity at constant volume': 'cv',
 'Heat capacity at vapor saturation pressure': 'cpe',
 "Henry's Law constant": 'Hc',
 'Interfacial tension': 's',
 'Isobaric coefficient of volume expansion': 'aV',
 'Isothermal compressibility': 'kT',
 'Monotectic temperature': 'Tmot',
 'Normal boiling temperature': 'Tb',
 'Normal melting temperature': 'Tm',
 'Osmotic coefficient': 'phi',
 'Ostwald coefficient': 'L',
 'Partial molar enthalpy': 'Hpm',
 'Partial molar volume': 'Vpm',
 'Refractive index': 'n',
 'Relative permittivity': 'rperm',
 'Self-diffusion coefficient': 'Dself',
 'Speed of sound': 'sos',
 'Surface tension liquid-gas': 'slg',
 'Thermal conductivity': 'Tcond',
 'Thermal diffusivity': 'Dterm',
 'Tieline': 'tline',
 'Tracer diffusion coefficient': 'Dtrac',
 'Upper consolute composition': 'Xucon',
 'Upper consolute pressure': 'Pucon',
 'Upper consolute temperature': 'Tucon',
 'Viscosity': 'visc'}

abr2prop = {v: k for k, v in prop2abr.items()}

proplistUrl = 'https://ilthermo.boulder.nist.gov/ILT2/ilprpls'

r = requests.get(proplistUrl)
prpDict = r.json()

prpNames = []
prpKeys = []
for pcls in prpDict['plist']:
    pcls['name'] = map(str.strip, pcls['name'])
    prpNames += pcls['name']
    prpKeys += pcls['key']
prop2key = dict(zip(prpNames, prpKeys))