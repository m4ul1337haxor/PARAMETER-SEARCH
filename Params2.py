import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse, urljoin


G = '\033[92m' # Green
Y = '\033[93m' # Yellow
R = '\033[91m' # Red
W = '\033[0m'  # White

def get_params(url):
    print(f"{Y}[!] Scanning Target: {url}{W}")
    params_found = set()
    
    try:
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if '?' in full_url:
                params_found.add(full_url)
                
       
        for form in soup.find_all('form'):
            action = form.get('action')
            inputs = form.find_all(['input', 'select', 'textarea'])
            if action:
                form_url = urljoin(url, action)
                param_str = "&".join([f"{i.get('name')}=test" for i in inputs if i.get('name')])
                if param_str:
                    params_found.add(f"{form_url}?{param_str}")

        if params_found:
            print(f"{G}[+] Found {len(params_found)} Potential Vulnerable Points:{W}")
            for p in params_found:
                print(f"{R}[TARGET] -> {p}{W}")
                # Simpan otomatis ke file buat lu pake di sqlmap
                with open('vuln_list.txt', 'a') as f:
                    f.write(p + '\n')
        else:
            print(f"{R}[-] No parameters found. Try deeper page.{W}")

    except Exception as e:
        print(f"{R}[ERROR] Connection failed: {e}{W}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Y}Usage: python crawl.py http://target.com{W}")
        sys.exit()
    
    target = sys.argv[1]
    get_params(target)
              
