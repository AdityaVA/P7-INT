<<<<<<< HEAD
P7 (P4 Programmable Patch Panel): an instant 100G emulated network testbed in a pizza box
==

## About P7
Options to validate a network topology, including the link metrics, are traditionally based on virtual environments (e.g., Mininet), limiting the experiments with transmission speeds over 10Gbps. By leveraging P4 programmability and new generation hardware, P7 comes as an alternative to define emulation characteristics of the links and represent a network topology with high fidelity and computation power using a single physical P4 switch (e.g., Tofino). It is possible to emulate network topologies using recirculations, port configurations, different match+action tables, and even DAC cables. What is more, we can connect physical servers to inject traffic to the topology.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**This is still a work in progress. Feedback is welcome!**

## Requirements

- git 
- python3
- matplotlib
- networkX
- regex

**Necessary to run compile, run and set P4 code**

 - Stratum. *Please refer to the official building guide (https://github.com/stratum/stratum/blob/main/stratum/hal/bin/barefoot/README.build.md)*
 - P4Studio. *Tested with SDE 9.5+*

## Contributing
PRs are very much appreciated. For bugs/features consider creating an issue before sending a PR.

## Documentation
For further information, please read our wiki (https://github.com/intrig-unicamp/p7/wiki)

## Team
We are members of [INTRIG (Information & Networking Technologies Research & Innovation Group)](http://intrig.dca.fee.unicamp.br) at University of Campinas - Unicamp, SP, Brazil and [RNP (Rede Nacional de Ensino e Pesquisa)](https://www.rnp.br/).  

**P7 project was supported by and in technical collaboration with the Brazilian National Research and Education Network (RNP - Rede Nacional de Ensino e Pesquisa) (https://www.rnp.br/en)**  

Thanks to all [contributors](https://github.com/intrig-unicamp/p7/wiki#team)!

## How to run
First run `sudo python3 main.py` after installing necessary dependencies

Now, compile the code by running

`sudo -E ~/tools/p4_build.sh files/int_mod.p4 P4_VERSION=p4-16 \P4_ARCHITECTURE=tna \P4FLAGS="--verbose 2 --create-graphs -g -Xp4c="--disable-parse-depth-limit"" \P4PPFLAGS="-DTOFINO" \P4JOBS=4  \P4_NAME=int_mod \enable_thrift=yes`

Now run the tofino model, switchd, bfswitchd commands in this order

`./run_tofino_model.sh -p p7_default int_mod -f ~/btp/p7/ports.json`

`./run_switchd.sh -p p7_default int_mod -c ~/btp/p7-int/p4src/multiprogram_custom_bfrt.conf`

`./run_bfshell.sh -b ~/btp/p7-int/files/bfrt.py`

`./run_bfshell.sh -f ~/btp/p7-int/files/ports_config.txt -i`