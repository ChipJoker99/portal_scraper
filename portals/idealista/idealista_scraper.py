from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_phone_number(url):
    # Imposta il driver di Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Esegui il browser in modalità headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Apri la pagina web
        driver.get(url)
        time.sleep(3)  # Attendi che la pagina si carichi completamente
        
        # Trova e clicca sul pulsante "Vedi il telefono"
        see_phone_button = driver.find_element(By.CLASS_NAME, 'see-phones-btn')
        see_phone_button.click()
        time.sleep(3)  # Attendi che il numero di telefono venga visualizzato
        
        # Trova il numero di telefono
        phone_number_element = driver.find_element(By.CLASS_NAME, '_mobilePhone')
        phone_number = phone_number_element.text.strip()
        
        return phone_number
    
    except Exception as e:
        return f"Errore durante l'estrazione del numero di telefono: {e}"
    
    finally:
        # Chiudi il driver di Selenium
        driver.quit()

if __name__ == "__main__":
    url = "https://www.idealista.it/immobile/32298952/"
    phone_number = get_phone_number(url)
    print(f"Numero di telefono: {phone_number}")