from collections import defaultdict
from heapq import *

from collections import defaultdict
from heapq import *
import copy
from matplotlib import pyplot as plt

'''
dijkstra with min heap
'''
def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c, r))
    # dist records the min value of each node in heap.
    q, seen, dist = [(0, f, ())], set(), {f: 0}
    while q:
        (cost, v1, path) = heappop(q)
        if v1 in seen:
            continue

        seen.add(v1)
        path += (v1,)
        if v1 == t:
            return cost, path

        for c, v2 in g.get(v1, ()):
            if v2 in seen:
                continue
            # Not every edge will be calculated. The edge which can improve the value of node in heap will be useful.
            if v2 not in dist or cost+c < dist[v2]:
                dist[v2] = cost+c
                heappush(q, (cost+c, v2, path))

    return float("inf"), None


'''
draw the whole graph
'''


def first(ys, xs, all_y, all_x):
    x_number_list = xs
    y_number_list = ys
    x_help = []
    y_help = []
    plt.scatter(x_number_list, y_number_list, edgecolors=None, c='blue')
    for i in range(len(names)):
        plt.annotate(names[i], (float(x_number_list[i]), float(y_number_list[i])))
    for k in range(len(all_x) - 1):
        if k % 2 == 0:
            x_help.append([all_x[k], all_x[k+1]])
            y_help.append([all_y[k], all_y[k+1]])
    for j in range(len(x_help)):
        plt.plot(x_help[j], y_help[j], 'r')
    plt.show()


'''
drawing the paths for each car
'''


def draw_car_path(names, ys, xs, x_values, y_values, all_x, all_y):
    x_number_list = xs
    y_number_list = ys
    x_help = []
    y_help = []
    plt.scatter(x_number_list, y_number_list, edgecolors=None, c='blue')
    for i in range(len(names)):
        plt.annotate(names[i], (float(x_number_list[i]), float(y_number_list[i])))

    for k in range(len(all_x) - 1):
        if k % 2 == 0:
            x_help.append([all_x[k], all_x[k+1]])
            y_help.append([all_y[k], all_y[k+1]])
    for j in range(len(x_help)):
        plt.plot(x_help[j], y_help[j], 'r')

    plt.scatter(x_values, y_values)
    plt.plot(x_values, y_values)
    plt.show()


