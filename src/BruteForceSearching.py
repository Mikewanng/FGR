import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from alg1 import *
from alg2 import *
from alg2k import *
from hopspf import *
from Topo import *
import copy, time
import networkx as nx

# fth作为自变量，单sd,数据保存于代码主文件夹下的txt文件中，运行次数count可以自定义。
# 算法输入为拓扑，源，目的，保真度阈值，请求数量。
# 算法返回值为：路径集，提纯决策集，保真度集，纠缠消耗集，吞吐量集，总吞吐量，寻路时间。

# 算法变量设置
# 总仿真次数
count = 1000
# 模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
topology_fidelity_mode = 0
# 单S-Dpair的请求connection数量
nrof_requests = 100
# Alg1的运行模式，BFS搜索为0，k-shortest为1
alg1_mode = 1
# 链路容量设置
link_capacity = 50
# 保真度的范围
# x=np.arange(0.55,0.95,0.05)
x = np.arange(0.7, 0.71, 0.05)
# 本次仿真中启用的对比算法
enable_Hspf = 1  # 基于跳数的
enable_alg1 = 1
enable_alg2 = 1
# 随机拓扑设置，1代表开启
random_topology = 1
# 0代表每次生成随机的，1代表读取文件中的拓扑
random_topology_mode = 0
random_topology_nodes_num = 15

start_time = time.time()
graph_topology_file_name1 = 'random_topology_nodes_with_nrof_nodes_' + str(random_topology_nodes_num) + '.txt'
graph_topology_file_name2 = 'random_topology_edges_with_nrof_nodes_' + str(random_topology_nodes_num) + '.txt'
filename = 'Single_SDPair_vs_Fidelity.txt'
fp = open(filename, 'w')
# 先写入数据标题
utput_label = 'fth      '
if enable_Hspf == 1:
    utput_label += 'throughput_hopCount      avgFidelity_hopCount      consumption_hopcount      time_hopCount      '
if enable_alg1 == 1:
    utput_label += 'throughput_alg1      avgFidelity_alg1      consumption_alg1      time_alg1      '
if enable_alg2 == 1:
    utput_label += 'throughput_alg2      avgFidelity_alg2      consumption_alg2      time_alg2'
utput_label += '\n'
# output_label = 'fth    tphopcount    tpalg1    tpalg2    tpalg2k    tpalg2k3    tpalg2k4    tpalg2k5    ' \
#                    'avefhopcount    avefalg1    avefalg2    avefalg2k    avefalg2k3    avefalg2k4    avefalg2k5    ' \
#                    'consuhopcount    consualg1    consualg2    consualg2k    consualg2k3    consualg2k4    consualg2k5    ' \
#                    'timehop    timealg1    timealg2    timealg2k    timealg2k3    timealg2k4    timealg2k5\n'
fp.write(utput_label)

stphspf = [0] * len(x)
stpalg1 = [0] * len(x)
stpalg2 = [0] * len(x)
stpalg2k = [0] * len(x)
stpalg2k3 = [0] * len(x)
stpalg2k4 = [0] * len(x)
stpalg2k5 = [0] * len(x)

avefhopcount = [0] * len(x)
avefalg1 = [0] * len(x)
avefalg2 = [0] * len(x)
avefalg2k = [0] * len(x)
avefalg2k3 = [0] * len(x)
avefalg2k4 = [0] * len(x)
avefalg2k5 = [0] * len(x)

consuhopcount = [0] * len(x)
consualg1 = [0] * len(x)
consualg2 = [0] * len(x)
consualg2k = [0] * len(x)
consualg2k3 = [0] * len(x)
consualg2k4 = [0] * len(x)
consualg2k5 = [0] * len(x)

timeh = [0] * len(x)
time1 = [0] * len(x)
time2 = [0] * len(x)
time2k = [0] * len(x)
time2k3 = [0] * len(x)
time2k4 = [0] * len(x)
time2k5 = [0] * len(x)
countf = [0] * len(x)
countf1 = [0] * len(x)
countf2 = [0] * len(x)
countf2k = [0] * len(x)
countf2k3 = [0] * len(x)
countf2k4 = [0] * len(x)
countf2k5 = [0] * len(x)

