#coding=utf-8

import os
import re
import copy
import cProfile
import pstats
from operator import itemgetter,attrgetter
import matplotlib.pyplot as plt
# from memory_profiler import profile
# from memory_profiler import memory_usage
import time
import sys
from copy import deepcopy


INPUT_FILE_NAME="..\\MyFilter\\1k.txt"


class FileProc(object):
    '''
    classdocs
    '''
    pattern=re.compile(r'\@\s*(\d+)\.(\d+).(\d+).(\d+)\/(\d+)\s*(\d+)\.(\d+).(\d+).(\d+)\/(\d+)\s*(\d+)\s*\:\s*(\d+)\s*(\d+)\s*\:\s*(\d+)')

    def __init__(self):
        pass



    def GenRules(self, input_file):
        '''
        
        :param input_file: " .txt"
        '''
        filter_set=[]
        with open(input_file, mode='r') as input_handle:
#         input_handle= open(self.input_file, mode='r')
    
            for line in input_handle.readlines():
#                 print(line)
                m1=re.match(self.pattern,line)
                if m1:                   
                    for x in (0,5):
                        ip1=int(m1.group(x+1))<<24 & 0xFF000000
                        ip2=int(m1.group(x+2))<<16 & 0x00FF0000
                        ip3=int(m1.group(x+3))<<8 & 0x0000FF00
                        ip4=int(m1.group(x+4)) & 0x000000FF
                        tmask=int(m1.group(x+5))
                        tmpdip=(ip1 | ip2 | ip3 | ip4)
                    
                        if(tmask < 32):
                            mask=2**(32-tmask)-1
                            ipend=tmpdip | mask
                            ipstart= tmpdip & (~mask)
                        else:
                            ipend=tmpdip
                            ipstart=tmpdip
                        
                        H16_ipstart=(ipstart >> 16) & 0xFFFF
                        H16_ipend=(ipend >> 16) & 0xFFFF
                        
                        L16_ipstart=ipstart & 0xFFFF
                        L16_ipend=ipend & 0xFFFF
                        
                        if(x==0):
                            sIPH_start=H16_ipstart
                            sIPH_end=H16_ipend
                            sIPL_start=L16_ipstart
                            sIPL_end=L16_ipend           
                        else:
                            dIPH_start=H16_ipstart
                            dIPH_end=H16_ipend
                            dIPL_start=L16_ipstart
                            dIPL_end=L16_ipend
        
                    for x in (11,13):
                        port_start=int(m1.group(x))
                        port_end=int(m1.group(x+1))
                        
                        if(x==11):
                            sPort_start=port_start
                            sPort_end=port_end
                        else:
                            dPort_start=port_start
                            dPort_end=port_end
                        
                    #array[6][2]
                    tmp_rule=((sIPH_start,sIPH_end),
                              (sIPL_start,sIPL_end),
                              (dIPH_start,dIPH_end),
                              (dIPL_start,dIPL_end),
                              (sPort_start,sPort_end),
                              (dPort_start,dPort_end))
                    
#                     print(tmp_rule)
                    filter_set.append(tmp_rule)     
                                   
                else:
                    print("no match rules...")
                    
        return filter_set
    
    
    def GenIP(self,input_file):
        ips_set=[]
        
        with open(input_file, mode='r') as input_handle:
#         input_handle= open(self.input_file, mode='r')
    
            for line in input_handle.readlines():
#                 print(line)
                m1=re.match(self.pattern,line)
                if m1:                   
                    for x in (0,5):
                        ip1=int(m1.group(x+1))<<24 & 0xFF000000
                        ip2=int(m1.group(x+2))<<16 & 0x00FF0000
                        ip3=int(m1.group(x+3))<<8 & 0x0000FF00
                        ip4=int(m1.group(x+4)) & 0x000000FF
                        tmask=int(m1.group(x+5))
                        tmpdip=(ip1 | ip2 | ip3 | ip4)
                    
                        if(tmask < 32):
                            mask=2**(32-tmask)-1
                            ipend=tmpdip | mask
                            ipstart= tmpdip & (~mask)
                        else:
                            ipend=tmpdip
                            ipstart=tmpdip
                        
                        H16_ipstart=(ipstart >> 16) & 0xFFFF
                        H16_ipend=(ipend >> 16) & 0xFFFF
                        
                        L16_ipstart=ipstart & 0xFFFF
                        L16_ipend=ipend & 0xFFFF
                        
                        if(x==0):
                            sIPH_start=H16_ipstart
                            sIPH_end=H16_ipend
                            sIPL_start=L16_ipstart
                            sIPL_end=L16_ipend           
                        else:
                            dIPH_start=H16_ipstart
                            dIPH_end=H16_ipend
                            dIPL_start=L16_ipstart
                            dIPL_end=L16_ipend
        
                    for x in (11,13):
                        port_start=int(m1.group(x))
                        port_end=int(m1.group(x+1))
                        
                        if(x==11):
                            sPort_start=port_start
                            sPort_end=port_end
                        else:
                            dPort_start=port_start
                            dPort_end=port_end
                        
                    #array[6][2]
                    tmp_ips=((sIPH_start),
                              (sIPL_start),
                              (dIPH_start),
                              (dIPL_start),
                              (sPort_start),
                              (dPort_start))
                    
