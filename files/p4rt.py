import p4runtime_sh.shell as sh
import argparse

sh.setup(
        device_id=1,
        grpc_addr='',  #Update with the Stratum IP
        election_id=(0, 1), # (high, low)
        config=sh.FwdPipeConfig('/workspace/output_dir/p4info.txt', '/workspace/output_dir/pipeline_config.pb.bin')
        )

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '136'
te.action['link']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '128'
te.action['link']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '132'
te.action['link']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '136'
te.action['link']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '128'
te.action['link']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '132'
te.action['link']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '5'
te.match['dest_ip'] = '10.0.2.2'
te.action['sw_id']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '5'
te.match['dest_ip'] = '10.0.1.1'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '10.0.2.2'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '10.0.1.1'
te.action['sw_id']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '3'
te.match['dest_ip'] = '10.0.2.2'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '3'
te.match['dest_ip'] = '10.0.1.1'
te.action['sw_id']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '1'
te.match['dest_ip'] = '10.0.2.2'
te.action['port']  = '128'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '1'
te.match['dest_ip'] = '10.0.1.1'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '0'
te.match['dest_ip'] = '10.0.1.1'
te.action['port']  = '136'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '0'
te.match['dest_ip'] = '10.0.2.2'
te.action['sw_id']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '5'
te.match['dest_ip'] = '10.0.0.254'
te.action['sw_id']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '10.0.0.254'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '3'
te.match['dest_ip'] = '10.0.0.254'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '2'
te.match['dest_ip'] = '10.0.0.254'
te.action['port']  = '132'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '2'
te.match['dest_ip'] = '10.0.1.1'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '0'
te.match['dest_ip'] = '10.0.0.254'
te.action['sw_id']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '2'
te.match['dest_ip'] = '10.0.2.2'
te.action['sw_id']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '1'
te.match['dest_ip'] = '10.0.0.254'
te.action['sw_id']  = '2'
te.insert()

sh.teardown()
