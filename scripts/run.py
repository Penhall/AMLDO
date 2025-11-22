#!/usr/bin/env python3
"""
AMLDO - Script de Execução com Menu Interativo

Script multiplataforma (Windows/Linux/Mac) para executar as aplicações do AMLDO.

Uso:
    python scripts/run.py           # Menu interativo
    python scripts/run.py --api     # FastAPI diretamente
    python scripts/run.py --streamlit  # Streamlit diretamente
    python scripts/run.py --adk     # Google ADK diretamente
    python scripts/run.py --all     # Todas as aplicações
    python scripts/run.py --kill    # Matar processos nas portas (8000, 8501, 8080)

Notas:
    - Ao iniciar uma aplicação, processos ocupando a porta serão encerrados automaticamente
    - Use --kill para liberar as portas manualmente sem iniciar nenhuma aplicação
"""

import os
import sys
import subprocess
import platform
import signal
import time
import socket
from pathlib import Path
from typing import List, Optional, Set
from dotenv import load_dotenv

# Cores ANSI para output colorido (funciona em Windows 10+ e Unix)
if platform.system() == "Windows":
    # Habilitar cores ANSI no Windows
    os.system("")

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

# Lista de processos iniciados (para cleanup)
processes: List[subprocess.Popen] = []

# Portas usadas pelas aplicações
PORTS = {
    "api": 8000,
    "streamlit": 8501,
    "adk": 8080
}


def is_port_in_use(port: int) -> bool:
    """
    Verifica se uma porta está em uso.

    Args:
        port: Número da porta a verificar

    Returns:
        True se a porta está em uso, False caso contrário
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_pid_on_port(port: int) -> Optional[int]:
    """
    Obtém o PID do processo usando uma porta específica.

    Args:
        port: Número da porta

    Returns:
        PID do processo ou None se não encontrado
    """
    system = platform.system()

    try:
        if system == "Windows":
            # Windows: netstat -ano | findstr :PORT
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True, capture_output=True, text=True
            )
            for line in result.stdout.strip().split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if parts:
                        return int(parts[-1])
        else:
            # Linux/Mac: lsof -ti :PORT ou ss -tlnp
            # Tentar lsof primeiro (mais comum)
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                # Pode retornar múltiplos PIDs, pegar o primeiro
                return int(result.stdout.strip().split('\n')[0])

            # Fallback para ss (Linux)
            result = subprocess.run(
                ['ss', '-tlnp', f'sport = :{port}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                # Extrair PID do output do ss
                import re
                match = re.search(r'pid=(\d+)', result.stdout)
                if match:
                    return int(match.group(1))
    except Exception:
        pass

    return None


def kill_process_on_port(port: int, force: bool = False) -> bool:
    """
    Mata o processo usando uma porta específica.

    Args:
        port: Número da porta
        force: Se True, usa SIGKILL (força encerramento imediato)

    Returns:
        True se conseguiu matar o processo, False caso contrário
    """
    pid = get_pid_on_port(port)
    if pid is None:
        return False

    system = platform.system()

    try:
        if system == "Windows":
            # Windows: taskkill
            cmd = ['taskkill', '/F', '/PID', str(pid)] if force else ['taskkill', '/PID', str(pid)]
            subprocess.run(cmd, capture_output=True)
        else:
            # Linux/Mac: kill
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, sig)

        # Aguardar um pouco para o processo terminar
        time.sleep(0.5)

        # Verificar se a porta foi liberada
        return not is_port_in_use(port)
    except Exception:
        return False


def kill_processes_on_ports(ports: Set[int], verbose: bool = True) -> dict:
    """
    Mata processos em múltiplas portas.

    Args:
        ports: Conjunto de portas a liberar
        verbose: Se True, imprime mensagens de status

    Returns:
        Dicionário com status de cada porta {porta: (tinha_processo, foi_morto)}
    """
    results = {}

    for port in ports:
        if is_port_in_use(port):
            pid = get_pid_on_port(port)
            if verbose:
                print(f"{Colors.YELLOW}⚠️  Porta {port} ocupada (PID: {pid}){Colors.NC}")

            # Tentar matar graciosamente primeiro
            killed = kill_process_on_port(port, force=False)

            if not killed:
                # Se não funcionou, forçar
                if verbose:
                    print(f"{Colors.YELLOW}   Forçando encerramento...{Colors.NC}")
                killed = kill_process_on_port(port, force=True)

            if killed:
                if verbose:
                    print(f"{Colors.GREEN}   ✅ Porta {port} liberada{Colors.NC}")
                results[port] = (True, True)
            else:
                if verbose:
                    print(f"{Colors.RED}   ❌ Não foi possível liberar a porta {port}{Colors.NC}")
                results[port] = (True, False)
        else:
            results[port] = (False, False)

    return results


def ensure_ports_available(app_names: List[str], verbose: bool = True) -> bool:
    """
    Garante que as portas necessárias estão disponíveis.

    Args:
        app_names: Lista de nomes de aplicações ("api", "streamlit", "adk")
        verbose: Se True, imprime mensagens de status

    Returns:
        True se todas as portas estão disponíveis, False caso contrário
    """
    ports_needed = {PORTS[name] for name in app_names if name in PORTS}

    # Verificar quais portas estão em uso
    ports_in_use = {port for port in ports_needed if is_port_in_use(port)}

    if not ports_in_use:
        return True

    if verbose:
        print(f"\n{Colors.YELLOW}🔍 Verificando portas...{Colors.NC}")

    # Matar processos nas portas ocupadas
    results = kill_processes_on_ports(ports_in_use, verbose=verbose)

    # Verificar se todas as portas foram liberadas
    all_freed = all(
        not had_process or was_killed
        for had_process, was_killed in results.values()
    )

    if verbose and all_freed:
        print()

    return all_freed


def print_banner():
    """Imprime banner do AMLDO."""
    banner = f"""
{Colors.CYAN}════════════════════════════════════════════════════════════
{Colors.GREEN}    ___    __  _____    ____  ____   ____
   /   |  /  |/  / /   / __ \\/ __ \\ / __ \\
  / /| | / /|_/ / /   / / / / / / // / / /
 / ___ |/ /  / / /___/ /_/ / /_/ // /_/ /