#                     print(tmp_rule)
                    ips_set.append(tmp_ips)     
                                   
                else:
                    print("no match rules...")
                    
                    
        return ips_set
    
    def ShowFilter(self,filter_set):
        for x in range(0, len(filter_set)):
            print("rule [%d]"%x, end=" ")
            print(filter_set[x])
            
    def ShowIPs(self,ips_set):
        for x in range(0, len(ips_set)):
            print("ips [%d]"%x, end=" ")
            print(ips_set[x])
        


#       
# class Space():
#     def __init__(self,space_range=None,rule_inc=None,space_points=None,seg_set=None):
#         '''
#         
#         :param space_range:
#         :param rule_inc:
#         :param space_points:
#         :param seg_set:
#         '''
#         self.space_range = space_range
#         self.rule_inc = rule_inc
#         self.space_points = space_points
#         self.seg_set = seg_set
#         
#     def GenSpace(self,space_range,rule_inc,space_points,seg_set):
#         self.space_range = space_range
#         self.rule_inc = rule_inc
#         self.space_points = space_points
#         self.seg_set = seg_set
#         
#         
#     def ShowSpaceInfo(self):
#         '''
#         space_range=(0,65536),rule_inc=[],space_points=[],seg_set=[]
#         '''
#         print("space_range:",self.space_range)
#         print("space_points:",self.space_points)
#         print("rule_inc:",self.rule_inc)
#         print("%-16s%-25s%-25s"%("seg_rule_cnt","seg_include_rule","seg_range"))
#         for seg in self.seg_set:
#             print("%-16s%-25s%-25s"%(seg[0],seg[1],seg[2]))


class Segments(object):
    def __init__(self):
        
        # seg_num is seg_index
        self.seg_num=0
        # seg_num+1
        self.seg_point=[]
        # seg_num
        self.rule_inc=[]
        # seg_num
        self.rule_cnt=[]
        
    def SetPoint(self,seg_point):
        self.seg_point=seg_point
        
        return
    
    def GetPoint(self, indx):
        return self.seg_point[indx]

    
    def SetIncRules(self,inc_rules):
        self.rule_inc=inc_rules
        
        return
    
    def GetIncRules(self, indx):
        return self.rule_inc[indx]
        
        
    
    def SetRulecCnt(self,rule_cnt):
        self.rule_cnt=rule_cnt
        
        return
    
    def GetRulecCnt(self, indx):
        return self.rule_cnt[indx]
        
        
        
    
    

class TreeNode(object):
    #
    def __init__(self):
        self.j=None
#         self.space_range=None
#         self.space_points=None
#         self.seg_set=None
        self.d2s = None
        self.left_node=None
        self.right_node =None
        self.indx_range=None
        self.rule_inc=None
        self.hierarchy=None

    
    
    def SetTreeNode(self,j,indx_range):
        self.j = j
        self.indx_range=indx_range

        return

    
    def SetIncRule(self,inc_rule):
        self.rule_inc=inc_rule
         
        return
    
    def SetSplit(self,d2s):
        self.d2s=d2s
        
        return
    
    def SetHierarchy(self,h):
        self.hierarchy=h
         
        return 
    
    def GetHierarchy(self,j):
        
        return  self.hierarchy
        
    def SetPairNode(self, left_node, right_node):
        '''
        :param root_node:
        :param left_node:
        :param right_node:
        '''
        self.left_node = left_node
        self.right_node = right_node
        
        return
    

    
    def ShowNode(self):
        print("%-12s%-12s%-12s%-12s"%("j","hierarchy","d2s","rule_inc"))
        print("%-12s%-12s%-12s%-12s"%(self.j,self.hierarchy,self.d2s,self.rule_inc))
        print("%-12s%-12s"%("space_range","space_points"))
        print("%-12s%-12s"%(self.space_range,self.space_points))
        for x in range(0, len(self.seg_set)):
            print("seg %d :%s"%(x, self.seg_set[x]))
        print()
        
        


class KdTree(object):
    #
    def __init__(self, tree_root=None):
        self.tree_root = tree_root
        
    
    def SetRoot(self,tree_root):
        self.tree_root = tree_root
    
    
    def PreOrderTraverse(self,node):
        '''
        Pre-order Tracing
        :param node: root
        '''
        if node:
            print (node.data,end=',')  
            self.PreOrderTraverse(node.left)                   
            self.PreOrderTraverse(node.right)            
        return       
       
    
    def ShowTree(self):
        '''
        Trace Tree
        '''
        self.PreOrderTraverse(self.tree_root)
        return
    
