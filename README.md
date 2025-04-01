# Portal Scraper

## Descrizione

Portal Scraper è uno strumento per l'estrazione di dati da vari portali immobiliari. Questo progetto è organizzato in modo da eseguire lo scraping su più portali, con un'architettura modulare che permette di aggiungere facilmente nuovi portali.

## Struttura delle Cartelle

La struttura delle cartelle del progetto è la seguente:

```plaintext
portal_scraper/
├── portals/
│   ├── immobiliare/
│   │   ├── immobiliare_scraper.py
│   │   └── ocr_analysis.py
│   ├── idealista/
│   │   └── idealista_scraper.py
├── start.py
├── proxy.json
```

- `portals/`: Contiene le cartelle per ciascun portale supportato.
- `immobiliare/`: Contiene gli script specifici per il portale immobiliare.it.
- `idealista/`: Contiene gli script specifici per il portale idealista.it.
- `start.py`: Script principale che gestisce l'esecuzione degli scraper per i vari portali.
- `proxy.json`: File JSON contenente i proxy utilizzati per le richieste HTTP.

## Requisiti

- Python 3.x
- pacchetti: requests, BeautifulSoup4, pytesseract, Pillow

## Installazione

1. Clona il repository:

   ```sh
   git clone git@github.com:ChipJoker99/portal_scraper.git
   cd portal_scraper
   ```

2. Crea un ambiente virtuale e attivalo:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installa le dipendenze richieste:

   ```sh
   pip install -r requirements.txt
   ```

## Configurazione

1. Configura i proxy nel file `proxy.json`. Esempio di contenuto:

   ```json
   [
       "http://63.35.64.177:3128",
       "http://61.158.175.38:9002"
   ]
   ```

## Utilizzo

1. Esegui lo script `start.py` per iniziare lo scraping:

   ```sh
   python3 start.py
   ```

2. Segui le istruzioni a schermo per selezionare i portali da scrapare.

## Esempi di Script

### immobiliare_scraper.py

Script per scaricare il contenuto HTML di una pagina di annuncio su immobiliare.it.

### ocr_analysis.py

Script per eseguire l'OCR (riconoscimento ottico dei caratteri) sulle immagini dei numeri di telefono di immobiliare.it.

## Contributi

Sono benvenuti contributi al progetto. Per favore, apri una pull request o segnala un problema su GitHub.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file LICENSE per ulteriori dettagli.