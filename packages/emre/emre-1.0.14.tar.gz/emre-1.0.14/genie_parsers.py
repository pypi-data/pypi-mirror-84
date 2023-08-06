import re
import sys
from lxml import etree
import xml.dom.minidom
import xml.etree.ElementTree as ET

def genie_str_to_class(classname):
    try:
        module = getattr(sys.modules[__name__], classname)
        return module()
    except Exception as e:
        return '%%%%% No genie module with name: ' + classname

# ==================================================
# Parser for 'show vlan id <vlan id> Get the ports associated if it exists
# ==================================================
class ShowVlanId():

    def parse(self, output=None):

    # Init vars
        parsed_dict = {}
        dict = parsed_dict.setdefault('connected_vlan_ports', {})

    # VLAN Name Status Ports
    # ---- -------------------------------- --------- -------------------------------
    # 2 VLAN0002 active Gi1/0/1, Gi1/0/2

        p1 = re.compile(r'.*active(\s+)(?P<port>(\S+)).*')

        for line in output.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                port = str(group["port"]).rstrip(",")
                port_dict = dict.setdefault(port, {})
                break
        return parsed_dict

# ==================================================
# Parser for 'show monitor capture CAP buffer brief
# ==================================================
class ShowMonitorCapture():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        dict = parsed_dict.setdefault('bgp_keepalive', {})

        #   181 150.405563   10.1.12.1 -> 10.1.3.3 BGP 73 KEEPALIVE Message
        p1 = re.compile(r'.{17}(?P<localhost>(\S+)).{4}(?P<neighbor>(\S+))(\s+)BGP 73 KEEPALIVE Message')

        for line in output.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                localhost = str(group["localhost"])
                host_dict = dict.setdefault(localhost, {})
                host_dict['neighbor'] = str(group['neighbor'])
                host_dict['message'] = "BGP_73_KEEPALIVE_Message"                
                break
        return parsed_dict

# ==================================================
# Parser for 'show ip route 10.1.12.1 Get the ip route if it exists
# ==================================================
class ShowIpRouteVlan():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        dict = parsed_dict.setdefault('connected_vlan', {})

        #   Local host: 10.1.12.1, Local port: 33984
        p1 = re.compile(r'.*directly connected,(\s+)via(\s+)(?P<vlan>(\S+)).*')

        for line in output.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                vlan = str(group["vlan"])
                vlan_number = vlan.replace("Vlan", "")
                vlan_dict = dict.setdefault(vlan_number, {})
                break
        return parsed_dict


# ==================================================
# Parser for 'show ip bgp neighbor | include Local' - extract local IP address
# ==================================================
class ShowIpBgpNeighbor():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        dict = parsed_dict.setdefault('bgp_neighbor', {})

        #   Local host: 10.1.12.1, Local port: 33984
        p1 = re.compile(r'Local host:.{1}(?P<local>(\S+)).*')

        for line in output.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                host = str(group["local"].rstrip(','))
                host_dict = dict.setdefault(host, {})
                break
        return parsed_dict


# ==================================================
# Parser for 'show tech acl' - extract image name
# ==================================================
class ShowTechAclImage():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        acl_dict = parsed_dict.setdefault('acl_image', {})

        #   System image file is "flash:cat9k_iosxe.2020-09-23_18.29_petervh.SSA.bin"
        p1 = re.compile(r'System image file is.{1}(?P<image>(\S+))')

        for line in output.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                image = str(group["image"].lstrip('"').rstrip('"'))
                image_dict = acl_dict.setdefault(image, {})
                break
        return parsed_dict

# ==================================================
# Parser for 'show tech acl' - extract platform information
# ==================================================
class ShowTechAclPlatform():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        acl_dict = parsed_dict.setdefault('acl_platform', {})

#        Switch  Ports    Model                Serial No.   MAC address     Hw Ver.       Sw Ver.
#        ------  -----   ---------             -----------  --------------  -------       --------
#         1       41     C9300-24T             FCW2123L0H4  a0f8.490e.4a80  V01           17.05.01
        p0 = re.compile(r'Switch(\s+)Ports(\s+)Model(\s+)Serial.*')
        p1 = re.compile(r'(?P<switch>(\d+))(\s+)(\d+)(\s+)(?P<model>(\S+))(\s+)(?P<serial>(\S+))(\s+)(?P<mac>(.{14}))(\s+)(?P<hwver>(\S+))(\s+)(?P<swver>(\S+)).*')
        skip = 0
        for line in output.splitlines():
            line = line.strip()
    #
    # Find the line with the column headers for platform information then skip to the actual data
    #
            if skip == 2:
                m = p1.match(line)

                if m:
                    group = m.groupdict()
                    switch = str(group["switch"].lstrip('"').rstrip('"'))
                    switch_dict = acl_dict.setdefault(switch, {})
                    switch_dict['model'] = str(group['model'])
                    switch_dict['serial'] = str(group['serial'])
                    switch_dict['mac'] = str(group['mac'])
                    switch_dict['hwver'] = str(group['hwver'])
                    switch_dict['swver'] = str(group['swver'])
                    return parsed_dict

            if skip == 1:
                skip = 2
            if skip == 0:
                match = p0.match(line)
                if match:
                    skip = 1
        return parsed_dict

