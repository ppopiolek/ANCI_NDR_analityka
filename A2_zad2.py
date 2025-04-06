def analyze_application_categories(flows_df, title="Analiza kategorii aplikacji"):
    if flows_df.empty or 'application_category_name' not in flows_df.columns:
        print("Brak danych do analizy kategorii aplikacji.")
        return {}

    # Grupowanie przepływów według kategorii aplikacji
    category_stats = flows_df.groupby('application_category_name').agg({
        'id': 'count',
        'bidirectional_packets': 'sum',
        'bidirectional_bytes': 'sum'
    }).reset_index()

    # Zmiana nazw kolumn dla czytelności
    category_stats.columns = ['category', 'flows', 'packets', 'bytes']

    # Sortowanie według liczby przepływów (malejąco)
    category_stats = category_stats.sort_values('flows', ascending=False)

    # Wyświetlenie wyników
    print(f"\n{'='*50}")
    print(f"{title.upper()}")
    print(f"{'='*50}")

    for _, row in category_stats.iterrows():
        print(f"Kategoria: {row['category']}")
        print(f"   Przepływy: {row['flows']} ({100*row['flows']/flows_df.shape[0]:.1f}%)")
        print(f"   Pakiety: {row['packets']:,} ({100*row['packets']/flows_df['bidirectional_packets'].sum():.1f}%)")
        print(f"   Bajty: {row['bytes']:,} ({100*row['bytes']/flows_df['bidirectional_bytes'].sum():.1f}%)")
        print()

    # Wizualizacja
    plt.figure(figsize=(15, 10))

    # Wykres liczby przepływów według kategorii
    plt.subplot(3, 1, 1)
    sns.barplot(x='flows', y='category', data=category_stats)
    plt.title('Liczba przepływów według kategorii aplikacji')
    plt.xlabel('Liczba przepływów')

    # Wykres liczby pakietów według kategorii
    plt.subplot(3, 1, 2)
    sns.barplot(x='packets', y='category', data=category_stats)
    plt.title('Liczba pakietów według kategorii aplikacji')
    plt.xlabel('Liczba pakietów')

    # Wykres liczby bajtów według kategorii
    plt.subplot(3, 1, 3)
    sns.barplot(x='bytes', y='category', data=category_stats)
    plt.title('Liczba bajtów według kategorii aplikacji')
    plt.xlabel('Liczba bajtów')

    plt.tight_layout()
    plt.suptitle(title, fontsize=16)
    plt.subplots_adjust(top=0.92)
    plt.show()

    return category_stats

# Analiza kategorii aplikacji
normal_categories = analyze_application_categories(normal_traffic, "Analiza kategorii aplikacji - ruch normalny")
malicious_categories = analyze_application_categories(malicious_traffic, "Analiza kategorii aplikacji - ruch złośliwy")
