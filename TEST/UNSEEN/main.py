import random

import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import random
import math
import time
from PIL import Image

class Node:
    #定义Node类
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None  #通过逆向回溯路径
        self.cost = 100000
    #  x是纵向方向， y是横向， 左上角是零点

def distance(x0,y0,x1,y1):
    d = np.sqrt(np.square(x0-x1)+np.square(y0-y1))
    return d
def get_dis(node1, node2): #两点之间的距离
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
def dis_to_root(node): #当前点到root距离
    total_dis = 0
    while True:
        if node.parent is not None:
            total_dis += get_dis(node, node.parent)
            node = node.parent
        else:
            break
    return total_dis
def random_sample_node(max_bound):
    return Node(random.randint(0, max_bound), random.randint(0, max_bound))
def get_nearest_node(node_list, node):
    dis_list = [get_dis(nd, node) for nd in node_list]
    return node_list[dis_list.index(min(dis_list))]
def check_collision(img_binary, new_node):
    flag = False
    if img_binary[new_node.x][new_node.y] == 0:
        flag = True
    return flag
def check_path(img_binary, node1, node2):
    flag = False
    step_length = max(abs(node1.x - node2.x), abs(node1.y - node2.y))
    x = np.linspace(node1.x, node2.x, step_length + 1)
    y = np.linspace(node1.y, node2.y, step_length + 1)
    for i in range(step_length + 1):
        if check_collision(img_binary, Node(int(x[i]), int(y[i]))):
            flag = True
    return flag
def nodes_in_range(target_node, range, nodes_list): #范围内的点,用于rrt*
    range_nodes = []
    for node in nodes_list:
        if get_dis(target_node, node) <= range and node is not target_node.parent:
            range_nodes.append(node)
    return range_nodes
def RRT(map,startx,starty,goalx,goaly,failnum):

    RRTsuccess = False
    c_best = 5000
    num_sample_nodes = 0
    start = Node(startx,starty)
    goal = Node(goalx,goaly)
    node_list = []
    node_list.append(start)

    if failnum<=10:
        maxsample = 3000
        expandDis = 15
    else:
        maxsample = 6000
        expandDis = 10


    while num_sample_nodes<maxsample:
        num_sample_nodes += 1
        # print(num_sample_nodes)
        rand_node = random_sample_node(map.shape[0] - 1)
        nearest_node = get_nearest_node(node_list, rand_node)
        theta = math.atan2(rand_node.y - nearest_node.y, rand_node.x - nearest_node.x)
        expand_x = nearest_node.x + expandDis * math.cos(theta)
        expand_y = nearest_node.y + expandDis * math.sin(theta)
        if expand_x >= map.shape[0] or expand_y >= map.shape[1] or expand_x <= 0 or expand_y <= 0:
            continue
        new_node = Node(int(expand_x), int(expand_y))
        new_node.parent = nearest_node
        new_node.cost = nearest_node.cost + get_dis(new_node, nearest_node)
            # 检查是否与障碍物重叠
        if check_collision(map, new_node):
            continue
        #检查路径是否穿过障碍物
        if check_path(map, new_node, new_node.parent):
            continue
        #此时，newnode生成了
        node_list.append(new_node)
        range_nodes = nodes_in_range(new_node, 3 * expandDis, node_list)
        # 寻找newnode的新parent
        for nd in range_nodes:
            if get_dis(nd, new_node) + nd.cost < new_node.cost and nd is not goal:
                if not check_path(map, new_node, nd):
                    new_node.parent = nd
                    new_node.cost = get_dis(nd, new_node) + nd.cost

        # 对范围内的节点检查，将newnode作为parent是否减少cost
        for nd in range_nodes:
            if nd is not new_node.parent:
                if get_dis(nd, new_node) + new_node.cost < nd.cost:
                    if not check_path(map, new_node, nd):
                        nd.parent = new_node
                        nd.cost = get_dis(nd, new_node) + new_node.cost
                        # for nt in node_list:
                        #     if nt.parent is not None:
                        #         np = nt.parent
                        #         if np.x==nd.x and np.y==nd.y:
                        #             nt.cost = nd.cost + get_dis(nd,nt)
        # 如果newnode与goalnode距离在expandDis以内
        if get_dis(new_node, goal) < expandDis * 3 and not RRTsuccess:
            if check_path(map, new_node, goal):
                continue
            goal.parent = new_node
            goal.cost = new_node.cost + get_dis(goal, new_node)
            RRTsuccess = True
            node_list.append(goal)
            initial_path_cost = goal.cost
            c_best = initial_path_cost
        if get_dis(new_node, goal) < expandDis * 3 and RRTsuccess:
            if check_path(map, new_node, goal):
                continue
            if goal.cost < c_best:
                c_best = min(goal.cost, c_best)
                goal.parent = new_node
                goal.cost = new_node.cost + get_dis(goal, new_node)
        if dis_to_root(goal) < c_best and RRTsuccess:
            c_best = min(dis_to_root(goal), c_best)
    if RRTsuccess:

        goal_node = goal
        l_tree = [start]

        while True:
            if goal_node.parent is not None:
                l_tree.append(goal_node)
                goal_node = goal_node.parent
            else:
                break
    else:
        l_tree = []
    return RRTsuccess, node_list, l_tree,c_best
