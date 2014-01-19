from PIL import Image as pil
import os
import sys
import numpy
import random

# A python class used to generate noise on a set of images

# Creates the noisy images from the base images
def create_noisy_images(base_folder, result_folder, copies=1000):
  for base_image in os.listdir(base_folder):
    image_name = os.path.splitext(base_image)[0]
    clone_folder = result_folder + '/' + image_name
    os.makedirs(result_folder + '/' + image_name)
    make_noisy_clones(base_folder + '/' + base_image, clone_folder, image_name, copies)

# Takes an image in array form and returns it with added noise
def add_noise(image):
  noisy_image = image.copy()
  (height, width) = noisy_image.shape
  # Loops through each column
  for i, row in enumerate(noisy_image):
    # Loops through each pixel
    for j, pixel in enumerate(row):
      # If the pixel contains a black value and is over a threshold
      if noisy_image[i][j] == 0 and random.random() > 0.8:
          # Generates a threshold
          numrand = random.randrange(0, 4)
          # For each value in the threshold
          for x in xrange(0, numrand):
            # Generates the co-ordinates for a neighbour pixel
            xrand = random.randrange(0, 3) - 1
            yrand = random.randrange(0, 3) - 1
            # Checks to make sure pixel is in bound
            if ((0 <= (i + xrand) < height) and (0 <= (j + yrand) < width)):
              # Another threshold to determine whether to turn the pixel on or off
              test = random.randrange(0, 10)
              if (test <= 4):
                # Turns the pixel on
                noisy_image[i + xrand][j + yrand] = 0
              else:
                # Turns the pixel off
                noisy_image[i + xrand][j + yrand] = 255 - pixel

  return noisy_image

# Makes the noisy clones from a base image
def make_noisy_clones(base_file, result_folder, name, copies):
  # open the file and convert it into a monochromatic format
  base_image = pil.open(base_file).convert("L")
  image_array = numpy.array(base_image)

  # For each required copy
  for x in range(copies):
    # Creates a noisy clone image
    clone_array = add_noise(image_array)
    clone_image = pil.fromarray(clone_array)

    # Generates the path for the clone and saves it
    clone_path = result_folder + '/' + name + '.' + str(x+1) + '.png'
    clone_image.save(clone_path)

# Allows the noisy generator to be run as main
if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "USAGE: python noisy.py base_folder result_folder"
    sys.exit(1)

  base_folder = sys.argv[1]
  result_folder = sys.argv[2]

  for base_image in os.listdir(base_folder):
    image_name = os.path.splitext(base_image)[0]
    make_noisy_clones(base_folder + '/' + base_image, result_folder + '/' + image_name, 100)


