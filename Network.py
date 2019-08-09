#!/usr/bin/env python

from netmiko import ConnectHandler
import time
import cgi
form = cgi.FieldStorage()
import cgitb
cgitb.enable()
print "Content-Type: text/html: text/html;charsert=utf-8"

print "Content-type:text/html\r\n\r\n"
radioSel = form["radioSel"]
# checkk = form["check"]
# postcheckk = form["postcheck"]

user = form["ip"]
user1 = form["ospfID"]
user2 = form["ospfArea"]
user3 = form ["bgpID"]
user4 = form["expRT"]
user5 = form["impRT"]
user6 = form["RD"]
user7 = form["ospfID1"]
user8 = form["ospfArea1"]

#print(user.value)
#print(user1)
#print('Content-Type: text/plain')
print('')
#print('getting from server:'+ user.value);
#print('')
#print('getting from server:'+ user1.value);

webList = list()
webList =[user.value,user1.value,user2.value,user3.value,user4.value,user5.value,user6.value,user7.value,user8.value]
#print(webList)

def precheck():
    from netmiko import ConnectHandler
    # with open('Device.txt') as f:
    #     devices = f.read().splitlines()
    device_list = list()
    # for ip in devices:
    cisco_device = {
        'device_type': 'cisco_ios',
        'ip': webList[0],
        'username': 'aditi',
        'password': 'aditi',
        'port': 22,
        'secret': 'aditi',  # this is the enable secret password
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
    # with open('Device.txt') as f:
    #     devices = f.read().splitlines()
    device_list = list()
    # for ip in devices:
    cisco_device = {
        'device_type': 'cisco_ios',
        'ip': webList[0],
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

        #print(device['ip'])
        if device['ip'] == '10.10.10.1':
            print('Configuring the router ' + hostname)
            time.sleep(1)
            #print('now running pre in if')
            with open(conf_list[0], 'r') as file:
                filedata = file.read()
                file.close()

               
                filedata = filedata.replace('${ospfID}', webList[1])
                filedata = filedata.replace('${area}', webList[2])
                filedata = filedata.replace('${bgpID}', webList[3])
                filedata = filedata.replace('${RT_exp}', webList[4])
                filedata = filedata.replace('${RT_imp}', webList[5])
                filedata = filedata.replace('${RD}', webList[6])

                #new = raw_input('Enter the new configuration file:')
                # Router_list = list()
                with open('/var/www/cgi-bin/new1.txt', 'w+') as file:
                    file.write(filedata)
                file.close()

                #n1= new1.txt

                
            print('#' * 40)
            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            output = connection.send_config_from_file('new1.txt')
            print(output)
            print('End of Configuration')
            print('#' * 60)

        elif device['ip'] == '10.10.10.2':
            print('Configuring the router ' + hostname)
            time.sleep(2)
            #print('now running pre in if')
            # p1.precheck()
            with open(conf_list[1], 'r') as file:
                filedata = file.read()
            file.close()

            # ospf_id = raw_input('Enter the OSPF process id: ')
            # area_id = raw_input('Enter the area for the OSPF: ')

            filedata = filedata.replace('${ospfID}', webList[7])
            filedata = filedata.replace('${area}', webList[8])


            #new = raw_input('Enter the new configuration file:')
            # Router_list = list()
            with open('/var/www/cgi-bin/new2.txt', 'w+') as file:
                file.write(filedata)
            file.close()

            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            # print(new)
            output = connection.send_config_from_file('new2.txt')
            print(output)
            print('End of Configuration')
            print('#' * 60)

        elif device['ip'] == '10.10.10.3':
            print('Configuring the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            # p1.precheck()
            with open(conf_list[2], 'r') as file:
                filedata = file.read()
            file.close()

            filedata = filedata.replace('${ospfID}', webList[1])
            filedata = filedata.replace('${area}', webList[2])
            filedata = filedata.replace('${bgpID}', webList[3])
            filedata = filedata.replace('${RT_exp}', webList[4])
            filedata = filedata.replace('${RT_imp}', webList[5])
            filedata = filedata.replace('${RD}', webList[6])


            #new = raw_input('Enter the new configuration file:')
            with open('/var/www/cgi-bin/new3.txt', 'w+') as file:
                file.write(filedata)
            file.close()
            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            output = connection.send_config_from_file('new3.txt')
            print(output)
            print('End of Configuration')
            print('#' * 60)

        elif device['ip'] == '10.10.10.4':
            print('Configuring the router ' + hostname)
            time.sleep(2)
            with open(conf_list[3], 'r') as file:
                filedata = file.read()
            file.close()

            filedata = filedata.replace('${ospfID}', webList[7])
            filedata = filedata.replace('${area}', webList[8])


            #new = raw_input('Enter the new configuration file:')
            # Router_list = list()
            with open('/var/www/cgi-bin/new4.txt', 'w+') as file:
                file.write(filedata)
            file.close()

            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            time.sleep(2)
            output = connection.send_config_from_file('new4.txt')
            print(output)
            print('End of Configuration')
            print('#' * 60)
        else:
            print('Configuring the router ' + hostname)
            time.sleep(2)
            # p1.precheck()
            with open(conf_list[4], 'r') as file:
                filedata = file.read()
            file.close()

            # ospf_id = raw_input('Enter the OSPF process id: ')
            # area_id = raw_input('Enter the area for the OSPF: ')

            filedata = filedata.replace('${ospfID}', webList[7])
            filedata = filedata.replace('${area}', webList[8])

            #new = raw_input('Enter the new configuration file:')
            # Router_list = list()
            with open('/var/www/cgi-bin/new5.txt', 'w+') as file:
                file.write(filedata)
            file.close()

            print('Sending the configurations to the router ' + hostname)
            time.sleep(2)
            print('Running commands from file to device:' + device['ip'])
            output = connection.send_config_from_file('new5.txt')
            print(output)
            print('End of Configuration')
            print('#' * 60)

def postcheck():
    print('Now post checking the routers: ')
    from netmiko import ConnectHandler
    # with open('Device_postcheck.txt') as f:
    #     devices = f.read().splitlines()
    device_list = list()
    # for ip in devices:
    cisco_device = {
        'device_type': 'cisco_ios',
        'ip': webList[0],
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
            ip11 = IPP[0]
            ip22 = IPP[1]

        ip1 = '10.10.10.4'
        ip2 = '10.10.10.5'
        if device['ip'] == ip1:
            
            output = connection.send_command('ping ' + ip11)
            print(output)
            if 'Success rate is 0 percent' in output:
                print('Destination is not reachable')
                output = connection.send_command('traceroute ' + ip11)
                print(output)
            else:
                print('Ping is successful')
        else:
            output = connection.send_command('ping ' + ip22)
            #print(output)
            if 'Success rate is 0 percent' in output:
                print('Destination is not reachable')
                output = connection.send_command('traceroute ' + ip11)
                print(output)
            else:
                print('Ping is successful')
        connection.disconnect()

if radioSel.value == 'precheck':
    precheck()
elif radioSel.value == 'check':
    check()
else:
    postcheck()


