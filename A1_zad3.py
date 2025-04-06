# Wczytanie normalnego ruchu z analizą statystyczną (jeśli nie zostało to już zrobione)
if 'stats_traffic' not in locals():
    normal_stats_streamer = NFStreamer(
        source="normal_traffic.pcap",
        statistical_analysis=True
    )
    stats_traffic = normal_stats_streamer.to_pandas()

# Wczytanie złośliwego ruchu z analizą statystyczną
malicious_streamer = NFStreamer(
    source="malicious_traffic.pcap",
    statistical_analysis=True
)
malicious_traffic = malicious_streamer.to_pandas()

# Porównanie podstawowych statystyk
print("=== Porównanie ruchu normalnego i złośliwego ===")
print(f"Normalny ruch - liczba przepływów: {len(stats_traffic)}")
print(f"Złośliwy ruch - liczba przepływów: {len(malicious_traffic)}")

# Średnia liczba pakietów
normal_avg_packets = stats_traffic['bidirectional_packets'].mean()
malicious_avg_packets = malicious_traffic['bidirectional_packets'].mean()
print(f"Normalny ruch - średnia liczba pakietów na przepływ: {normal_avg_packets:.2f}")
print(f"Złośliwy ruch - średnia liczba pakietów na przepływ: {malicious_avg_packets:.2f}")

# Średni rozmiar pakietów
normal_avg_ps = stats_traffic['bidirectional_mean_ps'].mean()
malicious_avg_ps = malicious_traffic['bidirectional_mean_ps'].mean()
print(f"Normalny ruch - średni rozmiar pakietu: {normal_avg_ps:.2f} B")
print(f"Złośliwy ruch - średni rozmiar pakietu: {malicious_avg_ps:.2f} B")
