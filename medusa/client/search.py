#!/usr/bin/env python
#coding:utf-8
#A*算法思路
#1，先判断两点之间是否有直线可走,如果有那么直接走直线,如果没有进行A*算法
#2，把起始格添加到开启列表。
#3，重复如下的工作：
#a) 寻找开启列表中F值最低的格子。我们称它为当前格。
#b) 把它切换到关闭列表。
#c) 对相邻的8格中的每一个？
#* 如果它不可通过或者已经在关闭列表中，略过它。反之如下。
#* 如果它不在开启列表中，把它添加进去。把当前格作为这一格的父节点。记录这一格的F,G,和H值。
#* 如果它已经在开启列表中，用G值为参考检查新的路径是否更好。更低的G值意味着更好的路径。如果是这样，就把这一格的父节点改成当前格，并且重新计算这一格的G和F值。如果你保持你的开启列表按F值排序，改变之后你可能需要重新对开启列表排序。
#d) 停止，当你
#* 把目标格添加进了关闭列表(注解)，这时候路径被找到，或者
#* 没有找到目标格，开启列表已经空了。这时候，路径不存在。
#3.保存路径。从目标格开始，沿着每一格的父节点移动直到回到起始格。这就是你的路径。

map=[
'#####################',
'#..S#..............##',
'#...#....############',
'#...#E..............#',
'#.#################.#',
'#.........#.........#',
'#.....#....#........#',
'#...................#',
'#####################'
]

# map=[
# '#####################',
# '#..S..............E#',
# '#...#....############',
# '#...#...............#',
# '#.#################.#',
# '#.........#.........#',
# '#.....#....#........#',
# '#...................#',
# '#####################'
# ]

def find_nearby(map, POINT_E):
    map_height = len(map)
    map_width = len(map[0])
    (row, column) = POINT_E
    temp = 0
    while 1:
        increment = 0
        for i in vec:
            if 0 <= row+i[0]+increment <= map_height and 0 <= column+i[1]+increment <= map_width: 
                if map[row+i[0]+increment][column+i[1]+increment] != wall:
                    temp = 1
                    POINT_E = (row+i[0]+increment, column+i[1]+increment)
                    break
        if temp:
            break
        else:
            increment += 1
    return POINT_E

def assert_has_line(map, POINT_S, POINT_E, wall):
    walk_lines = True
    if POINT_S[0] == POINT_E[0]:
        for i in range(POINT_S[1]+1, POINT_E[1]+1):
            if map[POINT_S[0]][i] == wall:
                walk_lines = False
    elif POINT_S[1] == POINT_E[1]:
        for i in range(POINT_S[0]+1, POINT_E[0]+1):
            if map[i][POINT_S[1]] == wall:
                walk_lines = False
    else:
        walk_lines = False
    return walk_lines

def get_g_value(point, curr):
    edge = 14
    if point[0] == curr[point_index][0] or point[1] == curr[point_index][1]:
        edge = 10
    return curr[g_value_index] + edge

def get_h_value(point, POINT_E):
    h_value = (abs(POINT_E[0] - point[0])+abs(POINT_E[1] - point[1])) * 10
    return h_value

def add_open_list(open_list, curr):
    f_parent = open_list[0][f_parent_index]
    if f_parent == None:
        open_list[0][f_parent_index] = curr
    else:
        while f_parent != None:
            temp_parent = f_parent
            f_parent = f_parent[f_parent_index]

        temp_parent[f_parent_index] = curr
    return open_list

def print_way(curr):
    path = []
    while curr:
        p = curr[point_index]
        if map[p[0]][p[1]] != 'S' and map[p[0]][p[1]] != 'E':
            map[p[0]][p[1]] = 'O'
        path.append(p)
        curr = curr[f_parent_index]
    path.reverse()
    print path
    for i in range(0, len(map)):
        print ''.join(map[i])

def a_star():

    global point_index
    global g_value_index
    global h_value_index
    global f_value_index
    global f_parent_index
    global wall
    global vec

    point_index = 0
    g_value_index = 1
    h_value_index = 2
    f_value_index = 3
    f_parent_index = 4

    wall = '#'
    vec = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

    close_list = [] #关闭点列表
    open_list = []  #打开点列表

    #寻找出开始点和结束点
    for row in range(0, len(map)):
        map[row] = list(map[row])
        for column in range(0, len(map[row])):
            if map[row][column] == 'S':
                POINT_S = (row, column)
            elif map[row][column] == 'E':
              POINT_E = (row, column)

    #初始化open_list,先把起码放入
    open_list.append([POINT_S, 0, 40, 40, None])
    #当前点
    curr = None

    # map[row][column] = wall
    if map[row][column] == wall:
        POINT_E = find_nearby(map, POINT_E)
    # print POINT_E

    if assert_has_line(map, POINT_S, POINT_E, wall):
        if POINT_S[0] == POINT_E[0]:
            for i in range(POINT_S[1]+1, POINT_E[1]+1):
                curr = [(POINT_S[0], i), 0, 40, 40, None]
                open_list = add_open_list(open_list, curr)
        elif POINT_S[1] == POINT_E[1]:
            for i in range(POINT_S[0]+1, POINT_E[0]+1):
                curr = [(i, POINT_S[1]), 0, 40, 40, None]
                open_list[item][f_parent_index] = curr
        print_way(open_list[0])

    else:
        while len(open_list):
            curr = open_list[0]

            for i in range(0, len(open_list)):
                if open_list[i][f_value_index] < curr[f_value_index]:
                    curr = open_list[i]

            open_list.remove(curr)
            close_list.append(curr)

            if curr[point_index] == POINT_E:
                break

            for i in vec:
                p = (curr[point_index][0] + i[0], curr[point_index][1] + i[1])

                #如果该点在关闭列表中直接退出
                closed = False
                for item in close_list:
                    if item[point_index] == p:
                        closed = True
                        break

                if map[p[0]][p[1]] == wall or closed:
                    continue

                opened = False
                for item in range(0, len(open_list)):
                    if open_list[item][point_index] == p:
                        opened = True
                        break
                g_value = get_g_value(p, curr)
                h_value = get_h_value(p, POINT_E)
                f_value = g_value + h_value
                if opened:
                    if g_value < open_list[item][g_value_index]:
                        open_list[item][f_parent_index] = curr
                        open_list[item][g_value_index] = g_value
                        open_list[item][f_value_index] = f_value
                else:
                    open_list.append([p, g_value, h_value, f_value, curr])

        print_way(curr)


if __name__ == "__main__":
    a_star()