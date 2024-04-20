#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

global flow_count
global ip
global port

flow_count = 0
ip='192.168.147.62' # Ip address of floodlight server
port=6653 # Remote controller port listining on floodlight

#Function to save repeated code when attempting to do test pings.
# Example usage:
# check_ping(h99, [h2,h3,h4], timeout=2)
def check_ping(source, destinations, timeout,net):
    for destination in destinations:
        print(f"\nChecking if {source} can ping {destination}")
        if net.ping([source, destination], timeout=timeout) == 0:
            print(f"Success: {source} can ping {destination}. \n")
        else:
            print(f"\n\t\t----> Failure: {source} cannot ping {destination}. \n")
            net.stop()
            net.exit()



#Function to save repeated code when attempting to do test pings.
# Example usage:
# check_ping_should_fail(h99, [h2,h3,h4], timeout=2)
def check_ping_should_fail(source, destinations, timeout, net):

    for destination in destinations:
        print(f"\nChecking if {source} can ping {destination} (should fail)...")
        if net.ping([source, destination], timeout=timeout) > 0:
            print(f"Success: {source} cannot ping {destination} as expected. \n")
        else:
            print(f"\t\t----> Failure: {source} should not be able to ping {destination}. \n")
            net.stop()
            net.exit()


#Main Smoke test. Ensure everything is up and running
def smokeTestTest(net):
    print("\n")
    print("=====================================================")
    print("\nRunning smoke test to ensure all hosts can ping each other...\n")
    print("=====================================================")

    # Retrieve hosts by name using net.get . Leaving this here so that we can change for test purposes later
    h1 = net.get('h1')
    h99 = net.get('h99')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    h7 = net.get('h7')
    h8 = net.get('h8')
    h9 = net.get('h9')
    h10 = net.get('h10')
    h11 = net.get('h11')
    h12 = net.get('h12')
    h13 = net.get('h13')


    # Conducting all pings to test initial connectivity
    if net.pingAll(timeout=2) == 0:
        print("Success: All hosts can ping each other.\n")
    else:
        print("----> Failure: Some hosts cannot ping each other, check network setup.")

    print("\nTesting connectivity from h99 to all hosts ...\n")
    check_ping(h99, [h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13], 2, net)

    print("\nTesting connectivity from h1 to all hosts ...\n")
    check_ping(h1, [h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13], 2, net)



    print("\n")
    print("=====================================================\n")
    print("\n\nSmoke test complete.\n\n")
    print("=====================================================\n")


#Tests to make sure that mobile test cases are correctly routed
# (e.g test cases from h99 go to correct hosts)
def enableMobileOnlyTest(net):
    print("\n\n")
    print("=====================================================\n")
    print("\n\n Left hand side - Testing that mobile devices can only ping mobile devices...\n\n")
    print("=====================================================\n")

    h1 = net.get('h1')
    h99 = net.get('h99')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    h7 = net.get('h7')
    h8 = net.get('h8')
    h9 = net.get('h9')
    h10 = net.get('h10')
    h11 = net.get('h11')
    h12 = net.get('h12')
    h13 = net.get('h13')

    info('Setting rules so that traffic goes to s2 when nw_src=10.0.0.99 (not s4)\n')
    # Command for switch s1
    net['s1'].cmd('ovs-ofctl add-flow s1 priority=100,ip,nw_src=10.0.0.99,actions=output:3')

    info('Setting rules so that traffic is redirected to S7 when nw_src=10.0.0.99 (not s3) (does not run on h2,h3,h4')
    # Command for switch s2
    net['s2'].cmd('ovs-ofctl add-flow s2 priority=100,ip,nw_src=10.0.0.99,actions=output:2')

    info('Flow configured : h99->s1->s2->s7->[h5,h6,h7]')
    check_ping(h99, [h5,h6,h7], 2, net)
    check_ping_should_fail(h99, [h2,h3,h4,h8,h9,h10], 2, net)

    print("\nChecking that h99 cannot ping right hand side mobile devices due to s2 rule - h11,h12,h13 (should fail) ...\n")
    check_ping_should_fail(h99, [h11,h12,h13], 2, net)


    print("\n")
    print("=====================================================\n")
    print("Left hand side - Mobile host specific testing complete.")
    print("=====================================================\n")
    print("\n")


