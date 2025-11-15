"""
Script para criar tarefa agendada no Windows
Executa a automação diariamente às 5h da manhã
"""

import subprocess
import sys
from pathlib import Path
import os

def criar_tarefa_agendada():
    """Cria tarefa no Agendador de Tarefas do Windows"""
    
    script_dir = Path(__file__).parent.resolve()
    bat_path = script_dir / "executar_automacao.bat"
    
    if not bat_path.exists():
        print(f"❌ Erro: Arquivo não encontrado: {bat_path}")
        return False
    
    # Comando para criar tarefa agendada
    # Usa SCHTASKS (ferramenta do Windows)
    
    task_name = "Lubrimax_Atualizacao_Diaria"
    
    print("=" * 70)
    print("🤖 CONFIGURANDO AUTOMAÇÃO NO WINDOWS")
    print("=" * 70)
    print()
    
    # Verificar se tarefa já existe
    check_cmd = f'schtasks /Query /TN "{task_name}" 2>nul'
    resultado = subprocess.run(check_cmd, shell=True, capture_output=True)
    
    if resultado.returncode == 0:
        print("⚠️  Tarefa já existe. Removendo...")
        delete_cmd = f'schtasks /Delete /TN "{task_name}" /F'
        subprocess.run(delete_cmd, shell=True)
    
    # Criar nova tarefa
    print("📅 Criando tarefa agendada...")
    print(f"   Nome: {task_name}")
    print(f"   Horário: 5:00 AM (todos os dias)")
    print(f"   Script: {bat_path}")
    print()
    
    # Comando para criar tarefa
    create_cmd = f'''schtasks /Create /TN "{task_name}" /TR "\\"{bat_path}\\" agendado" /SC DAILY /ST 05:00 /RL HIGHEST /F'''
    
    resultado = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print("✅ Tarefa criada com sucesso!")
        print()
        print("📋 Detalhes da tarefa:")
        
        # Mostrar informações da tarefa
        info_cmd = f'schtasks /Query /TN "{task_name}" /V /FO LIST'
        info_resultado = subprocess.run(info_cmd, shell=True, capture_output=True, text=True)
        
        if info_resultado.returncode == 0:
            # Mostrar apenas linhas relevantes
            for linha in info_resultado.stdout.split('\n'):
                linha = linha.strip()
                if any(key in linha for key in ['Nome da Tarefa', 'Status', 'Próxima Execução', 
                                                   'Última Execução', 'Horário de Início',
                                                   'Task To Run', 'Next Run Time', 'Status']):
                    print(f"   {linha}")
        
        print()
        print("=" * 70)
        print("✅ CONFIGURAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print()
        print("🔔 Próximos passos:")
        print("   1. A automação vai executar TODO DIA às 5:00 AM")
        print("   2. Você pode testar agora executando:")
        print(f"      schtasks /Run /TN \"{task_name}\"")
        print()
        print("   3. Para desabilitar:")
        print(f"      schtasks /Change /TN \"{task_name}\" /DISABLE")
        print()
        print("   4. Para remover:")
        print(f"      schtasks /Delete /TN \"{task_name}\" /F")
        print()
        print("   5. Ver histórico no Agendador de Tarefas do Windows:")
        print("      Pressione Win+R > taskschd.msc > Enter")
        print()
        
        return True
    else:
        print("❌ Erro ao criar tarefa!")
        print()
        print("Erro:")
        print(resultado.stderr)
        print()
        print("⚠️  Tente executar como Administrador:")
        print("   1. Clique direito no PowerShell")
        print("   2. Executar como Administrador")
        print(f"   3. cd {script_dir}")
        print("   4. python agendar_automacao.py")
        print()
        return False

def main():
    print()
    print("Este script vai configurar a automação para executar")
    print("automaticamente TODO DIA às 5:00 da manhã.")
    print()
    
    resposta = input("Deseja continuar? (s/n): ").strip().lower()
    
    if resposta != 's':
        print("❌ Operação cancelada")
        return 1
    
    print()
    
    if criar_tarefa_agendada():
        return 0
    else:
        return 1

if __name__ == "__main__":
    try:
        # Verificar se está executando como administrador no Windows
        if sys.platform == 'win32':
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            
            if not is_admin:
                print("⚠️  ATENÇÃO: Execute como Administrador para melhores resultados!")
                print()
        
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