class HyperSplit(object):
  

    def __init__(self):      
                
        ## global variable   
        self.DIM=6
        self.DIM_RANGE=65536
        self.THRESHOLD=1
        self.MAX_HIERARCHY=3
        self.logging="logging.txt"
#         self.BIT=0b0
        
        ## global object
        self.kd_tree=KdTree()        
        
        self.seg_in_feild=[]
        for x in range(0, self.DIM):
            segs=Segments()
            self.seg_in_feild.append(segs)
        
        self.field_info=[]
        self.field_sequence=[]
        self.pre_leaf_set=[]
        self.post_leaf_set=[]

        self.node_cnt=0
        self.node_inter_cnt=0
        self.node_leaf_cnt=0
        
        self.ruleset=[]
        self.ips_set=[]
        self.lookup_results=[]   

    def SetPara(self, max_h, thresh_rule_cnt):
        self.MAX_HIERARCHY = max_h
        self.THRESHOLD = thresh_rule_cnt
        
        return
        
        
        
    def DumpInputData(self,filters):     
        proc=FileProc()
        self.ruleset=proc.GenRules(filters)
        self.ips_set=proc.GenIP(filters)
        
        print("Reading......")
        print("len(self.ruleset) is %d"% len(self.ruleset))
        print("len(self.ips_set) is %d"% len(self.ips_set))
        print("Reading Over" )
        
        return
        
        
    def SortElement(self,sortedset):
        '''
        
        :param sortedset: list
        return list
        '''
        sortedset.sort()
        cmpint=None
        for element in sortedset[::-1]:
            if(element != cmpint):
                cmpint=element
            else:
                sortedset.remove(element)
                
        return sortedset
    



    def BuildSegments(self):
        
        for j in range(0,self.DIM):                        
            point_set=[]
            
            #gen porints
            for rule in self.ruleset:
                '''               
                rule_start=rule[j][0]
                rule_end=rule[j][1]+1
                '''
                
                point_set.append(rule[j][0])
                point_set.append(rule[j][1]+1)
                           
            point_set=self.SortElement(point_set)      
            self.seg_in_feild[j].seg_point=point_set
            
            
            #init
            #gen seg_cnt
            #gen seg_inc
            #gen=len(point_set)-1
 
            seg_num=len(point_set)-1
            self.seg_in_feild[j].seg_num=seg_num
            
            self.seg_in_feild[j].rule_cnt=[0]*seg_num
            for x in range(0, seg_num):                
                self.seg_in_feild[j].rule_inc.append([])

            for rule_indx in range(0, len(self.ruleset)):
                
                 rule_start=self.ruleset[rule_indx][j][0]
                 rule_end=self.ruleset[rule_indx][j][1]+1
                 indx_start=point_set.index(rule_start)
                 indx_end=point_set.index(rule_end)-1
                 
                 for x in range(indx_start, indx_end+1):
                     self.seg_in_feild[j].rule_cnt[x]+=1
                     self.seg_in_feild[j].rule_inc[x].append(rule_indx)

        return
    

    def SelectDimention(self):
        

        for j in range(0,self.DIM):
            cnt=0
            for x in self.seg_in_feild[j].rule_cnt:
                cnt=cnt+x
            
        
            avg_weight=int(cnt*100/len(self.seg_in_feild[j].rule_cnt))
            self.field_info.append((avg_weight,j))
            
    
#         self.field_info.sort()
        self.field_info=sorted(self.field_info, key=itemgetter(0),reverse=True)
        
        seq=[]
        for info in self.field_info:
            seq.append(info[1])
        
        self.field_sequence=seq
        
        print(self.field_info) 
        print(self.field_sequence) 
        
        return
    
    def InitRoot(self):
        '''
        return root
        '''
                
        #root_node
        #seg_num=len(point_set)-1
        root_j=self.field_sequence[0]
        root_range=(0, self.seg_in_feild[root_j].seg_num-1)
        root_inc_rule=list(range(0, len(self.ruleset)))
        
        root=TreeNode()
        root.SetTreeNode(root_j,  root_range)
        root.SetIncRule(root_inc_rule)
        root.SetHierarchy(0)
        
#         print("\n___________________Tree Root Info________________\seg_num")
#         root_node.ShowNode()   
        
        return root
        
    def CalcHalfWeight(self, j, node,tmp_seg_in_feild):
        '''
        return half_weight

        '''
        half_weight=0        
        for indx in range(node.indx_range[0], node.indx_range[1]+1):
            half_weight=half_weight+tmp_seg_in_feild.rule_cnt[indx]
        
        return half_weight / 2                        
     
