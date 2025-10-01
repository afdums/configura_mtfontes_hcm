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


def novo_fonte(chave: str, wNomeFonte: str, wSufixo: str, wSistema: str):

    URL = "http://10.1.6.130/mtfontes-cgi/NovoFonte.cgi"

    fields = {
        "Chave": (None, chave),
        "wNomeFonte": (None, wNomeFonte),
        "wSufixo": (None, wSufixo),
        "wSistema": (None, wSistema),
        "wDesc1Fonte": (None, wNomeFonte),
        "wDesc2Fonte": (None, ""),   # vazio
        "Atualiza": (None, "Processa"),
    }

    resp = requests.post(URL, files=fields, timeout=30)
    print("Status:", resp.status_code)
    print("Resposta:", resp.text[:500], "...\n")  # preview da resposta


def libera_fonte(chave: str, nome_fonte: str, wSistema: str, wDescricao: str):

    URL = "http://10.1.6.130/mtfontes-cgi/LiberaFonte.cgi"

    # Campos fixos
    fields = {
        "Chave": (None, chave),
        "wRevisao": (None, ""),
        "TrocaSistema": (None, ""),
        "wSistema": (None, wSistema),
        "wNomeFonte": (None, nome_fonte),
        "wDescricao": (None, wDescricao),
        "Atualiza": (None, "Processa"),
    }
    

    resp = requests.post(URL, files=fields, timeout=30)
    print("Status:", resp.status_code)
    print("Resposta:", resp.text[:50000], "...\n")  # preview da resposta 


def processar_csv_sistemas(caminho_csv: str, chave: str):
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # ajuste se for vírgula
        for row in reader:
            nome_sessao = row["nome_sessao"]
            diretorio_wrk = row["fld_diretoriowrk_0"]
            diretorio_prd = row["fld_diretorioprd_0"]

            print(f"\n➡️ Enviando: {nome_sessao}, {diretorio_wrk}, {diretorio_prd}")
            resp = enviar_config(chave, nome_sessao, diretorio_wrk, diretorio_prd)

            print(f"Status: {resp.status_code}")
            print(f"Resposta: {resp.text[:500]}...")  # imprime só os primeiros 500 chars

def processar_csv_fontes(caminho_csv: str, chave: str):
    """
    Lê o CSV e envia cada linha para o servidor.
    CSV esperado: wNomeFonte;wSufixo;wSistema
    """
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            wNomeFonte = row["wNomeFonte"]
            wSufixo = row["wSufixo"]
            wSistema = row["wSistema"]

            try:
                novo_fonte(chave, wNomeFonte, wSufixo, wSistema)
            except Exception as e:
                print(f"Erro ao enviar {wNomeFonte}: {e}")            


def processar_csv_libera(caminho_csv: str, chave: str):
    """
    Lê o CSV e envia cada linha para o servidor.
    CSV esperado: wNomeFonte;wSufixo;wSistema
    """
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            wNomeFonte = row["wNomeFonte"]
            wSufixo = row["wSufixo"]
            wSistema = row["wSistema"]

            try:
                libera_fonte(chave, wNomeFonte, wSistema, "Carga Inicial")
            except Exception as e:
                print(f"Erro ao enviar {wNomeFonte}: {e}") 

# Exemplo de uso
if __name__ == "__main__":
    chave="1ANculYqKN.7c.K"
    #processar_csv_sistemas("sistemas_hcm.csv", chave)
    processar_csv_fontes("fontes_hcm.csv", chave)
    processar_csv_libera("fontes_hcm.csv", chave)