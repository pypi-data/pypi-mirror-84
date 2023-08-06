# The MIT License

# Copyright (c) 2020 Axel Fischer (sweep-me.net), Felix Kaschura (sweep-me.net)

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import time
from .ErrorMessage import error, debug
import subprocess # needed for TCPIP to find IP addresses


try:
    import serial
    import serial.tools.list_ports
    import serial.rs485
except:
    pass

try:
    import pyvisa
    import visa # needed to make sure that DeviceClasses using 'import visa' work
except:
    pass


def get_porttypes():
    """ returns a list of all supported port types """ 

    return list(port_types.keys())

        
def get_resources(keys):
    """ returns all resource strings for the given list of port type string """ 

    resources = []

    for key in keys:
        resources += port_types[key].find_resources()
        
    return resources()

def open_resourcemanager(visafile_path = ""):
    """ returns an open resource manager instance """

    rm = None
    
    if visafile_path == "":
    
        try:
            # typically the resource manager is created correctly with the default path
            rm = pyvisa.ResourceManager()
        except:
        
            try:
                # typical path for National instruments visa runtime
                rm = pyvisa.ResourceManager("C:\\Windows\\System32\\visa32.dll")
            except:
            
                try:
                    # typical path for Agilent visa runtime
                    rm = pyvisa.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll")
                except:
                    pass
                    # error("pyvisa was not been loaded. Check if ni-visa runtime is installed.")

                        
    else:
        try:
            rm = pyvisa.ResourceManager(visafile_path)
            
        except:
            error("Creating resource manager from visa dll file '%s' failed." % visafile_path)

    return rm

   
def close_resourcemanager():
    """ closes the current resource manager instance """
    
    if get_resourcemanager():
        rm.close()
      
def get_resourcemanager():
    """ returns and open resource manager object"""

    # first, we have to figure out whether rm is open or closed
    # of open session is a handle, otherwise an error is raised
    # if rm is closed, we have to renew the resource manager
    # to finally return a useful object


    global rm
    
    try:
        rm.session # if object exists the resource manager is open
                
    except pyvisa.errors.InvalidSession:
        
        rm = open_resourcemanager()
        
    except AttributeError: # if rm is not defined
        return False
        
    except:
        return False
 
    return rm
        
    
def is_resourcemanager():
    """ check whether there is a resource manager instance """

    if "rm" in globals():
        return True
    else:
        return False
    
    
def get_port(ID, properties={}):
    """returns an open port object for the given ID and port properties"""
                         
    if ID.startswith("GPIB") or ID.startswith("Prologix"):  # todo: Prologix can be removed here, if ID does not start with Prologix anymore
                    
        try:
            port = GPIBport(ID)
        except:
            error("Ports: Cannot create GPIB port object for %s" % ID)
            return False
            
    elif ID.startswith("ASRL"):
                    
        try:
            port = ASRLport(ID)
        except:
            error("Ports: Cannot create ASRL port object for %s" % ID)
            return False
                   
 
    elif ID.startswith("TCPIP"):
            
        try:
            port = TCPIPport(ID)
        except:
            error("Ports: Cannot create TCPIP port object for %s" % ID)
            return False
         
    elif ID.startswith("COM"):
        
        try:
            port = COMport(ID)
        except:
            error("Ports: Cannot create COM port object for %s" % ID)
            return False         
    
    elif ID.startswith("USB") or ID.startswith("USBTMC"):

        try:
            port = USBTMCport(ID)
        except:
            error("Ports: Cannot create USBTMC port object for %s" % ID)
            return False  

    else:
        error("Ports: Cannot create port object for %s as port type is not defined." % ID)
        return False  
            

    # make sure the initial parameters are set
    port.initialize_port_properties()
                    
        
    # here default properties are overwritten by specifications given in the DeviceClass
    # only overwrite by the DeviceClass which opens the port to allow to alter the properties further in open()
    port.port_properties.update(properties)             
                         
    # port is checked if being open and if not, port is opened
    if port.port_properties["open"] == False:
        
        # in open(), port_properties can further be changed by global PortDialog settings 
        port.open()
        
    # print(port.port_properties)    
        
    return port
        

    
