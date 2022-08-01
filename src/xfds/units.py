from pint import UnitRegistry

ureg = UnitRegistry()

custom_units = """
cfm = 1 * ft^3/min
""".strip()

for custom_unit in custom_units.splitlines():
    ureg.define(custom_unit)