#     
#     
#     def ProjectSpcae(self,j,space_range,include_rules):
#         '''
#         
#         :param j: j is feild_index
#         :param space_range: space_range is [range_start, range_end)
#         :param rule_inc:      
#         
#         return space_points
#         '''
# 
#         tmp_space_points=[]
# 
#         
#         for rule_indx in include_rules:
#             rules_start=self.ruleset[rule_indx][j][0]
#             # rule is a type of indx_range [rule_start, rule_end)
#             rules_end=self.ruleset[rule_indx][j][1]+1
#             
#             # space_range is [ , )
#             if rules_start < space_range[0] :
#                 rules_start=space_range[0]
#             if rules_end > space_range[1] :
#                 rules_end=space_range[1]
#                 
#             tmp_space_points.append(rules_start) 
#             tmp_space_points.append(rules_end)            
#         
#         space_points=self.ElementRepetition(tmp_space_points)
# 
#         return space_points
#     
#     
#     def ProjectSpcaeAllowedEmpty(self,j,space_range,include_rules):
#         '''
#         
#         :param j: j is feild_index
#         :param space_range: space_range is [range_start, range_end)
#         :param rule_inc:      
#         
#         return space_points
#         '''
# 
#         tmp_space_points=[]
#         higher_rules_start=None
#         higher_rules_end=None
#         
#         for rule_indx in include_rules:
#             rules_start=self.ruleset[rule_indx][j][0]
#             # rule_indx is a type of indx_range [rule_start, rule_end)
#             rules_end=self.ruleset[rule_indx][j][1]+1
#             
#             # space_range is [ , )
#             # modify rules_start & rules_end
#             if rules_start < space_range[0] :
#                 rules_start=space_range[0]
#             if rules_end > space_range[1] :
#                 rules_end=space_range[1]
#             
#             # PriorityCover
#             # rule_indx is the priority
#             if rule_indx == include_rules[0]:
#                 higher_rules_start=self.ruleset[rule_indx][j][0]
#                 higher_rules_end=self.ruleset[rule_indx][j][1]
#             else:
#                 if (rules_start > higher_rules_start ) and (rules_end <higher_rules_end):
#                     continue
#                 if (rules_start > higher_rules_start) and (rules_start < higher_rules_end+1):
#                     pass
#                 if (rules_end < higher_rules_end) and (rules_end -1 > higher_rules_start):
#                     pass
#             
#             tmp_space_points.append(rules_start) 
#             tmp_space_points.append(rules_end)            
#         
#         space_points=self.ElementRepetition(tmp_space_points)
# 
#         return space_points
# 
# 
#                 
#         
#         
#     def SegmentSpace(self,j,space_points,include_rules):
#         '''
#         
#         :param j:
#         :param space_points: project from space_range  [range_start, range_end)
#         :param rule_inc:
#     
#         return seg_set    (seg_rule_cnt,seg_include_rule,seg_range)
#         
#         '''
#         seg_set=[]
# 
#         seg_start=space_points[0]
#         for end_point in space_points:
#             #skip
#             if(end_point==space_points[0]):
#                 continue
#             
#             #init
#             seg_rule_cnt=0
#             seg_include_rule=[]
#             seg_end=end_point
#             
#             for rule_indx in include_rules:  
#                 rule_start=self.ruleset[rule_indx][j][0]
#                 rule_end=self.ruleset[rule_indx][j][1]+1               
#                 
#                 # segment [seg_start, seg_end)
#                 # rule [rule_start, rule_end)
#                 if((rule_end > seg_start and  rule_start < seg_end  )):
#                     seg_rule_cnt=seg_rule_cnt+1
#                     seg_include_rule.append(rule_indx)
# 
#             seg_range=(seg_start,seg_end)
#             
#             seg_set.append((seg_rule_cnt,seg_include_rule,seg_range))     
#                       
#             seg_start=seg_end
# 
#         return seg_set

    
            

    
           
        
    def QurrySplitIndx(self,j,node,tmp_seg_in_feild):
        '''
        return qurry_result=(split_point, split_seg_indx, left_rule_include, right_rule_include)

        '''

        half_weight=self.CalcHalfWeight(j,node,tmp_seg_in_feild)    
#         start_indx=node.indx_range[0]
#         end_indx=node.indx_range[1]
        
        tmp_weight=0
        for indx in range(node.indx_range[0], node.indx_range[1]+1):
            tmp_weight=tmp_weight+tmp_seg_in_feild.rule_cnt[indx]
            if(tmp_weight > half_weight):
                return indx

    def QurryD2S(self,j, indx, tmp_seg_in_feild):
        '''
        return d2s
        '''
        return tmp_seg_in_feild.seg_point[indx]
    
