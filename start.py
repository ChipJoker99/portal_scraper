import os
import subprocess

def run_scraper(portal):
    script_path = os.path.join('portals', portal, f'{portal}_scraper.py')
    if os.path.exists(script_path):
        subprocess.run(['python3', script_path])
    else:
        print(f"Scraper script for {portal} not found.")

def main():
    portals = ['immobiliare', 'idealista']
    for portal in portals:
        choice = input(f"Do you want to scrape {portal}? (y/n): ").strip().lower()
        if choice == 'y':
            run_scraper(portal)

if __name__ == "__main__":
    main()