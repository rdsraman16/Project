#!/usr/bin/env python

from netmiko import ConnectHandler
import time

#import cgi
#form = cgi.FieldStorage()
#user= form["formData"]	
#print(user)



def precheck():
    #from netmiko import ConnectHandler
    with open('Device.txt') as f:
        devices = f.read().splitlines()
    device_list = list()
    for ip in devices:
        cisco_device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': 'aditi',
            'password': 'aditi',
            'port': 22,
            'secret': 'aditi',  # this is the enable password
            'verbose': True
        }
        device_list.append(cisco_device)

    for device in device_list:
        print('Connecting to ' + device['ip'])
        connection = ConnectHandler(**device)

        print('Entering enable mode ...')
        connection.enable()
        time.sleep(2)

        prompt = connection.find_prompt()
        hostname = prompt[:-1]

        conf_list = ['PE1.txt', 'P.txt', 'PE2.txt', 'CE1.txt', 'CE2.txt']

        print('Checking the initial configuration of the router ' + hostname)
        output = connection.send_command('show run')
        print(output)
        time.sleep(2)
        output = connection.send_command('show version')
        print(output)
        time.sleep(2)

        print('Now checking the status of the interfaces of ' + hostname)
        time.sleep(2)

        with open('Interfaces.txt') as f:
            int = f.read().splitlines()
            # print(int)
        seperator = ','
        # interface = input('Enter the interface you want to enable:')
        # print(input)

        # out = interface
        # print(interface)
        # Yaha pr I can add the interfaces provided in the file, interface wale object ki jagah, output me 'int' daal denge
        # check the interface status
        for interface in int:
            print(interface)
            output = connection.send_command('sh ip interface ' + interface)
            # print(output)
            # if an invalid interface has been entered
            if 'Invalid input detected' in output:
                print('You entered and invalid interface')
                time.sleep(2)
            else:
                first_line = output.splitlines()[0]  # 1st line of the sh ip interface command output
                print(first_line)
                time.sleep(2)
                if not 'up' in first_line:  # if the interface is not up
                    print('The interface is down. Enabling the interface ...')
                    time.sleep(2)
                    commands = ['interface ' + interface, 'no shut', 'exit']  # enabling the interface
                    output = connection.send_config_set(commands)
                    print(output)
                    time.sleep(2)
                    print('#' * 40)
                    time.sleep(2)
                    print('The interface has been enabled')
                    time.sleep(2)
                else:  # if the interface is already enabled
                    print('Interface ' + interface + ' is already enabled')
                    time.sleep(2)
        connection.disconnect()


