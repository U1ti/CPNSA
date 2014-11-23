'''
Created on June 16, 2013

@author: Toshiba
'''
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi import builder, view



class SNMPManager():
   
    
    def change2int(self, list):
        new_list = []
        for i in list:
            new_list.append(int(i))
        return new_list
   
    def requestSNMP(self,ip,port,OID): 
        mibBuilder = builder.MibBuilder().loadModules()
        mibViewController = view.MibViewController(mibBuilder)
    
        
        errorIndication, errorStatus, errorIndex, \
                         varBindTable = cmdgen.CommandGenerator().nextCmd(
            cmdgen.CommunityData('test-agent', 'public'),
            cmdgen.UdpTransportTarget((ip, port)),
            (OID)
            )
        
        if errorIndication:
            
            raise Exception( errorIndication)
        else:
            if errorStatus:
                err =  '%s at %s\n' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                raise Exception(err)
            else:
                temp_dic = {}
              
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
                        final_form  =  tuple(self.change2int(name.prettyPrint().split('.')))
                        oid, label, suffix = mibViewController.getNodeName(
                                     final_form
                        )
                        
                        temp_dic[name.prettyPrint()] = [label,val.prettyPrint()]
               
                return temp_dic
                        
    
if __name__ == '__main__':                    
    snm = SNMPManager('127.0.0.1')
    snm.requestSNMP()
                        