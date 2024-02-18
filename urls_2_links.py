import requests
import sys
from bs4 import BeautifulSoup

# Script que lê URLs de um arquivo de texto e gera um arquivo HTML com seus respectivos links
# Os links são nomeados com o título da página, facilitando a leitura e visualização para listas grandes de URLs

# User-Agent da uma versão recente do Google Chrome. Alguns sites bloqueiam requisições feitas por scripts, como da biblioteca "requests"
headers_values = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

def get_titles(urls_file):
    titles_ok = [] # Páginas que retornam status HTTP 200 OK
    titles_error = [] # Páginas que retornam status HTTP diferente de 200 OK, provavelmente com problemas
    print(f"Lendo URLs do arquivo: {urls_file}\n")
    with open(urls_file, 'r', encoding='UTF-8', errors='ignore') as file:
        urls = file.readlines()
        urls = [line for line in urls if line.strip()] # Ignora linhas em branco
        urls = [line for line in urls if line.startswith('http')] # Ignora linhas que não iniciam em http:// ou https://
        print(f"URLs lidas: {len(urls)}\n")
        for index, url in enumerate(urls):
            url = url.strip()
            print(f"{index + 1}/{len(urls)} - Acessando: {url}")          
            try:
                response = requests.get(url, verify=True, headers=headers_values)  # Adiciona verificação de SSL e User-Agent
                status_code = response.status_code
                print(f"Status HTTP: {status_code}") 
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string
                print(f"Titúlo: {title}\n")
                if status_code == 200:
                    titles_ok.append((url, title))
                else:
                    titles_error.append((url, title))
            except Exception as e:
                print(f"Erro ao acessar {url}: {e}\n")
    return titles_ok, titles_error

def generate_html_file(titles, output_file):
    print(f"Gerando arquivo HTML em: {output_file}")
    titles_ok_list, titles_error_list = titles 
    with open(output_file, 'w', encoding='UTF-8', errors='ignore') as file:
        file.write("<html>\n")
        file.write("<body>\n")
        
        file.write("<h1>Links Funcionais - Status HTTP 200 OK</h1>\n")
        file.write("<ol>\n")
        for url, title in titles_ok_list:
            file.write(f"<li><a href='{url}' target='_blank'>{title}</a></li>\n")
        file.write("</ol>\n")
        
        file.write("<h1>Links Não Funcionais - Status HTTP diferente de 200 OK</h1>\n")
        file.write("<ol>\n")
        for url, title in titles_error_list:
            file.write(f"<li><a href='{url}' target='_blank'>{title}</a></li>\n")
        file.write("</ol>\n")
        
        file.write("</body>\n")
        file.write("</html>\n")
    print("Arquivo HTML gerado com sucesso!\n")

def main():
    if len(sys.argv) != 3:
        print("Uso: python urls_2_links.py arquivo_de_urls.txt arquivo_de_saida.html")
        sys.exit(1)

    urls_file = sys.argv[1]  # Nome do arquivo contendo as URLs
    output_file = sys.argv[2]  # Nome do arquivo HTML de saída

    titles = get_titles(urls_file)
    generate_html_file(titles, output_file)

if __name__ == "__main__":
    main()