#Tests to make sure that desktop test cases are correctly routed
# (e.g test cases from h1 go to correct hosts)
def enableDesktopOnlyTest(net):
    # setup and test that desktop test cases are run only by desktop computers
    print("\n")
    print("===================================================== \n")
    print("Left hand side - Testing that desktop devices can only ping desktop devices...")
    print("===================================================== \n")

    # Command for switch s1
    info('Setting rules so that traffic does from s1 to s2 when nw_src=10.0.0.1 (not s4')
    net['s1'].cmd('ovs-ofctl add-flow s1 priority=200,ip,nw_src=10.0.0.1,actions=output:3')

    # Command for switch s2
    info('Setting rules so that s2 goes to s3 - traffic does not go to s7 (does not run on h5,h6,h7')
    net['s2'].cmd('ovs-ofctl add-flow s2 priority=200,ip,nw_src=10.0.0.1,actions=output:3')

    info('Flow configured : h1->s1->s2->s3->[h2,h3,h4]')
    # Hosts setup
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    h7 = net.get('h7')

    check_ping(h1, [h2,h3,h4], 2, net)
    check_ping_should_fail(h1, [h5,h6,h7], 2, net)


    print("\n")
    print("=====================================================\n")
    print("Left hand side Desktop host specific testing complete.")
    print("=====================================================\n")


#Function to add round robin rule so that both sides of the topo are being used
# based on the flow rules changes
def add_round_robin_rule(net):
    global flow_count

    print("=====================================================\n")
    print("Test Load Balancer - Round Robin Rule\n")
    print("=====================================================\n")

    h99 = net.get('h99')
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    h7 = net.get('h7')

    h8 = net.get('h8')
    h9 = net.get('h9')
    h10 = net.get('h10')
    h11 = net.get('h11')
    h12 = net.get('h12')
    h13 = net.get('h13')

    src_ip = '10.0.0.99'  # Mobile IP origin
    src_ip_desktop = '10.0.0.1'  # Desktop ip origin

    output_port = 3 if flow_count % 2 == 0 else 4  # Alternating between output port 3 (s2) and 4 (s4) for mobile
    output_port_desktop = 3 if flow_count % 2 == 0 else 4  # Alternating between output port 3 (s2) and 4 (s4) for mobile

    flow_count += 1  #Swap between s2 & s4 every 2nd run

    info(f'Adding flow rule for {src_ip} to output on port {output_port} \n')
    info(f'Adding flow rule for {src_ip_desktop} to output on port {output_port} \n \n')

    info("\nflow count: ", flow_count)

    # If we are running a batch of test cases and 2 remainder "flow count" is 1
    # use other (left) side of the topo
    if (flow_count % 2 == 1):
        #Switch between s2 & s4 from s1 for mobile
        net['s1'].cmd(f'ovs-ofctl add-flow s1 priority=100,ip,nw_src={src_ip},actions=output:{output_port}')

        #Switch between s2 & s4 from s1 for desktop
        net['s1'].cmd(f'ovs-ofctl add-flow s1 priority=300,ip,nw_src={src_ip_desktop},actions=output:{output_port_desktop}')

        info('\nMobile flow configured by s1 to be  : h99->s1->s2->[with previous rules s7] -> [h5,h6,h7] \n')
        info('Desktop Flow configured by s1 to be  : h1->s1->s2-[with previous rules s3] -> [h2,h3,h4] \n')

        net.pingAll(timeout=2)
        # Check that mobile test cases routed correctly
        check_ping(h99, [h5,h6,h7], 2,net)
        check_ping_should_fail(h99, [h11,h12,h13], 2, net)

        # Check that desktop test cases routed correctly
        check_ping(h1, [h2,h3,h4], 2,net)
        check_ping_should_fail(h1, [h8,h9,h10], 2, net)

    # If we are running a batch of test cases for teh second time ,
    # use other (right) side of the topo
    if (flow_count % 2 == 0):
        net['s1'].cmd('ovs-ofctl add-flow s1 priority=900,ip,nw_src=10.0.0.99,actions=output:4')
        net['s4'].cmd('ovs-ofctl add-flow s4 priority=900,ip,nw_src=10.0.0.99,actions=output:3')

        info('\nMobile Flow configured by s1 to be  : h99->s1->s4-[with previous rules s6] -> [h11,h12,h13] \n')

        net['s1'].cmd('ovs-ofctl add-flow s1 priority=900,ip,nw_src=10.0.0.1,actions=output:4')
        net['s4'].cmd('ovs-ofctl add-flow s4 priority=900,ip,nw_src=10.0.0.1,actions=output:2')
        info('Desktop Flow configured by s1 to be  : h1->s1->s4-[with previous rules s5] -> [h8,h9,h10] \n')

        net.pingAll(timeout=2)

        check_ping(h99, [h11,h12,h13], 2,net)
        check_ping_should_fail(h99, [h8,h9,h10], 2, net)

        check_ping(h1, [h8,h9,h10], 2,net)
        check_ping_should_fail(h1, [h11,h12,h13], 2, net)

