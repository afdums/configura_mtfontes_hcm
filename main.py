import requests
import csv

def enviar_config(nome_sessao: str, diretorio_wrk: str, diretorio_prd: str):
    url = "http://10.1.6.130/mtfontes-cgi/ManutencaoArquivoConf.cgi"
    
    fields = {
        "Chave": (None, "DIISVTCYyZiKE.K"),
        "Arquivo": (None, "sistemas.conf"),
        "nome_sessao": (None, nome_sessao),
        "fld_ativo_0": (None, "1"),
        "fld_diretoriowrk_0": (None, diretorio_wrk),
        "fld_diretorioprd_0": (None, diretorio_prd),
        "fld_windows_0": (None, "1"),
        "Processa": (None, "Processa"),
    }


    response = requests.post(url, fields)
    
    # Retorna a resposta do servidor
    return response

def processar_csv(caminho_csv: str):
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # ajuste se for vírgula
        for row in reader:
            nome_sessao = row["nome_sessao"]
            diretorio_wrk = row["fld_diretoriowrk_0"]
            diretorio_prd = row["fld_diretorioprd_0"]

            print(f"\n➡️ Enviando: {nome_sessao}, {diretorio_wrk}, {diretorio_prd}")
            resp = enviar_config(nome_sessao, diretorio_wrk, diretorio_prd)

            print(f"Status: {resp.status_code}")
            print(f"Resposta: {resp.text[:500]}...")  # imprime só os primeiros 500 chars


# Exemplo de uso
if __name__ == "__main__":
    processar_csv("sistemas_hcm.csv")