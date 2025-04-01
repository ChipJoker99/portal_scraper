import os
import requests
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

def download_html(announcement_url, proxies):
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
            logging.debug(f'Invio richiesta a {announcement_url} con headers: {headers} e proxies: {proxy_dict}')
            response = requests.get(announcement_url, headers=headers, proxies=proxy_dict, timeout=10, verify=False)
            logging.debug(f'Risposta HTTP ricevuta: {response.status_code}')
            response.raise_for_status()  # Verifica che la richiesta sia andata a buon fine

            # Salva il contenuto HTML in un file
            html_path = 'announcement.html'
            logging.debug(f'Salvataggio del contenuto HTML in: {html_path}')
            with open(html_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            
            return html_path

        except (ProxyError, ConnectTimeout, SSLError) as e:
            logging.error(f'Errore durante il tentativo {attempt + 1}: {e}')
            if attempt < max_retries - 1:
                logging.debug('Riprovo con un altro proxy...')
            else:
                logging.error('Raggiunto il numero massimo di tentativi. Uscita.')
                return None

if __name__ == "__main__":
    logging.debug('Inizio esecuzione script principale')
    proxies = load_proxies('proxy.json')
    announcement_url = "https://www.immobiliare.it/annunci/95342796/"
    html_path = download_html(announcement_url, proxies)
    if html_path:
        logging.info(f'Contenuto HTML scaricato e salvato in: {html_path}')
    else:
        logging.warning('Non è stato possibile scaricare il contenuto HTML.')