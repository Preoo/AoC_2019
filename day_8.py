from pathlib import Path
import numpy as np

inputfile = Path('input/day_8')
"""
For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following image layers:

    Layer 1: 123
            456

    Layer 2: 789
            012

The image you received is 25 pixels wide and 6 pixels tall.
"""
input_data = inputfile.read_text()
#input_data = '123456789012'
input_number_seq = (int(i) for i in input_data)
image_dim = (6,25)
#image_dim = (2,3)
pixel_array = np.fromiter(input_number_seq, int)

# Shape is Layers x Rows x Columns 
image = pixel_array.reshape((-1, *image_dim))
#print(image)

# array where ind matches laye index and value is number of 0 in that layer
num_of_0 = np.zeros(image.shape[0], dtype=int)

for index, layer in enumerate(image):
    num_of_0[index] = (layer == 0).sum()

index_of_target_layer = np.argmin(num_of_0)
print(f'We are on layer {index_of_target_layer}')
# On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
target_layer = image[index_of_target_layer]

answer_1 = np.prod([(target_layer == 1).sum(), (target_layer == 2).sum()])
print(f'Answer count(1s)*count(2s) = {answer_1}')

#decoding image when layers are stacked top->down (layer[0] is on top) and pixel values 0:black, 1:white, 2:transparent
#can we go along first axis (depth) and take 1st value where val != 2?
def merge_layers_along_depth(v):
    pix_val = 2
    for px in v:
        if px != 2:
            pix_val = px
            break
    return pix_val

decoded_image = np.apply_along_axis(merge_layers_along_depth, 0, image)

def pretty_print(arr):
    font = {0 : ' ', 1 : '#'}
    for line in arr:
        for c in line:
            print(font[c], end='')
        print('')
     #eyeball it: HGBCF

pretty_print(decoded_image)