# ==================================================
# Parser for 'show tech acl' - extract ACL names
# ==================================================
class ShowTechAclNames():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        acl_dict = parsed_dict.setdefault('acl_names', {})

#------------------ show access-lists ------------------------
#
#
#Extended IP access list IP-Adm-V4-Int-ACL-global
#IPv6 access list implicit_permit_v6

        p0 = re.compile(r'-*(\s+)show(\s+)access-lists.*')
        p1 = re.compile(r'Extended(\s+)IP(\s+)access(\s+)list(\s+)(?P<v4acl>(\S+)).*')
        p2 = re.compile(r'IPv6(\s+)access(\s+)list(\s+)(?P<v6acl>(\S+)).*')
        skip = 0

        for line in output.splitlines():
            line = line.strip()
    #
    # Find the line with the column headers for ACL names then skip to the actual data
    #
            if skip == 3:
                mv4 = p1.match(line)
                if mv4:
                    group = mv4.groupdict()
                    acl_type = "ipv4"
                    switch_dict = acl_dict.setdefault(acl_type, {})
                    switch_dict['name'] = str(group['v4acl'])
                    continue

                mv6 = p2.match(line)
                if mv6:
                    group = mv6.groupdict()
                    acl_type = "ipv6"
                    switch_dict = acl_dict.setdefault(acl_type, {})
                    switch_dict['name'] = str(group['v6acl'])
                    continue

            if skip == 2:
                skip = 3
            if skip == 1:
                skip = 2
            if skip == 0:
                match = p0.match(line)
                if match:
                    skip = 1
        return parsed_dict

# ==================================================
# Parser for 'show tech acl' - extract ACL counters
# ==================================================
class ShowTechAclCounters():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        acl_dict = parsed_dict.setdefault('acl_counters', {})

#=========== Cumulative Stats Across All Asics ===========
#Ingress IPv4 Forward             (0x12000003):         873 frames

        p0 = re.compile(r'=========== Cumulative Stats Across All Asics.*')
        p1 = re.compile(r'(?P<counter>(\S+\s+\S+\s+\S+))\s+\((?P<mask>(.{10})).{2}\s+(?P<frames>(\d+)).*')
        skip = 0

        for line in output.splitlines():
            line = line.strip()
    #
    # Find the ACL counter header line then skip to the actual data
    #
            if skip == 1:
                cnt = p1.match(line)
                if cnt:
                    group = cnt.groupdict()
                    if int(group['frames']) != 0:
                        counter = str(group['counter'])
                        switch_dict = acl_dict.setdefault(counter, {})
                        switch_dict['mask'] = str(group['mask'])
                        switch_dict['frames'] = str(group['frames'])
                continue

            if skip == 0:
                match = p0.match(line)
                if match:
                    skip = 1
        return parsed_dict

# ==================================================
# Parser for 'show tech acl' - extract ACL Exception Statistics
# ==================================================
class ShowTechAclExceptions():

    def parse(self, output=None):

        # Init vars
        parsed_dict = {}
        acl_dict = parsed_dict.setdefault('acl_exceptions', {})

#****EXCEPTION STATS ASIC INSTANCE 0 (asic/core 0/0)****
#=================================================================================
# Asic/core |                NAME                  |   prev   |  current  |  delta
#=================================================================================
#0  0  NO_EXCEPTION                                   0          277         277

        p0 = re.compile(r'.*EXCEPTION STATS ASIC INSTANCE.*')
        p1 = re.compile(r'(?P<asic>(\d+))(\s+)(?P<core>(\d+))(\s+)(?P<name>(.{40}))(\s+)(?P<prev>(\d+))(\s+)(?P<current>(\d+))(\s+)(?P<delta>(\d+)).*')
        skip = 0
        record = 1
        for line in output.splitlines():
            line = line.strip()
    #
    # Find the ACL counter header line then skip to the actual data
    #
            try:
                if skip == 1:
                    cnt = p1.match(line)
                    if cnt:
                        group = cnt.groupdict()
                        if int(group['current']) != 0:
                            switch_dict = acl_dict.setdefault(str(record), {})
                            switch_dict['asic'] = int(group['asic'])
                            switch_dict['core'] = int(group['core'])
                            switch_dict['name'] = str(group['name']).rstrip().replace(" ", "_")
                            switch_dict['prev'] = int(group['prev'])
                            switch_dict['current'] = int(group['current'])
                            switch_dict['delta'] = int(group['delta'])
                            record = record + 1
                    continue

                if skip == 0:
                    match = p0.match(line)
                    if match:
                        skip = 1
            except Exception as e:
                print("%%%% EMRE Error: ShowTechAclExceptions parser: " + str(e))
        return parsed_dict