if __name__ == "__main__":
    cars = []
    terafic, time = 0, 0
    edges = []
    edges_copy = []
    edges_copy_terafic = []
    points = []
    inputsNum = input().split()
    x1,x2,y1,y2 = 0, 0, 0, 0
    ys = []
    xs = []
    all_y = []
    all_x = []
    names = []
    '''
    In this section we get the inputs for graph and save the x's and y's
    we calculate the length between edges and save them into variable edges
    we save the weight between edges in variable edges_copy
    we save the traffic and time in variable edges_copy_terafic 
    '''
    edgeNum, verticleNum = int(inputsNum[0]), int(inputsNum[1])
    for i in range(edgeNum):
        info = input()
        points.append(info)
        infos = info.split()
        ys.append(float(infos[1]))
        xs.append(float(infos[2]))
        names.append(infos[0])
    for j in range(verticleNum):
        edge = []
        edge_copy = []
        verticle = input().split()
        for k in range(len(points)):
            sth = points[k].split()
            if sth[0] == verticle[0]:
                y1 = float(sth[1])
                x1 = float(sth[2])
                all_y.append(y1)
                all_x.append(x1)
            if sth[0] == verticle[1]:
                y2 = float(sth[1])
                x2 = float(sth[2])
                all_y.append(y2)
                all_x.append(x2)
        length = pow((y2-y1)*(y2-y1) + (x2-x1)*(x2-x1), 1/2)
        edge.append(verticle[0])
        edge.append(verticle[1])
        edge_copy.append(verticle[0])
        edge_copy.append(verticle[1])
        edge_copy.append(terafic)
        edge_copy.append(time)

        edge.append(length)
        edges.append(edge)
        edges_copy_terafic.append(edge_copy)
        edge = []
        edge_copy = []
        edge_copy.append(verticle[1])
        edge_copy.append(verticle[0])
        edge_copy.append(terafic)
        edge_copy.append(time)
        edges_copy_terafic.append(edge_copy)

        edge.append(verticle[1])
        edge.append(verticle[0])
        edge.append(length)
        edges.append(edge)
        edges_copy = copy.deepcopy(edges)
    help = []
    requests = []
    car_num = int(input())
    first(ys, xs, all_y, all_x)
    for i in range(car_num):
        requests.append(input())

    '''
    In this section we get the inputs for requests
    we call the dijkstra algorithm if it is the first car
    but if it is not the first car, we check all the previous cars to see if they have arrived or not and correct the traffic and weight
    then we call the dijkstra for the car and change the traffic again
    '''
    for j in range(car_num):
        request = requests[j].split()
        if j == 0:
            notImportant, path = dijkstra(edges, request[1], request[2])
            sum_weight = 0
            if notImportant != float("inf"):
                print("Best Path for Your Car Is ",path)
                for i in range(len(path) - 1):
                    for k in range(len(edges_copy)):
                        if edges_copy[k][0] == path[i] and edges_copy[k][1] == path[i + 1]:
                            sum_weight += edges[k][2]
                            edges_copy_terafic[k][2] += 1
                            weight = edges_copy[k][2] * (1 + 0.3 * edges_copy_terafic[k][2])
                            edges[k][2] = weight
                        if edges_copy[k][0] == path[i + 1] and edges_copy[k][1] == path[i]:
                            edges_copy_terafic[k][2] += 1
                            weight = edges_copy[k][2] * (1 + 0.3 * edges_copy_terafic[k][2])
                            edges[k][2] = weight
                time = 120 * sum_weight
                for i in range(len(path) - 1):
                    for k in range(len(edges_copy)):
                        if edges_copy[k][0] == path[i] and edges_copy[k][1] == path[i + 1]:
                            edges_copy_terafic[k][3] = time
                        if edges_copy[k][0] == path[i + 1] and edges_copy[k][1] == path[i]:
                            edges_copy_terafic[k][3] = time
                help.append(path)
                help.append(time)
                help.append(float(request[0]))
                cars.append(help)
                help = []
                print("It Takes ", time, "Minutes")
                path_y = []
                path_x = []
                for z in range(len(path)):
                    for u in range(len(points)):
                        draw = points[u].split()
                        if path[z] == draw[0]:
                            path_y.append(float(draw[2]))
                            path_x.append(float(draw[1]))
                draw_car_path(names, ys, xs, path_y, path_x, all_x, all_y)

        else:
            time_now = float(request[0])
            n = len(cars) - 1
            while n >= 0:
                if cars[n][1]+ cars[n][2] < time_now:
                    path_change = cars[n][0]
                    cars.remove(cars[n])
                    n -= 1
                else:
                    n -= 1
                    path_change = []
                sum_weight = 0
                for i in range(len(path_change) - 1):
                    sum_weight = 0
                    for k in range(len(edges_copy)):
                        if edges_copy[k][0] == path_change[i] and edges_copy[k][1] == path_change[i + 1]:
                            edges_copy_terafic[k][2] -= 1
                            weight = edges_copy[k][2] * (1 + 0.3 * edges_copy_terafic[k][2])
                            edges[k][2] = weight
                        if edges_copy[k][0] == path_change[i + 1] and edges_copy[k][1] == path_change[i]:
                            edges_copy_terafic[k][2] -= 1
                            weight = edges_copy[k][2] * (1 + 0.3 * edges_copy_terafic[k][2])
                            edges[k][2] = weight

            notImportant, path = dijkstra(edges, request[1], request[2])
            sum_weight = 0
            if notImportant != float("inf"):
                print("Best Path for Your Car Is ",path)
                for i in range(len(path) - 1):
                    for k in range(len(edges_copy)):
                        if edges_copy[k][0] == path[i] and edges_copy[k][1] == path[i + 1]:
                            sum_weight += edges[k][2]
                            edges_copy_terafic[k][2] += 1
                            weight = edges_copy[k][2] * (1 + 0.3 * edges_copy_terafic[k][2])
                            edges[k][2] = weight
                        if edges_copy[k][0] == path[i + 1] and edges_copy[k][1] == path[i]:
                            edges_copy_terafic[k][2] += 1
                            weight = edges_copy[k][2] * (1 + 0.3 * edges_copy_terafic[k][2])
                            edges[k][2] = weight
                time = 120 * sum_weight
                for i in range(len(path) - 1):
                    for k in range(len(edges_copy)):
                        if edges_copy[k][0] == path[i] and edges_copy[k][1] == path[i + 1]:
                            edges_copy_terafic[k][3] = time
                        if edges_copy[k][0] == path[i + 1] and edges_copy[k][1] == path[i]:
                            edges_copy_terafic[k][3] = time
                help.append(path)
                help.append(time)
                help.append(time_now)
                cars.append(help)
                print("It Takes ", time, "Minute")

                help = []
            path_y = []
            path_x = []
            for z in range(len(path)):
                for u in range(len(points)):
                    draw = points[u].split()
                    if path[z] == draw[0]:
                        path_y.append(float(draw[2]))
                        path_x.append(float(draw[1]))
            draw_car_path(names, ys, xs, path_y, path_x, all_x, all_y)



