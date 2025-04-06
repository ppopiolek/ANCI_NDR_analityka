# Twój kod dla zadania 1
# Przykład:
malicious_stats = generate_flow_summary(malicious_traffic, "Podsumowanie statystyk złośliwego ruchu")
malicious_comm = analyze_host_communication(malicious_traffic)
visualize_flow_statistics(malicious_traffic, "Wizualizacja statystyk złośliwego ruchu")

# Porównanie kluczowych parametrów
comparison_metrics = [
    'total_flows', 'unique_src_ips', 'unique_dst_ips', 
    'avg_packets_per_flow', 'avg_bytes_per_flow', 'avg_duration_ms'
]
 
print("\n=== PORÓWNANIE NORMALNEGO I ZŁOŚLIWEGO RUCHU ===")
for metric in comparison_metrics:
    normal_value = normal_stats.get(metric, 0)
    malicious_value = malicious_stats.get(metric, 0)
    print(f"{metric}: Normal={normal_value:.2f}, Malicious={malicious_value:.2f}, Ratio={malicious_value/normal_value if normal_value else 0:.2f}")