def close_port(port): 
    """close the given port object"""
    # port is checked if being open and if so port is closed    
    if port.port_properties["open"] == True:
        port.close()
        
        
class PortType(object):
    """ base class for any port type such as GPIB, COM, USBTMC, etc. """

    GUIproperties = {}
    
    properties = {                                                          
                        "VID": None,
                        "PID": None,
                        "RegID": None,
                        "Manufacturer": None,
                        "Product": None,
                        "Description": None,
                        "identification": None, # String returned by the instrument
                        "query": None,
                        "Exception": True, # throws exception if no response by port
                        "EOL": "\n",
                        "EOLwrite": None,
                        "EOLread": None,
                        "timeout": 2,
                        "delay": 0.0,
                        "rstrip": True,
                }

    def __init__(self):
        
        self.ports = {}
       
        
    def find_resources(self):
        
        resources = self.find_resources_internal()
        return resources
        
    def find_resources_internal(self):
        return []
        
        
    def add_port(self, ID):
        pass
        

class COM(PortType):

    GUIproperties = {
                    "baudrate": ["50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800", "9600", "19200", "38400", "57600", "115200"][::-1],
                    "terminator": [r"\n", r"\r", r"\r\n", r"\n\r"],
                    "parity": ["N", "O", "E", "M", "S"],
                    }
                    
                    
    properties = PortType.properties                
                   
    properties.update({
                        "baudrate": 9600,
                        "bytesize": 8,
                        "parity": 'N',
                        "stopbits": 1,
                        "xonxoff": False,
                        "rtscts": False,
                        "dsrdtr": False,
                        "rts": True,
                        "dtr": True, 
                        "raw_write": False,
                        "raw_read": False,
                        "encoding": "latin-1",
                        })
                    
    def __init__(self):
        super().__init__()
        


    def find_resources_internal(self):
    
        resources = []
        
        # we list all prologix com port addresses to exclude them from the com port resources
        prologix_addresses = []
        for controller in get_prologix_controllers():
            prologix_addresses.append(controller.get_address())
    
        try:
            for ID in serial.tools.list_ports.comports():

                ID = str(ID.device).split(' ')[0]
                
                if not ID in prologix_addresses:
                    resources.append(ID)
                
        except:
            error("Error during findind COM ports.")                                        
        
        return resources
        
        
class MODBUS(PortType):

    properties = PortType.properties                
                   
    properties.update({}) # no additional properties at the moment

    def __init__(self):
        super().__init__()
        

    def find_resources_internal(self):
    
        resources = []
    
        try:
        
            for ID in serial.tools.list_ports.comports():

                ID = str(ID.device).split(' ')[0] + ":<address>"
                
                resources.append(ID)
                
        except:
            error("Error during findind COM ports for MODBUS communication.")                                        
        
        return resources
        
        
        
class GPIB(PortType):

    properties = PortType.properties                
                   
    properties.update({
                        "GPIB_EOLwrite": None,
                        "GPIB_EOLread": None,
                        })

    def __init__(self):
        super().__init__()
        
    
    def find_resources_internal(self):
    
        resources = []
        
        # check whether Prologix controller is used
        for controller in get_prologix_controllers():
            resources += controller.list_resources()
        
        # get visa resources
        if get_resourcemanager():
        
            resources += rm.list_resources("GPIB?*")
            
            ## one has to remove Interfaces such as ('GPIB0::INTFC',)
            resources = [x for x in resources if not "INTFC" in x]
        
        return resources
        
       
       
       
class ASRL(PortType):

    properties = PortType.properties                
                   
    properties.update({
                        "baudrate"     : 9600,
                        "bytesize"     : 8,
                        "stopbits"     : 1,
                        "parity"       : "N",
                        # "flow_control" : 2,
                        })

    def __init__(self):
        super().__init__()
        
    
    def find_resources_internal(self):
    
        resources = []
        
        if get_resourcemanager():
        
            resources += rm.list_resources("ASRL?*")
                    
        return resources

        
        
