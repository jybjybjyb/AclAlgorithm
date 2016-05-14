# coding=utf-8


import os
import re
import copy
import cProfile
import pstats
from operator import itemgetter, attrgetter

import time
import sys
sys.setrecursionlimit(1000)

# import matplotlib



''' global '''
DIM=5
DIM_RANGE = 0xFFFFFFFF
THRESHOLD = 1
MAX_HIERARCHY = 32
LEAF_RULENUM=32

import logging
log_filename="hs_log.txt"
logging.basicConfig(filename=log_filename, filemode="w", level=logging.DEBUG)



class FileProc(object):
    '''
    classdocs
    '''
    pattern = re.compile(r'\@\s*(\d+)\.(\d+).(\d+).(\d+)\/(\d+)\s*(\d+)\.(\d+).(\d+).(\d+)\/(\d+)\s*(\d+)\s*\:\s*(\d+)\s*(\d+)\s*\:\s*(\d+)\s*\d\w(\d*)\/\d\w(\w+)')
    pattern_2 = re.compile(r'(\d+)\s(\d+)\s(\d+)\s(\d+)\s(\d+)')

    def __init__(self):
        pass



    def GenRules(self, input_file):
        filter_set = []
        with open(input_file, mode='r') as input_handle:
#         input_handle= open(self.input_file, mode='r')
            
            for line in input_handle.readlines():
#                 print(line)
                m1 = re.match(self.pattern, line)
                if m1:
                    tmp_rule=[]                  
                    for x in (0, 5):
                        ip1 = int(m1.group(x + 1)) << 24 & 0xFF000000
                        ip2 = int(m1.group(x + 2)) << 16 & 0x00FF0000
                        ip3 = int(m1.group(x + 3)) << 8 & 0x0000FF00
                        ip4 = int(m1.group(x + 4)) & 0x000000FF
                        tmask = int(m1.group(x + 5))
                        tmpdip = (ip1 | ip2 | ip3 | ip4)
                    
                        if(tmask < 32):
                            mask = 2 ** (32 - tmask) - 1
                            ipend = tmpdip | mask
                            ipstart = tmpdip & (~mask)
                        else:
                            ipend = tmpdip
                            ipstart = tmpdip
                        
                        if x==0:
                            sipend=ipend
                            sipstart=ipstart
                        else:
                            dipend=ipend
                            dipstart=ipstart
        
                    for x in (11, 13):
                        port_start = int(m1.group(x))
                        port_end = int(m1.group(x + 1))
                        
                        if(x == 11):
                            sPort_start = port_start
                            sPort_end = port_end
                        else:
                            dPort_start = port_start
                            dPort_end = port_end
                    
                    pro=int(m1.group(14),16)
                    len=int(m1.group(15),16)
                    
#                     print(pro,len)  
                    if len==255:
                        pfrom=pro
                        pto=pro
                    else:
                        pfrom=0
                        pto=255
                        
                    # array[5][2]
                    tmp_rule = ((sipstart, sipend),
                              (dipstart, dipend),
                              (sPort_start, sPort_end),
                              (dPort_start, dPort_end),
                              (pfrom,pto))
                    
#                     print(tmp_rule)
                    filter_set.append(tmp_rule)     
                                   
                else:
                    print("no match rules...")
                    
        return filter_set
    
    
    def GenIP(self, input_file):
        ips_set = []
        
        with open(input_file, mode='r') as input_handle:
   
            for line in input_handle.readlines():
#                 print(line)
                m1 = re.match(self.pattern_2, line)
                if m1:                   
                    tmpips=[]
                    for x in range(1,6):
                        tmpips.append(int(m1.group(x)))
                    ips_set.append(tmpips)     
                                   
                else:
                    print("no match rules...")
                    
                    
        return ips_set
    
     


class TreeNode(object):
    # 节点类
    def __init__(self):
        self.d2s = 0xFFFF
        self.hierarchy = 0x0
        self.thresh = 0x0
        self.left_node = None
        self.right_node = None
        
        # the one below will be release otherwise leaf             
        self.ruleset = []
#         self.seg_num=0xFFFF

        self.nodeRange=[]
        for i in range(5):
            self.nodeRange.append([0,0xFFFFFFFF])



class KdTree(object):
    # 树类
    def __init__(self, tree_root=None):
        self.tree_root = tree_root
        
    
    def SetRoot(self, tree_root):
        self.tree_root = tree_root



    
