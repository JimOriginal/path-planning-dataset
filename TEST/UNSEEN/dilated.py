
import cv2
import numpy as np
from PIL import Image

if __name__ == '__main__':



    # j=0
    # for i in range(2077): #closing operation
    #     # img = Image.open('train/label/%d.png'%i)
    #     if i in fail_list:
    #         continue
    #     else:
    #         img = cv2.imread(r'D:\Desktop\Unet RRT star\demo\train\label\%d.png'%i,0)
    #         # print(type(img))
    #         kernel = np.ones((15, 15), np.uint8)
    #         closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    #         # cv2.imshow('%d'%i,closing)
    #         # cv2.waitKey()
    #         # print(i)
    #         cv2.imwrite(r"D:\Desktop\Unet RRT star\demo\train\label_closing\%d_close.jpg" % j,closing)
    #         j+=1



    # j = 0
    # for i in range(2078):  #transfer to jpg
    #     if i in fail_list:
    #         continue
    #     else:
    #         map = Image.open(r"D:\Desktop\Unet RRT star\demo\train\map_wo_point\%d.png" % i)
    #     # label = Image.open(r"D:\Desktop\Unet RRT star\demo\train\label\%d.png" % i)
    #         map.save(r"D:\Desktop\Unet RRT star\demo\train\train_final_wo_point\%d.jpg" % j)
    #
    #     # label.save(r"D:\Desktop\Unet RRT star\demo\train\label\%d.jpg" % i)
    #         map = Image.open(r"D:\Desktop\Unet RRT star\demo\train\map_point\%d.png" % i)
    #         map.save(r"D:\Desktop\Unet RRT star\demo\train\train_final_point\%d.jpg" % j)
    #         j+=1


    # for k in range(12000): #delete obstable
    #
    #     # map = cv2.imread(r'D:\Desktop\Unet RRT star\Unet-master-pytorch-v3\RRT\design_map_wo_coord\%d.jpg'% k)
    #     label = cv2.imread(r"C:\Users\huang\Desktop\Dataset\result\%d.jpg" %k,cv2.IMREAD_GRAYSCALE)
    #     ret,label_binary = cv2.threshold(label,127,255,cv2.THRESH_BINARY)
    #     # map = Image.open(r"D:\Desktop\Unet RRT star\demo\train\map\%d.png" % k)
    #     # label = Image.open(r"D:\Desktop\Unet RRT star\demo\train\label\%d.png" % k)
    #     im = Image.fromarray(label_binary)
    #     im.save(r"C:\Users\huang\Desktop\Dataset\result_binary\{}.jpg".format(k), dpi=(300, 300), quality=95)
    #     print("第%d张二值化label"%k)



    for k in range(12000): #dilate operation

        label_binary = cv2.imread(r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TRAIN\PATH [2PIXEL]\%d.jpg" % k)

        kernel = np.uint8(np.ones((25,25))) #30，25, 20
        label_binary_dilate = cv2.dilate(label_binary,kernel)
        im = Image.fromarray(label_binary_dilate)
        im.save(r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TRAIN\PATH [25PIXEL]\{}.jpg".format(k), dpi=(300, 300), quality=95)
        print("第%d张膨胀化label"%k)
        # label_binary_dilate = cv2.cvtColor(label_binary_dilate, cv2.COLOR_BGR2GRAY)
        # ret, label_binary_dilate = cv2.threshold(label_binary_dilate, 127, 255, cv2.THRESH_BINARY)
        #
        # cv2.imwrite(r"D:\Desktop\Unet RRT star\Unet-master-pytorch-v3\RRT\singlepath_groundtruth\%d.jpg"% k,label_binary_dilate)

    #
    # for k in range(2000): # quzhangaiwu
    #     map = cv2.imread(r'D:\Desktop\Unet RRT star\demo\train\singlemap\%d.jpg' % k)
    #     label = cv2.imread(r"D:\Desktop\Unet RRT star\demo\train\singlepath_groundtruth\%d.jpg" % k,
    #                        cv2.IMREAD_GRAYSCALE)
    #     ret, label_binary = cv2.threshold(label, 127, 255, cv2.THRESH_BINARY)
    #     # map = Image.open(r"D:\Desktop\Unet RRT star\demo\train\map\%d.png" % k)
    #     # label = Image.open(r"D:\Desktop\Unet RRT star\demo\train\label\%d.png" % k)
    #
    #     map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
    #
    #     # print(map.shape)
    #
    #     # cv2.imshow('%d'%k,map)
    #     # cv2.waitKey()
    #
    #     for i in range(512):
    #         for j in range(512):
    #             if map[j][i] <= 150:
    #                 label_binary[j][i] = 0
    #     cv2.imwrite(r'D:\Desktop\Unet RRT star\demo\train\singlepath_groundtruth_no_obstacle\%d.jpg'%k,label_binary)