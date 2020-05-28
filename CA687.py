#!/usr/bin/python
"""
spanning_tree.py 
Custom opology creation for routing example.
"""
from mininet.topo import Topo
from mininet.node import Node

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmdPrint('iptables --table nat --append POSTROUTING --out-interface r0-eth3 -j MASQUERADE')

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class MyTopo( Topo ):

    def __init__( self ):
    
        "Create custom topo."
    
        #Initialize topology
        Topo.__init__( self )

        defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
        r0 = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )
        
        # Add hosts and switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        s4 = self.addSwitch('s4')

        #s5 = self.addSwitch('s5')
    
        #h1 = self.addHost('h1')
        #h2 = self.addHost('h2')        
        
        h1 = self.addHost( 'h1', ip='10.0.0.2/8',
                           defaultRoute='via 10.0.0.1' )
        
        h2 = self.addHost( 'h2', ip='10.0.0.3/8',
                           defaultRoute='via 10.0.0.1' )        

        h3 = self.addHost('h3', ip='192.168.1.100/24',
                                defaultRoute='via 192.168.1.1' )

        
        #Add links
        self.addLink(s4, r0, intfName2='r0-eth1',
                      params2={ 'ip' : defaultIP } )

        self.addLink( s3, r0, intfName2='r0-eth3',
                      params2={ 'ip' : '10.0.0.1/8' } )

        #self.addLink(s5, s3)
        
        self.addLink(s1, h1)
        self.addLink(s2, h2)

        self.addLink(s1, s2)
        self.addLink(s3, s2)
        self.addLink(s3, s1)
        
        self.addLink(s4, h3)

        
topos = { 'mytopo': ( lambda: MyTopo() ) }


locations = {'c0':(50,50), 'r0':(650,100), 's4':(650,300), 'h3':(650,450), 's1':(100,300), 's2':(450,300), 's3':(275,100),'h1':(100,450),'h2':(450,450)}