class VirtualBench(PortType):
    """ Attention: Virtual Bench is no longer supported as port type. Finding ports should be handled in DeviceClasses."""
 

    def __init__(self):
        super(__class__,self).__init__()
        
    
    def find_resources_internal(self):
        """ Attention: Virtual Bench is no longer supported as port type. The code below can be used to find devices for win32"""
        
        # VirtualBenchPorts
        dev_list = []
        resources = []
        
        try:
        
            objSWbemServices = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".","root\cimv2")
            
            for item in objSWbemServices.ExecQuery("SELECT * FROM Win32_PnPEntity"):
                
                dev = USBdevice()
                
                for name in dev.properties:
                    
                    a = getattr(item, name, None)
                                   
                    if a is not None:
                        try:                    
                            dev.properties[name] = str(a)
                        except:
                            pass
                            
                dev_list.append(dev)      

            VirtualBenchController = {}
            VirtualBenchModels = {}              
                            
            for dev in dev_list:

                if "VID" in dev.properties["DeviceID"] and "PID" in dev.properties["DeviceID"]:
                    if dev.properties["Manufacturer"] != "(Generic USB Hub)" and \
                        dev.properties["Service"] != 'WwanUsbServ' and \
                        dev.properties["Service"] != 'Mbm3CBus' and \
                        dev.properties["Service"] != 'Mbm3DevMt' and \
                        dev.properties["Service"] != 'Modem' and \
                        dev.properties["Service"] != 'ecnssndis':        

                        if dev.properties["Service"] == "usbccgp":  
                        
                            VID = dev.properties["DeviceID"].split("\\")[1].split("&")[0].split("_")[1]
                            PID = dev.properties["DeviceID"].split("\\")[1].split("&")[1].split("_")[1]
                            ControllerID = dev.properties["DeviceID"].split("\\")[2]
                            
                            # print "VID:", VID
                            # print "PID:", PID
                            # print "ControllerID:", ControllerID
                            
                            if VID == "3923": # National Instruments
                        
                                VirtualBenchController[VID+PID] = ControllerID

                        if dev.properties["Name"] != None and "NI VB-" in dev.properties["Name"]:  
                            if "Interface 1 of 4" in dev.properties["Name"]:   
                            
                                VID = dev.properties["DeviceID"].split("\\")[1].split("&")[0].split("_")[1]
                                PID = dev.properties["DeviceID"].split("\\")[1].split("&")[1].split("_")[1]
                                Model = dev.properties["Name"].split(" ")[1].replace("-", "")
                                
                                # print "VID:", VID
                                # print "PID:", PID
                                # print "Model:", Model
                                
                                VirtualBenchModels[VID+PID] = Model

            
            for controller in VirtualBenchController:
                for model in VirtualBenchModels:
                    if controller == model:
                    
                        ID = VirtualBenchModels[model] + "-" + VirtualBenchController[controller]
                        
                        resources.append(ID)
                        
                        if ID in self.ports.keys():
                            self.ports[ID].port_properties["active"] = True
                        else:
                            self.ports[ID] = Port(ID)
                            # here a PortObject is created
                            
        except:
            error("PortManager: VirtualBench cannot be loaded")
            
        finally:
            return resources
        
        
class USBdevice(object):
    # created in order to collect all properties in one object
    
    def __init__(self):
    
        self.properties = {}
        
        for name in ('Availability', 'Caption', 'ClassGuid', 'ConfigManagerUserConfig',
             'CreationClassName', 'Description','DeviceID', 'ErrorCleared', 'ErrorDescription',
             'InstallDate', 'LastErrorCode', 'Manufacturer', 'Name', 'PNPDeviceID', 'PowerManagementCapabilities ',
             'PowerManagementSupported', 'Service', 'Status', 'StatusInfo', 'SystemCreationClassName', 'SystemName'):
             
            self.properties[name] = None
        
        
class USBTMC(PortType):

    properties = PortType.properties

    def __init__(self):
        super().__init__()
        
     
    def find_resources_internal(self):     
    
        resources = []
        
        if get_resourcemanager():
                    
            resources += rm.list_resources("USB?*")
            
        return resources
        
              