# ==================================================
# Parser for 'show mac address-table dynamic'
# ==================================================
class ShowMatm():

    ''' Parser for "show mac address-table dynamic" '''

    cli_command = ['show mac address-table dynamic',
                   'show mac address-table dynamic vlan {vlan_id}']

    def cli(self, vlan_id=None, output=None):
        if output is None:
            if vlan_id:
                cmd = self.cli_command[1].format(vlan_id=vlan_id)
            else:
                cmd = self.cli_command[0]
                out = self.device.execute(cmd)
        else:
            out = output

        # Init vars
        parsed_dict = {}
        if out:
            mac_table_dict = parsed_dict.setdefault('mac_table', {})

        #   50    0000.063b.9e74    DYNAMIC     pw100007
        p1 = re.compile(r'^(?P<vlan>(\d+))(\s+)(?P<mac>.{14})(\s+)'
                        '(?P<type>([a-z0-9A-Z]+))(\s+)'
                        '(?P<ports>(\S+))')

        # Total Mac Addresses for this criterion: 5 
        p2 = re.compile(r'Total +Mac +Addresses +for +this +criterion: +(?P<total>(\d+))')

        for line in out.splitlines():
            line = line.strip()

            #   50    0000.063b.9e74    DYNAMIC     pw100007
            m = p1.match(line)
            if m:
                group = m.groupdict()
                mac = str(group['mac'])
                vlan = int(group['vlan'])
                per_vlan_mac_table_dict = mac_table_dict.setdefault('per_vlan_mac_table', {}).setdefault(vlan, {})
                per_vlan_mac_table_dict['vlan'] = vlan
                one_mac_dict = per_vlan_mac_table_dict.setdefault('mac_entry', {}).setdefault(mac, {})
                one_mac_dict['mac'] = mac
                one_mac_dict['type'] = group['type']
                one_mac_dict['ports'] = group['ports']
                continue

            # Total Mac number of addresses:: 1
            m = p2.match(line)
            if m:
                group = m.groupdict()
                mac_table_dict['total'] = int(group['total'])

        return parsed_dict

class ShowInterfaces():
    def print_class_name():
        print("here is the class name: ShowInterfaces")

class ShowProcessesMemoryPlatformSorted():

    ''' Parser for "show processes memory platform sorted" '''

    cli_command = 'show processes memory platform sorted'

    def test():
        print("this is a test from ShowProcessesMemoryPlatformSorted")

    def cli(self, output=None):
        if output is None:
            print("Error: Please provide output from the device")
            return None
        else:
            out = output

        # Init vars
        parsed_dict = {}
        if out:
            mem_dict = parsed_dict.setdefault('system_memory', {})
            procmem_dict = mem_dict.setdefault('per_process_memory', {})

        # System memory: 7703908K total, 3863776K used, 3840132K free, 
        p1 = re.compile(r'System +memory: +(?P<total>(\d+\w?)) +total,'
                        ' +(?P<used>(\d+\w?)) +used,'
                        ' +(?P<free>(\d+\w?)) +free,')

        # Lowest: 3707912K
        p2 = re.compile(r'Lowest: (?P<lowest>(\d+\w?))')


        #    Pid    Text      Data   Stack   Dynamic       RSS              Name
        # ----------------------------------------------------------------------
        #  16994  233305    887872     136       388    887872   linux_iosd-imag
        p3 = re.compile(r'(?P<pid>(\d+))(\s+)(?P<text>(\d+))(\s+)(?P<data>(\d+))'
                        '(\s+)(?P<stack>(\d+))(\s+)(?P<dynamic>(\d+))'
                        '(\s+)(?P<RSS>(\d+))(\s+)(?P<name>([\w-])+)')

        for line in out.splitlines():
            line = line.strip()
 
            m = p1.match(line)
            if m:
                group = m.groupdict()
                mem_dict['total'] = str(group['total'])
                mem_dict['used'] = str(group['used'])
                mem_dict['free'] = str(group['free'])
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                mem_dict['lowest'] = str(group['lowest'])
                continue

            m = p3.match(line)
            if m:
                group = m.groupdict()
                name = str(group['name'])
                one_proc_dict = procmem_dict.setdefault(name, {})
                one_proc_dict['pid'] = int(group['pid'])
                one_proc_dict['text'] = int(group['text'])
                one_proc_dict['data'] = int(group['data'])
                one_proc_dict['stack'] = int(group['stack'])
                one_proc_dict['dynamic'] = int(group['dynamic'])
                one_proc_dict['RSS'] = int(group['RSS'])
                continue

        return parsed_dict