def optimalpathgeneration(path,file,path_binarymap,path_RGBmapwithcoordi,path_RGBmapwithpath,path_onlypath,path_sg_coordinate,path_coordinate,path_cost):
    i = 900
    failnum = 0
    # j=0
    while i < 1200:

        print("第{}张地图".format(i))

        maporiginal = cv2.imread(path+"/{}.jpg".format(i))
        maporiginal = cv2.resize(maporiginal,(201,201))
        map = cv2.cvtColor(maporiginal, cv2.COLOR_RGB2GRAY)
        res,map = cv2.threshold(map,127,255,cv2.THRESH_BINARY)
        im = Image.fromarray(map)
        im.save(path_binarymap+r"\{}.jpg".format(i),dpi = (300, 300), quality=95)
        np.array(map).astype(int)
        h = map.shape[0]
        w = map.shape[1]
        hmax = round(h/2)
        wmax = round(w/2)
        flag = False
        while not flag:
            seed = random.randint(0,1)
            if i<600:
                if seed == 0:
                    startx = random.randint(0,hmax-50)
                    starty = random.randint(0,wmax-50)
                    goalx = random.randint(hmax+50,h-1)
                    goaly = random.randint(wmax+50,w-1)
                if seed == 1:
                    startx = random.randint(0,hmax-50)
                    starty = random.randint(wmax+50,w-1)
                    goalx = random.randint(hmax+50,h-1)
                    goaly = random.randint(0,wmax-50)
                d = distance(startx,starty,goalx,goaly)
                if (map[starty][startx]==255) and (map[goaly][goalx]==255) and d>=150:
                    flag = True
            else:
                # if failnum<=10:
                #     if seed == 0:
                #         startx = random.randint(0,hmax-30)
                #         starty = random.randint(0,wmax-30)
                #         goalx = random.randint(hmax+30,h-1)
                #         goaly = random.randint(wmax+30,w-1)
                #     if seed == 1:
                #         startx = random.randint(0,hmax-30)
                #         starty = random.randint(wmax+30,w-1)
                #         goalx = random.randint(hmax+30,h-1)
                #         goaly = random.randint(0,wmax-30)
                #     d = distance(startx,starty,goalx,goaly)
                #     if (map[starty][startx]==255) and (map[goaly][goalx]==255) and d>=175:
                #         flag = True
                # else:
                if seed == 0:
                    startx = random.randint(0, hmax)
                    starty = random.randint(0, wmax)
                    goalx = random.randint(hmax, h - 1)
                    goaly = random.randint(wmax, w - 1)
                if seed == 1:
                    startx = random.randint(0, hmax)
                    starty = random.randint(wmax, w - 1)
                    goalx = random.randint(hmax, h - 1)
                    goaly = random.randint(0, wmax)
                d = distance(startx, starty, goalx, goaly)
                if (map[starty][startx] == 255) and (map[goaly][goalx] == 255) and d >= 150:
                    flag = True
        RRTsuccess, node_list, l_list,c_best = RRT(map,startx,starty,goalx,goaly,failnum)


        # print(len(l_list))

        if RRTsuccess:
            #save map RGB, map with path, path, coordinate
            mapRGBwithcoordi = maporiginal
            cv2.rectangle(mapRGBwithcoordi, (starty - 1, startx - 1), (starty + 1, startx + 1), (0, 0, 255), 2)
            cv2.rectangle(mapRGBwithcoordi, (goaly - 1, goalx - 1), (goaly + 1, goalx + 1), (255, 0, 0), 2)
            mapRGBwithcoordi = cv2.cvtColor(mapRGBwithcoordi, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(mapRGBwithcoordi)
            im.save(path_RGBmapwithcoordi + r"\{}.jpg".format(i), dpi=(300, 300), quality=95)

            mapRGBwithpath = maporiginal
            for nd in l_list:
                if nd.parent is not None:
                    cv2.line(mapRGBwithpath, (nd.y, nd.x), (nd.parent.y, nd.parent.x), (127, 127, 127), 2)
            cv2.line(mapRGBwithpath, (l_list[0].y, l_list[0].x), (l_list[-1].y, l_list[-1].x), (127, 127, 127), 2)
            mapRGBwithpath = cv2.cvtColor(mapRGBwithpath, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(mapRGBwithpath)
            im.save(path_RGBmapwithpath + r"\{}.jpg".format(i), dpi=(300, 300), quality=95)

            onlypath = np.zeros((h, w, 3), np.uint8)
            for nd in l_list:
                if nd.parent is not None:
                    cv2.line(onlypath, (nd.y, nd.x), (nd.parent.y, nd.parent.x), (255, 255, 255), 2)
            cv2.line(onlypath, (l_list[0].y, l_list[0].x), (l_list[-1].y, l_list[-1].x), (255, 255, 255), 2)
            onlypath = cv2.cvtColor(onlypath, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(onlypath)
            im.save(path_onlypath + r"\{}.jpg".format(i), dpi=(300, 300), quality=95)

            f = open(path_sg_coordinate+r"/{}.txt".format(i),'w')
            f.write(str(startx)+"\n")
            f.write(str(starty)+"\n")
            f.write(str(goalx)+"\n")
            f.write(str(goaly)+"\n")

            g = open(path_coordinate + r"/{}.txt".format(i), 'w')
            for t in range(len(l_list)):
                if t is not len(l_list):
                    g.write(str(l_list[t].x)+"\n")
                    g.write(str(l_list[t].y)+"\n")
                else:
                    g.write(str(l_list[t].x+"\n"))
                    g.write(str(l_list[t].y))
            h = open(path_cost + r"/{}.txt".format(i), 'w')
            h.write(str(c_best))

            i += 1
            # j += 1
            failnum = 0
        else:
            failnum += 1
            continue

        # if RRT, save coordinate.txt, map.jpeg, update j
        # if not RRT, j not update, again

if __name__==   "__main__":
    path = r'C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\MAP [ORIGINAL]' # original map
    path_binarymap = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\MAP [BINARY]" #binary map
    path_RGBmapwithcoordi = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\MAP [EXAMPLE]" # RGB map with coordinate
    path_RGBmapwithpath = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\MAP [RESULT]" # RGB map with path
    path_onlypath = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\PATH [2PIXEL]" # only path
    path_sg_coordinate = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\COORDINATE [TARGET&GOAL]"
    path_coordinate = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\COORDINATE [SIGNIFICANT WAYPOINT]"
    path_cost = r"C:\Users\huang\Desktop\OPEN DATASET\DATASET\TEST\UNSEEN\PATH [COST]"
    file = os.listdir(path)
    optimalpathgeneration(path,file,path_binarymap,path_RGBmapwithcoordi,path_RGBmapwithpath,path_onlypath,path_sg_coordinate,path_coordinate,path_cost)