class HyperSplit(object):
  

    def __init__(self):
      
        self.kd_tree = KdTree()
        self.ruleset = []
        self.ips_set = []
        self.lookup_results = []        
        self.leafset = []
        self.node_cnt = 0
        
        self.lookupNode = None
    

        
        
    def DumpInputData(self):     
        proc=FileProc()
        print("Reading...")
        

        self.ruleset=proc.GenRules("..\\MyFilter\\acl4k_1")  
        print("len(self.ruleset) is %d" % len(self.ruleset))
#         for r in self.ruleset:
#             print(r)
        
        self.ips_set=proc.GenIP("..\\MyFilter\\acl4k_1_trace") 
        print("len(self.ips_set) is %d" % len(self.ips_set))

#         for p in self.ips_set:
#             print(p)        
        return
        


    def InitRoot(self):
        '''
        return root
        '''
                
        # root_node
        root = TreeNode()
        root.ruleset = list(range(0, len(self.ruleset)))
        
        return root
        
             
    def CalcAvgWeight(self, seg_set):
        '''
        return
        :param space:
        '''
        avg_weight = 0 
   
        for seg in seg_set:
            # seg_set[x][0] is num_rule
            # (seg_rule_cnt,seg_include_rule,seg_range)
            avg_weight = avg_weight + seg[0]

        try:
            avg_weight = avg_weight * 100 / len(seg_set)  
        except ZeroDivisionError:
            print("the seg_set is empty !!!")   
                         
        return avg_weight  
       


    def ReformPtSet(self, tmpPts):
        Pts=[]
        PtInfo=[]
        
        tmpPts=sorted(tmpPts,key=itemgetter(0,1),reverse=False)

        tmpelement=(0,0)
        for element in tmpPts[::-1]:
            if(element != tmpelement):
                tmpelement = element
            else:
                tmpPts.remove(element)
        
        for e in tmpPts:
            Pts.append(e[0])
            PtInfo.append(e[1])
        
        return Pts, PtInfo
    
    

    def GetSplitDimPt(self,currNode):
  
#         print("GetSplitDimPt ...")
        
        min_avg_weight=0xffffffff
        thresh=0xffffffff
        d2s=0xffff
        seg_num=0xffffffff
        

        for j in range(DIM):
            tmpPts=[]
#             Pts=[]
#             PtInfo=[]        
            
            # get ptSet
            for rindx in currNode.ruleset:
                rule_start=self.ruleset[rindx][j][0]
                rule_end=self.ruleset[rindx][j][1]
            
                if self.ruleset[rindx][j][0] < currNode.nodeRange[j][0]:
                    rule_start=currNode.nodeRange[j][0]
                tmpPts.append((rule_start,0))
                
                if self.ruleset[rindx][j][1] > currNode.nodeRange[j][1]:
                    rule_end=currNode.nodeRange[j][1]
                tmpPts.append((rule_end,1))
                
            Pts, PtInfo=self.ReformPtSet(tmpPts)
              
            
            # set ruleNum in Seg
            ruleNuminSeg=[0]*(len(Pts)-1)
            all_weight=0
            
            
            for ptindx in range(len(Pts)-1):
#                 if ptindx == 0:
#                     continue
                for rindx in currNode.ruleset:
                    if self.ruleset[rindx][j][1] >= Pts[ptindx+1] \
                    and self.ruleset[rindx][j][0] <= Pts[ptindx]:
                        
                        ruleNuminSeg[ptindx]+=1
                        all_weight+=1
            
            
#             print("j= ",j)
#             print("Pts",Pts)
#             print("PtInfo",PtInfo)            
#             print("ruleNuminSeg",ruleNuminSeg)  
#             print("all_weight",all_weight)
                  
            # set avg_weight in DIM     
            try:
                avg_weight = all_weight / len(ruleNuminSeg)
            except ZeroDivisionError:                
                print("the ruleNuminSeg is empty !!!")  
                exit(1) 
                
#             print("avg_weight",avg_weight)
            
            # set d2s and thresh
            if avg_weight < min_avg_weight:
#                 print("Pts",Pts)
#                 print("PtInfo",PtInfo)  
#                 print("seg_num",seg_num) 
                seg_num=len(Pts)-1
                min_avg_weight=avg_weight
                d2s=j
                
                #set thresh
                tmp_weight=ruleNuminSeg[0]
                for indx in range(1,len(ruleNuminSeg)):
                    
                    if PtInfo[indx]==0:
                    #start
                        thresh=Pts[indx]-1
                    else:
                    #end
                        thresh=Pts[indx]

                    if tmp_weight > all_weight / 2:
                        break
                    
                    tmp_weight+=ruleNuminSeg[indx]
  
            
