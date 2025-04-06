# Wczytanie pliku PCAP z włączoną analizą statystyczną
print("Wczytywanie pliku PCAP z włączoną analizą statystyczną...")
stats_streamer = NFStreamer(
    source="normal_traffic.pcap",
    statistical_analysis=True  # Włączenie analizy statystycznej
)

# Konwersja wczytanych przepływów na ramkę danych pandas
stats_traffic = stats_streamer.to_pandas()

# Wyświetlenie informacji o DataFrame
print(f"Wczytano {len(stats_traffic)} przepływów.")

# Porównanie kolumn
stats_columns = set(stats_traffic.columns.tolist())
new_columns = stats_columns - basic_columns
print(f"\nLiczba nowych kolumn po włączeniu analizy statystycznej: {len(new_columns)}")
print("\nNowe kolumny statystyczne:")
print(sorted(list(new_columns)))

# Wyświetlenie 4 interesujących kolumn statystycznych
interesting_stats = ['bidirectional_min_ps', 'bidirectional_max_ps', 'bidirectional_mean_ps', 'bidirectional_stddev_ps']
print("\nWyniki dla 4 ciekawych kolumn statystycznych:")
display(stats_traffic[interesting_stats].head(8))
