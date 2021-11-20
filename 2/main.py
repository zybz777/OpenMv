import sensor, image, time
import car
from pid import PID
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()
green_threshold   = (76, 96, -110, -30, 8, 66)
size_threshold = 2000
x_pid = PID(p=0.5, i=1, imax=100)
h_pid = PID(p=0.05, i=0.1, imax=50)
def find_max(blobs):
	max_size=0
	for blob in blobs:
		if blob[2]*blob[3] > max_size:
			max_blob=blob
			max_size = blob[2]*blob[3]
	return max_blob
while(True):
	clock.tick()
	img = sensor.snapshot()
	blobs = img.find_blobs([green_threshold])
	if blobs:
		max_blob = find_max(blobs)
		x_error = max_blob[5]-img.width()/2
		h_error = max_blob[2]*max_blob[3]-size_threshold
		print("x error: ", x_error)
		'''
		for b in blobs:
			img.draw_rectangle(b[0:4])
			img.draw_cross(b[5], b[6])
		'''
		img.draw_rectangle(max_blob[0:4])
		img.draw_cross(max_blob[5], max_blob[6])
		x_output=x_pid.get_pid(x_error,1)
		h_output=h_pid.get_pid(h_error,1)
		print("h_output",h_output)
		car.run(-h_output-x_output,-h_output+x_output)
	else:
		car.run(18,-18)