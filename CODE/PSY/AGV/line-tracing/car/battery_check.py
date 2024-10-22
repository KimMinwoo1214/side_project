from pymycobot.myagv import MyAgv

MA = MyAgv('/dev/ttyAMA2', 115200)

print(MA.get_battery_info())
