import os
import requests
from bs4 import BeautifulSoup
import subprocess
import random
import logging
import json
from requests.exceptions import ProxyError, ConnectTimeout, SSLError

# Configurazione del logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_proxies(file_path):
    logging.debug(f'Caricamento dei proxy dal file: {file_path}')
    with open(file_path, 'r') as file:
        proxies = json.load(file)
    logging.debug(f'Proxy caricati: {proxies}')
    return proxies

def get_random_proxy(proxies):
    logging.debug('Selezione di un proxy casuale dagli HTTP proxy disponibili')
    http_proxies = [proxy for proxy in proxies if proxy.startswith('http://')]
    if not http_proxies:
        logging.error('Nessun proxy HTTP disponibile.')
        return None
    proxy = random.choice(http_proxies)
    logging.debug(f'Proxy selezionato: {proxy}')
    return proxy

def get_phone_image_url(announcement_url, proxies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    max_retries = 2
    for attempt in range(max_retries):
        proxy = get_random_proxy(proxies)
        if not proxy:
            return None
        proxy_dict = {
            'http': proxy,
            'https': proxy,
        }
        try:
            # Effettua la richiesta HTTP per ottenere il contenuto della pagina
            logging.debug(f'Invio richiesta a {announcement_url} con headers: {headers} e proxies: {proxy_dict}')
            response = requests.get(announcement_url, headers=headers, proxies=proxy_dict, timeout=10, verify=False)
            logging.debug(f'Risposta HTTP ricevuta: {response.status_code}')
            response.raise_for_status()  # Verifica che la richiesta sia andata a buon fine

            # Stampa il contenuto HTML per il debug
            logging.debug('Contenuto HTML ricevuto:')
            logging.debug(response.text)

            # Parsing del contenuto HTML con BeautifulSoup
            logging.debug('Parsing del contenuto HTML')
            soup = BeautifulSoup(response.text, 'html.parser')

            # Trova l'elemento <img> all'interno dell'elemento <p> con classe "in-privatePhone"
            phone_img_tag = soup.select_one('.in-privatePhone img')

            if phone_img_tag:
                # Estrai l'URL dell'immagine
                phone_img_url = phone_img_tag.get('src')
                logging.debug(f'URL dell\'immagine trovato: {phone_img_url}')
                return phone_img_url
            else:
                logging.warning('Non è stato possibile trovare l\'immagine del telefono.')
                return None

        except (ProxyError, ConnectTimeout, SSLError) as e:
            logging.error(f'Errore durante il tentativo {attempt + 1}: {e}')
            if attempt < max_retries - 1:
                logging.debug('Riprovo con un altro proxy...')
            else:
                logging.error('Raggiunto il numero massimo di tentativi. Uscita.')
                return None

def download_image(url, save_path):
    try:
        logging.debug(f'Download dell\'immagine da {url}')
        response = requests.get(url, timeout=10)
        logging.debug(f'Risposta HTTP ricevuta per il download dell\'immagine: {response.status_code}')
        response.raise_for_status()  # Verifica che la richiesta sia andata a buon fine

        # Salva l'immagine nella cartella specificata
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logging.debug(f'Immagine scaricata e salvata in: {save_path}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Si è verificato un errore durante il download dell\'immagine: {e}')

def perform_ocr(image_path):
    try:
        logging.debug(f'Esecuzione dell\'analisi OCR su {image_path}')
        # Richiama lo script ocr_analysis.py per effettuare l'analisi OCR
        result = subprocess.run(['python', 'ocr_analysis.py', image_path], capture_output=True, text=True)
        logging.debug(f'Risultato OCR: {result.stdout}')
        print(result.stdout)
    except Exception as e:
        logging.error(f'Si è verificato un errore durante l\'esecuzione dell\'analisi OCR: {e}')

if __name__ == "__main__":
    logging.debug('Inizio esecuzione script principale')
    proxies = load_proxies('proxy.json')
    announcement_url = "https://www.immobiliare.it/annunci/95342796/"
    phone_img_url = get_phone_image_url(announcement_url, proxies)
    if phone_img_url:
        logging.info(f'URL dell\'immagine del telefono: {phone_img_url}')

        # Creazione della cartella images se non esiste
        os.makedirs('images', exist_ok=True)

        # Definisci il percorso di salvataggio dell'immagine
        image_path = os.path.join('images', 'phone_number.jpg')

        # Scarica l'immagine
        download_image(phone_img_url, image_path)

        # Esegui l'analisi OCR sull'immagine scaricata
        perform_ocr(image_path)
    else:
        logging.warning('Non è stato possibile estrarre l\'URL dell\'immagine del telefono.')