class ShowPlatformSoftwareMemoryCallsite():
    """ Parser for show platform software memory <process> switch active <R0> alloc callsite brief """

    cli_command = 'show platform software memory {process} switch active {slot} alloc callsite brief'

    def cli(self, process, slot, output=None):

        if output is None:
            print("Error: Please provide output from the device")
            return None        
        else:
            out = output

        # Init vars
        parsed_dict = {}
        if out:
            callsite_dict = parsed_dict.setdefault('callsites', {})

        # The current tracekey is   : 1#2315ece11e07bc883d89421df58e37b6
        p1 = re.compile(r'The +current +tracekey +is\s*: +(?P<tracekey>[#\d\w]*)')

        # callsite      thread    diff_byte               diff_call
        # ----------------------------------------------------------
        # 1617611779    31884     57424                   2
        p2 = re.compile(r'(?P<callsite>(\d+))\s+(?P<thread>(\d+))\s+(?P<diffbyte>(\d+))\s+(?P<diffcall>(\d+))')

        max_diff_call = 0
        for line in out.splitlines():
            line = line.strip()
 
            # The current tracekey is   : 1#2315ece11e07bc883d89421df58e37b6
            m = p1.match(line)
            if m:
                group = m.groupdict()
                parsed_dict['tracekey'] = str(group['tracekey'])
                continue

            # callsite      thread    diff_byte               diff_call
            # ----------------------------------------------------------
            # 1617611779    31884     57424                   2
            m = p2.match(line)
            if m:
                group = m.groupdict()
                callsite = int(group['callsite'])
                diff_call = int(group['diffcall'])
                one_callsite_dict = callsite_dict.setdefault(callsite, {})
                one_callsite_dict['thread'] = int(group['thread'])
                one_callsite_dict['diff_byte'] = int(group['diffbyte'])
                one_callsite_dict['diff_call'] = diff_call
                # print_log("&&diff_call = " + str(diff_call) + " callsite = " + str(callsite))
                if diff_call > max_diff_call:
                    max_diff_call = diff_call
                    max_callsite = callsite
                continue
        parsed_dict['max_diff_call_callsite'] = max_callsite
        # print_log("&&&&&&max_diff_call_callsite = " + str(max_callsite) + " process = " + process)
        return parsed_dict


class ShowPlatformSoftwareMemoryBacktrace():
    """ Parser for show platform software memory <process> switch active <R0> alloc backtrace """

    cli_command = 'show platform software memory {process} switch active {slot} alloc backtrace'

    def cli(self, process, slot, output=None):
        if output is None:
            print("Error: Please provide output from the device")
            return None 
        else:
            out = output

         # Init vars
        parsed_dict = {}
        if out:
            backtraces_dict = parsed_dict.setdefault('backtraces', {})

        # backtrace: 1#2315ece11e07bc883d89421df58e37b6   maroon:7F740DEDC000+61F6 tdllib:7F7474D05000+B2B46 ui:7F74770E4000+4639A ui:7F74770E4000+4718C cdlcore:7F7466A6B000+37C95 cdlcore:7F7466A6B000+37957 uipeer:7F747A7A8000+24F2A evutil:7F747864E000+7966 evutil:7F747864E000+7745
        p1 = re.compile(r'backtrace: (?P<backtrace>[\w#\d\s:+]+)$')

        #   callsite: 2150603778, thread_id: 31884
        p2 = re.compile(r'callsite: +(?P<callsite>\d+), +thread_id: +(?P<thread_id>\d+)')

        #   allocs: 1, frees: 0, call_diff: 1
        p3 = re.compile(r'allocs: +(?P<allocs>(\d+)), +frees: +(?P<frees>(\d+)), +call_diff: +(?P<call_diff>(\d+))')

        for line in out.splitlines():
            line = line.strip()
 
            # backtrace: 1#2315ece11e07bc883d89421df58e37b6   maroon:7F740DEDC000+61F6 tdllib:7F7474D05000+B2B46 ui:7F74770E4000+4639A ui:7F74770E4000+4718C cdlcore:7F7466A6B000+37C95 cdlcore:7F7466A6B000+37957 uipeer:7F747A7A8000+24F2A evutil:7F747864E000+7966 evutil:7F747864E000+7745
            m = p1.match(line)
            if m:
                group = m.groupdict()
                backtrace = str(group['backtrace'])#.replace(" ", "*")
                one_backtrace_dict = backtraces_dict.setdefault(backtrace, {})
                continue

            #   callsite: 2150603778, thread_id: 31884
            m = p2.match(line)
            if m:
                group = m.groupdict()
                one_backtrace_dict['callsite'] = int(group['callsite'])
                one_backtrace_dict['thread_id'] = int(group['thread_id'])
                continue

            #   allocs: 1, frees: 0, call_diff: 1
            m = p3.match(line)
            if m:
                group = m.groupdict()
                one_backtrace_dict['allocs'] = int(group['allocs'])
                one_backtrace_dict['frees'] = int(group['frees'])
                one_backtrace_dict['call_diff'] = int(group['call_diff'])
                continue

        return parsed_dict


