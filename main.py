
"""
main.py: třetí projekt do Engeto Online Python Akademie

autor: Markéta Fejtek
email: demura.m@seznam.cz
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def arguments():
    """Tato funkce slouží ke zpracování a ověření dvou parametrů zadaných při spuštění scriptu."""
    if len(sys.argv) > 2:
        argument1 = sys.argv[1]
        argument2 = sys.argv[2]
        if (argument1.startswith("http://") or argument1.startswith("https://")) and argument2.endswith(".csv"):
            print(f"Stahuji data z vybraného odkazu {argument1}")
            return argument1, argument2
        else:
            print(f"Nebyly zadané spravné argumenty (očekávám URL začínající http:// nebo https:// a název souboru končící .csv). Ukončuji program.")
            sys.exit(1)
    else:
        print(f"Nebyly zadané spravné argumenty (očekávám URL a název souboru .csv). Ukončuji program.")
        sys.exit(1)

def get_links(url):
    """Tato funkce získává všechny odkazy na webové stránce."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    urls = [link.get('href') for link in links if link.get('href')]
    return urls

def clean_links(links):
    """Vrací odkazy, které mají v sobě 'obec=', tyhle odkazy použijeme níže na scrapování."""
    unique_links = list(dict.fromkeys(links))
    check_links = "obec="
    links = [link for link in unique_links if check_links in link]
    return links

def create_full_urls(clean_links):
    """Tato funkce vytváří odkazy, které použijeme ke scrapování níže."""
    main_link = 'https://www.volby.cz/pls/ps2017nss/'
    check_link = "vyber="
    full_urls = [main_link + link for link in clean_links if check_link in link]
    return full_urls

def get_soup_from_url(url):
    """Navrací soup z plnohodnotných a vyčištěných odkazu."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        return None

def extract_data_from_tables(soup):
    """Hledá název politické strany a výsledky voleb v tabulkách."""
    results = {}
    tables = soup.find_all("table")
    for table in tables:
        for tr in table.find_all("tr"):
            td_elements = tr.find_all("td")
            if len(td_elements) >= 3:
                key = td_elements[1].text.strip()
                value = td_elements[2].text.strip().replace('\xa0', '')
                results[key] = value
    return results

def extract_table_headers(soup):
    """Extrahuj názvy obcí z hlavní stránky tabulek."""
    hlavicky = []
    tabulky = soup.find_all("table")
    for tabulka in tabulky:
        hlavicky.extend(tabulka.find_all("td", {"class": "overflow_name"}))
    hlavicky_text = [h.text for h in hlavicky]
    return hlavicky_text

def extract_number_village(soup):
    """Extrahuj čísla obcí z hlavní stránky."""
    cisla_obci_tabulka = soup.find_all('td', class_='cislo')
    if cisla_obci_tabulka:
        cisla_obci = [cislo.text for cislo in cisla_obci_tabulka]
        return cisla_obci
    else:
        return None

def registered_voters(soup):
    """Funkce hledá počet voličů v seznamu."""
    volici = soup.find_all("td", {"headers": "sa2"})
    if volici:
        volici_text = [volic.text.replace('\xa0', '') for volic in volici]
        return volici_text
    else:
        return None

def issued_envelopes(soup):
    """Funkce hledá počet vydaných obálek."""
    vydane_obalky = soup.find_all("td", {"headers": "sa3"})
    if vydane_obalky:
        vydane_obalky_text = [vydane.text.replace('\xa0', '') for vydane in vydane_obalky]
        return vydane_obalky_text
    else:
        return None

def valid_votes(soup):
    """Funkce hledá počet platných hlasů."""
    platne_hlasy = soup.find_all("td", {"headers": "sa6"})
    if platne_hlasy:
        platne_hlasy_text = [hlasy.text.replace('\xa0', '') for hlasy in platne_hlasy]
        return platne_hlasy_text
    else:
        return None

def main():
    """Hlavní funkce, která řídí celý proces."""
    url, filename = arguments()
    
    # 1. Získání odkazů na obce
    soup_main = get_soup_from_url(url)
    if not soup_main:
        sys.exit(1)
        
    all_links = get_links(url)
    cleaned_links = clean_links(all_links)
    full_urls = create_full_urls(cleaned_links)
    
    if not full_urls:
        sys.exit(1)

    # 2. Získání hlaviček pro strany (z prvního odkazu)
    first_village_soup = get_soup_from_url(full_urls[0])
    if not first_village_soup:
        sys.exit(1)
    
    party_results = extract_data_from_tables(first_village_soup)
    if party_results:
        all_keys = list(party_results.keys())
        
        # Odstraníme první položku
        first_key = all_keys[0]
        del party_results[first_key]
        
        # Odstraníme poslední položku
        last_key = all_keys[-1]
        del party_results[last_key]
           
    party_names = list(party_results.keys())

    # 3. Vytvoření kompletní hlavičky
    header = ["Číslo obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    header.extend(party_names)

    # 4. Sběr dat pro všechny obce a zápis do CSV
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        cisla_obci = extract_number_village(soup_main)
        nazvy_obci = extract_table_headers(soup_main)
        
        if not cisla_obci or not nazvy_obci:
            sys.exit(1)
        
        for i, full_url in enumerate(full_urls):
            soup_village = get_soup_from_url(full_url)
            if not soup_village:
                continue

            # Extrahujeme data
            volici = registered_voters(soup_village)
            obalky = issued_envelopes(soup_village)
            platne = valid_votes(soup_village)
            vysledky_stran = extract_data_from_tables(soup_village)
            
            # Přidání kontrol pro zabránění TypeError
            volici_text = volici[0] if volici and volici[0] else '0'
            obalky_text = obalky[0] if obalky and obalky[0] else '0'
            platne_text = platne[0] if platne and platne[0] else '0'
            
            # Sestavíme řádek
            row = [cisla_obci[i], nazvy_obci[i], volici_text, obalky_text, platne_text]
            
            # Přidáme hlasy pro politické strany
            for party in party_names:
                row.append(vysledky_stran.get(party, '0'))
                
            writer.writerow(row)

    print(f"Data byla úspěšně uložena do souboru '{filename}'.")
    print(f"Ukončuji program scrapování.")


if __name__ == '__main__':
    main()