#     
#         
#     def QurryLeftSegIndx(self,seg_set):
#         '''
#         return left_seg_indx
# 
#         '''
#         tmp_weight=0
#         left_segindx=0
# #         right_segindx=0
#         half_weight=self.CalcHalfWeight(seg_set)
# #         print("half_weighth = ",half_weight)
#         
# 
#         for segindx in indx_range(0, len(seg_set)):
#             #seg_set[segindx][0] is rule_cnt
#             #(seg_rule_cnt,seg_include_rule,seg_range)
#             tmp_weight=tmp_weight+seg_set[segindx][0]
#             
#             #
#             if tmp_weight <= half_weight:            
#                 left_segindx=segindx
#             else:
#                 break                
# 
#         return left_segindx  
# 
# 
#         
#         

        
    
    def isLeaf(self,j,node, tmp_seg_in_feild):
        '''
        
        :param node:
        '''
        #space may be a point
#         if j==self.field_sequence[5]:
#             if (len(node.space_points) == 2) or  (len(node.rule_inc) <=self.THRESHOLD) or node.GetHierarchy(j) >= self.MAX_HIERARCHY:
#                 return True
#         else:
#             if len(node.space_points) == 2 or node.GetHierarchy(j) >= self.MAX_HIERARCHY or len(node.rule_inc) <=self.THRESHOLD:
#                 return  True
        
#         if node.indx_range[0]==node.indx_range[1] or node.GetHierarchy(j) >= self.MAX_HIERARCHY:
#             return  True
#        
#         
        rule_cnt=0
        inc_rule=[]
        for indx in range(node.indx_range[0], node.indx_range[1]+1):
            rule_cnt+=tmp_seg_in_feild.rule_cnt[indx]
            inc_rule.extend(tmp_seg_in_feild.rule_inc[indx])
            
        inc_rule=self.SortElement(inc_rule)
        

        if len(inc_rule) <=self.THRESHOLD or node.indx_range[0]==node.indx_range[1] or node.hierarchy >= self.MAX_HIERARCHY:
                node.rule_inc=inc_rule
                return  True

        return False
    

        
        
        
#     def GenSpace(self,j,space_range,rule_inc):
#         '''
#         
#         :param j:
#         :param space_range:
#         :param rule_inc:
#         :param space: out
#         '''
#         
#         space=Space()
#         space.space_range=space_range
#         space.rule_inc=rule_inc
#         space_points=self.ProjectSpcae(j, space_range,rule_inc)
#         self.SegmentSpace(j, space_points,rule_inc
# 
#         return 
        
        
#     def GenInitNode(self, j, space_range,include_rules):
#         '''
#         
#         :param j:
#         :param space:
#         :param node: out
#         '''
#         node=TreeNode()
#         space_points=self.ProjectSpcae(j, space_range, include_rules)
#         segment_set=self.SegmentSpace(j, space_points, include_rules)
#         node.SetTreeNode(j, space_range, space_points, segment_set, include_rules, 0)
#         
#         return node
#     
#     def GenSubLeftNode(self, j, node, left_segindx):
#         '''
#         
#         :param node:
#         :param split_point:
#         
#         return left_node
#         
#         '''
#         split_point=node.seg_set[left_segindx][2][1]
#         
#         #    left node attribute
#         #    seg_set    (seg_rule_cnt,seg_include_rule,seg_range)
#         left_space_range=(node.space_range[0], split_point)
#         left_space_points=[]
#         for point_L in node.space_points:
#             if point_L <= split_point:
#                 left_space_points.append(point_L)
#                 
#         left_segment_set=[]
#         left_include_rules=[]
#         for segindx_L in indx_range(0, left_segindx+1):
#             left_segment_set.append(node.seg_set[segindx_L])
#             left_include_rules.extend(node.seg_set[segindx_L][1])
#             
#         if len(left_include_rules)==0:
#             return None
#         
#         left_include_rules=self.ElementRepetition(left_include_rules)
# 
#             
#         left_node=TreeNode()
#         left_node.SetTreeNode(j, left_space_range, left_space_points, left_segment_set, left_include_rules )
# #         print(type(node.GetHierarchy(j) +1))
#         left_node.SetHierarchy(j,(node.GetHierarchy(j) +1))
#         
#         return left_node
#         
#     
#     def GenSubRightNode(self, j, node, left_segindx):
#         '''
#         
#         :param node:
#         :param split_point:
#         
#         return left_node
#         
#         '''
#         split_point=node.seg_set[left_segindx][2][1]
#         
#         #    left node attribute
#         #    seg_set    (seg_rule_cnt,seg_include_rule,seg_range)
#         right_space_range=(split_point, node.space_range[1] )
#         right_space_points=[]
#         for point_R in node.space_points:
#             if point_R >= split_point:
#                 right_space_points.append(point_R)
#                 
#         right_segment_set=[]
#         right_include_rules=[]
#         for segindx_R in indx_range(left_segindx+1,len(node.seg_set)):
#             right_segment_set.append(node.seg_set[segindx_R])
#             right_include_rules.extend(node.seg_set[segindx_R][1])
#             
#         if len(right_include_rules)==0:
#             return None
#         
#         right_include_rules=self.ElementRepetition(right_include_rules)
# 
#             
#         right_node=TreeNode()
#         right_node.SetTreeNode(j, right_space_range, right_space_points, right_segment_set, right_include_rules)
#         right_node.SetHierarchy(j,node.GetHierarchy(j)+1)
#        
#         return right_node        
#     

             
#     def CalcAvgWeight(self,seg_set):
#         '''
#         
#         :param space:
#         return avg_weight
#         '''
#         avg_weight=0 
#    
#         for seg in seg_set:
#             #seg_set[x][0] is num_rule
#             #(seg_rule_cnt,seg_include_rule,seg_range)
#             avg_weight=avg_weight+seg[0]
# 
#         try:
#             avg_weight=avg_weight * 100 / len(seg_set)  
#         except ZeroDivisionError:
#             print("the seg_set is empty !!!")   
#                          
#         return int(avg_weight)  
       
