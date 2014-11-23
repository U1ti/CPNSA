#!/usr/bin/python

import subprocess
import xml.dom.minidom
import types,os,signal
class nmapGlueClass():
    def __init__(self):
        self.p = None
        

    def nmapScan(self,cmd):
        cmd = cmd.split()
        
        cmd.insert(len(cmd)-1, '--system-dns')
        cmd.insert(len(cmd)-1,'-oX')
        cmd.insert(len(cmd)-1, '-')
        
        
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
       
        if cmd[0] != 'nmap':
            raise RuntimeError("Command should start with 'nmap'.")
        try:
            if os.name == 'nt':
                print cmd
                self.p = subprocess.Popen(cmd, bufsize=100000, startupinfo=startupinfo,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.p = subprocess.Popen(cmd, bufsize=100000, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
            (nmap_output, nmap_err) = self.p.communicate()
            print nmap_output  
            if not nmap_err == "":
                raise RuntimeError(nmap_err)
             
        except RuntimeError as e:
            raise RuntimeError("Error with nmap command:\n"+str(e))
        except Exception as e:
            raise Exception('Nmap is not set properly.\nHint: Make sure nmap is set in the environment variables.\n'+str(e))
        
        
        dom = xml.dom.minidom.parseString(nmap_output)
        global result
        # nmap command line
        result = {'status':{},
                  'scaninfo':{}
                  
                       }
        result['status'] = {
            'cmd': dom.getElementsByTagName('nmaprun')[0].getAttributeNode('args').value,
            'timestr':dom.getElementsByTagName("finished")[0].getAttributeNode('timestr').value,
            'elapsed':dom.getElementsByTagName("finished")[0].getAttributeNode('elapsed').value,
            'uphosts':dom.getElementsByTagName("hosts")[0].getAttributeNode('up').value,
            'downhosts':dom.getElementsByTagName("hosts")[0].getAttributeNode('down').value,
            'totalhosts':dom.getElementsByTagName("hosts")[0].getAttributeNode('total').value
            }
        
        # info about scan
        for val in dom.getElementsByTagName('scaninfo'):
            result['scaninfo'][val.getAttributeNode('protocol').value] = {                
                'type': val.getAttributeNode('type').value,
                'services': val.getAttributeNode('services').value
                }
        
    
        result['scan'] = {}
     
        for dhost in  dom.getElementsByTagName('host'):
            # host ip
           
            host = dhost.getElementsByTagName('address')[0].getAttributeNode('addr').value
            if len(dhost.getElementsByTagName('address'))>1:
                mac = dhost.getElementsByTagName('address')[1].getAttributeNode('addr').value
                if dhost.getElementsByTagName('address')[1].getAttributeNode('vendor'):
                    mac_vendor = dhost.getElementsByTagName('address')[1].getAttributeNode('vendor').value
                else: mac_vendor = "undefined"
            else: 
                mac = "undefined"
                mac_vendor = "undefined"
            if len(dhost.getElementsByTagName('osmatch')) > 0:
                osType = dhost.getElementsByTagName('osmatch')[0].getAttributeNode('name').value
                accuracy = dhost.getElementsByTagName('osmatch')[0].getAttributeNode('accuracy').value
            else:
                osType = "undefined"
                accuracy = "0"
            hostname = ''
            for dhostname in dhost.getElementsByTagName('hostname'):
                hostname = dhostname.getAttributeNode('name').value
                
            result['scan'][host] = {'hostname': hostname}
            for dstatus in dhost.getElementsByTagName('status'):
                # status : up...
                result['scan'][host]['status'] = {'state': dstatus.getAttributeNode('state').value,
                                               'reason': dstatus.getAttributeNode('reason').value,
                                               'mac': mac,
                                               'mac_vendor': mac_vendor,
                                               'OS': osType,
                                               'accuracy': accuracy}
            try:   
                count = 0
                for dport in dhost.getElementsByTagName('port'):
                    # protocol
                    proto = dport.getAttributeNode('protocol').value
                    # port number converted as integer
                    port =  int(dport.getAttributeNode('portid').value)
                    # state of the port
                    state = dport.getElementsByTagName('state')[0].getAttributeNode('state').value
                    # reason
                    reason = dport.getElementsByTagName('state')[0].getAttributeNode('reason').value
                    # name if any
                    name = ''
                    
                    for dname in dport.getElementsByTagName('service'):
                        name = dname.getAttributeNode('name').value
                        print 'service='
                    # store everything
                    
                    
                        
                    result['scan'][host]['port'+str(count)]= {'state': state,
                                                      'reason': reason,
                                                      'name': name,
                                                      'protocol':proto,
                                                      'port':port
                                                      }
                    count+=1
                    
                    
            except Exception as e:
                print e
                return
                
       
        return result
    
    def stopScan(self):
        try:
            self.p.terminate()
        except Exception:
            pass
def main():
        x = nmapGlueClass()
        x.nmapScan('nmap  -A 192.168.1.1')
if __name__ == '__main__':
    main()