class TCPIP(PortType):

    def __init__(self):
        super().__init__()
        
            
    def find_resources_internal(self):
    
        resources = []

        if get_resourcemanager():
    
            resources += list(rm.list_resources("TCPIP?*"))
            # resources += ["TCPIP::xxx.xxx.xxx.xxx::port::SOCKET", "TCPIP::xxx.xxx.xxx.xxx::SOCKET", "TCPIP::www.example.com::INSTR"]
            # return resources

            try:
            
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                process = subprocess.Popen("arp -a", shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, startupinfo=startupinfo)

                for line in iter(process.stdout.readline, b''):
                
                    try:
                        

                        for encoding in ["utf-8", "cp1251", "ascii"]:
                        
                            try:
                                text = line.decode(encoding) 
                                break
                            except:
                                pass
                    
                        try:
                            text = text.replace("\r", "").replace("\n", "")   
                        except:
                            continue
                    
                        if len(text) > 0:
                                
                            if text[0:2] == "  ":
                                
                                if not text.replace(" ", "").isalpha():
                                
                                    ip_addr, mac_addr, addr_type = text.split()
                                    
                                    # print(ip_addr, mac_addr, addr_type)
                                    
                                    if mac_addr != "ff-ff-ff-ff-ff-ff":
                                    
                                        resource = "TCPIP::"+ip_addr+"::INSTR"
                                        
                                        if not resource in resources:                            
                                            resources.append(resource)
                                            
                                        resource = "TCPIP::"+ip_addr+"::SOCKET"
                                        
                                        if not resource in resources:                            
                                            resources.append(resource)

                    except:
                        error()
                
            except:
                error()
                
        # print(resources)            
        return resources
        

        
        """
        from pyVisa project page:
        
        TCPIP::dev.company.com::INSTR	
        -> A TCP/IP device using VXI-11 or LXI located at the specified address. This uses the default LAN Device Name of inst0.
        TCPIP0::1.2.3.4::999::SOCKET
        -> Raw TCP/IP access to port 999 at the specified IP address.
        """

    
        
        
class Port(object):
    """ base class for any port """
    
    def __init__(self, ID):
    
        self.port = None
        
        self.port_ID = ID
        self.port_properties = {
                                "type" : type(self).__name__[:-4],  # removeing port from the end of the port
                                "active": True,
                                "open": False,
                                "Name": None,
                                "NrDevices": 0,
                                "debug": False,
                                "ID": self.port_ID,  # String to open the device 'COM3', 'GPIB0::1::INSTR', ...
                                }
        
        
        self.initialize_port_properties()
                                    
        self.actualwritetime = time.clock() 
        

    def __del__(self):
        pass
        
    def initialize_port_properties(self):
        
        # we need to know the PortType Object
        self.port_type = type(port_types[self.port_properties["type"]])
        
        # we have to overwrite with the properties of the Port_type
        self.update_properties(self.port_type.properties)
                                    
        # in case any port like to do something special, it has the chance now
        self.initialize_port_properties_internal()

    def initialize_port_properties_internal(self):
        pass
        
    def update_properties(self, properties = {}):
    
        self.port_properties.update(properties)
        
    def set_logging(self, state):
        self.port_properties["debug"] = bool(state)
        
    def get_logging(self, state):
        return self.port_properties["debug"]
        
        
    def get_identification(self):
        return "not available"


    def open(self):
              
        self.open_internal()           

        self.port_properties["open"] = True
        
    def open_internal():
        pass
        
    def close(self):  
    
        self.close_internal()
            
        self.port_properties["open"] = False
        
    def close_internal(self):
        pass
        
    def write(self, cmd):
        """ write a command via a port"""
        
        if self.port_properties["debug"]:
            debug(" ".join([self.port_properties["ID"], "write:", repr(cmd)]))
        
        if cmd != "":
            self.write_internal(cmd)
        
        
    def write_internal(self, cmd):
        pass
        
    def write_raw(self, cmd):
        """ write a command via a port without encoding"""
        
        if cmd != "":
            self.write_raw_internal(cmd)
            
    def write_raw_internal(self, cmd):
        # if this function is not overwritten, it defines a fallback to write()
        self.write(cmd)
        
    def read(self, digits = 0):
        """ read a command from a port"""
    
        answer = self.read_internal(digits)
                              
        if self.port_properties["rstrip"] and not self.port_properties["raw_read"]:  # with 'raw_read', everything should be returned.
            answer = answer.rstrip()
            
        if self.port_properties["debug"]:
            debug(" ".join([self.port_properties["ID"], "read:", repr(answer)]))
            
        if answer == "" and self.port_properties["Exception"] == True:
            self.close()
            raise Exception('Port \'%s\' with ID \'%s\' does not respond. Check port properties, e.g. timeout, EOL,..' % (self.port_properties["type"],self.port_properties["ID"]) )

        return answer
        
    def read_internal(digits):
        # has to be overwritten by each Port
        return ""
        
    
    def read_raw(self, digits = 0):
        """ write a command via a port without encoding"""
        
        return self.read_raw_internal(digits)
            
    def read_raw_internal(self, digits):
        # if this function is not overwritten, it defines a fallback to read()
        return self.read(digits)
      

