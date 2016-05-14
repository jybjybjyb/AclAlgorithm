#!/usr/bin/python
# coding=utf-8

import matplotlib.pyplot as plt
import itertools
from dataproc import data_process as db
import time

class VEC(object):
    
    def __init__(self):
        self.nBit = 1
        self.mask = 0b0
        self.j = "-inf"
        self.p = 0
        self.blockset = []
        
        return
        
class BLOCK(object):
    
    def __init__(self,):
        self.rulenum = 0
        self.ruleset = []
        
        
        
        

class TrieNode(object):
    def __init__(self):
        self.rulenum = 0
        self.ruleset = []
        self.leftnode = None
        self.rightnode = None
        



class DDBS(object):
    
    
    def __init__(self):
        self.BIT_LEN = 4
        self.FIELD_NUM = 1
        self.MAX_DUPLICATION = 5
        self.SWAP_LMIT = 10
        self.SIZE_RULE = 12
        
        self.ruleWidth = 0
        self.pupper = 0       
        self.ruleset = []
        self.mask = 0
        self.dTable = []
        
        return

        
        
        
    def DumpRule(self, ruleset):
#         self.ruleset = ["001*", "0100", "10*0", "1111", "111*", "1*00", "****"]  
        self.ruleset = ruleset
        self.ruleWidth = len(self.ruleset[0])  
        self.pupper = int(len(self.ruleset) * self.MAX_DUPLICATION)   
        print(">> ruleset[0] is %s" % self.ruleset[0])
        print(">> self.ruleWidth is %d" % self.ruleWidth)
#         print(">> rule type is %s", type(self.ruleset[0]))
        
        return
    
    
#     def IntCmpCharBit(self, char_bit, binary_bit):
#         if char_bit == '*' :
#             return 2
#          
#         if char_bit == '1':
#             return 1
#         
#         if char_bit == '0':
#             return 0

        
        
#     def RuleviaMask(self, char_rule, mask):
#         
#         int_rule=0
#         for i in range(len(char_rule)):
#             tmp_bit=self.AndBitviaMask(char_rule[0], mask & (0x1<<i))
#             int_rule= int_rule | (tmp_bit << i)
#         return int_rule             



    def BRPRule(self, rule, pos, leftnode, rightnode):
        char_bit = rule[pos]
        if char_bit != '0':
            rightnode.ruleset.append(rule)
            rightnode.rulenum += 1
        
        if char_bit != '1':
            leftnode.ruleset.append(rule)  
            leftnode.rulenum += 1      

        return
        

    
    def BRPCurrNode(self, currnode, pos):
        
        leftnode = TrieNode()
        rightnode = TrieNode()
        
        for r in currnode.ruleset:
            self.BRPRule(r, pos, leftnode, rightnode)
        
        if leftnode.rulenum == 0 or rightnode.rulenum == 0:
            leftnode = None
            rightnode = None
            return -1

        currnode.leftnode = leftnode
        currnode.rightnode = rightnode
        
        # recycle memory
#         currnode.ruleset=None   
    
        return 0

    
    def FastGrowth(self, ruleset):
        # init...
        iret = 0
        mask = 0
        j = 0xFFFFFFFF
        currleafset = []
        nextleafset = []
        tmpleafset = []
        
        # init tree root
        tree_root = TrieNode()
        tree_root.rulenum = len(self.ruleset)
        tree_root.ruleset = self.ruleset
        currleafset.append(tree_root)
        
        p = 0
        for n in range(1, self.ruleWidth + 1):
            
            if p > self.pupper:
                print(">> p[%u] run over pupper[%u]" % (p, self.pupper))
                return mask
            
            # pos is the 0x1 << pos    
            for pos in range(self.ruleWidth):          
        
                if mask & (0x1 << pos) != 0:
                    continue

                # process brp
                for leaf in currleafset:
                    
                    iret = self.BRPCurrNode(leaf, pos)
                    if iret == -1:
                        tmpleafset.append(leaf)
                    else:
                        tmpleafset.append(leaf.leftnode)
                        tmpleafset.append(leaf.rightnode)
                        
                
                
                # calc J,P
                tmpMaxRuleNum = 0
                tmp_p = 0
                for leaf in tmpleafset:
                    # tmpMaxRuleNum
                    if tmpMaxRuleNum < leaf.rulenum:
                        tmpMaxRuleNum = leaf.rulenum
                        
                    tmp_p += leaf.rulenum
                    
                tmpj = tmpMaxRuleNum 
                
                if tmpj < j:
                    j = tmpj
                    set1 = pos
                    nextleafset = tmpleafset                    
                    p = tmp_p
                
                tmpleafset = []
                
            # post process
            # end pos tracing            
            currleafset = nextleafset
            nextleafset = []
            mask = mask | 0x1 << set1

            if p > self.pupper:
                print(">> p[%u] run over pupper[%u]" % (p, self.pupper))
                # recycle
                currleafset = []
                nextleafset = []
                tmpleafset = []
                return mask    
            
        print(print(">> p[%u] stay not over pupper[%u]" % (p, self.pupper)))    
        # recycle
        currleafset = []
        nextleafset = []
        tmpleafset = []        
        return mask