# 
#     def SelectDimention_bak(self):
#         '''
#         calc avg_weight to select dimention to split
#         field_sequence = (field_indx, avg_weight)
#         return field_sequence
#         
#         '''
#         #init
#         init_rule_include=list(indx_range(0,len(self.ruleset)))
#         
# #         for x in indx_range(0,len(self.ruleset)) :
# #             init_rule_include.append(x)
#        
# 
#         # Avg_weight in DIM
#         for j in indx_range(0,self.DIM):
#             space_points=self.ProjectSpcae(j, self.DIM_RANGE, init_rule_include)
#             seg_set=self.SegmentSpace(j, space_points, init_rule_include)
#             avg_weight=self.CalcAvgWeight(seg_set)
# 
#             #get avg_weight in j
#             self.field_info.append((j,avg_weight,len(space_points)))
# 
#         self.field_info=sorted(self.field_info, key=itemgetter(1),reverse=True)
#          
#         for sequence in self.field_info:
#             self.field_sequence.append(sequence[0])
#             
# #         print("field_info is ",field_info)
# #         print("self.field_sequence",self.field_sequence)
#         
#         return
#     

    
    
    def ReleaseNode(self,currNode):
#         currNode.space_range=None
#         currNode.space_points=None
#         currNode.seg_set=None
#         currNode.rule_inc=None
#         currNode.hierarchy=None
#         
        return
    
    
    def GenSubNode(self,j,indx_range,tmp_seg_in_feild):
        
        rule_cnt=0
        for indx in range(indx_range[0],indx_range[1]+1):
            rule_cnt+=tmp_seg_in_feild.rule_cnt[indx]
        if rule_cnt== 0:
            return None
        
        #seg_num=len(point_set)-1
        gen_node=TreeNode()
        gen_node.SetTreeNode(j, indx_range)

        
        return gen_node
#     
#     def ClearLogging(self):
#         with open(self.logging, mode='w') as handle:
#             handle.write("#############################################################\seg_num")
#             handle.write("########################   logging  #########################\seg_num")
#             handle.write("#############################################################\seg_num")
#             
#         return
#     
#     
#     
    
    def BuildTires(self, j, node, tmp_seg_in_feild):
        
        # isLeaf
        if self.isLeaf(j, node, tmp_seg_in_feild):  
            self.post_leaf_set.append(node)
            
            #            
            self.node_cnt += 1

            return
        
        else:                  
            # split the space
            # hight speed improved
            
            split_indx=self.QurrySplitIndx(j, node, tmp_seg_in_feild)
            d2s=self.QurryD2S(j, split_indx,tmp_seg_in_feild)
            
            # gen sub node
            # seg_num=len(point_set)-1
            left_range=(node.indx_range[0], split_indx-1)
            right_node=(split_indx, node.indx_range[1])
            left_node=self.GenSubNode(j, left_range,tmp_seg_in_feild)
            right_node=self.GenSubNode(j, right_node,tmp_seg_in_feild)

            
            #insert pairs of nodes
            node.SetSplit(d2s)            
            node.SetPairNode(left_node,right_node)
            
            
            #account
            self.node_cnt += 1
            
            # iterated
            if  left_node != None:
                left_node.SetHierarchy(node.hierarchy+1)
                self.BuildTires(j, left_node,tmp_seg_in_feild)
            if  right_node != None:
                right_node.SetHierarchy(node.hierarchy+1)
                self.BuildTires(j, right_node,tmp_seg_in_feild)



