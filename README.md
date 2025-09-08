# Projekt 3: Elections Scraper
Tento Python skript slouží ke stažení a zpracování dat o výsledcích voleb z webové stránky volby.cz. Skript prochází jednotlivé obce a ukládá důležité informace, jako je počet voličů, vydané obálky, platné hlasy a výsledky jednotlivých politických stran, do souboru ve formátu CSV.
## Instalace a spuštění
Než skript spustíte, důrazně doporučujeme vytvořit a aktivovat virtuální prostředí (venv). Tím zajistíte izolaci závislostí vašeho projektu a předejdete možným konfliktům s jinými Python projekty na vašem systému.

### 1. Vytvoření virtuálního prostředí
Otevřete terminál ve složce projektu a spusťte následující příkaz:

python3 -m venv venv


### 2. Aktivace virtuálního prostředí

Pro macOS a Linux:
source venv/bin/activate

Pro Windows (PowerShell):
venv\Scripts\activate


### 3. Instalace knihoven
Po aktivaci virtuálního prostředí nainstalujte potřebné knihovny pomocí souboru **requirements.txt**, který si můžete automaticky vygenerovat.

pip install -r requirements.txt


### 4. Spuštění skriptu

Spusťte skript z příkazové řádky se dvěma argumenty:

URL adresa: Odkaz na stránku s přehledem obcí, ze které chcete získat data.
Název souboru: Název výstupního souboru CSV, kam budou data uložena.

**Příklad:**

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_voleb.csv


### 5. Struktura výstupního souboru CSV

Výstupní soubor bude mít následující hlavičky a každý řádek pak bude obsahovat data pro jednu obec:

Číslo obce
Název obce
Voliči v seznamu
Vydané obálky
Platné hlasy
Název strany 1
Název strany 2
...

### Poznámka
Skript je navržen pro konkrétní strukturu webu volby.cz. V případě změn v HTML struktuře stránek nemusí fungovat správně a bude potřeba ho aktualizovat.