#     
#     def PfunGrowStage(self,ruleset,vec):
#         
#         num_rule=0
#         for r in ruleset:
#             for x in range(2**vec.nBit):
#                 if r[0] < x:
#                     num_rule+=1
#         
#         #
#         p=num_rule*self.RULE_SIZE*self.FIELD_NUM
#         
#         return p
#         
#         
#     
#     
#     def FastGrowth(self,ruleset):
#         #init
#         vec=0
#         J="-inf"
#         vec_bit_num=1      
#        
#         while self.PfunGrowStage(ruleset, vec_bit_num) < self.pupper:
#         
#             for x in range(0,vec_bit_num):            
#                 if vec & 0b1 <<x ==0:
#                     tmp_vec=vec | 0b1 <<x
#                     tmp_J=self.JfunGrowStage(ruleset, vec_bit_num)
#                     if tmp_J>J:
#                         J=tmp_J
#                         vec=tmp_vec
#             vec_bit_num+=1
#        
#                              
#         self.IntelliSwap(ruleset, vec, J, vec_bit_num)                    
#         
#         return vec_bit_num,vec
#     
#        
#     


    def CalcJViaMask(self, ruleset, mask, nbit_mask):
        
        # init D-table 
        dTable = []
        for x in range(2 ** nbit_mask):
            dTable.append([])      
        
        cntlist = [0] * (2 ** nbit_mask)
        maxRulenum = 0
        
        #
        for char_rule in ruleset:
            e = 0
            insert_indx_set = [0]

            for pos in range(self.ruleWidth):
                if 0x1 << pos & mask != 0:
                    if char_rule[pos] == '0':
                        pass
                    if char_rule[pos] == '1':
                        for i in range(len(insert_indx_set)):
                            insert_indx_set[i] += 2 ** e

                    if char_rule[pos] == '*':
                        add_indxset = insert_indx_set[:]
                        for i in range(len(add_indxset)):
                            add_indxset[i] += 2 ** e
                        insert_indx_set = add_indxset + insert_indx_set
                        add_indxset = []                                               
                    
                    e += 1
                    if e > nbit_mask:
                        print(">> error: e>nbit_mask!!!")
                        print(char_rule, pos, mask, nbit_mask)
                    

            for insert_indx in insert_indx_set:
                # alternatively                
                dTable[insert_indx].append(char_rule) 
                cntlist[insert_indx] += 1             
        
        for n in cntlist:
            if maxRulenum < n:
                maxRulenum = n
        
        # recycle
        dTable = []
        cntlist = []        
        insert_indx_set = []
        
        return maxRulenum

    def IntelliSwap(self, ruleset, mask, nbit_mask):
        
        pos_0 = []
        pos_1 = []
        result_mask=mask          
        
        # init
        for n in range(0, self.ruleWidth):
            if 0x1 << n & mask == 0:
                pos_0.append(n)
            else:
                pos_1.append(n)
        
        j = self.CalcJViaMask(self.ruleset, mask, nbit_mask)
        # swithing
        for x in range(len(pos_0)):
            for y in range(len(pos_1)):
                tmp_mask = mask
#                 print(bin(tmp_mask))

                tmp_mask |= (0x1 << pos_0[x])
                tmp_mask &= ~(0x1 << pos_1[y])
