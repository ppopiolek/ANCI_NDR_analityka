def detect_port_scan(flow):
    """
    Wykrywa potencjalne skanowanie portów na podstawie charakterystyki przepływu.
    Args:
    flow: Wiersz DataFrame reprezentujący pojedynczy przepływ
    Returns:
    bool: True jeśli przepływ przypomina skanowanie portu, False w przeciwnym razie
    str: Powód uznania przepływu za skanowanie (lub None)
    """
    # Domyślnie zakładamy, że to nie jest skanowanie portów
    is_port_scan = False
    reason = None
    
    # Sprawdzanie liczby pakietów (1-3 pakiety)
    if flow['bidirectional_packets'] <= 3:
        # Sprawdzanie czasu trwania przepływu (poniżej 500 ms)
        if flow['bidirectional_duration_ms'] < 500:
            # Sprawdzanie ilości przesłanych danych (poniżej 300 bajtów)
            if flow['bidirectional_bytes'] < 300:
                is_port_scan = True
                reason = f"Podejrzane skanowanie portu: {flow['bidirectional_packets']} pakietów, "\
                        f"{flow['bidirectional_duration_ms']} ms trwania, "\
                        f"{flow['bidirectional_bytes']} bajtów transferu"
    
    return is_port_scan, reason

# Po zaimplementowaniu reguły, zastosuj ją do danych:
port_scan_results = detect_port_scan(malicious_traffic)

port_scan_results