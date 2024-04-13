 ################################################################################
 # Copyright 2022 INTRIG
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #     http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 ################################################################################

from src.data import *

topo = generator('main')

# Stratum ip:port
# topo.addstratum("10.1.1.223:9559")

# Recirculation port default 68
topo.addrec_port(196)
topo.addrec_port_user(68)

# addswitch(name)
topo.addswitch("sw1")
topo.addswitch("sw2")
topo.addswitch("sw3")
topo.addswitch("sw4")
topo.addp4("p4src/int.p4")

# addhost(name,port,D_P,speed_bps,AU,FEC,vlan)
# include the link configuration
topo.addhost("h1","2/0", 136, 10000000000, "False", "False", 1920, "10.0.1.1") 
topo.addhost("h2","1/0", 128, 10000000000, "False", "False", 1920, "10.0.2.2") 

# addlink(node1, node2, bw, pkt_loss, latency, jitter, percentage)
# bw is considered just for the first defined link
topo.addlink("h1","sw1", 10000000000, 0, 0, 0, 100)
topo.addlink("h2","sw4", 10000000000, 0, 0, 0, 100)
topo.addlink("sw1","sw2", 10000000000, 0, 0, 0, 100)
topo.addlink("sw2","sw3", 10000000000, 0, 0, 0, 100)
topo.addlink("sw3","sw4", 10000000000, 0, 0, 0, 100)

# addvlan_port(port,D_P,speed_bps,AU,FEC)
# Vlan and port not P7 process
# topo.addvlan_port("6/-", 168, 100000000000, "False", "False")
# topo.addvlan_port("8/-", 184, 100000000000, "False", "False")

# addvlan_link(D_P1, D_P2, vlan)
# topo.addvlan_link(168,184, 716)

# add table entry sw1
topo.addtable('sw1','Ingress.Int_source.tb_activate_source')
topo.addaction('Int_source.add_with_activate_source')
topo.addmatch('ingress_port','136')
topo.insert()

topo.addtable('sw1','Ingress.Int_source.tb_int_source')
topo.addaction('Int_source.add_with_configure_source')
topo.addparams('''srcAddr=IPAddress(\"10.0.1.1\"),
                srcAddr_mask=0xFFFFFFFF,
                dstAddr=IPAddress(\"10.0.2.2\"),
                dstAddr_mask=0xFFFFFFFF,
                l4_src=0x11FF,
                l4_src_mask=0x0000,
                l4_dst=0x22FF,
                l4_dst_mask=0x0000,
                max_hop = 4,
                hop_metadata_len = 10,
                ins_cnt = 8,
                ins_mask = 0xFF''')
topo.insert()

topo.addtable('sw1','Ingress.Int_source.tb_int_source')
topo.addaction('Int_source.add_with_configure_source')
topo.addparams('''srcAddr=IPAddress(\"10.0.3.3\"),
                    srcAddr_mask=0xFFFFFFFF,
                    dstAddr=IPAddress(\"10.0.4.4\"),
                    dstAddr_mask=0xFFFFFFFF,
                    l4_src=0x11FF,
                    l4_src_mask=0x0000,
                    l4_dst=0x4268,
                    l4_dst_mask=0x0000,
                    max_hop = 4,
                    hop_metadata_len = 6,
                    ins_cnt = 4,
                    ins_mask = 0xCC''')
topo.insert()

# topo.addtable('sw1','Ingress.Int_source.tb_int_source')
# topo.addaction('Int_source.mod_with_configure_source')
# topo.addparams('''srcAddr=IPAddress(\"10.0.3.3\"),
#                     srcAddr_mask=0xFFFFFFFF,
#                     dstAddr=IPAddress(\"10.0.5.5\"),
#                     dstAddr_mask=0xFFFFFFFF,
#                     l4_src=0x11FF,
#                     l4_src_mask=0x0000,
#                     l4_dst=0x4268,
#                     l4_dst_mask=0x0000,
#                     max_hop = 4,
#                     hop_metadata_len = 6,
#                     ins_cnt = 4,
#                     ins_mask = 0xCC''')
# topo.insert()

topo.addtable('sw1','Egress.Int_transit.tb_int_transit')
topo.addaction('Int_transit.set_default_with_configure_transit')
topo.addparams('switch_id=1, l3_mtu=1500')
topo.insert()

topo.addtable('sw2','Egress.Int_transit.tb_int_transit')
topo.addaction('Int_transit.set_default_with_configure_transit')
topo.addparams('switch_id=2, l3_mtu=1500')
topo.insert()

topo.addtable('sw3','Egress.Int_transit.tb_int_transit')
topo.addaction('Int_transit.set_default_with_configure_transit')
topo.addparams('switch_id=3, l3_mtu=1500')
topo.insert()

topo.addtable('sw4','Ingress.Int_sink_config.tb_int_sink')
topo.addaction('Int_sink_config.add_with_configure_sink')
topo.addparams('ucast_egress_port=132, sink_reporting_port=132')
topo.insert()

topo.addtable('sw4','Egress.Int_sink.Int_report.tb_int_reporting')
topo.addaction('Int_sink.add_with_send_report')
topo.addparams('dp_mac=\'f6:61:c0:6a:00:00\', dp_ip=IPAddress(\'10.0.1.1\'), collector_mac=\'f6:61:c0:6a:14:21\', collector_ip=IPAddress(\'10.0.0.254\'), collector_port=6000')
topo.insert()

topo.addtable('sw4','Egress.Int_transit.tb_int_transit')
topo.addaction('Int_transit.add_with_configure_transit')
topo.addparams('switch_id=4, l3_mtu=1500')
topo.insert()
# add table entry sw2

topo

#Generate files
topo.generate_chassis()
topo.generate_ports()
topo.generate_p4rt()
topo.generate_bfrt()
topo.generate_p4code()
topo.generate_graph()
topo.parse_usercode()
