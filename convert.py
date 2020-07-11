# This Project convert an image by a dixce-made picture
# In this program I do not use dice number 6. because number 5 is more suitable for darker blocks
import sys
from PIL import Image, ImageOps
import numpy as np
import argparse
#set the arguments for command line
parser = argparse.ArgumentParser(description="Convert image To dice matrix")
parser.add_argument('-n', '--name', help='Enter yot filename to convert', required=True)
parser.add_argument('-col','--column',  help='Select number of dices column. default is 100', default=100)
args = vars(parser.parse_args())

# Get the picture file name from the command line
pic_name = args['name']

# number of Blocks in X dimention
block_no_x = args['column']

# set the math of dice images
dice_path= "dices\\"

# width and height of dice image
dice_w , dice_h = (32,32)
# Number of dices used for the picture
statistcs= [0,0,0,0,0,0]

# This function normalize picture pixel color to range of 1 to 6
def normalize(buffer):
    t= (buffer-buffer.min())/(buffer.max()-buffer.min())
    return np.floor(t/0.166)

# This function select proper dice image for a block of image
def select(number):
    global statistcs
    if number<1: number=1
    elif number>=6: number =5
    statistcs[int(number)]+=1
    im= Image.open(dice_path+str(number)[0]+'.png')
    return im

img = Image.open(pic_name)
img2 = ImageOps.grayscale(img)

w,h = img2.size
px = img2.load()
bw=bh = w // block_no_x
block_no_y = h // bh
buffer= np.zeros((block_no_x,block_no_y))

# This part of code devide the image into blocks and calculate the average of darkness of the bolcks.
for i in range(0, block_no_x):
    for j in range(0,block_no_y):
        s=0
        for k in range(1, bw):
            for l in range(1, bh):
                s+= px[i * bw + k, j * bh + l]
        s = s//(bw*bh)
        buffer[i,j]=255-s

buffer = normalize(buffer)
# make a new image base on dice matrix
new_pic=Image.new('RGB', (block_no_x * dice_w, block_no_y * dice_h), color=(100, 100, 100))
for i in range(0, block_no_x):
     for j in range(0,block_no_y):
         new_pic.paste(select(buffer[i,j]), (i * dice_w, j * dice_h))

statistcs[0]=sum(statistcs[1:])
output_name= pic_name[:pic_name.find('.')]+'.png'
new_pic.save(output_name)
print("Image Converted!")
print("Total Dice used: %d | One: %d , Two: %d , Three: %d, Four: %d, Five: %d"%tuple(statistcs))