class GPIBport(Port):
    
    def __init__(self, ID):
        
        super(__class__,self).__init__(ID)
                                    
                                    
    def open_internal(self):
  
        ## differentiate between visa GPIB and prologix_controller
        if "Prologix" in self.port_properties["ID"]:
            
            com_port = self.port_properties["ID"].split("::")[-1][9:]  # we take the last part of the ID and cutoff 'Prologix@' to get the COM port
            
            # the prologix controller behaves like a port object and has all function like open, close, clear, write, read
            self.port = prologix_controller[com_port]
            
            # we give the prologix GPIB port the chance to setup
            self.port.open(self.port_properties)  
            
        else:
        
            if get_resourcemanager() ==  False:
                return False

            self.port = rm.open_resource(self.port_properties["ID"])
            self.port.timeout = self.port_properties["timeout"]*1000 # must be in ms now
            if self.port_properties["GPIB_EOLwrite"] != None:
                self.port.write_termination = self.port_properties["GPIB_EOLwrite"]
            if self.port_properties["GPIB_EOLread"] != None:
                self.port.read_termination = self.port_properties["GPIB_EOLread"]
                
            self.port.clear()

        
    def close_internal(self):
    
        self.port.clear()
        self.port.close()
        
        
    def get_identification(self):
        
        self.write("*IDN?")
        return self.read()
        
        
    def write_internal(self, cmd):
    
        if "Prologix" in self.port_properties["ID"]:
            self.port.write(cmd, self.port_properties["ID"].split("::")[1])
        
        else:
            self.port.write(cmd)
        
        time.sleep(self.port_properties["delay"])
        
    def read_internal(self, digits = 0):
    
        if "Prologix" in self.port_properties["ID"]:
            answer = self.port.read(self.port_properties["ID"].split("::")[1])
        else:
            answer = self.port.read()
 
        return answer      
        
        
class ASRLport(Port):
    
    def __init__(self, ID):
        
        super(__class__,self).__init__(ID)

        from pyvisa.constants import StopBits, Parity

        self.parities = {
                    "N": Parity.none,
                    "O": Parity.odd,
                    "E": Parity.even,
                    "M": Parity.mark,
                    "S": Parity.space,
                    }
                    
        self.stopbits = {
                            1   : StopBits.one,
                            1.5 : StopBits.one_and_a_half,
                            2   : StopBits.two,
                            }
   
    # def initialize_port_properties_internal(self):
    
        # self.port_properties.update({
                                    # "baudrate"     : 9600,
                                    # "bytesize"     : 8,
                                    # "stopbits"     : 1,
                                    # "parity"       : "N",
                                    ## "flow_control" : 2,
                                    # })
                                    

    def open_internal(self):       
    
        if get_resourcemanager() ==  False:
            return False
    
        self.port = rm.open_resource(self.port_properties["ID"])
        self.port.timeout = int(self.port_properties["timeout"])*1000  # must be in ms now
        self.port.baud_rate = int(self.port_properties["baudrate"])
        self.port.data_bits = int(self.port_properties["bytesize"])
        self.port.stop_bits = self.stopbits[float(self.port_properties["stopbits"])]
        self.port.parity = self.parities[str(self.port_properties["parity"])]
        # self.port.flow_control = self.parities[str(self.port_properties["parity"])]
        self.port.clear()

        
    def close_internal(self):  
        self.port.clear()
        self.port.close()
        self.port_properties["open"] = False
        
    def write_internal(self, cmd):
                    
        self.port.write(cmd)
        time.sleep(self.port_properties["delay"])  
        
    def read_internal(self, digits = 0):
                
        answer = self.port.read()
 
        return answer      
                
        
