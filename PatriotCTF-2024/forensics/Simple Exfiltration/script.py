from scapy.all import rdpcap, ICMP, IP

pcap_file = "exfiltration_activity_pctf_challenge.pcapng"
packets = rdpcap(pcap_file)

arr = []
for packet in packets:
    if IP in packet and ICMP in packet and packet[ICMP].type == 8:
        arr.append(packet[IP].ttl)

print(arr)
flag : str = "".join(chr(val) for val in arr)
print(flag)
