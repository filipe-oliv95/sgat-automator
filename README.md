# 🧾 SGAT Form Autofill

Automação para preenchimento de formulários no sistema **SGAT (Markway)** utilizando **Python** e **Selenium**.  
O script realiza login automático, preenche campos configuráveis do formulário de atendimento e executa esse processo para um **intervalo de datas**, excluindo feriados, folgas ou dias específicos definidos.

---

## 📌 Funcionalidades

- Login automático no sistema SGAT
- Preenchimento de formulário com dados configuráveis
- Execução para um intervalo de datas (com exclusões)
- Navegação e submissão automática
- Facilidade de configuração via `.env`

---

## ⚙️ Requisitos

- Python 3.8+
- Google Chrome instalado
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatível com sua versão do Chrome

---

## 🧪 Ambiente Virtual (recomendado)

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

---

## 📦 Instalação das Dependências

> O arquivo `requirements.txt` já está incluso no repositório.

```bash
pip install -r requirements.txt
```

---

## 🧰 Instalando o ChromeDriver

1. Acesse: [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)
2. Baixe a versão que corresponde ao seu Google Chrome.
3. Extraia o `chromedriver.exe` em uma pasta no seu computador (ex: `C:\chromedriver-win64\chromedriver.exe`).
4. Use esse caminho na variável `CAMINHO_CHROMEDRIVER` no `.env`.

---

## 🔧 Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Caminho para o chromedriver.exe
CAMINHO_CHROMEDRIVER=C:\chromedriver-win64\chromedriver.exe

# Credenciais do sistema
USUARIO=seu_usuario
SENHA=sua_senha

# URLs do sistema SGAT (NÃO ALTERAR)
URL_FORMULARIO=https://sgat.markway.com.br/sgatWay/faces/atendimento/create.xhtml

# Intervalo de datas (formato dd/mm/aaaa)
DATA_INICIAL=01/07/2025
DATA_FINAL=31/07/2025

# Datas a serem ignoradas (folgas, finais de semana, férias, etc)
DATAS_EXCLUIDAS=03/07/2025,04/07/2025

# Dados do formulário
CLIENTE=MARKWAY
ETAPA_COMERCIAL=Não se aplica
CATEGORIA_ATIVIDADE=Trabalho Markway
LOCAL_EXECUCAO=Home Office
HORA_INICIO=10:00
HORA_FIM=18:00
DESCRICAO=Descrição da atividade
```

---

## 🚀 Executando o Script

Com o ambiente ativado e o `.env` configurado corretamente, execute:

```bash
python main.py
```

---

## 📋 Exemplo de Execução

O script irá:

1. Acessar o formulário diretamente
2. Realizar login se necessário
3. Preencher todos os campos com base nas configurações
4. Repetir o processo para cada data válida
5. Ignorar automaticamente as datas listadas como excluídas
6. Finalizar o navegador após a última submissão

---

## 💡 Dicas

- Sempre teste com um pequeno intervalo de datas antes de usar em produção
- Ajuste o tempo dos `sleep()` ou substitua por `WebDriverWait` se a página for lenta
- Verifique se o Chrome está atualizado para evitar erros de compatibilidade com o ChromeDriver

---

## 🛠 Tecnologias Utilizadas

- Python
- Selenium WebDriver
- python-dotenv

---

Desenvolvido para automatizar tarefas repetitivas no SGAT e economizar tempo com segurança e confiabilidade.