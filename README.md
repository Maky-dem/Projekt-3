# Projekt-3  Czech Election Scraper

Tento Python skript slouží ke stažení a zpracování dat o výsledcích voleb z webové stránky [volby.cz](https://www.volby.cz/pls/ps2017nss/). Skript prochází jednotlivé obce a ukládá data, jako je počet voličů, vydané obálky, platné hlasy a výsledky jednotlivých politických stran, do souboru ve formátu CSV.

## Instalace a spuštění

Než skript spustíte, **důrazně se doporučuje vytvořit a aktivovat virtuální prostředí (`venv`)**, abyste předešli konfliktům s jinými Python projekty.

### 1. Vytvoření virtuálního prostředí

Otevřete terminál ve složce projektu a spusťte následující příkaz:

```sh
python3 -m venv venv

2. Aktivace virtuálního prostředí
Pro macOS a Linux:

Bash

source venv/bin/activate
Pro Windows:

Bash

venv\Scripts\activate
3. Instalace závislostí
Po aktivaci virtuálního prostředí nainstalujte potřebné knihovny pomocí souboru requirements.txt:

Bash

pip install -r requirements.txt
4. Spuštění skriptu
Spusťte skript z příkazové řádky se dvěma argumenty:

URL adresa: Odkaz na stránku s přehledem obcí, ze které chcete získat data.

Název souboru: Název výstupního souboru CSV, kam budou data uložena.

Příklad:

Bash

python jmeno_tveho_skriptu.py [https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xKres=1](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xKres=1) ./vysledky_voleb.csv
Funkce skriptu
Skript je rozdělen do několika funkcí pro lepší přehlednost a modularitu:

arguments(): Zpracovává a ověřuje argumenty zadané při spuštění.

get_links(url): Získává všechny odkazy z hlavní webové stránky.

clean_links(links): Filtruje odkazy na jednotlivé obce.

create_full_urls(clean_links): Vytváří kompletní URL adresy pro scraping.

get_soup_from_url(url): Stahuje obsah stránky a vrací objekt BeautifulSoup.

extract_data_from_tables(soup): Hledá v tabulkách výsledky politických stran.

extract_table_headers(soup): Extrahuj názvy obcí.

extract_number_village(soup): Extrahuj čísla obcí.

volici_v_seznamu(soup): Získává počet voličů v seznamu.

vydane_obalky(soup): Získává počet vydaných obálek.

platne_hlasy(soup): Získává počet platných hlasů.

main(): Hlavní funkce, která řídí celý proces.

Struktura výstupního souboru CSV
Výstupní soubor bude mít následující hlavičky:

Číslo obce	Název obce	Voliči v seznamu	Vydané obálky	Platné hlasy	Název strany 1	Název strany 2	...

Exportovat do Tabulek
Každý řádek pak bude obsahovat data pro jednu obec.

Poznámka
Skript je navržen pro konkrétní strukturu webu volby.cz. V případě změn v HTML struktuře stránek nemusí fungovat správně a bude potřeba ho aktualizovat.
