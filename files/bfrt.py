from netaddr import IPAddress
p4p7 = bfrt.p7_default.pipe_p7
p4user = bfrt.int_mod.pipe

def clear_all(verbose=True, batching=True):
    global p4p7
    global p4user
    global bfrt

    for table_types in (['MATCH_DIRECT', 'MATCH_INDIRECT_SELECTOR'],
                        ['SELECTOR'],
                        ['ACTION_PROFILE']):
        for table in p4p7.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')
        for table in p4user.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')

clear_all(verbose=True)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=136,   link=0)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=128,   link=1)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=136,   link=0)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=128,   link=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, dest_ip=IPAddress('10.0.2.2'),   link_id=1, sw_id=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, dest_ip=IPAddress('10.0.1.1'),   link_id=3, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, dest_ip=IPAddress('10.0.2.2'),   link_id=4, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, dest_ip=IPAddress('10.0.1.1'),   link_id=2, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('10.0.2.2'),   link_id=3, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('10.0.1.1'),   link_id=0, sw_id=0)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=1, dest_ip=IPAddress('10.0.2.2'),   port=128)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('10.0.1.1'),   link_id=4, sw_id=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=0, dest_ip=IPAddress('10.0.1.1'),   port=136)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, dest_ip=IPAddress('10.0.2.2'),   link_id=2, sw_id=0)

Int_source = p4user.Ingress.Int_source.tb_activate_source
Int_source.add_with_activate_source(sw_id= 0, ingress_port = 136)
Int_source = p4user.Ingress.Int_source.tb_int_source
Int_source.add_with_configure_source(srcAddr=IPAddress("10.0.1.1"),
                srcAddr_mask=0xFFFFFFFF,
                dstAddr=IPAddress("10.0.2.2"),
                dstAddr_mask=0xFFFFFFFF,
                l4_src=0x11FF,
                l4_src_mask=0x0000,
                l4_dst=0x22FF,
                l4_dst_mask=0x0000,
                max_hop = 4,
                hop_metadata_len = 10,
                ins_cnt = 8,
                ins_mask = 0xFF, sw_id= 0)
Int_source = p4user.Ingress.Int_source.tb_int_source
Int_source.add_with_configure_source(srcAddr=IPAddress("10.0.3.3"),
                    srcAddr_mask=0xFFFFFFFF,
                    dstAddr=IPAddress("10.0.4.4"),
                    dstAddr_mask=0xFFFFFFFF,
                    l4_src=0x11FF,
                    l4_src_mask=0x0000,
                    l4_dst=0x4268,
                    l4_dst_mask=0x0000,
                    max_hop = 4,
                    hop_metadata_len = 6,
                    ins_cnt = 4,
                    ins_mask = 0xCC, sw_id= 0)
Int_transit = p4user.Egress.Int_transit.tb_int_transit
Int_transit.set_default_with_configure_transit(switch_id=1, l3_mtu=1500, sw_id= 0)
Int_transit = p4user.Egress.Int_transit.tb_int_transit
Int_transit.set_default_with_configure_transit(switch_id=2, l3_mtu=1500, sw_id= 1)
Int_transit = p4user.Egress.Int_transit.tb_int_transit
Int_transit.set_default_with_configure_transit(switch_id=3, l3_mtu=1500, sw_id= 2)
Int_sink_config = p4user.Ingress.Int_sink_config.tb_int_sink
Int_sink_config.add_with_configure_sink(ucast_egress_port=132, sink_reporting_port=132, sw_id= 3)
Int_sink = p4user.Egress.Int_sink.Int_report.tb_int_reporting
Int_sink.add_with_send_report(dp_mac='f6:61:c0:6a:00:00', dp_ip=IPAddress('10.0.1.1'), collector_mac='f6:61:c0:6a:14:21', collector_ip=IPAddress('10.0.0.254'), collector_port=6000, sw_id= 3)
Int_transit = p4user.Egress.Int_transit.tb_int_transit
Int_transit.add_with_configure_transit(switch_id=4, l3_mtu=1500, sw_id= 3)

bfrt.complete_operations()

print("""
******************* PROGAMMING RESULTS *****************
""")
print ("Table vlan_fwd:")
vlan_fwd.dump(table=True)
print ("Table arp_fwd:")
arp_fwd.dump(table=True)
print ("Table basic_fwd:")
basic_fwd.dump(table=True)
print ("Table Int_source:")
Int_source.dump(table=True)
print ("Table Int_sink:")
Int_sink.dump(table=True)
print ("Table Int_transit:")
Int_transit.dump(table=True)
print ("Table Int_sink_config:")
Int_sink_config.dump(table=True)