class ShowMemoryDebugLeaksChunks():
    """ Parser for show show memory debug leaks chunks """

    cli_command = 'show memory debug leaks chunks'

    def cli(self, output=None):
        if output is None:
            print("Error: Please provide output from the device")
            return None 
        else:
            out = output

         # Init vars
        parsed_dict = {}
        section = ""
        match_found = False
        if out:
            addresses_dict = parsed_dict.setdefault('addresses', {})


        #   Address        Size    Parent     Name                Alloc_pc
        # 7EFFCC9AB728    28 7EFFCA3DF410 (MallocLite)     :55FAE8AC9000+897EB09
        p1 = re.compile(r'^(?P<address>\w+) +(?P<size>\d+) +(?P<parent>\w+) +(?P<name>\S+)\s* (?P<alloc_pc>:\w+\+\w+)')

        # Tracekey : 1#2b336c808e968add0d0ca6a35d7a1d82
        p2 = re.compile(r'Tracekey : (?P<tracekey>[#\w]+)')

        
        for line in out.splitlines():
            line = line.strip()
 
            m = p2.match(line)
            if m:
                group = m.groupdict()
                tracekey = str(group['tracekey'])
                parsed_dict["tracekey"] = tracekey
                continue

            if 'reserve Processor memory' in line:
                section = "reserve_processor_memory"
                continue
            elif 'lsmpi_io memory' in line:
                section = "lsmpi_io_memory"
                continue
            elif 'Processor memory' in line:
                section = "processor_memory"
                continue


            m = p1.match(line)
            if m:
                group = m.groupdict()
                address = str(group['address'])
                one_address_dict = addresses_dict.setdefault(address, {})
                one_address_dict["size"] = group['size']
                one_address_dict["parent"] = str(group['parent'])
                one_address_dict["name"] = str(group['name'])
                one_address_dict["alloc_pc"] = str(group['alloc_pc'])
                one_address_dict["memory_type"] = section
                one_address_dict["tracekey"] = tracekey
                match_found = True
                continue

        if match_found:
            return parsed_dict
        else:
            return {}

#####################################################################################
#
#  Parser for TCAM memory use
#
#  Sample show command data to match:
#
#  Table                  Subtype      Dir      Max     Used    %Used       V4       V6     MPLS    Other
#  ------------------------------------------------------------------------------------------------------
#  Mac Address Table      EM           I       32768       22       0%        0        0        0       22
#  Mac Address Table      TCAM         I        1024       21       2%        0        0        0       21
#  L3 Multicast           EM           I        8192        0       0%        0        0        0        0
#
#####################################################################################
class ShowPlatformHardwareFedSwActiveFwdasicResourceTcamUtilization():

    ''' Parser for "show platform hardware fed sw active fwd-asic resource tcam utilization" '''

    cli_command = 'show platform hardware fed sw active fwd-asic resource tcam utilization'

    def test():
        print("this is a test from ShowPlatformHardwareFedSwActiveFwdasicResourceTcamUtilization")

    def cli(self, output=None):
        if output is None:
            print("Error: Please provide output from the device")
            return None
        else:
            out = output
