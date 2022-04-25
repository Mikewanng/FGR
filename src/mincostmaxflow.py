from queue import Queue
import sys
class Mcmf:
    def __init__(self):
        self._num_edge=-1
        self.maxn=500
        self.cost=[]
        self.pre=[]
        self.last=[]
        self.flow=[]
        self.head=[]
        self.vis=[]
        self._edge=[]
        self.q=Queue()
        self.maxflow=0
        self.mincost=0
        for i in range(self.maxn):
            self.cost.append(0)
            self.pre.append(0)
            self.last.append(0)
            self.flow.append(0)
            self.head.append(-1)
            self.vis.append(False)
            t=Edge()
            self._edge.append(t)

    def addedge(self,fr,to,flow,cost):
        self._edge[++self._num_edge]._from=self.head[fr]
        self._edge[self._num_edge]._to = to
        self._edge[self._num_edge]._flow = flow
        self._edge[self._num_edge]._cost = cost
        self.head[fr] = self._num_edge

        self._edge[++self._num_edge]._from=self.head[to]
        self._edge[self._num_edge]._to = fr
        self._edge[self._num_edge]._flow = 0
        self._edge[self._num_edge]._cost = -cost
        self.head[to] = self._num_edge

    def Spfa(self,s,t):
        for i in range(self.maxn):
            self.cost[i]=sys.maxsize/2
            self.flow[i]=sys.maxsize/2
            self.vis[s]=False
        self.q.put(s)
        self.cost[s]=0
        self.pre[t]=-1

        while self.q.empty() is False:
            now=self.q.get()
            self.vis[now]=False
            i=self.head[now]
            while i!=-1:
                if self._edge[i]._flow>0 and self.cost[self._edge[i]._to]>self.cost[now]+self._edge[i]._cost:
                    self.cost[self._edge[i]._to]=self.cost[now]+self._edge[i]._cost
                    self.pre[self._edge[i]._to]=now
                    self.last[self._edge[i]._to]=i
                    self.flow[self._edge[i]._to]=min(self.flow[now],self._edge[i]._flow)
                    if self.vis[self._edge[i]._to] is False:
                        self.vis[self._edge[i]._to]=True
                        self.q.put(self._edge[i]._to)
                i = self._edge[i]._from
        return self.pre[t]!=-1


    def Mcmf(self,network,s,t):
        
        
        for i in network[1]:
            self.addedge(i._from,i._to,i._flow,i._cost)
        while self.Spfa(s,t) is True:
            now=t
            self.maxflow+=self.flow[t]
            self.mincost+=self.flow[t]*self.cost[t]
            while now!=s:
                self._edge[self.last[now]]._flow-=self.flow[t]
                self._edge[self.last[now]^1]._flow+=self.flow[t]
                now=self.pre[now]

        return self.maxflow,self.mincost

class Edge:
    def __init__(self,fr=0,to=0,flow=0,cost=0):
        self._from=fr
        self._to=to
        self._flow=flow
        self._cost=cost