def check():
    from netmiko import ConnectHandler
    with open('Device.txt') as f:
        devices = f.read().splitlines()
    device_list = list()
    for ip in devices:
        cisco_device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': 'aditi',
            'password': 'aditi',
            'port': 22,
            'secret': 'aditi',  # this is the enable password
            'verbose': True
        }
        device_list.append(cisco_device)

    for device in device_list:
        print('Connecting to ' + device['ip'])
        connection = ConnectHandler(**device)

        print('Entering enable mode ...')
        connection.enable()
        time.sleep(2)
        # print('Now configuring MPLS/VPN, Please provide your inputs')

        prompt = connection.find_prompt()
        hostname = prompt[:-1]

        conf_list = ['PE1.txt', 'P.txt', 'PE2.txt', 'CE1.txt', 'CE2.txt']

        print(device['ip'])
        if device['ip'] == '10.10.10.1':
            print('Configuring the router ' + hostname)
            time.sleep(1)
            print('now running pre in if')
            with open(conf_list[0], 'r') as file:
                filedata = file.read()
                file.close()

                ospf_id = raw_input('Enter the OSPF process id: ')
                area_id = raw_input('Enter the area for the OSPF: ')
                bgp_id = raw_input('Enter the BGP process id: ')
                rt_imp = raw_input('Enter the import route target (x:y) : ')
                rt_exp = raw_input('Enter the export route target (x:y) : ')
                rd = raw_input('Enter the route distinguisher ID  (x:y) : ')

                filedata = filedata.replace('${ospfID}', ospf_id)
                filedata = filedata.replace('${area}', area_id)
                filedata = filedata.replace('${bgpID}', bgp_id)
                filedata = filedata.replace('${RT_imp}', rt_imp)
                filedata = filedata.replace('${RT_exp}', rt_exp)
                filedata = filedata.replace('${RD}', rd)

                new = raw_input('Enter the new configuration file:')
                # Router_list = list()
                with open(new, 'w') as file:
                    file.write(filedata)
                    file.close()
            print('# *40')
            print('now running mpls in if')
            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            print(new)
            time.sleep(2)
            output = connection.send_config_from_file(new)
            print(output)

        elif device['ip'] == '10.10.10.2':
            print('Configuring the router ' + hostname)
            time.sleep(2)
            print('now running pre in if')
            # p1.precheck()
            with open(conf_list[1], 'r') as file:
                filedata = file.read()
            file.close()

            ospf_id = raw_input('Enter the OSPF process id: ')
            area_id = raw_input('Enter the area for the OSPF: ')

            filedata = filedata.replace('${ospfID}', ospf_id)
            filedata = filedata.replace('${area}', area_id)


            new = raw_input('Enter the new configuration file:')
            # Router_list = list()
            with open(new, 'w') as file:
                file.write(filedata)
            file.close()

            print('now running mpls in if')
            # mpls()
            print('now running post in if')
            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            print(new)
            output = connection.send_config_from_file(new)
            print(output)
        elif device['ip'] == '10.10.10.3':
            print('Configuring the router ' + hostname)
            time.sleep(2)
            # p1.precheck()
            with open(conf_list[2], 'r') as file:
                filedata = file.read()
            file.close()

            ospf_id = raw_input('Enter the OSPF process id: ')
            area_id = raw_input('Enter the area for the OSPF: ')
            bgp_id = raw_input('Enter the BGP process id: ')
            rt_imp = raw_input('Enter the import route target(x:y) : ')
            rt_exp = raw_input('Enter the export route target(x:y) : ')
            rd = raw_input('Enter the route distinguisher ID (x:y) : ')

            filedata = filedata.replace('${ospfID}', ospf_id)
            filedata = filedata.replace('${area}', area_id)
            filedata = filedata.replace('${bgpID}', bgp_id)
            filedata = filedata.replace('${RT_imp}', rt_imp)
            filedata = filedata.replace('${RT_exp}', rt_exp)
            filedata = filedata.replace('${RD}', rd)

            new = raw_input('Enter the new configuration file:')
            with open(new, 'w') as file:
                file.write(filedata)
            file.close()
            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            print(new)
            output = connection.send_config_from_file(new)
            print(output)
        elif device['ip'] == '10.10.10.4':
            print('Configuring the router ' + hostname)
            time.sleep(2)
            with open(conf_list[3], 'r') as file:
                filedata = file.read()
            file.close()

            ospf_id = raw_input('Enter the OSPF process id: ')
            area_id = raw_input('Enter the area for the OSPF: ')

            filedata = filedata.replace('${ospfID}', ospf_id)
            filedata = filedata.replace('${area}', area_id)


            new = raw_input('Enter the new configuration file:')
            # Router_list = list()
            with open(new, 'w') as file:
                file.write(filedata)
            file.close()

            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            print(new)
            output = connection.send_config_from_file(new)
            print(output)
        else:
            print('Configuring the router ' + hostname)
            time.sleep(2)
            # p1.precheck()
            with open(conf_list[4], 'r') as file:
                filedata = file.read()
            file.close()

            ospf_id = raw_input('Enter the OSPF process id: ')
            area_id = raw_input('Enter the area for the OSPF: ')

            filedata = filedata.replace('${ospfID}', ospf_id)
            filedata = filedata.replace('${area}', area_id)

            new = raw_input('Enter the new configuration file:')
            # Router_list = list()
            with open(new, 'w') as file:
                file.write(filedata)
            file.close()

            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            output = connection.send_config_from_file(new)
            print(output)