def create_topology():
    info('*** Adding controller\n')
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSSwitch, waitConnected=True)
    net.addController('c0', ip=ip, port=port)

    # Top level host (h99 test cases are mobile based , h1 test are desktop based
    h99 = net.addHost('h99', ip='10.0.0.99')
    h1 = net.addHost('h1', ip='10.0.0.1')

    # Create hosts
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    h5 = net.addHost('h5', ip='10.0.0.5')
    h6 = net.addHost('h6', ip='10.0.0.6')
    h7 = net.addHost('h7', ip='10.0.0.7')

    # desktop host devices
    h8 = net.addHost('h8', ip='10.0.0.8')
    h9 = net.addHost('h9', ip='10.0.0.9')
    h10 = net.addHost('h10', ip='10.0.0.10')

    # right hand side mobile devices
    h11 = net.addHost('h11', ip='10.0.0.11')
    h12 = net.addHost('h12', ip='10.0.0.12')
    h13 = net.addHost('h13', ip='10.0.0.13')

    # Create center switches
    s1 = net.addSwitch('s1')

    # Create switches for left hand side
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s7 = net.addSwitch('s7')

    # Create switches for right hand side
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')


    # Add links
    net.addLink(h99, s1, port1=1, port2=1)  # h99 connects to s1 on port 1 (h99) and port 1 (s1)
    net.addLink(h1, s1, port1=2, port2=2)  # h1 connects to s1 on port 2 (h1) and port 2 (s1)

    net.addLink(s1, s2, port1=3, port2=1)  # s1 connects to s2 on port 3 (s1) and port 1 (s2)
    net.addLink(s1, s4, port1=4, port2=1)  # s1 connects to s4 on port 4 (s1) and port 1 (s4)

    net.addLink(s2, s7, port1=2, port2=1)  # s2 connects to s7 on port 2 (s2) and port 1 (s7)
    net.addLink(s2, s3, port1=3, port2=1, )  # s2 connects to s3 on port 3 (s2) and port 1 (s3)

    net.addLink(s3, h2, port1=2, port2=1, bw=100)  # s3 connects to h2 on port 2 (s3) and port 1 (h2)
    net.addLink(s3, h3, port1=3, port2=1, bw=50)  # s3 connects to h3 on port 3 (s3) and port 1 (h3)
    net.addLink(s3, h4, port1=4, port2=1, bw=10)  # s3 connects to h4 on port 4 (s3) and port 1 (h4)

    net.addLink(s4, s5, port1=2, port2=7)
    net.addLink(s4, s6, port1=3, port2=6)

    net.addLink(s5, h8, port1=3, port2=1, bw=100)
    net.addLink(s5, h9, port1=4, port2=1, bw=50)
    net.addLink(s5, h10, port1=6, port2=1, bw=10)
    net.addLink(s5, s6, port1=5, port2=1)  # Change to use port 5 on s5 for link to s6

    # Connect hosts h11, h12, and h13 to switch s6
    net.addLink(s6, h11, port1=2, port2=1, bw=5)
    net.addLink(s6, h12, port1=3, port2=1, bw=1)
    net.addLink(s6, h13, port1=4, port2=1, bw=10)

    net.addLink(s7, h5, port1=2, port2=1, bw=10)  # s7 connects to h5 on port 2 (s7) and port 1 (h5)
    net.addLink(s7, h6, port1=3, port2=1, bw=5)  # s7 connects to h6 on port 3 (s7) and port 1 (h6)
    net.addLink(s7, h7, port1=4, port2=1, bw=1)  # s7 connects to h7 on port 4 (s7) and port 1 (h7)


    net.start()

    # Run tests
    smokeTestTest(net)  # Smoke Test 1 - ensure all is good
    enableMobileOnlyTest(net)  # Test 2 - ensure mobile devices can only ping mobile devices
    enableDesktopOnlyTest(net)  # Test 3 - ensure desktop devices can only ping desktop devices
    add_round_robin_rule(net) # Test 4 - ensure that lbs corretcly use left hand side of topo
    add_round_robin_rule(net)# Test 5 - if another test batch is started , use the right hand topo

    CLI(net) # Start the CLI
    net.stop() # When required to exit


if __name__ == '__main__':
    setLogLevel('info')
    create_topology() # Build the topology
