from PIL import Image as pil
import os
import sys
import numpy
import random

def create_noisy_images(base_folder, result_folder, copies=1000):
  for base_image in os.listdir(base_folder):
    image_name = os.path.splitext(base_image)[0]
    clone_folder = result_folder + '/' + image_name
    os.makedirs(result_folder + '/' + image_name)
    make_noisy_clones(base_folder + '/' + base_image, clone_folder, image_name, copies)

#Takes an image in array form and returns it with added noise
def add_noise(image):
  noisy_image = image.copy()
  (height, width) = noisy_image.shape
  for i, row in enumerate(noisy_image):
    for j, pixel in enumerate(row):
      if noisy_image[i][j] == 0:
          numrand = random.randrange(0, 4)
          for x in xrange(0, numrand):
            xrand = random.randrange(0, 3) - 1
            yrand = random.randrange(0, 3) - 1
            if ((0 <= (i + xrand) < height) and (0 <= (j + yrand) < width)):
              test = random.randrange(0, 10)
              if (test <= 4):
                noisy_image[i + xrand][j + yrand] = 0
              else:
                noisy_image[i + xrand][j + yrand] = 255 - pixel

  return noisy_image

def make_noisy_clones(base_file, result_folder, name, copies):
  #open the file and convert it into a monochromatic format
  base_image = pil.open(base_file).convert("L")
  image_array = numpy.array(base_image)

  for x in range(copies):
    clone_array = add_noise(image_array)
    clone_image = pil.fromarray(clone_array)

    clone_path = result_folder + '/' + name + '.' + str(x+1) + '.png'
    clone_image.save(clone_path)

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "USAGE: python noisy.py base_folder result_folder"
    sys.exit(1)

  base_folder = sys.argv[1]
  result_folder = sys.argv[2]

  for base_image in os.listdir(base_folder):
    image_name = os.path.splitext(base_image)[0]
    make_noisy_clones(base_folder + '/' + base_image, result_folder + '/' + image_name, 100)