#     def BuildinFeild(self,j):
#         '''
#         :param j: feild_index
#         :modify the post_leaf_set
#         '''                   
# 
#         # re-assembly pre_leaf_set
#         for node in self.pre_leaf_set:
#             # init variable
#             re_rule_include=node.rule_inc
#             re_space_range=self.DIM_RANGE
#             re_space_points=self.ProjectSpcae(j, re_space_range, re_rule_include)
#             re_segment_set=self.SegmentSpace(j, re_space_points, re_rule_include)
#              
#             # re-assembly node
#             node.SetTreeNode(j,re_space_range,re_space_points,re_segment_set,re_rule_include)
#             
#             self.BuildTires(j, node)
#             
#         return


    def ReformSegInField(self,j,node):
        tmp_seg_in_feild=Segments()
                    
        # set tmp_seg_in_feild
        # init
        tmp_seg_in_feild.seg_num=self.seg_in_feild[j].seg_num            
        tmp_seg_in_feild.seg_point=self.seg_in_feild[j].seg_point
        tmp_seg_in_feild.rule_cnt=[0]*tmp_seg_in_feild.seg_num
        
        for x in range(0, tmp_seg_in_feild.seg_num):
            tmp_seg_in_feild.rule_inc.append([])      
            
        # re-form rule_inc 
        # rule_cnt
        # node.indx_range
        tmp_range=[]
        for indx in range(0, tmp_seg_in_feild.seg_num):
            for rule in node.rule_inc:
                if self.seg_in_feild[j].rule_inc[indx].count(rule) > 0:
                    tmp_seg_in_feild.rule_cnt[indx]+=1
                    tmp_seg_in_feild.rule_inc[indx].append(rule)
                    tmp_range.append(indx) 
        
        #re-form node.indx_range
        new_indx_range=(tmp_range[0],tmp_range[-1])
        node.indx_range=new_indx_range
            
        return tmp_seg_in_feild
        
        


    def BuildFeildTree(self,j):
        
        #build sub_tree of pre_leaf_set                        
        for node in self.pre_leaf_set:
            #Be alive in this field
            tmp_seg_in_feild=self.ReformSegInField(j,node)

            self.BuildTires(j, node, tmp_seg_in_feild)
            
            #release memory
            tmp_seg_in_feild=None
            
            
        return
       
           
    def BuildkdTree(self):       
       
        #init
        #build segments in every single field
        self.BuildSegments()
       
        #SelectDimention
        self.SelectDimention()
        
        #set root
        root=self.InitRoot()
        self.kd_tree.SetRoot(root)
        
        # add root into pre_set
        self.pre_leaf_set.append(root)
        
        # processing in j feild
        for j in self.field_sequence:            
            self.BuildFeildTree(j)
           
            #switching pre_leaf_set post_leaf_set  
            self.pre_leaf_set=self.post_leaf_set
            self.post_leaf_set=[]
        
        return



    def CompressStructure(self):
        return 
    
    def MergeRulesInPriority(self):
        for leaf in self.pre_leaf_set:
            if leaf.space_points == 2 :
                leaf.rule_inc=min(leaf.rule_inc)
        return
    
    def PostProcess(self,include_rules):
        self.MergeRulesInPriority()
        self.CompressStructure
        return 

    
    def LookupkdTree(self,currNode,ip):
        '''
        
        :param currNode:
        :param ip:
        
        return leaf_node 
        '''
        
        if currNode.d2s == None:
