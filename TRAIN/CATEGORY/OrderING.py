import os
import PIL.Image as Image


start = 3000
for i in range(start,start+1000):
    f = Image.open(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TRAIN\CATEGORY\GAPS&BLOCKS/{}.jpg'.format(i))
    # f = f.convert("RGB")
    filesRENAME = os.listdir(r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TRAIN\CATEGORY\4")
    name = len(filesRENAME)
    f.save(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TRAIN\CATEGORY\4/{}.jpg'.format(name), dpi=(300,300), quality=95)