# def mpls():
#     from netmiko import ConnectHandler
#     print('Now configuring router ' + hostname)
#     time.sleep(2)
#     with open('Device.txt') as f:
#         devices = f.read().splitlines()
#     device_list = list()
#     print(device_list)
#     for ip in devices:
#         cisco_device = {
#             'device_type': 'cisco_ios',
#             'ip': ip,
#             'username': 'aditi',
#             'password': 'aditi',
#             'port': 22,
#             'secret': 'aditi',  # this is the enable password
#             'verbose': True
#         }
#         device_list.append(cisco_device)
#
#     for device in device_list:
#         print('Connecting to ' + device['ip'])
#         connection = ConnectHandler(**device)
#
#         print('Entering enable mode ...')
#         connection.enable()
#         time.sleep(2)
#
#         # for n in conf_list:
#         # if device['ip'] == '10.10.10.1':
#         #     n = 0
#         #     with open(conf_list[n], 'r') as file:
#         #         filedata = file.read()
#         # elif device['ip'] == '10.10.10.2':
#         #     n = 1
#         # with open(conf_list[num], 'r') as file:
#         #    filedata = file.read()
#
#         ospf_id = raw_input('Enter the OSPF process id: ')
#         bgp_id = raw_input('Enter the BGP process id: ')
#         rt_imp = raw_input('Enter the import route target(x:y) : ')
#         rt_exp = raw_input('Enter the export route target(x:y) : ')
#         rd = raw_input('Enter the route distinguisher ID (x:y) : ')
#
#         filedata = filedata.replace('${ospfID}', ospf_id)
#         filedata = filedata.replace('${bgpID}', bgp_id)
#         filedata = filedata.replace('${RT_imp}', rt_imp)
#         filedata = filedata.replace('${RT_exp}', rt_exp)
#         filedata = filedata.replace('${RD}', rd)
#
#         new = raw_input('Enter the new configuration file:')
#             # Router_list = list()
#         with open(new, 'w') as file:
#             file.write(filedata)
#                 # print(file)
#                 # print(new)
#                 # elif device['ip'] == '10.10.0.2' :
#                 #     with open('PE2.txt', 'r') as file:
#                 #         filedata = file.read()
#                 # file = raw_input('Enter configuration file for ' + device['ip'] +':')
#                 # print(file)
#         print('Sending the configurations to the router ' + hostname)
#         time.sleep(2)
#         print('Running commands from file to device:' + device['ip'])
#         output = connection.send_config_from_file(new)
#         print(output)
#         connection.disconnect()
# exit()

def postcheck():
    print('Now post checking the routers: ')
    from netmiko import ConnectHandler
    with open('Device_postcheck.txt') as f:
        devices = f.read().splitlines()
    device_list = list()
    for ip in devices:
        cisco_device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': 'aditi',
            'password': 'aditi',
            'port': 22,
            'secret': 'aditi',  # this is the enable password
            'verbose': True
        }
        device_list.append(cisco_device)

    for device in device_list:
        print('Connecting to ' + device['ip'])
        connection = ConnectHandler(**device)

        print('Entering enable mode ...')
        connection.enable()
        time.sleep(2)

        print('#' * 40)
        print('Now running Post-Check')
        output = connection.send_command('show ip protocols')
        print(output)
        time.sleep(2)

        with open('ping_ip_postcheck.txt') as f:
            IPP = f.read().splitlines()
            # print(IPP[0])
            # print(IPP[1])
            ip11 = IPP[0]
            # print(ip11)
            ip22 = IPP[1]
        # print(ip22)
        #	print(ip22)
        #	print(type(ip11))
        #	print(type(IPP[0]))

        ip1 = '10.10.10.4'
        ip2 = '10.10.10.5'
        if device['ip'] == ip1:
            # if device['ip'] = '10.10.10.4'
            # print(device['ip'])
            # output = connection.send_command('ping 192.168.1.22')
            # print(output)
            output = connection.send_command('ping ' + ip11)
            print(output)
            first_line = output.splitlines()[3]  # 1st line of the sh ip interface command output
            print(first_line)
            if 'Success rate is 0 percent' in first_line:
                print('Destination is not reachable')
                time.sleep(1)
                print('Tracing the route')
                output = connection.send_command('traceroute ' + ip11)
		print(output)
            else:
                print('Ping is successful')
        else:
            output = connection.send_command('ping ' + ip22)
            print(output)
            if 'Success rate is 0 percent' in output:
                print('Destination is not reachable')
                time.sleep(1)
                print('Tracing the route')
                output = connection.send_command('traceroute ' + ip11)
		print(output)
            else:
                print('Ping is successful')
        connection.disconnect()



#precheck()
#check()
postcheck()


