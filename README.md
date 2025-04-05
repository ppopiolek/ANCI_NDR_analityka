# **[ANCI] SKRYPT Laboratorium: Systemy analizy sieciowej i wykrywania zagrożeń (NIDS/NDR) + Proof-of-Concept**

---

## **1. Cel zajęć**
Zadaniem jest stworzenie prototypowego silnika detekcji systemu analizy sieciowej w konwencji **Proof of Concept (PoC)**, który:
1. Analizuje dane sieciowe na poziomie flow.
2. Wykorzystuje niektóre zasady **Detection as a Code**.
3. Integruje metody detekcji regułowej i uczenia maszynowego.

Nie wszystkie wymagania muszą zostać w pełni zrealizowane (chodzi o konkretne wymagania, które są podane w tabeli pod koniec instrukcji), ale należy:
- **Zmierzyć się z każdym wymaganiem**,
- Zaproponować **alternatywy** w przypadku trudności.

---

## **2. Wprowadzenie: Detection as a Code**

### **Czym jest Detection as a Code?**

Detection as a Code to nowoczesne podejście, w którym procesy detekcji zagrożeń są wyrażane jako logika programistyczna, zamiast statycznych reguł w narzędziach wykrywania. Dzięki temu możliwa jest dynamiczna analiza i integracja zaawansowanych technik, takich jak przetwarzanie pakietów czy uczenie maszynowe.

Kluczowe cechy:
1. **Automatyzacja**: Reguły detekcyjne mogą być łatwo wdrażane, modyfikowane i testowane w czasie rzeczywistym.
2. **Elastyczność**: Możliwość stosowania reguł napisanych w Pythonie do analizy ruchu sieciowego lub logów.
3. **Integracja z innymi technologiami**: Łączenie logiki detekcyjnej z analizą pakietów, enrichmentem danych, czy modelami uczenia maszynowego.
4. **Programowalność**: Zamiast ograniczać się do sztywnego formatu reguł (np. YAML), można dynamicznie implementować bardziej złożone warunki w Pythonie.

---

### **Przykład: Implementacja Detection as a Code przy użyciu NFStream**

W tym przykładzie analiza odbywa się na poziomie flow z użyciem NFStream, a wykrywanie zagrożeń jest realizowane za pomocą funkcji Python.

```python
from nfstream import NFStreamer

# Definicja funkcji detekcyjnej
def detect_large_flow(flow):
    """
    Wykrywa podejrzanie duży ruch sieciowy wysyłany do konkretnego portu.
    """
    if flow.destination_port == 443 and flow.bytes_sent > 1_000_000:
        return True, f"Suspicious large flow to port 443 from {flow.source_ip}"
    return False, None

# Przetwarzanie pliku PCAP
streamer = NFStreamer(source="sample.pcap")

# Analiza flow
for flow in streamer:
    result, message = detect_large_flow(flow)
    if result:
        print(f"ALERT: {message}")
```

**Wyjaśnienie**:
1. **NFStream**:
   - Biblioteka do analizy ruchu sieciowego na poziomie flow.
   - Pozwala odczytywać statystyki, takie jak liczba przesłanych bajtów, port docelowy czy adres źródłowy.

2. **Funkcja detekcyjna**:
   - Analizuje flow, sprawdzając, czy liczba przesłanych bajtów na port HTTPS (443) przekracza 1 MB.
   - W przypadku wykrycia podejrzanego ruchu generuje alert z odpowiednią informacją.

---

### **Przykład: Detection as a Code przy użyciu scapy**

W tym przykładzie analizujemy ruch na poziomie pakietów za pomocą scapy, sprawdzając określone pola pakietów.

```python
from scapy.all import rdpcap

# Definicja funkcji detekcyjnej
def detect_http_get(packet):
    """
    Wykrywa żądania HTTP GET w pakietach.
    """
    if packet.haslayer("TCP") and packet["TCP"].dport == 80:
        if b"GET" in bytes(packet.payload):
            return True, f"HTTP GET detected from {packet['IP'].src} to {packet['IP'].dst}"
    return False, None

# Wczytanie pliku PCAP
packets = rdpcap("sample.pcap")

# Analiza pakietów
for packet in packets:
    result, message = detect_http_get(packet)
    if result:
        print(f"ALERT: {message}")
```

**Wyjaśnienie**:
1. **Scapy**:
   - Narzędzie do manipulacji i analizy pakietów na poziomie L3/L4.
   - Pozwala na odczytywanie i modyfikowanie pól w pakietach.

2. **Funkcja detekcyjna**:
   - Sprawdza, czy pakiet jest żądaniem HTTP GET na porcie 80 (HTTP).
   - Jeśli tak, generuje alert z informacją o adresie źródłowym i docelowym.

---

### **Dlaczego Detection as a Code?**
- **Programowalność**: Logika oparta na Pythonie pozwala na elastyczność i integrację różnych metod detekcji.
- **Skalowalność**: Możliwość analizowania zarówno pojedynczych pakietów, jak i flow.
- **Praktyczność**: W przeciwieństwie do statycznych formatów, jak Sigma, Python umożliwia dynamiczną analizę w czasie rzeczywistym.


---


## **4. Zadanie: Budowa systemu analizy sieciowej**


### Oczekiwane funkcjonalności

| **ID**   | **Kategoria**        | **Opis wymagania**                                                                                      | **Typ**        | **Proponowany sposób udowodnienia/ dodatkowe komentarze**                                                                                             |
|----------|----------------------|---------------------------------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------------------------------------------------|
| **A.1**  | Analiza flow         | Wczytywanie plików PCAP przy użyciu NFStream.                                                            | Must-have      | -                                                   |
| **A.2**  | Analiza flow         | Dla wczytanych przepływów wyświetlanie podsumowania statystyk flow, takich jak podsumowanie ilości przesłanych pakietów pomiędzy danymi hostami. | Must-have      | -                                                |
| **D.1**  | Detection as a Code  | Implementacja przykładowej reguły detekcyjnej w Pythonie             | Must-have      | Napisanie przykładowej reguły i symulacja przy wykorzystaniu scapy.        |
| **ML.1** | Machine Learning     | Klasyfikacja flow na podstawie cech, takich jak czas trwania, liczba pakietów, protokół (np. z użyciem `scikit-learn`). | Must-have      | Raport generowany przez narzędzie zawiera output z modelu, np. w postaci pewności zwróconej przez model lub wizualizacji działania modelu. |
| **ML.2** | Machine Learning     | Redukcja liczby fałszywych pozytywów (FPR) za pomocą oceny jakości modelu i tuningu hiperparametrów.     | Must-have      | Liczenie metryk takich jak FPR, TPR lub wizualizacja macierzy konfuzji dla testowanego przypadku. |
| **E.1**  | Enrichment           | Pobieranie podstawowych informacji o IP/domenach, np. z `geopy` lub innych źródeł Threat Intelligence przy użyciu API. | Nice-to-have      | Enrichment widoczny w raporcie generowanym przez narzędzie.                                               |
| **V.1**  | Wizualizacja         | Mapa geograficzna przedstawiająca lokalizację adresów IP wykrytych jako podejrzane.                     | Nice-to-have   | Wizualizacja lokalizacji IP na mapie, np. przy użyciu bibliotek `folium` lub `plotly`.                     |