#            out = '''MacAddressTable      TCAM         I        1024       21       2%        0        0        0       21'''

        # Init vars
        parsed_dict = {}

        if out:
            tcam_dict = parsed_dict.setdefault('tcam_table', {})
            app_dict = tcam_dict.setdefault('application', {})

        #Table                  Subtype      Dir      Max     Used    %Used       V4       V6     MPLS    Other
        #------------------------------------------------------------------------------------------------------
        # Mac Address Table      EM           I       32768       26       0%        0        0        0       26

        try:
            p1 = re.compile(r'(?P<table>.{27})(\s+)(?P<dir>(\S+))(\s+)(?P<max>(\d+))(\s+)(?P<used>(\d+))(\s+)(?P<pused>(\d))\..{4}(\s+)(?P<v4>(\d+))(\s+)(?P<v6>(\d+))(\s+)(?P<mpls>(\d+))(\s+)(?P<other>(\d+)).*')
        except Exception as e:
            print(">>>> re exception: " + str(e))

        for line in out.splitlines():
            line = line.strip()
    #
    # remove % characters from line which prevent pattern match
    #
            line = line.replace('%', '')

            m = p1.match(line)
            if m:
                group = m.groupdict()
                name = str(group['table'])
                if "Label" in name:
                    name = 'CTSCellMatrixVPN' + name
                one_proc_dict = app_dict.setdefault(name.replace(' ', ''), {})
                one_proc_dict['dir'] = str(group['dir'])
                one_proc_dict['max'] = int(group['max'])
                one_proc_dict['used'] = int(group['used'])
                one_proc_dict['percent-used'] = int(group['pused'])
                one_proc_dict['v4'] = int(group['v4'])
                one_proc_dict['v6'] = int(group['v6'])
                one_proc_dict['mpls'] = int(group['mpls'])
                one_proc_dict['other'] = int(group['other'])
                continue
        return parsed_dict

########################################################################################
#
# ParseXRSyslogMessage parses an XR syslog message into a Python dictionary that
# can be asserted as a FACT in CLIPS
#
########################################################################################
class ParseXRSyslogMessage():

    def syslog(self, message=None):
        ''' Parser for XR Syslog messages with the form:
            RP/0/RSP0/CPU0:Apr 26 20:30:07.568 UTC: ifmgr[257]: %PKT_INFRA-LINEPROTO-5-UPDOWN : Line protocol Up 

            Syslog FACTS will have the form 'source':'date':'time':'component':'syslog':'content' '''
        # Init vars
        parsed_dict = {}
        one_proc_dict = parsed_dict.setdefault('syslog-message', {})

        try:
            p1 = re.compile(r'(?P<source>([^:]+))(?P<date>.{7})(?P<time>(.*:))'
                             '(\s+)(?P<component>(.*:))(\s+)(?P<syslog>(.*:))(\s+)(?P<content>(.*))')
        except Exception as e:
            print(">>>> re exception: " + str(e))
        m = p1.match(message)
        if m:
            group = m.groupdict()
            one_proc_dict['source'] = str(group['source']).lstrip().rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['date'] = str(group['date']).lstrip().rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['source'] = str(group['source']).lstrip().rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['time'] = str(group['time']).lstrip().rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['component'] = str(group['component']).lstrip().rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['syslog'] = str(group['syslog']).lstrip().rstrip().rstrip(":").lstrip(":").replace(" ", "_").rstrip("_")
            one_proc_dict['content'] = str(group['content']).lstrip().rstrip(":").lstrip(":").replace(" ", "_").replace(",", "").replace(")", "").replace("(", "")

        return parsed_dict


########################################################################################
#
# ParseXESyslogMessage parses an XR syslog message into a Python dictionary that
# can be asserted as a FACT in CLIPS
#
########################################################################################
class ParseXESyslogMessage():

    def syslog(self, message=None):
        ''' Parser for Xe Syslog messages with the form:
             *Apr 27 11:12:14.549: %SYS-5-CONFIG_I: Configured from console by admin on vty5 (10.24.105.165)
             *Apr 27 11:12:45.184: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback222, changed state to up
             *Apr 27 11:12:46.394: %SYS-5-CONFIG_I: Configured from console by admin on vty5 (10.24.105.165)

            Syslog FACTS will have the form 'source':'date':'time':'component':'syslog':'content' '''
        # Init vars
        parsed_dict = {}
        one_proc_dict = parsed_dict.setdefault('syslog-message', {})

        try:
            p1 = re.compile(r'(?P<date>.{8})(?P<time>(.*:))(\s+)()(?P<syslog>(.*:))(\s+)(?P<content>(.*))')

        except Exception as e:
            print(">>>> re exception: " + str(e))
        m = p1.match(message)
        if m:
            group = m.groupdict()
            one_proc_dict['source'] = 'source'
            one_proc_dict['date'] = str(group['date']).lstrip().lstrip("*").rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['time'] = str(group['time']).lstrip().rstrip(":").lstrip(":").replace(" ", "_")
            one_proc_dict['component'] = 'xe-syslog'
            one_proc_dict['syslog'] = str(group['syslog']).lstrip().rstrip().rstrip(":").lstrip(":").replace(" ", "_").rstrip("_")
            one_proc_dict['content'] = str(group['content']).lstrip().rstrip(":").lstrip(":").replace(" ", "_").replace(",", "").replace(")", "").replace("(", "")

        return parsed_dict