class USBTMCport(Port):
    
    def __init__(self, ID):
        
        super().__init__(ID)

    def open_internal(self):
    
        if get_resourcemanager() ==  False:
            return False

        self.port = rm.open_resource(self.port_properties["ID"])
        self.port.timeout = self.port_properties["timeout"]*1000 # must be in ms now
        self.port.clear()
                
    def close_internal(self):  
    
        self.port.clear()
        self.port.close()
        
        
    def get_identification(self):
        
        self.write("*IDN?")
        return self.read()
        

    def write_internal(self, cmd):
            
        self.port.write(cmd)
                    

    def read_internal(self, digits = 0):

        answer = self.port.read()            
        return answer
        
        
class TCPIPport(Port):
    
    def __init__(self, ID):
        
        super(__class__,self).__init__(ID)

        
    def open_internal(self):
    
        if get_resourcemanager() ==  False:
            return False
    
        self.port = rm.open_resource(self.port_properties["ID"])
        self.port.timeout = self.port_properties["timeout"]*1000 # must be in ms now
        self.port.clear()
            
    def close_internal(self):  
        self.port.clear()
        self.port.close()        
        
    def get_identification(self):
        
        self.write("*IDN?")
        return self.read()

    def write_internal(self, cmd):
    
        self.port.write(cmd)
        time.sleep(self.port_properties["delay"])
                 
        
    def read_internal(self, digits = 0):
        answer = self.port.read()
                
        return answer


        
