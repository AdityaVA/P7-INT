# -*- coding: utf-8 -*-

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

from src.gen_chassis import *
from src.gen_ports import *
from src.gen_p4rt import *
from src.gen_bfrt import *
from src.gen_p4 import *
from src.gen_topo import *
from src.dijkstra import *
from src.parse_p4 import *

class generator:

	def __init__(self, name):
		self.name = name
		self.p4_code = ''
		self.stratum_ip = ""
		self.name_sw = []
		self.host = []
		self.link = []
		self.tableEnt = []
		self.sw_ids = {}
		self.tableEnt_dijkstra = []
		self.vlan_port = []
		self.vlan_link = []
		self.rec_port = 68
		self.port_user = 128

		#Table
		self.table_name = []
		self.intable = 0
		self.action_name = []
		self.match = []
		self.actionvalue = []
		self.tableinfo = []

	def addstratum(self, ip):
		self.stratum_ip = ip

	def addrec_port(self, port):
		self.rec_port = port

	def addrec_port_user(self, port):
		self.port_user = port

	def addswitch(self, name):
		self.name_sw.append(name)
		self.sw_ids.update({name:(len(self.sw_ids))})
		
	def addp4(self, p4):
		self.p4_code = p4

	def addhost(self, name, port, D_P, speed_bps, AU, FEC, vlan, ip):
		host_data = [name,port, D_P, speed_bps, AU, FEC, vlan, ip]
		self.host.append(host_data)

	def addlink(self, node1, node2, bw, pkt_loss, latency, jitter, percent):
		link_data = [node1, node2, bw, pkt_loss, latency, jitter, percent]
		self.link.append(link_data)

	def addvlan_port(self, port, D_P, speed_bps, AU, FEC):
		vlan_data = [port, D_P, speed_bps, AU, FEC]
		self.vlan_port.append(vlan_data)

	def addvlan_link(self, D_P1, D_P2, vlan):
		link_data = [D_P1, D_P2, vlan]
		self.vlan_link.append(link_data)

	#Table
	def addtable(self, swith, name):
		if self.intable == 1:
			error = "Error in swith " + str(self.table_name[-1][0]) + " table " + str(self.table_name[-1][1])
			print(error)
			print("Please end the table entry with insert()")
			exit()
		else:
			table = [swith, name]
			self.table_name.append(table)
			self.intable = 1

	def addaction(self, name):
		self.action_name.append(name)

	def addmatch(self, name, value):
		match = [name, value]
		self.match.append(match)

	def addactionvalue(self, name, value):
		action = [name, value]
		self.actionvalue.append(action)

	def insert(self):
		self.intable = 0
		self.tableinfo.append([self.table_name,self.action_name,self.match,self.actionvalue])
		self.table_name = []
		self.action_name = []
		self.match = []
		self.actionvalue = []

	def generate_chassis(self):
		if (len(self.host) == 0):
			print("No VLAN for P7 defined")
		else:
			print("HOSTS")
			for i in range(len(self.host)):
				print("%s: \tport: %s (ID: %s) \n\tspeed: %sbps \n\tAU: %s \n\tFEC: %s \n\tP7 VLAN: %s" %(self.host[i][0],self.host[i][1],self.host[i][2],self.host[i][3],self.host[i][4],self.host[i][5],self.host[i][6]))
			print("\nLINKS")
			for i in range(len(self.link)):
				print("%s <--> %s \n\tBW: %sbps \n\tPacket Loss: %s%% \n\tLatency: %sms" %(self.link[i][0],self.link[i][1],self.link[i][2],self.link[i][3],self.link[i][4]))

		if (len(self.link) == 0):
			print("Need to define a correct link value for P7 VALN")
			print("e.g.  topo.addlink(\"h1\",\"h2\", 100000000000, 0, 5) ")
			exit()

		if (len(self.vlan_port) == 0):
			print("No additional VLANs added")
		else:
			print("\nVLANS")
			for i in range(len(self.vlan_port)):
			    print("port: %s (ID: %s) \n\tspeed: %s \n\tAU: %s \n\tFEC: %s" %(self.vlan_port[i][0],self.vlan_port[i][1],self.vlan_port[i][2],self.vlan_port[i][3],self.vlan_port[i][4]))

		print("\nGenrating Chassis Config...")
		generate_cha(self.host, self.link, self.vlan_port)

	def generate_ports(self):
		if (len(self.host) == 0):
			print("No VLAN for P7 defined")
		else:
			print("HOSTS")
			for i in range(len(self.host)):
				print("%s: \tport: %s (ID: %s) \n\tspeed: %sbps \n\tAU: %s \n\tFEC: %s \n\tP7 VLAN: %s" %(self.host[i][0],self.host[i][1],self.host[i][2],self.host[i][3],self.host[i][4],self.host[i][5],self.host[i][6]))
			print("\nLINKS")
			for i in range(len(self.link)):
				print("%s <--> %s \n\tBW: %sbps \n\tPacket Loss: %s%% \n\tLatency: %sms" %(self.link[i][0],self.link[i][1],self.link[i][2],self.link[i][3],self.link[i][4]))

		if (len(self.link) == 0):
			print("Need to define a correct link value for P7 VALN")
			print("e.g.  topo.addlink(\"h1\",\"h2\", 100000000000, 0, 5) ")
			exit()

		if (len(self.vlan_port) == 0):
			print("No additional VLANs added")
		else:
			print("\nVLANS")
			for i in range(len(self.vlan_port)):
			    print("port: %s (ID: %s) \n\tspeed: %s \n\tAU: %s \n\tFEC: %s" %(self.vlan_port[i][0],self.vlan_port[i][1],self.vlan_port[i][2],self.vlan_port[i][3],self.vlan_port[i][4]))

		print("\nGenrating Ports Config...")
		generate_port(self.host, self.link, self.vlan_port)

	def generate_p4rt(self):
		if (len(self.vlan_link) == 0 and len(self.vlan_port) > 0 ):
			print("Need to define a correct link value for aditionl VALNs")
			print("e.g.  topo.addvlan_link(180,0, 716)  ")
			exit()
		elif(len(self.vlan_link) > 0 and len(self.vlan_port) == 0 ):
			print("Need to define a correct port value for aditionl VALNs")
			print("e.g.  topo.addvlan_port(7, 180, 100000000000, \"False\", \"False\")")
			exit()
		else:
		    print("\nVLANS LINKS")
		    for i in range(len(self.vlan_link)):
		        print("Port %s <--> Port %s VLANL %s" %(self.vlan_link[i][0],self.vlan_link[i][1],self.vlan_link[i][2]))

		print("\nGenrating P4 RT file...")


		self.tableEnt, self.tableEnt_dijkstra = generateTableEntries(self.host, self.name_sw, self.link, self.sw_ids)

		generate_rt(self.stratum_ip, self.host, self.vlan_link, self.tableEnt)

	def generate_bfrt(self):
		if (len(self.vlan_link) == 0 and len(self.vlan_port) > 0 ):
			print("Need to define a correct link value for aditionl VALNs")
			print("e.g.  topo.addvlan_link(180,0, 716)  ")
			exit()
		elif(len(self.vlan_link) > 0 and len(self.vlan_port) == 0 ):
			print("Need to define a correct port value for aditionl VALNs")
			print("e.g.  topo.addvlan_port(7, 180, 100000000000, \"False\", \"False\")")
			exit()
		else:
		    print("\nVLANS LINKS")
		    for i in range(len(self.vlan_link)):
		        print("Port %s <--> Port %s VLANL %s" %(self.vlan_link[i][0],self.vlan_link[i][1],self.vlan_link[i][2]))

		print("\nGenrating BFRT file...")

		generate_bf(self.host, self.vlan_link, self.tableEnt, self.tableinfo, self.sw_ids, self.p4_code)

	def generate_p4code(self):
		if len(self.name_sw) > 0:
			print("\nSwitch")
			for i in range(len(self.name_sw)):
				print("\tAdding Switch %s" % self.name_sw[i])

		print("\nGenrating P4 Code...")
		generate_p4(self.rec_port, self.port_user, self.name_sw, self.host, self.link)

	def generate_graph(self):
		print("\nNetwork Topology created files/topo.png\n")
		gen_topo(self.tableEnt_dijkstra)

	def parse_usercode(self):
		print("\nParsing User P4 Code\n")
		editP4(self.p4_code, self.rec_port)

