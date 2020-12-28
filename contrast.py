import cv2
import numpy as np
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-f', help="Path to the input photo", type=str)
# parser.add_argument("-o", "--output", dest="outputPath", help="Provide PATH to photo")
parser.add_argument("-n", "--name", dest="nameFile", help="filename")

args = parser.parse_args()

image = cv2.imread(cv2.samples.findFile(args.f))
if image is None:
    print('Could not open or find the image: ', args.input)
    exit(0)

lab_img = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab_img)

percent_of_pixel = len(l.flat) * 0.7        # 70% of pixels should be good in order to not fix contrast

print("pixels: ", percent_of_pixel)         # number of pixels checking

counter = 0
for y in l.flat:
    if y < 20 or y > 200:
        counter+=1
        # amount of samples
        if counter > percent_of_pixel:
            break

jsondata={}
if counter <= percent_of_pixel:
    print('Picture needs contrast fix')

    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
    clahe_img = clahe.apply(l)

    updated_lab_img = cv2.merge((clahe_img,a,b))
    CLAHE_img = cv2.cvtColor(updated_lab_img, cv2.COLOR_LAB2BGR)

    # cv2.imshow("original", image)
    # cv2.imshow("clahe", CLAHE_img)
    
    cv2.imwrite(str('./tmp/out-contrast-' + str(args.nameFile)),CLAHE_img)
    # cv2.imwrite(str(args.f.split('.')[0])+'_fixed_photo.png',CLAHE_img)
    jsondata['contrast_fix'] = True

else:
    print('Picture does not need contrast fix')
    jsondata['contrast_fix'] = False

print(jsondata)                 # json data print

with open('./tmp/output1.json', 'w') as outfile:
    json.dump(jsondata, outfile) # save to json file