#         print("thresh",thresh)
#         print("d2s",d2s)
#         print("seg_num",seg_num)
#         print("min_avg_w",min_avg_weight)
        
        return d2s,thresh,seg_num



    def ReformIncrule(self,d2s, subNode, currNode):
        incrule=[]
        
        for rindx in currNode.ruleset:
            if self.ruleset[rindx][d2s][1] >= subNode.nodeRange[d2s][0]\
            and self.ruleset[rindx][d2s][0] <= subNode.nodeRange[d2s][1]:
            
                incrule.append(rindx)
        
        return incrule


    def BRPcurrNode(self, currNode):
        '''
        
        :param currNode:
        '''
        # if leaf
        if len(currNode.ruleset) <= LEAF_RULENUM:    
#             print("get leaf...")             
            self.leafset.append(currNode)            
            return
        
        
        # not is leaf
        self.node_cnt += 2

        
        leftNode = TreeNode()
        rightNode = TreeNode()
        
        d2s,thresh,seg_num = self.GetSplitDimPt(currNode)

        
        # if leaf
        if seg_num < 2:
#             print("Cannt further BRP !! ")
#             print("seg_num",seg_num)
#             print("thresh",thresh)
#             print("d2s",d2s)

            self.leafset.append(currNode) 
            return 
        

        # set d2s
        currNode.d2s = d2s
        currNode.thresh = thresh
        
        # generating sub node
        leftNode.nodeRange=copy.deepcopy(currNode.nodeRange)
        leftNode.nodeRange[d2s][0] = currNode.nodeRange[d2s][0]
        leftNode.nodeRange[d2s][1] = thresh
        leftNode.ruleset=self.ReformIncrule(d2s,leftNode,currNode)
        leftNode.hierarchy=currNode.hierarchy+1
        
        rightNode.nodeRange=copy.deepcopy(currNode.nodeRange)
        rightNode.nodeRange[d2s][0] = thresh + 1
        rightNode.nodeRange[d2s][1] = currNode.nodeRange[d2s][1]  
        rightNode.ruleset=self.ReformIncrule(d2s,rightNode,currNode) 
        rightNode.hierarchy=currNode.hierarchy+1
        
        
#         print("BRP self.node_cnt", self.node_cnt)
#         print("BRP hierarchy ",currNode.hierarchy+1)

        # padding subNode
        currNode.left_node=leftNode
        currNode.right_node=rightNode
        
        
        # release
#         currNode.nodeRange=None
#         currNode.hierarchy=None
#         currNode.ruleset=[]        
        
#         print("turn left...")          
        self.BRPcurrNode(leftNode)
#         print("turn right...")  
        self.BRPcurrNode(rightNode)
        


    
    
    def BuildkdTree(self):      
       

        # init KdTree
        tree_root = self.InitRoot()
        self.kd_tree.SetRoot(tree_root)

        
        # Building
        print("BRPcurrNode start ...")
        self.BRPcurrNode(tree_root)
        
        
        # PostProcess
