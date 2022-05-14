from t1 import *
from t2 import *
from t3 import *
from t4 import *
from t5 import *
#simulation1 : fth作为自变量，单sd
#simulation2 : c作为自变量，单sd
#simulation3 : fth作为自变量，多sd
#simulation4 : c作为自变量，多sd
#simulation5 : sd数作为自变量

#仿真运行选择,0为不运行。
sim1=1
sim2=0
sim3=0
sim4=0
sim5=0
#参数设置
if sim1==1:
	s1_count=10 #运行次数
	s1_x=np.arange(0.55,0.95,0.05) #fth区间
	s1_topology_fidelity_mode=0 #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
	s1_nrof_requests=10000 #单S-Dpair的请求connection数量
	s1_alg1_mode=1 #Alg1的运行模式，BFS搜索为0，k-shortest为1
	s1_link_capacity=10 #链路容量设置
	s1_random_topology = 0 # 随机拓扑设置，1代表开启
	s1_random_topology_mode=0 #0代表每次生成随机的，1代表读取文件中的拓扑
	s1_random_topology_nodes_num =5 #随机拓扑节点数量

if sim2==1:
	s2_count=10 #运行次数
	s2_x=np.arange(100,1000,100) #链路容量区间
	s2_topology_fidelity_mode=0 #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
	s2_nrof_requests=10000 #单S-Dpair的请求connection数量
	s2_alg1_mode=1 #Alg1的运行模式，BFS搜索为0，k-shortest为1
	s2_req_fth=0.7 #请求fth设置
	s2_random_topology = 0 # 随机拓扑设置，1代表开启
	s2_random_topology_mode=0 #0代表每次生成随机的，1代表读取文件中的拓扑
	s2_random_topology_nodes_num =5 #随机拓扑节点数量
if sim3==1:
	s3_count=1 #运行次数
	s3_x=np.arange(0.55,0.95,0.05) #fth区间
	s3_sumreq=400 #总需求
	s3_link_capacity=50 #链路容量设置
	s3_norfSD_Pair=4 #SD对数量
	s3_topology_fidelity_mode=0 #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
	s3_read_random_SDpair=0 #是否通过读取SDpair对，以保证仿真的一致性
	s3_random_topology = 0 # 随机拓扑设置，1代表开启
	s3_random_topology_mode=0 #0代表每次生成随机的，1代表读取文件中的拓扑
	s3_random_topology_nodes_num =5 #随机拓扑节点数量
if sim4==1:
	s4_count=1 #运行次数
	s4_x=np.arange(10,91,10) #链路容量区间
	s4_sumreq=400 #总需求
	s4_req_fth=0.7 #请求fth设置
	s4_norfSD_Pair=4 #SD对数量
	s4_topology_fidelity_mode=0 #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
	s4_read_random_SDpair=0 #是否通过读取SDpair对，以保证仿真的一致性
	s4_random_topology = 0 # 随机拓扑设置，1代表开启
	s4_random_topology_mode=0 #0代表每次生成随机的，1代表读取文件中的拓扑
	s4_random_topology_nodes_num =5 #随机拓扑节点数量
if sim5==1:
	s5_count=1 #运行次数
	s5_x=np.arange(19,20) #sd数量区间
	s5_topology_fidelity_mode=1 #模式0代表重新生成，模式1代表读取之前保存的链路保真度数值
	s5_fth = 0.7 #端到端保真度阈值
	s5_sumreq = 100 #总请求连接数量
	s5_link_capacity=50 #链路容量设置
	s5_save_mode = 1 #保存此次随机生成的S-0 Pair
	s5_read_mode = 0 #读取之前随机生成的S-D Pair


#仿真运行
if sim1==1:
	SingleSdFth(s1_count,s1_x,s1_topology_fidelity_mode,s1_nrof_requests,s1_alg1_mode,s1_link_capacity,s1_random_topology,s1_random_topology_mode,s1_random_topology_nodes_num)
if sim2==1:
	SingleSdC(s2_count,s2_x,s2_topology_fidelity_mode,s2_nrof_requests,s2_alg1_mode,s2_req_fth,s2_random_topology,s2_random_topology_mode,s2_random_topology_nodes_num)
if sim3==1:
	MultiSdFth(s3_count,s3_x,s3_sumreq,s3_link_capacity,s3_norfSD_Pair,s3_topology_fidelity_mode,s3_read_random_SDpair,s3_random_topology,s3_random_topology_mode,s3_random_topology_nodes_num)
if sim4==1:
	MultiSdC(s4_count,s4_x,s4_sumreq,s4_req_fth,s4_norfSD_Pair,s4_topology_fidelity_mode,s4_read_random_SDpair,s4_random_topology,s4_random_topology_mode,s4_random_topology_nodes_num)
if sim5==1:
	Sd(s5_count,s5_x,s5_topology_fidelity_mode,s5_fth,s5_sumreq,s5_link_capacity,s5_save_mode,s5_read_mode)