for i in range(count):
    print('running ' + str(i) + ' time:', str(time.time() - start_time) + '\n')

    # fp.write(str(i)+'    '+str(sou)+'    '+str(des)+'    ')
    if random_topology == 1:
        # 采用随机生成拓扑，或者读取相同的拓扑
        if random_topology_mode == 0:
            # 生成随机拓扑
            nodes, edges, positions = create_random_topology(random_topology_nodes_num, 0.06, 1)

            graph_topology_save_name1 = graph_topology_file_name1
            graph_topology_file1 = open(graph_topology_save_name1, 'w')
            graph_topology_save_name2 = graph_topology_file_name2
            graph_topology_file2 = open(graph_topology_save_name2, 'w')
            for index in range(len(nodes)):
                graph_topology_file1.write(str(nodes[index]) + '\n')
            for index in range(len(edges)):
                graph_topology_file2.write(str(edges[index]) + '\n')

        if random_topology_mode == 1:
            nodes = []
            edges0 = []
            # 读取已有的随机产生拓扑，以确保仿真的一致性
            graph_topology_save_name1 = graph_topology_file_name1
            graph_topology_save_name2 = graph_topology_file_name2
            graph_nodes_file = open(graph_topology_save_name1, 'r')
            graph_edges_file = open(graph_topology_save_name2, 'r')

            # 分别读取节点和边
            for line in graph_nodes_file.readlines():
                line = line.strip('\n')
                # line = line.strip('\'')
                nodes.append(line)
            for line in graph_edges_file.readlines():
                line = line.strip('\n')
                line.replace("''", "")
                edges0.append(line)
            # nodes=graph_nodes_file.readlines()
            # edges=graph_edges_file.readlines
            edges = []
            length = len(edges0) - 1
            for index in range(length):
                # edges.append((edges0[index]))
                # edges.append((nodes[j], nodes[i]))
                # print(index)
                # print(edges0[index])
                edges.append(eval(edges0[index]))
            # print(edges)
            # print(type(edges[1]))
        # 采用随机拓扑
        # nodes, edges, positions = create_random_topology(random_topology_nodes_num, 0.06, 1)
        network = Net().network
        network[0] = nodes
        network[1] = edges
        network = Vtopo().creatbasicvtopo(network, link_capacity, topology_fidelity_mode)
        g = Vtopo().creatvtopo(network)

    else:
        # 采用骨干网拓扑
        network = Net().network
        # print("test")
        # print(len(network[0]))
        # print(len(network[1]))
        network = Vtopo().creatbasicvtopo(network, link_capacity, topology_fidelity_mode)
        g = Vtopo().creatvtopo(network)
    # x=np.arange(0.5,1,0.05)
    # 随机产生sd点
    sou = random.randint(0, len(g) - 1)
    des = random.randint(0, len(g) - 1)
    while des == sou:
        des = random.randint(0, len(g) - 1)
    print('source=', sou, 'des=', des)
    tphspf = []
    yalg1 = []
    yalg2 = []
    yalg2k = []
    yalg2k3 = []
    yalg2k4 = []
    yalg2k5 = []
    for j in range(len(x)):
        print("fidelity threshold: " + str(x[j]))
        time_0 = time.time()

        if enable_Hspf == 1:
            path, d, fi, con, th, sumt, times = Alg1().alg1(copy.deepcopy(g), sou, des, x[j], nrof_requests, 0, 0)

            # print(path,d,fi,con,th,sumt)
            timeh[j] += times
            tmpsf = 0
            tmpsc = 0
            for i in range(len(fi)):
                tmpsf += fi[i]
                for c in con[i]:
                    tmpsc += c
            if len(fi) > 0:
                avefhopcount[j] += (tmpsf / len(fi))
                stphspf[j] += sumt
                consuhopcount[j] += tmpsc
                countf[j] += 1

        time_1 = time.time()
        if enable_alg1 == 1:
            path1, d1, fi1, con1, th1, sumt1, times1 = Alg1().alg1(copy.deepcopy(g), sou, des, x[j], nrof_requests, 0)
            # print(path1,d1,fi1,con1,th1,sumt1)
            time1[j] += times1
            tmpsf1 = 0
            tmpsc1 = 0
            for i in range(len(fi1)):
                tmpsf1 += fi1[i]
                for c in con1[i]:
                    tmpsc1 += c
            if len(fi1) > 0:
                avefalg1[j] += (tmpsf1 / len(fi1))
                stpalg1[j] += sumt1
                consualg1[j] += tmpsc1
                countf1[j] += 1

        time_2 = time.time()
        if enable_alg2 == 1:
            path2, d2, fi2, con2, th2, sumt2, times2 = Alg2().alg2(copy.deepcopy(g), sou, des, x[j], nrof_requests)
            # print(path2,d2,fi2,con2,th2,sumt2)
            time2[j] += times2
            tmpsf2 = 0
            tmpsc2 = 0
            for i in range(len(fi2)):
                tmpsf2 += fi2[i]
                for c in con2[i]:
                    tmpsc2 += c
            if len(fi2) > 0:
                avefalg2[j] += (tmpsf2 / len(fi2))
                stpalg2[j] += sumt2
                consualg2[j] += tmpsc2
                countf2[j] += 1
        """path2k,d2k,fi2k,con2k,th2k,sumt2k,times2k=Alg2k().alg2k(copy.deepcopy(g),sou,des,x[j],10000)
        time2k[j]+=times2k
        tmpsf2k=0
        tmpsc2k=0
        for i in range(len(fi2k)):
            tmpsf2k+=fi2k[i]
            for c in con2k[i]:
                tmpsc2k+=c
        if len(fi2k)>0:
            avefalg2k[j]+=(tmpsf2k/len(fi2k))
            stpalg2k[j]+=sumt2k
            consualg2k[j]+=tmpsc2k
            countf2k[j]+=1

        path2k3,d2k3,fi2k3,con2k3,th2k3,sumt2k3,times2k3=Alg2k().alg2k(copy.deepcopy(g),sou,des,x[j],10000,3)
        time2k3[j]+=times2k3
        tmpsf2k3=0
        tmpsc2k3=0
        for i in range(len(fi2k3)):
            tmpsf2k3+=fi2k3[i]
            for c in con2k3[i]:
                tmpsc2k3+=c
        if len(fi2k3)>0:
            avefalg2k3[j]+=(tmpsf2k3/len(fi2k3))
            stpalg2k3[j]+=sumt2k3
            consualg2k3[j]+=tmpsc2k3
            countf2k3[j]+=1

        path2k4,d2k4,fi2k4,con2k4,th2k4,sumt2k4,times2k4=Alg2k().alg2k(copy.deepcopy(g),sou,des,x[j],10000,4)
        time2k4[j]+=times2k4
        tmpsf2k4=0
        tmpsc2k4=0
        for i in range(len(fi2k4)):
            tmpsf2k4+=fi2k4[i]
            for c in con2k4[i]:
                tmpsc2k4+=c
        if len(fi2k4)>0:
            avefalg2k4[j]+=(tmpsf2k4/len(fi2k4))
            stpalg2k4[j]+=sumt2k4
            consualg2k4[j]+=tmpsc2k4
            countf2k4[j]+=1

        path2k5,d2k5,fi2k5,con2k5,th2k5,sumt2k5,times2k5=Alg2k().alg2k(copy.deepcopy(g),sou,des,x[j],10000,5)
        time2k5[j]+=times2k5
        tmpsf2k5=0
        tmpsc2k5=0
        for i in range(len(fi2k5)):
            tmpsf2k5+=fi2k5[i]
            for c in con2k5[i]:
                tmpsc2k5+=c
        if len(fi2k5)>0:
            avefalg2k5[j]+=(tmpsf2k5/len(fi2k5))
            stpalg2k5[j]+=sumt2k5
            consualg2k5[j]+=tmpsc2k5
            countf2k5[j]+=1"""

