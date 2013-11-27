import numpy as np
import cStringIO as cst
import re
from PIL import Image as pil
import os

def check_image(image, image_path, exp_height, exp_width):
	if image is None:
		print("Warning: %s is not a valid image!" % (image_path))
	else:
		(act_width, act_height) = image.size
		if (act_width != exp_width):
			print("Warning: %s has width %s, expected %s!" % (image_path, act_width, exp_width))
		if (act_height != exp_height):
			print("Warning: %s has height %s, expected %s!" % (image_path, act_height, exp_height))

def check_file(file_path):
	if (os.path.isfile(file_path)):
		return True
	else:
		print("Warning: %s does not exist! ...skipping..." % (file_path))
		return False

def open_url_canvas(url):
	image_str = re.search(r'base64,(.*)', url).group(1)
	pil_image = cst.StringIO(image_str.decode('base64'))
	return pil_image

def convert_url_to_array(url, img_id, height, width):
	image = open_url_canvas(url)
	if check_image(image, img_id, height, width):
		return convert_image_to_array(image)
	else:
		return None

def open_image(image_path, height, width):
	if check_file(image_path):
		image = pil.open(image_path)
		check_image(image, image_path, height, width)
		return image
	else:
		return None

def convert_array_to_image(array, height, width):
	array = array.flatten()
	print array.shape
	img_array = []
	for row in range(0, height):
		img_array.append(array[row*width : (row+1)*width])
	img_array = np.asarray(img_array, np.uint8) * 255
	return pil.fromarray(img_array)

def convert_image_to_array(image):
	if image is None:
		return None
	else:
		return np.array(image.convert("L")).flatten() / 255

def retrieve_image(image_path, height, width):
	image = open_image(image_path, height, width)
	return convert_image_to_array(image)

def retrieve_image_class(class_path, height, width):
	data = []
	for image_name in os.listdir(class_path):
		image = open_image(class_path + '/' + image_name, height, width)
		data.append(convert_image_to_array(image))
	return data

def retrieve_all_images(root_path, height, width):
	data = []
	for class_dir in os.listdir(root_path):
		class_data = retrieve_image_class(root_path + '/' + class_dir, height, width)
		data.append(class_data)
	return data