/_/  |_/_/  /_/_____/_____/\\____/ \\____/
{Colors.NC}
{Colors.BOLD}Sistema RAG para Legislação de Licitações{Colors.NC}
{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}
"""
    print(banner)

def check_prerequisites() -> bool:
    """
    Verifica pré-requisitos para executar as aplicações.

    Returns:
        True se todos os pré-requisitos estão OK, False caso contrário
    """
    errors = []
    warnings = []

    # 1. Verificar se está no diretório raiz do projeto
    if not Path("pyproject.toml").exists():
        errors.append("❌ Execute este script do diretório raiz do projeto AMLDO")
        errors.append("   Exemplo: python scripts/run.py")

    # 2. Verificar se o pacote está instalado
    try:
        import amldo
    except ImportError:
        errors.append("❌ Pacote 'amldo' não instalado")
        errors.append("   Execute: pip install -e .")

    # 3. Verificar compatibilidade Keras/Transformers
    try:
        import keras
        keras_version = keras.__version__
        if keras_version.startswith('3.'):
            errors.append(f"❌ Keras 3 detectado (versão {keras_version}) - incompatível com Transformers")
            errors.append("   SOLUÇÃO:")
            errors.append("   pip install tf-keras")
            errors.append("")
            errors.append("   Ou veja: .instructions/FIX_LANGCHAIN_HUGGINGFACE.md")
    except ImportError:
        # Keras não instalado, tudo bem
        pass

    # 4. Verificar tf-keras (solução alternativa)
    try:
        import transformers
        try:
            # Tentar importar o que causa o erro
            from transformers.activations_tf import get_tf_activation
        except ValueError as e:
            if "Keras 3" in str(e) or "tf-keras" in str(e):
                errors.append("❌ Transformers incompatível com Keras instalado")
                errors.append("   Execute: pip install tf-keras")
                errors.append("")
                errors.append("   Documentação: .instructions/FIX_LANGCHAIN_HUGGINGFACE.md")
        except Exception:
            # Outros erros podem ser ignorados nesta verificação
            pass
    except ImportError:
        # Transformers não instalado
        warnings.append("⚠️  Transformers não instalado (necessário para embeddings)")

    # 5. Verificar .env
    if not Path(".env").exists():
        warnings.append("⚠️  Arquivo .env não encontrado")
        warnings.append("   Crie um baseado em .env.example com GOOGLE_API_KEY")

    # Mostrar avisos
    if warnings:
        print(f"{Colors.YELLOW}Avisos:{Colors.NC}")
        for warning in warnings:
            print(f"  {warning}")
        print()

    # Mostrar erros
    if errors:
        print(f"{Colors.RED}Erros encontrados:{Colors.NC}")
        for error in errors:
            print(f"  {error}")
        print()
        return False

    return True

def cleanup_processes(signum=None, frame=None):
    """
    Encerra todos os processos iniciados.

    Args:
        signum: Sinal recebido (quando chamado por signal handler)
        frame: Frame de execução (quando chamado por signal handler)
    """
    if processes:
        print(f"\n{Colors.YELLOW}🛑 Encerrando aplicações...{Colors.NC}")
        for proc in processes:
            try:
                if proc.poll() is None:  # Processo ainda está rodando
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
            except Exception as e:
                pass
        print(f"{Colors.GREEN}✅ Todas as aplicações foram encerradas{Colors.NC}")

    if signum is not None:
        sys.exit(0)

def run_fastapi():
    """Executa FastAPI REST API."""
    # Garantir que a porta está disponível
    if not ensure_ports_available(["api"]):
        print(f"{Colors.RED}❌ Não foi possível liberar a porta 8000{Colors.NC}")
        sys.exit(1)

    print(f"{Colors.BLUE}🚀 Iniciando FastAPI REST API...{Colors.NC}\n")

    print(f"{Colors.GREEN}📊 Acessos disponíveis:{Colors.NC}")
    print(f"   Interface Web: http://127.0.0.1:8000")
    print(f"   Swagger Docs:  http://127.0.0.1:8000/docs")
    print(f"   ReDoc:         http://127.0.0.1:8000/redoc")
    print(f"   Health Check:  http://127.0.0.1:8000/health")
    print()
    print(f"{Colors.GREEN}🔍 Endpoints principais:{Colors.NC}")
    print(f"   POST /api/ask       - Consultas RAG")
    print(f"   POST /api/upload    - Upload de PDFs")
    print(f"   POST /api/process   - Processar documentos")
    print(f"   GET  /api/metrics/stats - Estatísticas")
    print()
    print(f"{Colors.CYAN}────────────────────────────────────────────────────────────{Colors.NC}")
    print(f"{Colors.GREEN}Pressione Ctrl+C para parar o servidor{Colors.NC}")
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}\n")

    # Executar amldo-api
    try:
        subprocess.run([sys.executable, "-m", "amldo.interfaces.api.run"], check=True)
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}✅ FastAPI encerrada{Colors.NC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Erro ao executar FastAPI: {e}{Colors.NC}")
        sys.exit(1)

def run_streamlit():
    """Executa Streamlit Web App."""
    # Garantir que a porta está disponível
    if not ensure_ports_available(["streamlit"]):
        print(f"{Colors.RED}❌ Não foi possível liberar a porta 8501{Colors.NC}")
        sys.exit(1)

    print(f"{Colors.BLUE}🎨 Iniciando Streamlit Web App...{Colors.NC}\n")

    print(f"{Colors.GREEN}📊 Interface disponível em:{Colors.NC}")
    print(f"   http://localhost:8501")
    print()
    print(f"{Colors.GREEN}📄 Páginas disponíveis:{Colors.NC}")
    print(f"   • Home        - Visão geral do sistema")
    print(f"   • Pipeline    - Processamento de documentos")
    print(f"   • RAG Query   - Consultas à base de conhecimento")
    print()
    print(f"{Colors.CYAN}────────────────────────────────────────────────────────────{Colors.NC}")
    print(f"{Colors.GREEN}Pressione Ctrl+C para parar o servidor{Colors.NC}")
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}\n")

    # Executar streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "src/amldo/interfaces/streamlit/app.py",
            "--server.port=8501"
        ], check=True)
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}✅ Streamlit encerrado{Colors.NC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Erro ao executar Streamlit: {e}{Colors.NC}")
        sys.exit(1)

def run_adk():
    """Executa Google ADK Interface."""
    # Garantir que a porta está disponível
    if not ensure_ports_available(["adk"]):
        print(f"{Colors.RED}❌ Não foi possível liberar a porta 8080{Colors.NC}")
        sys.exit(1)

    print(f"{Colors.BLUE}🤖 Iniciando Google ADK Interface...{Colors.NC}\n")

    # Verificar GOOGLE_API_KEY
    if not os.getenv("GOOGLE_API_KEY"):
        print(f"{Colors.YELLOW}⚠️  Aviso: GOOGLE_API_KEY não configurado no .env{Colors.NC}")
        print()

    print(f"{Colors.GREEN}📊 Interface disponível em:{Colors.NC}")
    print(f"   http://localhost:8080")
    print()
    print(f"{Colors.GREEN}🤖 Agentes RAG disponíveis:{Colors.NC}")
    print(f"   • rag_v1 - RAG básico (MMR search)")
    print(f"   • rag_v2 - RAG avançado (contexto hierárquico + MMR) ⭐")
    print(f"   • rag_v3 - RAG experimental (similarity search)")
    print()
    print(f"{Colors.CYAN}────────────────────────────────────────────────────────────{Colors.NC}")
    print(f"{Colors.GREEN}Pressione Ctrl+C para parar o servidor{Colors.NC}")
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}\n")

    # Executar adk web na porta 8080 (evitar conflito com FastAPI na 8000)
    try:
        subprocess.run(["adk", "web", "--port", "8080"], check=True)
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}✅ Google ADK encerrado{Colors.NC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Erro ao executar Google ADK: {e}{Colors.NC}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Comando 'adk' não encontrado{Colors.NC}")
        print(f"   Execute: pip install -e .[adk]")
        sys.exit(1)

def kill_all_apps():
    """Mata todos os processos nas portas usadas pelo AMLDO."""
    print(f"{Colors.YELLOW}🔪 Encerrando processos nas portas do AMLDO...{Colors.NC}\n")

    all_ports = set(PORTS.values())
    results = kill_processes_on_ports(all_ports, verbose=True)

    # Resumo
    killed_count = sum(1 for had, was_killed in results.values() if had and was_killed)
    in_use_count = sum(1 for had, _ in results.values() if had)

    print()
    if in_use_count == 0:
        print(f"{Colors.GREEN}✅ Nenhuma porta estava em uso{Colors.NC}")
    elif killed_count == in_use_count:
        print(f"{Colors.GREEN}✅ Todos os {killed_count} processos foram encerrados{Colors.NC}")
    else:
        failed = in_use_count - killed_count
        print(f"{Colors.YELLOW}⚠️  {killed_count}/{in_use_count} processos encerrados ({failed} falharam){Colors.NC}")


def run_all():
    """Executa todas as aplicações simultaneamente."""
    # Garantir que todas as portas estão disponíveis
    if not ensure_ports_available(["api", "streamlit", "adk"]):
        print(f"{Colors.RED}❌ Não foi possível liberar todas as portas necessárias{Colors.NC}")
        sys.exit(1)

    print(f"{Colors.BLUE}🚀 Iniciando TODAS as aplicações AMLDO...{Colors.NC}\n")

    # Registrar handler para Ctrl+C
    signal.signal(signal.SIGINT, cleanup_processes)
    if platform.system() != "Windows":
        signal.signal(signal.SIGTERM, cleanup_processes)

    # Criar diretório de logs
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    print(f"{Colors.GREEN}🚀 Iniciando aplicações em background...{Colors.NC}\n")

    # 1. Iniciar FastAPI
    print(f"{Colors.BLUE}[1/3]{Colors.NC} Iniciando FastAPI REST API...")
    api_log = open(logs_dir / "api.log", "w")
    api_proc = subprocess.Popen(
        [sys.executable, "-m", "amldo.interfaces.api.run"],
        stdout=api_log,
        stderr=subprocess.STDOUT
    )
    processes.append(api_proc)
    print(f"{Colors.GREEN}      ✅ FastAPI iniciada (PID: {api_proc.pid}){Colors.NC}")
    time.sleep(2)

    # 2. Iniciar Streamlit
    print(f"{Colors.BLUE}[2/3]{Colors.NC} Iniciando Streamlit Web App...")
    streamlit_log = open(logs_dir / "streamlit.log", "w")
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run",
         "src/amldo/interfaces/streamlit/app.py",
         "--server.port=8501", "--server.headless=true"],
        stdout=streamlit_log,
        stderr=subprocess.STDOUT
    )
    processes.append(streamlit_proc)
    print(f"{Colors.GREEN}      ✅ Streamlit iniciado (PID: {streamlit_proc.pid}){Colors.NC}")
    time.sleep(2)

    # 3. Iniciar Google ADK
    print(f"{Colors.BLUE}[3/3]{Colors.NC} Iniciando Google ADK Interface...")
    adk_log = open(logs_dir / "adk.log", "w")
    try:
        adk_proc = subprocess.Popen(
            ["adk", "web", "--port", "8080"],
            stdout=adk_log,
            stderr=subprocess.STDOUT
        )
        processes.append(adk_proc)
        print(f"{Colors.GREEN}      ✅ Google ADK iniciado (PID: {adk_proc.pid}){Colors.NC}")
    except FileNotFoundError:
        print(f"{Colors.YELLOW}      ⚠️  Google ADK não disponível (adk não instalado){Colors.NC}")
    time.sleep(2)

    print()
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}")
    print(f"{Colors.GREEN}✅ Aplicações iniciadas com sucesso!{Colors.NC}")
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}")
    print()
    print(f"{Colors.GREEN}📊 Interfaces disponíveis:{Colors.NC}")
    print()
    print(f"{Colors.BLUE}🔹 FastAPI REST API:{Colors.NC}")
    print(f"   Interface Web: http://127.0.0.1:8000")
    print(f"   Swagger Docs:  http://127.0.0.1:8000/docs")
    print(f"   ReDoc:         http://127.0.0.1:8000/redoc")
    print()
    print(f"{Colors.BLUE}🔹 Streamlit Web App:{Colors.NC}")
    print(f"   Interface:     http://localhost:8501")
    print()
    if len(processes) == 3:
        print(f"{Colors.BLUE}🔹 Google ADK:{Colors.NC}")
        print(f"   Interface:     http://localhost:8080")
        print()
    print(f"{Colors.YELLOW}📝 Logs disponíveis em:{Colors.NC}")
    print(f"   FastAPI:    logs/api.log")
    print(f"   Streamlit:  logs/streamlit.log")
    if len(processes) == 3:
        print(f"   Google ADK: logs/adk.log")
    print()
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}")
    print(f"{Colors.GREEN}Pressione Ctrl+C para parar todas as aplicações{Colors.NC}")
    print(f"{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.NC}\n")

    # Aguardar até Ctrl+C
    try:
        while True:
            # Verificar se algum processo terminou inesperadamente
            for proc in processes:
                if proc.poll() is not None:
                    print(f"{Colors.RED}⚠️  Processo {proc.pid} terminou inesperadamente{Colors.NC}")
                    cleanup_processes()
                    sys.exit(1)
            time.sleep(5)
    except KeyboardInterrupt:
        cleanup_processes()

def show_menu():
    """Exibe menu interativo e retorna a escolha do usuário."""
    print(f"{Colors.GREEN}Escolha a aplicação para executar:{Colors.NC}\n")
    print(f"  {Colors.BOLD}1{Colors.NC} - FastAPI REST API (porta 8000)")
    print(f"  {Colors.BOLD}2{Colors.NC} - Streamlit Web App (porta 8501)")
    print(f"  {Colors.BOLD}3{Colors.NC} - Google ADK Interface (porta 8080)")
    print(f"  {Colors.BOLD}4{Colors.NC} - Todas as aplicações (8000, 8501, 8080)")
    print(f"  {Colors.BOLD}5{Colors.NC} - {Colors.YELLOW}Matar processos nas portas{Colors.NC} (8000, 8501, 8080)")
    print(f"  {Colors.BOLD}0{Colors.NC} - Sair")
    print()

    while True:
        try:
            choice = input(f"{Colors.CYAN}Digite sua escolha [1-5, 0 para sair]: {Colors.NC}").strip()
            if choice in ["0", "1", "2", "3", "4", "5"]:
                return choice
            else:
                print(f"{Colors.RED}Opção inválida. Digite um número de 0 a 5.{Colors.NC}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.YELLOW}Operação cancelada{Colors.NC}")
            sys.exit(0)

def main():
    """Função principal."""
    load_dotenv()

    # Parse argumentos de linha de comando
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        # --kill não precisa verificar pré-requisitos
        if arg in ["--kill", "-K"]:
            kill_all_apps()
            return

        # Verificar pré-requisitos
        if not check_prerequisites():
            sys.exit(1)

        if arg in ["--api", "-a"]:
            run_fastapi()
        elif arg in ["--streamlit", "-s"]:
            run_streamlit()
        elif arg in ["--adk", "-k"]:
            run_adk()
        elif arg in ["--all", "-A"]:
            run_all()
        elif arg in ["--help", "-h"]:
            print(__doc__)
        else:
            print(f"{Colors.RED}Opção inválida: {arg}{Colors.NC}")
            print(__doc__)
            sys.exit(1)
        return

    # Menu interativo
    print_banner()

    # Verificar pré-requisitos
    if not check_prerequisites():
        sys.exit(1)

    print(f"{Colors.GREEN}✅ Pré-requisitos OK{Colors.NC}\n")

    # Mostrar menu
    choice = show_menu()

    if choice == "0":
        print(f"{Colors.YELLOW}Saindo...{Colors.NC}")
        sys.exit(0)
    elif choice == "1":
        run_fastapi()
    elif choice == "2":
        run_streamlit()
    elif choice == "3":
        run_adk()
    elif choice == "4":
        run_all()
    elif choice == "5":
        kill_all_apps()

if __name__ == "__main__":
    main()