for i in range(len(x)):
    stphspf[i] /= count
    stpalg1[i] /= count
    stpalg2[i] /= count
    stpalg2k[i] /= count
    stpalg2k3[i] /= count
    stpalg2k4[i] /= count
    stpalg2k5[i] /= count
    if countf[i] == 0:
        countf[i] = 1
    avefhopcount[i] /= countf[i]
    if countf1[i] == 0:
        countf1[i] = 1
    avefalg1[i] /= countf1[i]
    if countf2[i] == 0:
        countf2[i] = 1
    avefalg2[i] /= countf2[i]
    # avefalg2k[i]/=countf2k[i]
    # avefalg2k3[i]/=countf2k3[i]
    # avefalg2k4[i]/=countf2k4[i]
    # avefalg2k5[i]/=countf2k5[i]
    consuhopcount[i] /= count
    consualg1[i] /= count
    consualg2[i] /= count
    consualg2k[i] /= count
    consualg2k3[i] /= count
    consualg2k4[i] /= count
    consualg2k5[i] /= count
    timeh[i] /= count
    time1[i] /= count
    time2[i] /= count
    time2k[i] /= count
    time2k3[i] /= count
    time2k4[i] /= count
    time2k5[i] /= count

    # output_result = str(x[i])+'    '\
    #                 +str(stphspf[i])+'    '\
    #                 +str(stpalg1[i])+'    '\
    #                 +str(stpalg2[i])+'    '\
    #                 +str(stpalg2k[i])+'    '\
    #                 +str(stpalg2k3[i])+'    '\
    #                 +str(stpalg2k4[i])+'    '\
    #                 +str(stpalg2k5[i])+'    '\
    #                 +str(avefhopcount[i])+'    '\
    #                 +str(avefalg1[i])+'    '\
    #                 +str(avefalg2[i])+'    '\
    #                 +str(avefalg2k[i])+'    '\
    #                 +str(avefalg2k3[i])+'    '\
    #                 +str(avefalg2k4[i])+'    '\
    #                 +str(avefalg2k5[i])+'    '\
    #                 +str(consuhopcount[i])+'    '\
    #                 +str(consualg1[i])+'    '\
    #                 +str(consualg2[i])+'    '\
    #                 +str(consualg2k[i])+'    '\
    #                 +str(consualg2k3[i])+'    '\
    #                 +str(consualg2k4[i])+'    '\
    #                 +str(consualg2k5[i])+'    '\
    #                 +str(timeh[i])+'    '\
    #                 +str(time1[i])+'    '\
    #                 +str(time2[i])+'    '\
    #                 +str(time2k[i])+'    '\
    #                 +str(time2k3[i])+'    '\
    #                 +str(time2k4[i])+'    '\
    #                 +str(time2k5[i])+'\n'
    # output_result = str(x[i]) + '    '
    output_result = ''
    if enable_Hspf == 1:
        output_result += str(round(x[i], 2)) + '    ' + str(stphspf[i]) + '    ' + str(avefhopcount[i]) + '    ' + str(
            consuhopcount[i]) + '    ' + str(timeh[i]) + '    '
    if enable_alg1 == 1:
        output_result += str(round(x[i], 2)) + '    ' + str(stpalg1[i]) + '    ' + str(avefalg1[i]) + '    ' + str(
            consualg1[i]) + '    ' + str(time1[i]) + '    '
    if enable_alg2 == 1:
        output_result += str(round(x[i], 2)) + '    ' + str(stpalg2[i]) + '    ' + str(avefalg2[i]) + '    ' + str(
            consualg2[i]) + '    ' + str(time2[i]) + '    '
    output_result += '\n'
    print(output_result)
    # fp.write(str(x[i])+'    '+str(stphspf[i])+'    '+str(stpalg1[i])+'    '+str(stpalg2[i])+'    '+str(stpalg2k[i])+'    '+str(stpalg2k3[i])+'    '+str(stpalg2k4[i])+'    '+str(stpalg2k5[i])+'    '+str(avefhopcount[i])+'    '+str(avefalg1[i])+'    '+str(avefalg2[i])+'    '+str(avefalg2k[i])+'    '+str(avefalg2k3[i])+'    '+str(avefalg2k4[i])+'    '+str(avefalg2k5[i])+'    '+str(consuhopcount[i])+'    '+str(consualg1[i])+'    '+str(consualg2[i])+'    '+str(consualg2k[i])+'    '+str(consualg2k3[i])+'    '+str(consualg2k4[i])+'    '+str(consualg2k5[i])+'    '+str(timeh[i])+'    '+str(time1[i])+'    '+str(time2[i])+'    '+str(time2k[i])+'    '+str(time2k3[i])+'    '+str(time2k4[i])+'    '+str(time2k5[i])+'\n')
    fp.write(output_result)
fp.close()

fig = plt.figure()
plt.plot(x, stphspf, color='red')
plt.plot(x, stpalg1, color='green')
plt.plot(x, stpalg2, color='black')
plt.plot(x, stpalg2k, color='blue')
plt.plot(x, stpalg2k3, color='yellow')
plt.plot(x, stpalg2k4, color='purple')
plt.plot(x, stpalg2k5, color='cyan')
plt.title("")
plt.xlabel('fth')
plt.ylabel('expect throughput')
plt.show()

