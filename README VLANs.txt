— Limpiar configuracion previa MikroTik

/ip firewall filter remove [find]
/ip address remove [find]
/interface vlan remove [find]

//////////////////////////////////////////////////////////////////////

— Crear interfaces VLAN

# Switch Piso 1 (ether1)
/interface vlan add name=vlan10-sw1 vlan-id=10 interface=ether1
/interface vlan add name=vlan20-sw1 vlan-id=20 interface=ether1
/interface vlan add name=vlan30-sw1 vlan-id=30 interface=ether1
# Switch Piso 2 (ether2)
/interface vlan add name=vlan10-sw2 vlan-id=10 interface=ether2
/interface vlan add name=vlan20-sw2 vlan-id=20 interface=ether2
/interface vlan add name=vlan30-sw2 vlan-id=30 interface=ether2
# Switch Piso 3 (ether3)
/interface vlan add name=vlan10-sw3 vlan-id=10 interface=ether3
/interface vlan add name=vlan20-sw3 vlan-id=20 interface=ether3
/interface vlan add name=vlan30-sw3 vlan-id=30 interface=ether3

Verificar con: /interface vlan print

//////////////////////////////////////////////////////////////////////

— Crear bridges por VLAN

/interface bridge add name=bridge10
/interface bridge add name=bridge20
/interface bridge add name=bridge30

//////////////////////////////////////////////////////////////////////

— Agregar VLANs a los bridges
# Bridge VLAN 10 — Empleados
/interface bridge port add bridge=bridge10 interface=vlan10-sw1
/interface bridge port add bridge=bridge10 interface=vlan10-sw2
/interface bridge port add bridge=bridge10 interface=vlan10-sw3
# Bridge VLAN 20 — Invitados
/interface bridge port add bridge=bridge20 interface=vlan20-sw1
/interface bridge port add bridge=bridge20 interface=vlan20-sw2
/interface bridge port add bridge=bridge20 interface=vlan20-sw3
# Bridge VLAN 30 — IoT
/interface bridge port add bridge=bridge30 interface=vlan30-sw1
/interface bridge port add bridge=bridge30 interface=vlan30-sw2
/interface bridge port add bridge=bridge30 interface=vlan30-sw3

//////////////////////////////////////////////////////////////////////

— Asignar IPs gateway a cada VLAN
/ip address add address=10.0.10.1/24 interface=bridge10
/ip address add address=10.0.20.1/24 interface=bridge20
/ip address add address=10.0.30.1/24 interface=bridge30

Verificar con: /ip address print

//////////////////////////////////////////////////////////////////////

— Reglas de aislamiento y acceso
# Regla 1: IoT puede llegar a Home Assistant 
/ip firewall filter add chain=forward \
  src-address=10.0.30.0/24 dst-address=10.0.10.10 \
  action=accept comment="IoT-hacia-HomeAssistant"
# Regla 2: Home Assistant puede responder a IoT
/ip firewall filter add chain=forward \
  src-address=10.0.10.10 dst-address=10.0.30.0/24 \
  action=accept comment="HomeAssistant-reply-IoT"
# Reglas 3-6: Aislar VLANs entre si
/ip firewall filter add chain=forward src-address=10.0.10.0/24 dst-address=10.0.20.0
/24 action=drop
/ip firewall filter add chain=forward src-address=10.0.10.0/24 dst-address=10.0.30.0
/24 action=drop
/ip firewall filter add chain=forward src-address=10.0.20.0/24 dst-address=10.0.10.0
/24 action=drop
/ip firewall filter add chain=forward src-address=10.0.20.0/24 dst-address=10.0.30.0
/24 action=drop
# Regla 7: IoT sin acceso a internet ni a otras redes
/ip firewall filter add chain=forward \
  src-address=10.0.30.0/24 dst-address=0.0.0.0/0 \
  action=drop comment="IoT-sin-internet"
# Regla 8: Invitados sin acceso a red interna
/ip firewall filter add chain=forward \
  src-address=10.0.20.0/24 dst-address=10.0.0.0/8 \
  action=drop comment="Invitados-sin-red-interna"
Verificar con: /ip firewall filter print

//////////////////////////////////////////////////////////////////////

— Configurar las VPCS
Switch Piso 1
# Empleado-P1 (tambien simula Home Assistant)
PC1> ip 10.0.10.10/24 10.0.10.1
# Invitado-P1
PC2> ip 10.0.20.10/24 10.0.20.1
# IoT-P1
PC3> ip 10.0.30.10/24 10.0.30.1
Switch Piso 2
PC4> ip 10.0.10.11/24 10.0.10.1
PC5> ip 10.0.20.11/24 10.0.20.1
PC6> ip 10.0.30.11/24 10.0.30.1
Switch Piso 3
PC7> ip 10.0.10.12/24 10.0.10.1
PC8> ip 10.0.20.12/24 10.0.20.1
PC9> ip 10.0.30.12/24 10.0.30.1

//////////////////////////////////////////////////////////////////////

— Verificacion del funcionamiento
Pruebas desde Empleado-P1 (PC1 — 10.0.10.10)
# Ping al gateway — debe responder
PC1> ping 10.0.10.1
# Ping a Empleado de otro piso — debe responder (misma VLAN)
PC1> ping 10.0.10.11
# Ping a Invitado — debe dar timeout (VLANs aisladas)
PC1> ping 10.0.20.10
Pruebas desde IoT-P1 (PC3 — 10.0.30.10)
# Ping a Home Assistant — debe responder
PC3> ping 10.0.10.10
# Ping a otro Empleado — debe dar timeout (solo Home Assistant permitido)
PC3> ping 10.0.10.11
# Ping a Invitado — debe dar timeout
PC3> ping 10.0.20.10

//////////////////////////////////////////////////////////////////////

Resultados esperados
Desde	Hacia	IP Destino	Resultado esperado
Empleado-P1	Gateway VLAN10	10.0.10.1	Responde
Empleado-P1	Empleado-P2	10.0.10.11	Responde
Empleado-P1	Invitado-P1	10.0.20.10	Timeout
Empleado-P1	IoT-P1	10.0.30.10	Timeout
IoT-P1	Home Assistant	10.0.10.10	Responde
IoT-P1	Empleado-P2	10.0.10.11	Timeout
IoT-P1	Invitado-P1	10.0.20.10	Timeout
Invitado-P1	Empleado-P1	10.0.10.10	Timeout
Invitado-P1	Gateway VLAN20	10.0.20.1	Responde

