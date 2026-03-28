A continuación se detalla la configuración realizada en cada router del laboratorio de VPNs

ROUTER
# 2026-03-28 14:20:41 by RouterOS 7.22
# system id = DnRtBzsl49F
#
/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] disable-running-check=no
set [ find default-name=ether5 ] disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no
/ip address
add address=10.0.0.254/24 comment="WAN compartida" interface=ether1 network=10.0.0.0
/ip dhcp-client
add interface=ether1 name=client1
/ip dns
set servers=8.8.8.8

HQ
# 2026-03-28 14:21:25 by RouterOS 7.22
# system id = BXBpZkotiEH
#
/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] disable-running-check=no
set [ find default-name=ether5 ] disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no
/interface wireguard
add comment="VPN sucursales" listen-port=51820 mtu=1420 name=wg0
/ip pool
add name=pool-hq ranges=192.168.1.100-192.168.1.200
/interface wireguard peers
add allowed-address=10.10.0.2/32,192.168.2.0/24 comment=SucA endpoint-address=10.0.0.2 endpoint-port=51820 interface=wg0 \
    name=peer5 persistent-keepalive=25s public-key="3iMvbv9bbWJBPx29Fz/+SEAV71GwlZzpHF4RFMi/XV0="
add allowed-address=10.10.0.3/32,192.168.3.0/24 comment=SucB endpoint-address=10.0.0.3 endpoint-port=51820 interface=wg0 \
    name=peer6 persistent-keepalive=25s public-key="u8OiiZ4XI+zu8HyecR0I/CyrG1eA2qn7owxWAlixJEk="
/ip address
add address=10.10.0.1/24 comment="WG tunnel network" interface=wg0 network=10.10.0.0
add address=10.0.0.1/24 comment=WAN interface=ether1 network=10.0.0.0
add address=192.168.1.1/24 comment=LAN interface=ether2 network=192.168.1.0
/ip dhcp-client
add interface=ether1 name=client1
/ip dhcp-server
add address-pool=pool-hq interface=ether2 name=dhcp-hq
/ip dhcp-server network
add address=192.168.1.0/24 dns-server=8.8.8.8 gateway=192.168.1.1
/ip firewall nat
add action=masquerade chain=srcnat out-interface=ether1
/ip route
add comment="LAN SucA" dst-address=192.168.2.0/24 gateway=10.10.0.2
add comment="LAN SucB" dst-address=192.168.3.0/24 gateway=10.10.0.3
add comment="Default via Internet" dst-address=0.0.0.0/0 gateway=10.0.0.254

SucB
# 2026-03-28 14:22:02 by RouterOS 7.22
# system id = vhtZWMv7hBD
#
/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] disable-running-check=no
set [ find default-name=ether5 ] disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no
/interface wireguard
add comment="VPN hacia HQ" listen-port=51820 mtu=1420 name=wg0
/ip pool
add name=pool-sucb ranges=192.168.3.100-192.168.3.200
/interface wireguard peers
add allowed-address=10.10.0.1/32,192.168.1.0/24,192.168.2.0/24 comment=HQ endpoint-address=10.0.0.1 endpoint-port=51820 \
    interface=wg0 name=peer5 persistent-keepalive=25s public-key="Zy2H6K6FC9MGfXEsgOgpgEbCafDQyAFIpGmb/elPDjE="
add allowed-address=10.10.0.2/32,192.168.2.0/24 comment=SucA endpoint-address=10.0.0.2 endpoint-port=51820 interface=wg0 \
    name=peer6 persistent-keepalive=25s public-key="3iMvbv9bbWJBPx29Fz/+SEAV71GwlZzpHF4RFMi/XV0="
/ip address
add address=192.168.3.1/24 comment=LAN interface=ether2 network=192.168.3.0
add address=10.0.0.3/24 comment=WAN interface=ether1 network=10.0.0.0
add address=10.10.0.3/24 comment="WG tunnel" interface=wg0 network=10.10.0.0
/ip dhcp-client
add interface=ether1 name=client1
/ip dhcp-server
add address-pool=pool-sucb interface=ether2 name=dhcp-sucb
/ip dhcp-server network
add address=192.168.3.0/24 dns-server=8.8.8.8 gateway=192.168.3.1
/ip firewall nat
add action=masquerade chain=srcnat out-interface=ether1
/ip route
add comment="LAN HQ" dst-address=192.168.1.0/24 gateway=10.10.0.1
add comment="LAN SucA" dst-address=192.168.2.0/24 gateway=10.10.0.2
add comment="Default via Internet" dst-address=0.0.0.0/0 gateway=10.0.0.254

SucA
# 2026-03-28 14:22:54 by RouterOS 7.22
# system id = UrMrG8jdYkB
#
/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] disable-running-check=no
set [ find default-name=ether3 ] disable-running-check=no
set [ find default-name=ether4 ] disable-running-check=no
set [ find default-name=ether5 ] disable-running-check=no
set [ find default-name=ether6 ] disable-running-check=no
set [ find default-name=ether7 ] disable-running-check=no
set [ find default-name=ether8 ] disable-running-check=no
/interface wireguard
add comment="VPN hacia HQ" listen-port=51820 mtu=1420 name=wg0
/ip pool
add name=pool-suca ranges=192.168.2.100-192.168.2.200
/interface wireguard peers
add allowed-address=10.10.0.1/32,192.168.1.0/24,192.168.3.0/24 comment=HQ endpoint-address=10.0.0.1 endpoint-port=51820 \
    interface=wg0 name=peer5 persistent-keepalive=25s public-key="Zy2H6K6FC9MGfXEsgOgpgEbCafDQyAFIpGmb/elPDjE="
add allowed-address=10.10.0.3/32,192.168.3.0/24 comment=SucB endpoint-address=10.0.0.3 endpoint-port=51820 interface=wg0 \
    name=peer6 persistent-keepalive=25s public-key="u8OiiZ4XI+zu8HyecR0I/CyrG1eA2qn7owxWAlixJEk="
/ip address
add address=192.168.2.1/24 comment=LAN interface=ether2 network=192.168.2.0
add address=10.10.0.2/24 interface=wg0 network=10.10.0.0
add address=10.0.0.2/24 comment=WAN interface=ether1 network=10.0.0.0
/ip dhcp-client
add interface=ether1 name=client1
/ip dhcp-server
add address-pool=pool-suca interface=ether2 name=dhcp-suca
/ip dhcp-server network
add address=192.168.2.0/24 dns-server=8.8.8.8 gateway=192.168.2.1
/ip firewall nat
add action=masquerade chain=srcnat out-interface=ether1
/ip route
add comment="LAN HQ" dst-address=192.168.1.0/24 gateway=10.10.0.1
add comment="LAN SucB" dst-address=192.168.3.0/24 gateway=10.10.0.3
add comment="Default via Internet" dst-address=0.0.0.0/0 gateway=10.0.0.254