#                 print(bin(tmp_mask))
                
                tmp_j = self.CalcJViaMask(self.ruleset, tmp_mask, nbit_mask)
                if tmp_j < j:
                    j = tmp_j
                    result_mask = tmp_mask
                
        return result_mask
        
#         tmp_list=list(itertools.combinations(range(vec_bit_num),2))
#         print(">>combinations is")
#         print(tmp_list)
#         
#         for indxset in tmp_list:
#             tmp_vec=0            
#             for x in range(0, len(indxset)):               
#                 tmp_vec | 0x1 << x
#                 
#             tmp_J=self.JFun(ruleset, tmp_vec)            
#             if J<tmp_J:
#                 vec=tmp_vec
#                   
#         return vec

        
        
    
    def GenTB(self, ruleset, mask, nbit_mask):

        # init D-table 
        dTable = []
        for x in range(2 ** nbit_mask):            
            dTable.append(BLOCK())
#         print(">> dTable is")
#         print(dTable)
            
        
        #
        for char_rule in ruleset:
            e = 0
            insert_indx_set = [0]

            for pos in range(self.ruleWidth):
                if 0x1 << pos & mask != 0:
                    if char_rule[pos] == '0':
                        pass
                    if char_rule[pos] == '1':
                        for i in range(len(insert_indx_set)):
                            insert_indx_set[i] += 2 ** e

                    if char_rule[pos] == '*':
                        add_indxset = insert_indx_set[:]
                        for i in range(len(add_indxset)):
                            add_indxset[i] += 2 ** e
                        insert_indx_set = add_indxset + insert_indx_set
                        add_indxset = []                                               
                    
                    e += 1
                    

            for insert_indx in insert_indx_set:
                # alternatively                
                dTable[insert_indx].ruleset.append(char_rule) 
                dTable[insert_indx].rulenum += 1             
        
        
#         for n in cntlist:
#             if maxRulenum < n:
#                 maxRulenum = n
        
        # recycle
#         for x in range(2 ** nbit_mask):
#             dTable[x] = []
            
        return dTable
    
    def ShowBlock(self):
        pass
#     def MemoryUse(self,table):
#         rule_cnt=0
#         
#         for x in range(len(table)):
#             rule_cnt+=len(table[x])
#             
#         print("rule_cnt is %u"%rule_cnt)
                

    def CalcNbit(self, mask):
        nbit_mask = 0
        
        for n in range(0, self.ruleWidth):
            if 0x1 << n & mask != 0:
                nbit_mask += 1
        
        return nbit_mask
        
    def EMTBuild(self):
#         self.DumpRule()
        mask = self.FastGrowth(self.ruleset)
        nbit_mask = self.CalcNbit(mask)
        print(">> nbit_mask is %d" % nbit_mask)
        mask = self.IntelliSwap(self.ruleset, mask, nbit_mask)
        print(">> mask is %s" %hex(mask))
        dTable = self.GenTB(self.ruleset, mask, nbit_mask)
        self.mask = mask
        self.dTable = dTable

        return 

    def Statistic(self):
        print(">> statistic...")
        print(">> account of origin rules %u" % len(self.ruleset))
        rulesum = 0
        for b in self.dTable:
            rulesum += b.rulenum
        print(">> account of classified rules %d" % rulesum)
        print(">> duplication is %d" %int((rulesum)/len(self.ruleset)))
        print(">> account of memory used %d kByte" %((rulesum * 4>>10)))
        
    
    
    def Plot(self):
        
        plt.figure(figsize=(10,6), dpi=90)
        x_value = list(range(len(self.dTable)))
        y_value = []
        for b in self.dTable:
            y_value.append(b.rulenum)
        
        plt.xlabel("block[x]")
        plt.ylabel("rule num")
#         plt.legend(loc='upper left')
        plt.bar(x_value, y_value ,color = 'green')
        plt.savefig("ddbs_1.png")
        plt.show()

    
if __name__ == "__main__":


    ddbs = DDBS()
    r = db.IPDATA_PROC()
    
    ddbs.DumpRule(r.GenRule(160,1000))
    start=time.clock()
    ddbs.EMTBuild()
    end=time.clock()
    print ("totlal cpu is %f s " % (end-start))
    ddbs.Statistic()
    ddbs.Plot()
    
    

    
    

    
        
        
        
        
