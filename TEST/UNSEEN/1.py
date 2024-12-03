import os
import PIL.Image as Image


start = 2301
j = 0
for i in range(start,start+300):
    f = Image.open(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TRAIN\MAP [ORIGINAL]/{}.jpg'.format(i))
    f.save(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\SEEN\MAP [ORIGINAL]/{}.jpg'.format(j+600), dpi=(300,300), quality=95)
    j = j +1
    f.save(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\SEEN\CATEGORY\BLCOKS/{}.jpg'.format(j), dpi=(300,300), quality=95)