########################################################################################
#
# ParseRFC5277Message parses a NETCONF RFC5277 notification message into a Python dictionary that
# can be asserted as a FACT in CLIPS
#
########################################################################################
class ParseRFC5277Message():

    def rfc5277(self, message=None):
        messagexml = xml.dom.minidom.parseString(message)
        # Init vars
        parsed_dict = {}
        one_proc_dict = parsed_dict.setdefault('rfc5277-message', {})

        try:
            one_proc_dict['source'] = 'source'
            one_proc_dict['datetime'] = str(messagexml.getElementsByTagName('eventTime')[0].firstChild.nodeValue)
            one_proc_dict['component'] = str(messagexml.getElementsByTagName('clogHistFacility')[0].firstChild.nodeValue)
            one_proc_dict['severity'] = str(messagexml.getElementsByTagName('clogHistSeverity')[0].firstChild.nodeValue)            
            one_proc_dict['msgname'] = str(messagexml.getElementsByTagName('clogHistMsgName')[0].firstChild.nodeValue).lstrip().rstrip(":").lstrip(":").replace(" ", "_").replace(",", "").replace(")", "").replace("(", "")
            one_proc_dict['msgcontent'] = str(messagexml.getElementsByTagName('clogHistMsgText')[0].firstChild.nodeValue).lstrip().rstrip(":").lstrip(":").replace(" ", "_").replace(",", "").replace(")", "").replace("(", "")
        except Exception as e:
            print(">>>> rfc5277 exception: " + str(e))

        return parsed_dict

# ==================================================
# Parser for 'show platform software fed active matm macTable'
# ==================================================
class ShowPlatformSoftwareFedActiveMatmMactable():

    ''' Parser for "show platform software fed active matm macTable vlan {vlan_id}" '''

    cli_command = ['show platform software fed active matm macTable',
                   'show platform software fed active matm macTable vlan {vlan_id}']

    def cli(self, vlan_id=None, output=None):
        if output is None:
            if vlan_id:
                cmd = self.cli_command[1].format(vlan_id=vlan_id)
            else:
                cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output

        # Init vars
        parsed_dict = {}
        if out:
            mac_table_dict = parsed_dict.setdefault('mac_table', {})

        # 1      7488.bb78.37ff         0x1      2      0      0  0x7fde0972eb88      0x7fde0972e7d8      0x0                 0x7fde0899f078            300       17  HundredGigE1/0/11               Yes

        p1 = re.compile(r'^(?P<vlan>(\d+))(\s+)(?P<mac>.{14})(\s+)'
                        '(?P<type>(0[xX][a-f0-9A-F]+))(\s+)'
                        '(?P<seq>(\d+))(\s+)(?P<ec_bits>(\d+))(\s+)(?P<flags>(\d+))(\s+)'
                        '(?P<mac_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<si_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<ri_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<di_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<a_time>(\d+))(\s+)(?P<e_time>(\d+))(\s+)'
                        '(?P<ports>(\S+))(\s+)(?P<consistency>([a-zA-Z]+))')

        # Total Mac number of addresses:: 1
        p2 = re.compile(r'Total +Mac +number +of +addresses:: +(?P<total>(\d+))')

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                mac = str(group['mac'])
                vlan = int(group['vlan'])
                per_vlan_mac_table_dict = mac_table_dict.setdefault('per_vlan_mac_table', {}).setdefault(vlan, {})
                per_vlan_mac_table_dict['vlan'] = vlan
                one_mac_dict = per_vlan_mac_table_dict.setdefault('mac_entry', {}).setdefault(mac, {})
                #one_mac_dict['vlan'] = int(group['vlan'])
                one_mac_dict['mac'] = mac
                one_mac_dict['type'] = group['type']
                one_mac_dict['seq'] = int(group['seq'])
                one_mac_dict['ec_bits'] = int(group['ec_bits'])
                one_mac_dict['flags'] = int(group['flags'])
                one_mac_dict['mac_handle'] = group['mac_handle']
                one_mac_dict['si_handle'] = group['si_handle']
                one_mac_dict['ri_handle'] = group['ri_handle']
                one_mac_dict['di_handle'] = group['di_handle']
                one_mac_dict['a_time'] = int(group['a_time'])
                one_mac_dict['e_time'] = int(group['e_time'])
                one_mac_dict['ports'] = group['ports']
                one_mac_dict['consistency'] = group['consistency']
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                mac_table_dict['total'] = int(group['total'])

        return parsed_dict