#             rule_results=currNode.rule_inc

            return currNode
        
        else:
            j=currNode.j
            d2s=currNode.d2s
            
            if ip[j] < d2s:
                currNode=currNode.left_node              
            else:
                currNode=currNode.right_node
                
            return self.LookupkdTree(currNode,ip)
                
        

    
    def PickResultinPri(self, leaf_node, ip):
    
        if len(leaf_node.rule_inc) == 1 :
            result=leaf_node.rule_inc[0]
        else:
            result_set=leaf_node.rule_inc[:]

            for x in range(0, len(result_set))[::-1] :
                for j in range(0, self.DIM):
                    rule_start=self.ruleset[result_set[x]][j][0]
                    rule_end=self.ruleset[result_set[x]][j][1]
                    
                    if rule_start > ip[j] or ip[j] > rule_end:
                        result_set.remove(result_set[x])
                        break
                    
            result=min(result_set)
            
        return  result
    
    def LookupinLeaf(self,ip):
        '''
        
        :param ip:
        
        farther classification in this mothod
        '''
        
        #init
        root_node=self.kd_tree.tree_root
        leaf_node=self.LookupkdTree(root_node, ip)
        result=self.PickResultinPri(leaf_node, ip)

        return result





    def LookupIpSet(self):
        for ip in self.ips_set:
            rule_indx=self.LookupinLeaf(ip)
            self.lookup_results.append(rule_indx)
            
        return
    

    
    def Statistic(self):
        
        with open(self.logging, mode='w') as handle:
            handle.write("\n#################  statistic   #############\n")
           
            # Memory Used
            # TreeNode == 64bit(8 Byte)
            handle.write("\n________________memory info__________________\n")
            handle.write("account of node :%d\n"%(self.node_cnt))
            handle.write("account of leaf :%d\n"%(len(self.pre_leaf_set)))
            
            memory_use=self.node_cnt * 8
            if memory_use < 1024:
                handle.write("%d B memory used\n"%memory_use)
            elif memory_use < 1024*1024:
                handle.write("%d KB memory used\n"%int(memory_use / 1024))
            elif memory_use < 1024*1024*1024:     
                handle.write("%d MB memory used\n"%int(memory_use / 1024 / 1024))
            elif memory_use < 1024*1024*1024*1024:     
                handle.write("%d GB memory used\n"%int(memory_use / 1024 / 1024 / 1024))  
            else:
                handle.write("%d TB memory used\n"%int(memory_use / 1024 / 1024 / 1024 / 1024))
                
            handle.write("\n________________other info__________________\n")
            handle.write("field_info is %s\n"%str(self.field_info))
            handle.write("field_proc_sequence is %s\n"%str(self.field_sequence))
            handle.write("len of rules is %s\n"%str(len(self.ruleset)))
            handle.write("len of ips is %s\n"%str(len(self.ips_set)))
            handle.write("len of lookup_results is %s\n"%str(len(self.lookup_results)))
            
            #hierarchy info 
            leaf_depth=[]
            handle.write("\n_________[leaf set]__________\n")
            for node in self.pre_leaf_set:
                leaf_depth.append(node.hierarchy)   

            handle.write("minimum hierarchy is %d\n"%min(leaf_depth))
            handle.write("maximum hierarchy is %d\n"%max(leaf_depth))

        self.PlotLeaf()
        
        return
            
            
    def PlotLeaf(self):
        
        
        rule_cnt_set=[]
        depth_set=[]
        
        for leaf in self.pre_leaf_set:
            rule_cnt_set.append(len(leaf.rule_inc))
            depth_set.append(leaf.hierarchy)

        
        #---------------------------------------------------  
        x_value=list(range(len(self.pre_leaf_set)))
        y_value0=rule_cnt_set
        y_value1=depth_set

        fig = plt.figure()
        
        
        ax1 = fig.add_subplot(111)
        ax1.plot(x_value, y_value0,'or',label="rule_cnt",fillstyle='none');
        ax1.legend(loc=2)
        ax1.set_ylabel('Y values rule_cnt');
        
        
        ax2 = ax1.twinx() # this is the important function
        ax2.plot(x_value, y_value1, 'og',label = "depth",fillstyle='none')
        ax2.legend(loc=1)
#         ax2.set_xlim([0, np.e]);
        ax2.set_ylabel('Y values for depth');
        
        
        ax2.set_xlabel('leaf nodes');
        plt.savefig("leaf.png")
        plt.show()

        
        return

        
#         
#     def PlotWhole(self,hierarchy_set):
#         
#         #matplotlib
#         x_value=list(range(len(self.pre_leaf_set)))
#         y_value0=hierarchy_set[0]
#         y_value1=hierarchy_set[1]
#         y_value2=hierarchy_set[2]
#         y_value3=hierarchy_set[3]
#         y_value4=hierarchy_set[4]
#         y_value5=hierarchy_set[5]
#         
#         
#         plt.xlabel("leaf")
#         plt.ylabel("hierarchy[x]")
#         plt.plot(x_value, y_value0,'ob',label="f0" ,fillstyle='none')
#         plt.plot(x_value, y_value1,'or' ,label="f1" ,fillstyle='none')
#         plt.plot(x_value, y_value2,'og',label="f2"  ,fillstyle='none')
#         plt.plot(x_value, y_value3,'oy',label="f3"  ,fillstyle='none')
#         plt.plot(x_value, y_value4,'ok',label="f4"  ,fillstyle='none')
#         plt.plot(x_value, y_value5,'oc',label="f5"  ,fillstyle='none')
#         
#         plt.legend()
#         plt.savefig("hierarchy.png")
#         plt.show()
#         
#         return
            
if __name__ == "__main__":
    
    hs=HyperSplit()
    hs.SetPara(100, 32)
    hs.DumpInputData(INPUT_FILE_NAME)
    
#     for x in hs.ruleset:
#         print(x)
#     
#     hs.BuildkdTree()
 
    cProfile.run("hs.BuildkdTree()", "BuildkdTree.txt")
    #创建Stats对象
    p = pstats.Stats("BuildkdTree.txt")
#     p.strip_dirs().sort_stats("time").print_stats(10)
    p.strip_dirs().sort_stats("cumulative").print_stats(20)





    '''
#     hs.BuildkdTree()
    cProfile.run("hs.LookupIpSet()", "cProfile.txt")
    p = pstats.Stats("cProfile.txt")
    p.strip_dirs().sort_stats("time","cumulative").print_stats(10)

    '''
    hs.Statistic()
#     print(memory_usage())
    print("finish...")

    
    
    
    

    
    
    
    
    