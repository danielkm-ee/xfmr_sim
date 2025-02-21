import numpy as np
import cmath
from tabulate import tabulate
from xfmr import _8341_xfmr

xfmr = _8341_xfmr()

S = 55 # VA
angles = [0, 3, 6, 9, 12]
vr = []
eff = []
for theta in angles:
    print(f"Testing load regulation for {S} VA load with {theta} degree power angle")
    res = xfmr.load_reg(S, theta)
    vr.append(res)
    print("Result: VR = ", res)

for theta in angles:
    print(f"Testing efficiency for {S} VA load with {theta} degree power angle")
    res = xfmr.efficiency(S, theta)
    eff.append(res)
    print("Result: eff. = ", res)

print()
print("Voltage Regulation and Efficiency for 55VA Load")
print(tabulate([ ["Theta"] + angles, ["VReg (%)"] + vr, ["Eff. (%)"] + eff], tablefmt="simple_grid"))

print("Testing Overvoltage, Undervoltage, and Overcurrent")
print("Presenting undervoltage case with V = 100, C_uv = C_ov = 0.9")
res = "undervoltage" if xfmr.voltage_check(100, 0.9, 0.9) else "ok"
print("Result:", res)
if res:
    print("PASS")

print("Presenting overvoltage case with V = 200, C_uv = C_ov = 0.9")
over, under = xfmr.voltage_check(200, 0.9, 0.9)
res = "overvoltage" if over else ("undervolage" if under else "ok")
print("Result:", res)
if res=="overvoltage":
    print("PASS")

print("Presenting overcurrent case with I_line = 600mA, C_i = 0.9")
over = xfmr.current_check(600e-3, 0.9)
res = "overcurrent" if over else "ok"
print("Result:", res)
if res:
    print("PASS")
