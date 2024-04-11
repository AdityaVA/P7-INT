from scapy.all import *



# Source and destination IP addresses
src_ip = "192.168.0.1"
dst_ip = "192.168.0.7"

# Source and destination MAC addresses
src_mac = "00:00:00:00:00:01"
dst_mac = "00:00:00:00:00:02"

# Custom recirculation header
class RecircHeader(Packet):
    name = "RecircHeader"
    fields_desc = [
        BitField("ts", 0, 32),
        BitField("num", 1, 32),
        BitField("jitter", 0, 32),
        BitField("sw", 0, 16),
        BitField("sw_id", 0, 16),
        ShortEnumField("ether_type", 0x9966, {0x9966: "Recirculation"}),
        IPField("dest_ip", "0.0.0.0"),
        BitField("signal", 0, 1),
        BitField("pad", 0, 31)
    ]

# Create an Ethernet packet with VLAN tag
rec = RecircHeader(
    ts=int(time.time()),  # Initial timestamp
    num=1,  # Recirculation number
    jitter=0,  # Jitter value
    sw=1,  # Switch ID or link ID
    sw_id=0,  # Switch ID
    ether_type=0x0800,  # Original EtherType (IPv4)
    dest_ip=dst_ip,
    signal=0,  # Signal value
    pad=0
)

#get if list
def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

class CalcHeader(Packet):
    name = "CalcHeader"
    fields_desc = [
        ByteField("op", 0),
        IntField("result", 0)
    ]

# eth = Ether(src=src_mac, dst=dst_mac, type=0x8100)
# eth with ip type 
ETHERTYPE_VLAN = 0x8100
ETHERTYPE_IPV4 = 0x0800
eth = Ether(src=src_mac, dst=dst_mac, type=ETHERTYPE_VLAN)
# VLAN ID for P7
p7_vlan = 1920
vlan = Dot1Q(vlan=p7_vlan, type=ETHERTYPE_IPV4)
ip = IP(src=src_ip, dst=dst_ip, ttl = 0) 
arp = ARP(pdst=dst_ip)
payload = "Hello, World!"
calc = CalcHeader(op=2, result=10)  # Operation code and result
pkt = eth / vlan / ip / calc / payload

# pkt = eth / vlan / ip / calc / rec
# Add the custom recirculation header


# Send the packet
# print(get_if( ))
sendp(pkt, iface="veth10")