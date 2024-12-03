import os
import PIL.Image as Image


start = 600
for i in range(start,start+300):
    f = Image.open(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\SEEN\MAP [ORIGINAL]/{}.jpg'.format(i))
    # f = f.convert("RGB")
    filesRENAME = os.listdir(r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\SEEN\CATEGORY\BUGTRAP&BLOCKS")
    name = len(filesRENAME)
    f.save(r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\SEEN\CATEGORY\BUGTRAP&BLOCKS/{}.jpg'.format(name), dpi=(300,300), quality=95)