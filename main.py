import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv

URL_FORMULARIO = "https://sgat.markway.com.br/sgatWay/faces/atendimento/create.xhtml"

def log_message(message):
    """Função para log que funciona tanto no terminal quanto na GUI"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def load_environment_variables():
    """Carrega as variáveis de ambiente do arquivo .env"""
    load_dotenv()
    
    required_vars = [
        'USUARIO', 'SENHA', 'DATA_INICIAL', 'DATA_FINAL',
        'CLIENTE', 'ETAPA_COMERCIAL', 'CATEGORIA_ATIVIDADE', 'LOCAL_EXECUCAO',
        'HORA_INICIO', 'HORA_FIM', 'DESCRICAO'
    ]
    
    config = {}
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value is None or value.strip() == '':
            missing_vars.append(var)
        else:
            config[var] = value.strip()
    
    # DATAS_EXCLUIDAS é opcional
    datas_excluidas = os.getenv('DATAS_EXCLUIDAS', '').strip()
    config['DATAS_EXCLUIDAS'] = datas_excluidas
    
    if missing_vars:
        raise ValueError(f"Variáveis obrigatórias não encontradas no .env: {', '.join(missing_vars)}")
    
    return config

def setup_chrome_driver():
    """Configura o ChromeDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Usar o ChromeDriver local
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')
    
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver não encontrado em: {chromedriver_path}")
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def parse_date(date_str):
    """Converte string de data DD/MM/AAAA para objeto datetime"""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        raise ValueError(f"Formato de data inválido: {date_str}. Use DD/MM/AAAA")

def generate_date_list(data_inicial, data_final, datas_excluidas_str):
    """Gera lista de datas entre data inicial e final, excluindo as datas especificadas"""
    start_date = parse_date(data_inicial)
    end_date = parse_date(data_final)
    
    # Processar datas excluídas
    datas_excluidas = []
    if datas_excluidas_str:
        for data_str in datas_excluidas_str.split(','):
            data_str = data_str.strip()
            if data_str:
                try:
                    datas_excluidas.append(parse_date(data_str))
                except ValueError as e:
                    log_message(f"Aviso: {e}")
    
    # Gerar lista de datas
    date_list = []
    current_date = start_date
    
    while current_date <= end_date:
        if current_date not in datas_excluidas:
            date_list.append(current_date)
        current_date += timedelta(days=1)
    
    return date_list

def login(driver, usuario, senha):
    """Realiza login no sistema"""
    log_message("Realizando login...")
    
    try:
        # Aguardar campos de login aparecerem
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "j_username"))
        )
        password_field = driver.find_element(By.ID, "j_password")
        login_button = driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")
        
        # Preencher credenciais
        username_field.clear()
        username_field.send_keys(usuario)
        
        password_field.clear()
        password_field.send_keys(senha)
        
        # Fazer login
        login_button.click()
        
        # Aguardar redirecionamento
        time.sleep(3)
        
        log_message("Login realizado com sucesso!")
        
    except Exception as e:
        raise Exception(f"Erro durante o login: {str(e)}")

def fill_form(driver, config, data):
    """Preenche o formulário para uma data específica"""
    data_str = data.strftime("%d/%m/%Y")
    log_message(f"Preenchendo formulário para {data_str}...")
    
    try:
        # Aguardar página carregar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "create:atendimentoBeanAtendimentoCliente"))
        )
        
        Select(driver.find_element(By.ID, "create:atendimentoBeanAtendimentoCliente")).select_by_visible_text(config['CLIENTE'])
        time.sleep(0.1)

        Select(driver.find_element(By.ID, "create:atendimentoBeanAtendimentoEtapaComercial")).select_by_visible_text(config['ETAPA_COMERCIAL'])
        time.sleep(0.1)

        Select(driver.find_element(By.ID, "create:atendimentoBeanAtendimentoTipoAtendimento")).select_by_visible_text(config['CATEGORIA_ATIVIDADE'])
        time.sleep(0.1)

        Select(driver.find_element(By.ID, "create:atendimentoBeanLocalExecucaoAtividade")).select_by_visible_text(config['LOCAL_EXECUCAO'])
        time.sleep(0.1)

        campo_data = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoData")
        campo_data.clear()
        campo_data.send_keys(data_str)

        hora_inicio = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoHoraInicio")
        hora_inicio.clear()
        hora_inicio.send_keys(config['HORA_INICIO'])
        time.sleep(0.1)

        hora_fim = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoHoraTermino")
        hora_fim.clear()
        hora_fim.send_keys(config['HORA_FIM'])
        time.sleep(0.1)

        descricao = driver.find_element(By.ID, "create:atendimentoBeanAtendimentoDescricao")
        descricao.clear()
        descricao.send_keys(config['DESCRICAO'])
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Salvar").click()
        log_message(f"Formulário preenchido para a data {data_str}.")
        time.sleep(1)
        
    except Exception as e:
        log_message(f"Erro ao preencher formulário para {data_str}: {str(e)}")

def main():
    """Função principal"""
    try:
        log_message("Iniciando aplicação...")
        
        # Carregar configurações
        config = load_environment_variables()
        log_message("Configurações carregadas do arquivo .env")
        
        # Gerar lista de datas
        date_list = generate_date_list(
            config['DATA_INICIAL'],
            config['DATA_FINAL'],
            config['DATAS_EXCLUIDAS']
        )
        
        log_message(f"Processando {len(date_list)} datas")
        
        # Configurar driver
        driver = setup_chrome_driver()
        log_message("ChromeDriver configurado")
        
        try:
            # Navegar para o formulário
            driver.get(URL_FORMULARIO)
            log_message(f"Navegando para: {URL_FORMULARIO}")
            
            # Fazer login
            login(driver, config['USUARIO'], config['SENHA'])
            
            # Processar cada data
            for i, data in enumerate(date_list, 1):
                log_message(f"Processando {i}/{len(date_list)}")
                
                # Navegar para o formulário (caso tenha sido redirecionado)
                if driver.current_url != URL_FORMULARIO:
                    driver.get(URL_FORMULARIO)
                
                # Preencher formulário
                fill_form(driver, config, data)
                
                # Pequena pausa entre formulários
                time.sleep(1)
            
            log_message("Todos os formulários foram processados com sucesso!")
            
        finally:
            driver.quit()
            log_message("ChromeDriver fechado")
            
    except Exception as e:
        log_message(f"Erro na execução: {str(e)}")
        raise

if __name__ == "__main__":
    main()