# ==================================================
# Parser for 'show platform software fed switch active matm macTable'
# ==================================================
class ShowPlatformSoftwareFedSwitchActiveMatmMactable():

    ''' Parser for "show platform software fed switch active matm macTable vlan {vlan_id}" '''

    cli_command = ['show platform software fed switch active matm macTable',
                   'show platform software fed switch active matm macTable vlan {vlan_id}']

    def cli(self, vlan_id=None, output=None):
        if output is None:
            if vlan_id:
                cmd = self.cli_command[1].format(vlan_id=vlan_id)
            else:
                cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output

        # Init vars
        parsed_dict = {}
        if out:
            mac_table_dict = parsed_dict.setdefault('mac_table', {})

        # 1      7488.bb78.37ff         0x1      2      0      0  0x7fde0972eb88      0x7fde0972e7d8      0x0                 0x7fde0899f078            300       17  HundredGigE1/0/11               Yes

        p1 = re.compile(r'^(?P<vlan>(\d+))(\s+)(?P<mac>.{14})(\s+)'
                        '(?P<type>(0[xX][a-f0-9A-F]+))(\s+)'
                        '(?P<seq>(\d+))(\s+)(?P<ec_bits>(\d+))(\s+)(?P<flags>(\d+))(\s+)'
                        '(?P<mac_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<si_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<ri_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<di_handle>(0[xX][0-9a-fA-F]+))(\s+)'
                        '(?P<a_time>(\d+))(\s+)(?P<e_time>(\d+))(\s+)'
                        '(?P<ports>(\S+))(\s+)(?P<consistency>([a-zA-Z]+))')

        # Total Mac number of addresses:: 1
        p2 = re.compile(r'Total +Mac +number +of +addresses:: +(?P<total>(\d+))')

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                mac = str(group['mac'])
                vlan = int(group['vlan'])
                per_vlan_mac_table_dict = mac_table_dict.setdefault('per_vlan_mac_table', {}).setdefault(vlan, {})
                per_vlan_mac_table_dict['vlan'] = vlan
                one_mac_dict = per_vlan_mac_table_dict.setdefault('mac_entry', {}).setdefault(mac, {})
                #one_mac_dict['vlan'] = int(group['vlan'])
                one_mac_dict['mac'] = mac
                one_mac_dict['type'] = group['type']
                one_mac_dict['seq'] = int(group['seq'])
                one_mac_dict['ec_bits'] = int(group['ec_bits'])
                one_mac_dict['flags'] = int(group['flags'])
                one_mac_dict['mac_handle'] = group['mac_handle']
                one_mac_dict['si_handle'] = group['si_handle']
                one_mac_dict['ri_handle'] = group['ri_handle']
                one_mac_dict['di_handle'] = group['di_handle']
                one_mac_dict['a_time'] = int(group['a_time'])
                one_mac_dict['e_time'] = int(group['e_time'])
                one_mac_dict['ports'] = group['ports']
                one_mac_dict['consistency'] = group['consistency']
                continue

            m = p2.match(line)
            if m:
                group = m.groupdict()
                mac_table_dict['total'] = int(group['total'])

        return parsed_dict

class ShowHardwareAccessListResourceUtilization():

    ''' Parser for "show hardware access-list resource utilization" '''

    cli_command = 'show hardware access-list resource utilization'

    def test():
        print("this is a test from ShowHardwareAccessListResourceUtilization")

    def cli(self, output=None):
        if output is None:
            print("Error: Please provide output from the device")
            return None
        else:
            out = output

        # Init vars
        parsed_dict = {}

        if out:
            acl_tcam_dict = parsed_dict.setdefault('acl_tcam', {})

#    Protocol CAM                            0       246     0.00   
#    Mac Etype/Proto CAM                     0       14      0.00   
#    L4 op labels, Tcam 0                    0       1023    0.00   

        try:
            p1 = re.compile(r'(?P<type>.{40})(?P<used>(\d+))(\s+)(?P<free>(\d+))(\s+)(?P<percentused>\d*\.?\d*$)')

        except Exception as e:
            print(">>>> re exception: " + str(e))

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                name = str(group['type'])
                name = name.replace(' ', '').replace(',', '').replace('/', '')
                one_proc_dict = acl_tcam_dict.setdefault(name, {})
                one_proc_dict['used'] = int(group['used'])
                one_proc_dict['free'] = int(group['free'])
                one_proc_dict['percentused'] = float(group['percentused'])
                continue
        return parsed_dict

