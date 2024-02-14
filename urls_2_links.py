import requests
import sys
from bs4 import BeautifulSoup

# Cria um arquivo HTML com links para as URLs e seus respectivos titúlos

def get_titles(urls_file):
    titles = []
    with open(urls_file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            try:
                response = requests.get(url, verify=True)  # Adiciona verificação de SSL
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string
                titles.append((url, title))
            except Exception as e:
                print(f"Erro ao acessar {url}: {e}")
    return titles

def generate_html_file(titles, output_file):
    with open(output_file, 'w') as file:
        file.write("<html>\n")
        file.write("<body>\n")
        for url, title in titles:
            file.write(f"<a href='{url}' target='_blank'>{title}</a><br>\n")
        file.write("</body>\n")
        file.write("</html>\n")

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
