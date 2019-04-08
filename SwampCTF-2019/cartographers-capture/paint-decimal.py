from PIL import Image, ImageDraw
from socket import inet_aton
import struct

def ip2long(ip):
	packed = inet_aton(ip)
	lng = struct.unpack("!L", packed)[0]
	return lng

squaresize = 18

SIZE_X = 600
SIZE_Y = 420

image = Image.new('RGB', (SIZE_X, SIZE_Y), (255, 255, 255))
draw = ImageDraw.Draw(image)


with open('ip_addresses.txt') as f:
	i = 0
	for line in f.readlines():

		ip = ip2long(line.strip())

		if i%2 == 0:
			ipy = ip - 1106031935
		else:
			ipx = ip - 3265569056

			x = SIZE_X - ipx
			y = SIZE_Y - ipy
			draw.rectangle((x, y, x-squaresize, y-squaresize), fill=0)

		i += 1

image.save('flag.bmp')
