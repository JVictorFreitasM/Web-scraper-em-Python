import requests
import time
import csv

BASE_URL = "https://themosvagas.com.br/wp-json/wp/v2/posts"

# Cabeçalhos HTTP para evitar bloqueios
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

# Parâmetros da API
params = {
    "categories": 96,       # Categoria de Estágios
    "search": "TI",         # Busca vagas que contenham 'TI'
    "orderby": "date",      # Ordena por data
    "order": "desc",        # Mais recentes primeiro
    "per_page": 100,        # Máximo permitido por página
    "page": 1               # Página inicial
}

vagas = []

while True:
    print(f"📄 Buscando página {params['page']}...")
    resp = requests.get(BASE_URL, params=params, headers=HEADERS)

    if resp.status_code == 403:
        print("🚫 Erro 403: O servidor bloqueou a requisição. Tente novamente mais tarde.")
        break
    elif resp.status_code != 200:
        print(f"⚠️ Erro {resp.status_code} ao buscar página {params['page']}")
        break

    data = resp.json()

    if not data:
        print("✅ Nenhuma vaga nova encontrada. Encerrando.")
        break

    for post in data:
        vagas.append({
            "titulo": post["title"]["rendered"],
            "link": post["link"],
            "data": post["date"]
        })

    print(f"✅ {len(data)} vagas coletadas nesta página.")
    params["page"] += 1
    time.sleep(1)

# Grava no CSV
csv_filename = "vagas_ti_estagios.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["titulo", "link", "data"])
    writer.writeheader()
    writer.writerows(vagas)

print(f"\n💾 Arquivo salvo: {csv_filename}")
print(f"🔎 Total de vagas coletadas: {len(vagas)}")

# Mostra as primeiras vagas
for vaga in vagas[:5]:
    print(f"\nTítulo: {vaga['titulo']}")
    print(f"Link: {vaga['link']}")
    print(f"Data: {vaga['data']}")
