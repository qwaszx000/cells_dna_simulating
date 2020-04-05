#color calculations
def RGBToInt(rgb: str):
	rgb = rgb.replace("#", "")
	rgb_int = int(rgb, 16)

	return rgb_int

def IntToRGB(rgb_int: int):
	rgb = "#" + str(hex(rgb_int)).replace("0x", "")
	return rgb