#         self.PostProcess(self.leafset)
        
        return

    
    def TracekdTree(self, currNode, ip):
        '''
        
        :param currNode:
        :param ip:
        
        return leaf_node 
        '''
        
        if currNode.left_node == None:
            self.lookupNode=currNode
            return         

        j = currNode.d2s
        
        if ip[j] <= currNode.thresh:
            currNode = currNode.left_node              
        else:
            currNode = currNode.right_node
            
        self.TracekdTree(currNode, ip)
                
        

    
    def PickResultIndx(self, leaf_node, ip):

        for rindx in leaf_node.ruleset:
            for j in range(DIM):
                rule_start = self.ruleset[rindx][j][0]
                rule_end = self.ruleset[rindx][j][1]
                
                if rule_start <= ip[j] and ip[j] <= rule_end:
                    return rindx
        
        print("cannt find matchable rule ...")
        return -1



    def LookupIpSet(self):

        
        for ip in self.ips_set:  
            self.lookupNode=None          
            self.TracekdTree(self.kd_tree.tree_root, ip)
            
            if self.lookupNode==None:
                print("Dont find lookupNode!!!")
                exit(0)

            result=self.PickResultIndx(self.lookupNode,ip)
            
            if result < 0:
                print("Dont find rule in leaf!!!")
                exit(0)

            self.lookup_results.append(result)
            
            
        return
    

    
    def Statistic(self):
        
        max_h=0
        min_h=0xffffffff
        sum_h=0
        
        for n in self.leafset:
            sum_h+=n.hierarchy
            if n.hierarchy<min_h:
                min_h=n.hierarchy
            if n.hierarchy>max_h:
                max_h=n.hierarchy
                
        duplex=self.node_cnt / len(self.leafset)
         
        print(">> account of node : ",self.node_cnt)
        print(">> account of leaf : ",len(self.leafset))
        print(">> duplex : ", duplex)
        print(">> minimum hierarchy is",min_h)
        print(">> maximum hierarchy is",max_h)
        print(">> avarge hierarchy is",(sum_h/len(self.leafset)))
        memory_use = self.node_cnt * 8
        print(">> mem-cost is", int(memory_use >> 10))
        print(">> all rules matching...")
        
                    
        
        with open("leaf_info.txt", mode='w') as handle:
            handle.write("\n#################  statistic   #############\n")
           
            handle.write("\n________________[basic info]__________________\n")
            handle.write("len of rules is %s\n" % str(len(self.ruleset)))
            handle.write("len of ips is %s\n" % str(len(self.ips_set)))
            handle.write("len of lookup_results is %s\n" % str(len(self.lookup_results)))
            
            # Memory Used
            # TreeNode == 64bit(8 Byte)
            handle.write("\n________________[memory]__________________\n")
            handle.write("account of node :%d\n" % (self.node_cnt))
            handle.write("account of leaf :%d\n" % (len(self.leafset)))
            handle.write("duplex is  :%f\n" % duplex)
            
            memory_use = self.node_cnt * 8
            handle.write("Assuming 8Byte per node\n")
            handle.write("%d KB memory used\n" % int(memory_use >> 10))
            
            # hierarchy info 
            handle.write("\n_________[hierarchy]__________\n")
            handle.write("minimum hierarchy is %d\n"%min_h)
            handle.write("maximum hierarchy is %d\n"%max_h)
            handle.write("avarge hierarchy is %d\n"%(sum_h/len(self.leafset)))
            
            # hierarchy info 
            handle.write("\n_________[leaf info]__________\n")

        
        return
            
#             
#     def PlotLeaf(self):
#         
#         
#         rule_cnt_set = []
#         hierarchy_cnt = []
#         
#         for leaf in self.pre_leaf_set:
#             rule_cnt_set.append(len(leaf.include_rules))
#             hierarchy_cnt.append(leaf.hierarchy[self.field_sequence[5]])
#             
#         x_value = list(range(len(self.pre_leaf_set)))
#         y_value0 = rule_cnt_set
#         y_value1 = hierarchy_cnt
#         plt.xlabel("leaf")
#         plt.ylabel("")
#         plt.plot(x_value, y_value0, 'ob', label="rule_cnt" , fillstyle='none')
#         plt.plot(x_value, y_value1, 'r', label="hierarchy_cnt" , linestyle='--')
#         plt.legend()
#         plt.savefig("rule_cnt.png")
#         plt.show()
#         
#         return

        
#         
#     def PlotWhole(self, hierarchy_set):
#         
#         # matplotlib
#         x_value = list(range(len(self.pre_leaf_set)))
#         y_value0 = hierarchy_set[0]
#         y_value1 = hierarchy_set[1]
#         y_value2 = hierarchy_set[2]
#         y_value3 = hierarchy_set[3]
#         y_value4 = hierarchy_set[4]
#         y_value5 = hierarchy_set[5]
#         
#         
#         plt.xlabel("leaf")
#         plt.ylabel("hierarchy[x]")
#         plt.plot(x_value, y_value0, 'ob', label="0" , fillstyle='none')
#         plt.plot(x_value, y_value1, 'or' , label="1" , fillstyle='none')
#         plt.plot(x_value, y_value2, 'og', label="2"  , fillstyle='none')
#         plt.plot(x_value, y_value3, 'oy', label="3"  , fillstyle='none')
#         plt.plot(x_value, y_value4, 'ok', label="4"  , fillstyle='none')
#         plt.plot(x_value, y_value5, 'oc', label="5"  , fillstyle='none')
#         
#         plt.legend()
#         plt.savefig("hierarchy.png")
#         plt.show()
#         
#         return
#     
#     
    
            
if __name__ == "__main__":
    print(os.path.abspath(".."))
    f = FileProc()
    hs = HyperSplit()
    hs.DumpInputData()
    start1=time.time()
    hs.BuildkdTree()
    end1=time.time()
    hs.LookupIpSet()
    
#     cProfile.run("hs.BuildkdTree()", "BuildkdTree.txt")
#     p = pstats.Stats("BuildkdTree.txt")
#     p.strip_dirs().sort_stats("cumulative").print_stats(20)

    hs.Statistic()
    print("BuildkdTree time", str(end1-start1), "s")
    print("finish...")

    
    
    
    

    
    
    
    
    
