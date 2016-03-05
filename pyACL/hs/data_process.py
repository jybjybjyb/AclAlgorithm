#!/usr/bin/python
#coding=utf-8
import os
import re
from operator import itemgetter,attrgetter

# print(os.name)


class IPDATA_PROC:
#     global para
    interval=1
    read_start=0

    #32+32+16+16
    pattern=re.compile(r'\@\s*(\d+)\.(\d+).(\d+).(\d+)\/(\d+)\s*(\d+)\.(\d+).(\d+).(\d+)\/(\d+)\s*(\d+)\s*\:\s*(\d+)\s*(\d+)\s*\:\s*(\d+)')
    #32+32+16+16
    
    
    
    def __init__(self):
        self.rule_set=[]    
        self.merge_set=[]   
        self.read_lines=0     

    
    def TransFormat(self,m1):                
        '''
        
        :param m1:match
        
        retue rule 6 feilds
        
        '''
                            
        for x in range(0,6,5):
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
        
            H16_ipstart=str((ipstart >> 16) & 0xFFFF)
            H16_ipend=str((ipend >> 16) & 0xFFFF)
            
            L16_ipstart=str(ipstart & 0xFFFF)
            L16_ipend=str(ipend & 0xFFFF)

        for x in range(11,14,2):
            dport_start=m1.group(x)
            dport_end=m1.group(x+1)
        
        rule=(H16_ipstart,H16_ipend,L16_ipstart,L16_ipend,dport_start,dport_end)
        
        return rule
            
    def ReadFilterSet(self,file_name):
        
        with open(file_name, mode='r') as handle:                 
            
            for line in handle.readlines():                
                    
                # m1=re.search(r'(\d+\.\d+\.\d+\.\d+\/d+\s\d+\.\d+\.\d+\.\d+)',strings)
                m1=re.match(self.pattern,line)
                if m1:
                    rule=[]
                    for x in range(1, 15):    
#                         print(m1.group(x), end=" ") 
                        rule.append(int(m1.group(x)))
#                     print("\n") 
             
                    rule=tuple(rule)
#                     print(type(rule))
                    self.rule_set.append(rule)


                else:
                    print("no match rules...")

        return
    

    
    
        
    def Merge(self):
        
#         self.rule_set=sorted(self.rule_set,key=itemgetter(4,9,0,1,2,3,5,6,7,8,10,11,12,13),reverse=True)
        self.rule_set=sorted(self.rule_set,key=itemgetter(4,9),reverse=True)
#         self.rule_set.sort(key=None, reverse=True)
        cmp=None
        for x in self.rule_set:            
            if x!=cmp:
                cmp=x
                self.merge_set.append(x)
                print(x)

        return    
    
    def WriteMergeSet(self,file_name):
        
        with open(file_name,mode="w") as handle:
            for rule in self.merge_set:
#                 print(rule)
#                 handle.write(str(rule[4])+" "+str(rule[9])+"\n")
                handle.write("@ ")                
                handle.write(str(rule[0])+".")
                handle.write(str(rule[1])+".")
                handle.write(str(rule[2])+".")
                handle.write(str(rule[3])+"/")
                handle.write(str(rule[4])+" ")
                handle.write(str(rule[5])+".")
                handle.write(str(rule[6])+".")
                handle.write(str(rule[7])+".")
                handle.write(str(rule[8])+"/")
                handle.write(str(rule[9])+" ")                
                handle.write(str(rule[10])+":")
                handle.write(str(rule[11])+" ")
                handle.write(str(rule[12])+":")
                handle.write(str(rule[13])+"\n")


    
    
    def ReadWrite(self,in_file,out_file,cnt_interval,mask_limit):
        read_cnt=0
        tmp_cnt_interval=cnt_interval
        mask_set=[]
        m_set=[]
        with open(in_file, mode='r') as handle:  
       
            for line in handle.readlines():  
                m1=re.match(self.pattern,line)
                
                tmp_cnt_interval-=1              
                while    tmp_cnt_interval==0 :                  
                    tmp_cnt_interval=cnt_interval
                    read_cnt+=1
                    
                    mask_set.append(m1.group(5))                    
                    m_set.append(m1)
        
        #          
        mask_cnt=[]
        for x in range(0,33):
            mask_cnt.append(mask_set.count(str(x)))
        
        print("mask value  ", list(range(0,33)))
        print("mask_cnt is ",mask_cnt)
        print("read_cnt is ",read_cnt)
        gen_cnt=0
        
        with open(out_file, mode='w') as handle:  
     
            for m  in m_set:
                if int(m.group(5)) >= mask_limit and  int(m.group(10)) >= mask_limit:
#                     print(m.group(0))
                    handle.write(m.group(0)+"\n")   
                    gen_cnt+=1
        print("gen_cnt is ",gen_cnt)
        #matplot
        

        
if __name__ == "__main__":

        
    proc=IPDATA_PROC()
    proc.ReadWrite("100k.txt","proc_1k.txt",10,32)
    print("finish...")
    