class COMport(Port):
    
    def __init__(self, ID):
    
        
        super(__class__,self).__init__(ID)

        self.port = serial.Serial()

    # def initialize_port_properties_internal(self):
    
        # self.port_properties.update({
                                    # "baudrate": 9600,
                                    # "bytesize": 8,
                                    # "parity": 'N',
                                    # "stopbits": 1,
                                    # "xonxoff": False,
                                    # "rtscts": False,
                                    # "dsrdtr": False,
                                    # "rts": True,
                                    # "dtr": True, 
                                    # "raw_write": False,
                                    # "raw_read": False,
                                    # "encoding": "latin-1",
                                    # })
                                                     
   
    def refresh_port(self):
    
        self.port.port = str(self.port_properties["ID"])
        self.port.timeout = float(self.port_properties["timeout"])
        self.port.baudrate = int(self.port_properties["baudrate"])
        self.port.bytesize = int(self.port_properties["bytesize"])
        self.port.parity = str(self.port_properties["parity"])
        self.port.stopbits = self.port_properties["stopbits"]
        self.port.xonxoff = bool(self.port_properties["xonxoff"])
        self.port.rtscts = bool(self.port_properties["rtscts"])
        self.port.dsrdtr = bool(self.port_properties["dsrdtr"])
        self.port.rts = bool(self.port_properties["rts"])
        self.port.dtr = bool(self.port_properties["dtr"])
        
        
    def open_internal(self):

        self.refresh_port()
                            
        if not self.port.isOpen():
            self.port.open()
        else:
            self.port.close()
            self.port.open()
            
 
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        
        
    def close_internal(self):    
        self.port.close()
        self.port_properties["open"] = False
        
    def write_internal(self, cmd):
        
        
        while time.clock() - self.actualwritetime < self.port_properties["delay"]:
            time.sleep(0.01)
                            
        if self.port_properties["EOLwrite"] != None:    
            eol = self.port_properties["EOLwrite"]
        else: 
            eol = self.port_properties["EOL"]

        if not self.port_properties["raw_write"]:
            try:        
                cmd_bytes = (cmd + eol).encode(self.port_properties["encoding"])
            except:
                cmd_bytes = cmd + eol.encode(self.port_properties["encoding"])
                            
        else:
            cmd_bytes = cmd + eol.encode(self.port_properties["encoding"])
            # just send cmd as is without any eol/terminator because of raw_write
                            
        self.port.write(cmd_bytes)
            
        self.actualwritetime = time.clock() 
        
            
    def read_internal(self, digits = 0):
                
        if digits == 0:
            answer, EOLfound = self.readline()
            
            if not self.port_properties["raw_read"]:
                try:
                    answer = answer.decode(self.port_properties["encoding"])
                except:
                    error("Unable to decode the reading from %s. Please check whether the baudrate and the terminator are correct (Ports -> PortManager -> COM). You can get the raw reading by setting the key 'raw_read' of self.port_properties to True" % (self.port_properties["ID"]))
                    raise
                    
        else:
            answer = self.port.read(digits)
            
            EOLfound = True
            
            if not self.port_properties["raw_read"]:
                try:
                    answer = answer.decode(self.port_properties["encoding"])
                except:
                    error("Unable to decode the reading from %s. Please check whether the baudrate and the terminator are correct (Ports -> PortManager -> COM). You can get the raw reading by setting the key 'raw_read' of self.port_properties to True" % (self.port_properties["ID"]))
                    raise
                                    
        if answer == "" and not EOLfound and self.port_properties["Exception"] == True:
            self.close()
            raise Exception('Port \'%s\' with ID \'%s\' does not respond.\nCheck port properties, e.g. timeout, EOL,.. via Port -> PortManager -> COM' % (self.port_properties["type"],self.port_properties["ID"]) )
                    
        return answer
        
    def write_raw_internal(self, cmd):
    
        current = self.port_properties["raw_write"]
        self.port_properties["raw_write"] = True
        self.write(cmd)
        self.port_properties["raw_write"] = current
        
    def read_raw_internal(self, digits):
    
        current = self.port_properties["raw_read"]
        self.port_properties["raw_read"] = True
        answer = self.read(digits)
        self.port_properties["raw_read"] = current

        return answer
                

    def in_waiting(self):
        return self.port.in_waiting
        
    def readline(self):
        # this function allows to change the EOL, rewritten from pyserial
        
        if self.port_properties["EOLread"] != None:
            EOL = self.port_properties["EOLread"].encode(self.port_properties["encoding"])
        else:
            EOL = self.port_properties["EOL"].encode(self.port_properties["encoding"])
                        
        
        leneol = len(EOL)
        line = bytearray()
        
        EOL_found = False
        
        while True:
            c = self.port.read(1)
            if c:
                line += c
                if line[-leneol:] == EOL:
                    EOL_found = True
                    break
                    
            else:
                break
                
        return bytes(line[:-leneol]), EOL_found
        
        
