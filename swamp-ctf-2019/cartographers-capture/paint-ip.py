from PIL import Image, ImageDraw
from socket import inet_aton
import struct

def ip2long(ip):
    packed = inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng

squaresize = 10
blanksize = 2

SIZE_X = 32*(squaresize+blanksize)
SIZE_Y =  8*(squaresize+blanksize)

print("Image Size %sx%s" %(SIZE_X, SIZE_Y))

image = Image.new('RGB', (SIZE_X, SIZE_Y), (255, 255, 255))
draw = ImageDraw.Draw(image)

with open('ip_addresses.txt') as f:
	i = 0
	ip_x = []
	ip_y = []

	for line in f.readlines():
		ip = ip2long(line.strip())

		if i%2 == 0:
			ip_y.append(ip)
		else:
			ip_x.append(ip)
		i += 1

	# Uniq+Sort IPs
	ip_x_uniq = list(set(ip_x))
	ip_y_uniq = list(set(ip_y))
	ip_x_uniq.sort()
	ip_y_uniq.sort()
	x_values = {}
	y_values = {}
	for i in range(len(ip_x_uniq)):
		x_values[ip_x_uniq[i]] = i
	for i in range(len(ip_y_uniq)):
		y_values[ip_y_uniq[i]] = i

	# Paint
	for i in range(len(ip_x)):
		#x = x_values[ip_x[i]]*(squaresize+blanksize)
		#y = y_values[ip_y[i]]*(squaresize+blanksize)
		#draw.rectangle((x, y, x+squaresize, y+squaresize), fill=0)

		x = SIZE_X - x_values[ip_x[i]]*(squaresize+blanksize)
		y = SIZE_Y - y_values[ip_y[i]]*(squaresize+blanksize)
		draw.rectangle((x, y, x-squaresize, y-squaresize), fill=0)

	image.save('flag.bmp')
