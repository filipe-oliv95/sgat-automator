import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from datetime import datetime, timedelta
import threading
import subprocess
import sys

class FormularioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Preenchimento Automático do SGAT")
        self.root.geometry("800x700")
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de configuração
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configurações")
        
        # Aba de execução
        self.exec_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.exec_frame, text="Execução")
        
        self.create_config_widgets()
        self.create_exec_widgets()
        
        # Variáveis para armazenar os valores
        self.variables = {}
        
    def create_config_widgets(self):
        # Frame principal com scroll
        canvas = tk.Canvas(self.config_frame)
        scrollbar = ttk.Scrollbar(self.config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_label = ttk.Label(scrollable_frame, text="Configurações do Formulário", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Frame para os campos
        fields_frame = ttk.Frame(scrollable_frame)
        fields_frame.pack(fill='x', padx=20, pady=10)
        
        # Definir os campos e suas descrições
        self.field_definitions = [
            ("USUARIO", "Usuário", "Nome de usuário para login"),
            ("SENHA", "Senha", "Senha para login"),
            ("DATA_INICIAL", "Data Inicial", "Data inicial no formato DD/MM/AAAA"),
            ("DATA_FINAL", "Data Final", "Data final no formato DD/MM/AAAA"),
            ("DATAS_EXCLUIDAS", "Datas Excluídas", "Datas a excluir separadas por vírgula (DD/MM/AAAA)"),
            ("CLIENTE", "Cliente", "Nome do cliente"),
            ("ETAPA_COMERCIAL", "Etapa Comercial", "Etapa comercial do projeto"),
            ("CATEGORIA_ATIVIDADE", "Categoria da Atividade", "Categoria da atividade"),
            ("LOCAL_EXECUCAO", "Local de Execução", "Local onde a atividade será executada"),
            ("HORA_INICIO", "Hora de Início", "Hora de início no formato HH:MM"),
            ("HORA_FIM", "Hora de Fim", "Hora de fim no formato HH:MM"),
            ("DESCRICAO", "Descrição", "Descrição da atividade")
        ]
        
        self.entries = {}
        
        for i, (var_name, label_text, description) in enumerate(self.field_definitions):
            # Frame para cada campo
            field_frame = ttk.Frame(fields_frame)
            field_frame.pack(fill='x', pady=5)
            
            # Label
            label = ttk.Label(field_frame, text=label_text + ":", width=20, anchor='w')
            label.pack(side='left', padx=(0, 10))
            
            # Entry
            if var_name == "DESCRICAO":
                # Text widget para descrição longa
                text_widget = tk.Text(field_frame, height=3, width=50)
                text_widget.pack(side='left', fill='x', expand=True)
                self.entries[var_name] = text_widget
            elif var_name == "SENHA":
                # Entry com show='*' para senha
                entry = ttk.Entry(field_frame, show='*', width=50)
                entry.pack(side='left', fill='x', expand=True)
                self.entries[var_name] = entry
            else:
                # Entry normal
                entry = ttk.Entry(field_frame, width=50)
                entry.pack(side='left', fill='x', expand=True)
                self.entries[var_name] = entry
            
            # Label de descrição
            desc_label = ttk.Label(field_frame, text=description, 
                                 font=('Arial', 8), foreground='gray')
            desc_label.pack(side='right', padx=(10, 0))
        
        # Botões
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=20)
        
        save_button = ttk.Button(button_frame, text="Salvar Configurações", 
                               command=self.save_config)
        save_button.pack(side='left', padx=5)
        
        load_button = ttk.Button(button_frame, text="Carregar Configurações", 
                               command=self.load_config)
        load_button.pack(side='left', padx=5)
        
        # Configurar o canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_exec_widgets(self):
        # Título
        title_label = ttk.Label(self.exec_frame, text="Execução do Script", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Frame para botões
        button_frame = ttk.Frame(self.exec_frame)
        button_frame.pack(pady=10)
        
        self.run_button = ttk.Button(button_frame, text="Executar Script", 
                                   command=self.run_script, style='Accent.TButton')
        self.run_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Parar Execução", 
                                    command=self.stop_script, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        # Área de log
        log_label = ttk.Label(self.exec_frame, text="Log de Execução:")
        log_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.log_text = scrolledtext.ScrolledText(self.exec_frame, height=20, width=80)
        self.log_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Barra de progresso
        self.progress = ttk.Progressbar(self.exec_frame, mode='indeterminate')
        self.progress.pack(fill='x', padx=20, pady=(0, 10))
        
        # Variável para controlar o processo
        self.process = None
        
    def save_config(self):
        """Salva as configurações em um arquivo .env"""
        try:
            env_content = []
            for var_name, entry in self.entries.items():
                if var_name == "DESCRICAO":
                    value = entry.get("1.0", tk.END).strip()
                else:
                    value = entry.get().strip()
                
                # Escapar aspas duplas no valor
                value = value.replace('"', '\\"')
                env_content.append(f'{var_name}="{value}"')
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write('\n'.join(env_content))
            
            messagebox.showinfo("Sucesso", "Configurações salvas no arquivo .env")
            self.log_message("Configurações salvas com sucesso.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
            self.log_message(f"Erro ao salvar configurações: {str(e)}")
    
    def load_config(self):
        """Carrega as configurações do arquivo .env"""
        try:
            if not os.path.exists('.env'):
                messagebox.showwarning("Aviso", "Arquivo .env não encontrado.")
                return
            
            with open('.env', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    # Remover aspas do valor
                    value = value.strip('"\'')
                    
                    if key in self.entries:
                        if key == "DESCRICAO":
                            self.entries[key].delete("1.0", tk.END)
                            self.entries[key].insert("1.0", value)
                        else:
                            self.entries[key].delete(0, tk.END)
                            self.entries[key].insert(0, value)
            
            messagebox.showinfo("Sucesso", "Configurações carregadas do arquivo .env")
            self.log_message("Configurações carregadas com sucesso.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {str(e)}")
            self.log_message(f"Erro ao carregar configurações: {str(e)}")
    
    def log_message(self, message):
        """Adiciona uma mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def run_script(self):
        """Executa o script principal"""
        # Primeiro salvar as configurações
        self.save_config()
        
        # Verificar se o arquivo main.py existe
        if not os.path.exists('main.py'):
            messagebox.showerror("Erro", "Arquivo main.py não encontrado!")
            return
        
        # Mudar para a aba de execução
        self.notebook.select(1)
        
        # Limpar log
        self.log_text.delete(1.0, tk.END)
        
        # Desabilitar botão de execução e habilitar botão de parar
        self.run_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # Iniciar barra de progresso
        self.progress.start()
        
        # Executar em thread separada
        self.script_thread = threading.Thread(target=self._execute_script)
        self.script_thread.daemon = True
        self.script_thread.start()
    
    def _execute_script(self):
        """Executa o script em thread separada"""
        try:
            self.log_message("Iniciando execução do script...")
            
            # Executar o script
            self.process = subprocess.Popen(
                [sys.executable, 'main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Ler output em tempo real
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.log_message(line.strip())
            
            # Aguardar conclusão
            self.process.wait()
            
            if self.process.returncode == 0:
                self.log_message("Script executado com sucesso!")
            else:
                self.log_message(f"Script finalizado com código de erro: {self.process.returncode}")
                
        except Exception as e:
            self.log_message(f"Erro durante a execução: {str(e)}")
        
        finally:
            # Reabilitar botões
            self.root.after(0, self._execution_finished)
    
    def _execution_finished(self):
        """Chamado quando a execução termina"""
        self.run_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress.stop()
        self.process = None
    
    def stop_script(self):
        """Para a execução do script"""
        if self.process:
            try:
                self.process.terminate()
                self.log_message("Execução interrompida pelo usuário.")
            except Exception as e:
                self.log_message(f"Erro ao parar execução: {str(e)}")

def main():
    root = tk.Tk()
    app = FormularioApp(root)
    
    # Carregar configurações automaticamente se existir
    if os.path.exists('.env'):
        app.load_config()
    
    root.mainloop()

if __name__ == "__main__":
    main()

