import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Carrega variáveis de ambiente do .env
load_dotenv()

# Configurações
CAMINHO_CHROMEDRIVER = os.getenv("CAMINHO_CHROMEDRIVER")
USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")
URL_FORMULARIO = os.getenv("URL_FORMULARIO")
DATA_INICIAL = os.getenv("DATA_INICIAL")
DATA_FINAL = os.getenv("DATA_FINAL")
DATAS_EXCLUIDAS = os.getenv("DATAS_EXCLUIDAS")

def gerar_datas_validas(data_inicial_str, data_final_str, datas_excluidas_str):
    data_inicial = datetime.strptime(data_inicial_str, "%d/%m/%Y")
    data_final = datetime.strptime(data_final_str, "%d/%m/%Y")
    datas_excluidas = [datetime.strptime(d.strip(), "%d/%m/%Y") for d in datas_excluidas_str.split(",") if d.strip()]
    
    dias = (data_final - data_inicial).days + 1
    todas_datas = [data_inicial + timedelta(days=i) for i in range(dias)]
    
    datas_validas = [d.strftime("%d/%m/%Y") for d in todas_datas if d not in datas_excluidas]
    return datas_validas

DATAS = gerar_datas_validas(DATA_INICIAL, DATA_FINAL, DATAS_EXCLUIDAS)

# Valores de preenchimento
cliente = os.getenv("CLIENTE")
etapa_comercial = os.getenv("ETAPA_COMERCIAL")
categoria_atividade = os.getenv("CATEGORIA_ATIVIDADE")
local_execucao = os.getenv("LOCAL_EXECUCAO")
hora_inicio_valor = os.getenv("HORA_INICIO")
hora_fim_valor = os.getenv("HORA_FIM")
descricao_valor = os.getenv("DESCRICAO")

def iniciar_driver():
    service = Service(executable_path=CAMINHO_CHROMEDRIVER)
    driver = webdriver.Chrome(service=service)
    return driver

def realizar_login(driver):
    try:
        campo_usuario = driver.find_element(By.ID, "j_username")
        campo_senha = driver.find_element(By.ID, "j_password")
        campo_usuario.send_keys(USUARIO)
        campo_senha.send_keys(SENHA)
        botao_login = driver.find_element(By.NAME, "j_idt22")
        botao_login.click()
        print("Login realizado com sucesso.")
        time.sleep(2)
    except NoSuchElementException:
        print("Usuário já está logado ou página de login não foi exibida.")

def acessar_formulario(driver):
    driver.get(URL_FORMULARIO)
    time.sleep(1)

def preencher_formulario(driver, data):
    try:

        Select(driver.find_element(By.ID, "create:atendimentoBeanAtendimentoCliente")).select_by_visible_text(cliente)
        time.sleep(0.1)

        Select(driver.find_element(By.ID, "create:atendimentoBeanAtendimentoEtapaComercial")).select_by_visible_text(etapa_comercial)
        time.sleep(0.1)

        Select(driver.find_element(By.ID, "create:atendimentoBeanAtendimentoTipoAtendimento")).select_by_visible_text(categoria_atividade)
        time.sleep(0.1)

        Select(driver.find_element(By.ID, "create:atendimentoBeanLocalExecucaoAtividade")).select_by_visible_text(local_execucao)
        time.sleep(0.1)

        campo_data = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoData")
        campo_data.clear()
        campo_data.send_keys(data)

        hora_inicio = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoHoraInicio")
        hora_inicio.clear()
        hora_inicio.send_keys(hora_inicio_valor)
        time.sleep(0.1)

        hora_fim = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoHoraTermino")
        hora_fim.clear()
        hora_fim.send_keys(hora_fim_valor)
        time.sleep(0.1)

        descricao = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoDescricao")
        descricao.clear()
        descricao.send_keys(descricao_valor)
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Salvar").click()
        print(f"Formulário preenchido para a data {data}.")
        time.sleep(1)
    except NoSuchElementException as e:
        print(f"Erro ao preencher o formulário na data {data}: {e}")

def main():
    driver = iniciar_driver()
    
    # Acesso inicial para verificar login
    driver.get(URL_FORMULARIO)
    
    realizar_login(driver)

    for data in DATAS:
        acessar_formulario(driver)
        preencher_formulario(driver, data.strip())

    print("Processo finalizado.")
    driver.quit()

if __name__ == "__main__":
    main()
