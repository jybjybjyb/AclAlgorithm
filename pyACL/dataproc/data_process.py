#!/usr/bin/python
#coding=utf-8
import os
import re
from operator import itemgetter,attrgetter
import random
import string
# print(os.name)

class IPDATA_PROC:

    def __init__(self):        
        return
    
    def GenRule(self,rule_width,rule_num):
#         r=random.randint(0,0xFFFFFFFF)
#         rchar=str(bin(r))
#          
#         print(rchar)
#         rchar=list(rchar)
#         rchar[2]='*'
#         r=','
#         r.join(rchar)
#         
#         print(r)

#         r=rchar.split(sep='')
#         print(r)
#         print(type(rchar))
#         rchar[0]='*'
 
 
        ruleset=[] 
        for x in range(rule_num):
            rule=''
            for x in range(rule_width):
    #             r=random.choice(['0','1','*'])
    #             print(r)
                rule+=random.choice(['0','1','*'])
    
#             print(rule)
#             print(rule[0])
#             print(type(rule))
            
            ruleset.append(rule)
        
        return ruleset
                


        
if __name__ == "__main__":       
    proc=IPDATA_PROC()
    ruleset=proc.GenRule()
    print(ruleset)

    