class PrologixGPIBcontroller():
                
    def __init__(self, address):
    
        # basically the address could be used for COM ports but also for Ethernet
        # at the moment, only COM is supported, but Ethernet could be added later
        self.set_address(address)
        
        self._current_gpib_ID = None
        
        self.ID_port_properties = {}
        
        self.port = serial.Serial()
        self.port.port = self.get_address()
        self.port.baudrate = 115200  # fixed, Prologix adapter automatically recognize the baudrate (tested with v6.0)
        
    def set_address(self, address):
        self._address = str(address)
    
    def get_address(self):
        return self._address

    def list_resources(self):
        if not self._address is None:
            return ["GPIB::%i::Prologix@%s" % (i, self._address) for i in range(1,31,1)]
        else:
            return []

    def open(self, port_properties):
    
        ID = port_properties["ID"].split("::")[1]

        self.ID_port_properties[ID] = port_properties
       
        if not self.port.isOpen():
            self.port.open()
       
        self.port.timeout = self.ID_port_properties[ID]["timeout"]
        
        self.set_mode(1)  # 1 = controller in charge, controller mode
        
        self.set_eos(0)  # 0 =  CR/LF
        
        self.set_eoi(1)  # 1 = eoi at end
        
        self.set_auto(0)  # 0 =  no read-after-write
        
        self.set_readtimeout(self.ID_port_properties[ID]["timeout"])  # read timeout in s
        
        # print("mode to listenonly set")

    def clear(self):
        if self.port.isOpen():
            self.port.reset_input_buffer()
            self.port.reset_output_buffer()    

    def close(self):
        if self.port.isOpen():
            self.port.close()
        

    def write(self, cmd = "", ID = ""):
        """ sends a non-empty command string to the prologix controller and changes the GPIB address if needed beforehand """
    
        if cmd != "":
    
            if ID == "" or cmd.startswith("++"):
                msg = (cmd+"\n").encode('latin-1')
                
            else:
          
                if ID != self._current_gpib_ID:
                    
                    self._current_gpib_ID = str(ID)
                    
                    ## set to current GPIB address
                    ## calls 'write' again, but as the command starts with '++' will not lead to an endless iteration
                    self.write("++addr %s" % self._current_gpib_ID)  
                
                ## some special characters need to be escaped before sending
                ## we start to replace ESC as it will be added by other commands as well and would be otherwise replaced again
                cmd.replace(chr(27), chr(27)+chr(27)) # ESC (ASCII 27)
                cmd.replace(chr(13), chr(27)+chr(13)) # CR  (ASCII 13)
                cmd.replace(chr(10), chr(27)+chr(10)) # LF  (ASCII 10)
                cmd.replace(chr(43), chr(27)+chr(43)) # ‘+’ (ASCII 43) 


                msg = (cmd+"\n").encode(self.ID_port_properties[ID]["encoding"])
                
            # print("write:", msg)
            self.port.write(msg)

        
    def read(self, ID):
        """ requests an answer from the instruments and returns it """
        
        self.write("++read eoi")  # requesting an answer
        
        msg = self.port.readline()
        if self.ID_port_properties[ID]["rstrip"]:
            msg = msg.rstrip()
                        
        return msg.decode(self.ID_port_properties[ID]["encoding"])
        
        
    def set_mode(self, mode):
        self.write("++mode %s" % str(mode))
        
    def get_mode(self):
        self.write("++mode")
        return self.port.readline().rstrip().decode()
    
    def set_eos(self, eos):
        self.write("++eos %s" % str(eos))  # EOS terminator - 0:CR+LF, 1:CR, 2:LF, 3:None
           
    def get_eos(self):
        self.write("++eos")
        return self.port.readline().rstrip().decode()

    def set_eoi(self, eoi):
        self.write("++eoi %s" % str(eoi))  #  0 = no eoi at end, 1 = eoi at end
           
    def get_eoi(self):
        self.write("++eoi")
        return self.port.readline().rstrip().decode()

    def set_auto(self, auto):
        self.write("++auto %s" % str(auto))  # 0 not read-after-write, 1 = read-after-write

    def get_auto(self):
        self.write("++auto")
        return self.port.readline().rstrip().decode()
        
        
    def set_readtimeout(self, readtimeout):
        """ set the read timeout in s """
        
        self.write("++read_tmo_ms %i" % int(max(1, min( 3000,float(readtimeout)*1000 ) ) ) )  # conversion from s to ms, maximum is 3000, minimum is 1
        
    def get_readtimeout(self):
        self.write("++read_tmo_ms")
        return float(self.port.readline().rstrip().decode())/1000.0  # conversion from ms to s
        
    def set_listenonly(self, listenonly):
        """ set listen-only, only supported in mode = device! """
        self.write("++lon %s" % str(listenonly))  # 0 disable 'listen-only' mode, 1 enable 'listen-only' mode

    def get_listenonly(self):
        self.write("++lon")
        return self.port.readline().rstrip().decode()
        
    def get_version(self):
        self.write("++ver")
        return self.port.readline().rstrip().decode()


def add_prologix_controller(address):
    controller = PrologixGPIBcontroller(address) 
    prologix_controller[address] = controller
    
def remove_prologix_controller(address):
    if address in prologix_controller:
        del prologix_controller[address]
    
def get_prologix_controllers():
    return list(prologix_controller.values())
              
              
prologix_controller = {}
# add_prologix_controller("COM23")

        
rm = open_resourcemanager()

    
port_types = {
             "COM" : COM(),
             # "MODBUS": MODBUS(),
             "GPIB": GPIB(),
             # "ASRL": ASRL(), # Serial communication via visa runtime, just used for testing at the moment
             "USBTMC": USBTMC(),
             "TCPIP": TCPIP(),
             # "VB": VirtualBench(), # no longer supported as finding ports can be done in Device Class / Driver
             }
             

        
""" """