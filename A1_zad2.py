# Wczytanie wszystkich przepływów z analizą statystyczną
full_streamer = NFStreamer(
    source="normal_traffic.pcap",
    statistical_analysis=True
)
all_flows = full_streamer.to_pandas()
all_flows_count = len(all_flows)
print(f"Całkowita liczba przepływów: {all_flows_count}")

# Wczytanie tylko ruchu HTTP/HTTPS
http_streamer = NFStreamer(
    source="normal_traffic.pcap",
    statistical_analysis=True,
    bpf_filter="tcp port 80 or tcp port 443"  # Filtr BPF dla HTTP/HTTPS
)
http_flows = http_streamer.to_pandas()
http_flows_count = len(http_flows)
print(f"Liczba przepływów HTTP/HTTPS: {http_flows_count}")

# Obliczenie procentu ruchu HTTP/HTTPS
http_percentage = (http_flows_count / all_flows_count) * 100 if all_flows_count > 0 else 0
print(f"Ruch HTTP/HTTPS stanowi {http_percentage:.2f}% całkowitego ruchu sieciowego")