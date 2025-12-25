import os
import time
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import pyautogui
import pyperclip
from io import StringIO

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            r'C:\Projetos\Lubrimax\Site_Consulta\logs\lubrimax_scraper.log',
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

def login_adj():        
    """Função de login no sistema"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    service = Service(r'C:\Projetos\Lubrimax\Site_Consulta\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://cloud.sistemaiadmin.com.br")
    wait = WebDriverWait(driver, 10)
    time.sleep(2)
    campo_usuario = driver.find_element(By.ID, 'Editbox1')
    campo_usuario.send_keys('Lubrimax_Gerencia')
    time.sleep(2)
    campo_senha = driver.find_element(By.ID, 'Editbox2')    
    campo_senha.send_keys('Lubrimax#24')
    botao_entrar = driver.find_element(By.ID, 'buttonLogOn')
    time.sleep(5)
    botao_entrar.click()
    time.sleep(10)
    wait.until(EC.number_of_windows_to_be(2))
    todas_abas = driver.window_handles
    aba_original = driver.current_window_handle
    for aba in todas_abas:
            if aba != aba_original:
                driver.switch_to.window(aba)
                logging.info(f"[OK] Trocado para nova aba: {aba}")
                break
    
    # Tentativa de localizar a imagem com retries
    max_retries = 5
    iAdmin = None
    
    for attempt in range(max_retries):
        try:
            logging.info(f"Tentativa {attempt + 1}/{max_retries} de localizar iAdmin.png...")
            time.sleep(5) # Espera carregar
            iAdmin = pyautogui.locateOnScreen(r'C:\Projetos\Lubrimax\Site_Consulta\imagens\iAdmin.png', confidence=0.8)
            if iAdmin:
                pyautogui.click(iAdmin)
                logging.info("[OK] Clicado no ícone iAdmin") 
                break
        except Exception as e:
            logging.warning(f"Imagem não encontrada na tentativa {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                logging.error("Não foi possível localizar o ícone iAdmin após várias tentativas.")
                raise e
    
    time.sleep(5)
    pyautogui.click(860,575)
    time.sleep(1)
    pyautogui.click(731,622)
    time.sleep(1)
    pyautogui.click(604,674)
    time.sleep(2)
    pyautogui.write('ALEXANDRE')
    time.sleep(2)
    pyautogui.click(612,778)
    time.sleep(2)
    pyautogui.write('1234')
    time.sleep(2)
    pyautogui.click(645,848)
    logging.info("[OK] Realizado login no iAdmin")
    time.sleep(10)    
    return driver

def login():        
    """Função de login no sistema"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    service = Service(r'C:\Projetos\Lubrimax\Site_Consulta\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://cloud.sistemaiadmin.com.br")
    wait = WebDriverWait(driver, 10)
    time.sleep(2)
    campo_usuario = driver.find_element(By.ID, 'Editbox1')
    campo_usuario.send_keys('Lubrimax_Gerencia')
    campo_senha = driver.find_element(By.ID, 'Editbox2')    
    campo_senha.send_keys('Lubrimax#24')
    botao_entrar = driver.find_element(By.ID, 'buttonLogOn')
    time.sleep(5)
    botao_entrar.click()
    time.sleep(10)
    wait.until(EC.number_of_windows_to_be(2))
    todas_abas = driver.window_handles
    aba_original = driver.current_window_handle
    for aba in todas_abas:
            if aba != aba_original:
                driver.switch_to.window(aba)
                logging.info(f"[OK] Trocado para nova aba: {aba}")
                break
    
    # Tentativa de localizar a imagem com retries
    max_retries = 5
    iAdmin = None
    
    for attempt in range(max_retries):
        try:
            logging.info(f"Tentativa {attempt + 1}/{max_retries} de localizar iAdmin.png...")
            time.sleep(5) # Espera carregar
            iAdmin = pyautogui.locateOnScreen(r'C:\Projetos\Lubrimax\Site_Consulta\imagens\iAdmin.png', confidence=0.8)
            if iAdmin:
                pyautogui.click(iAdmin)
                logging.info("[OK] Clicado no ícone iAdmin") 
                break
        except Exception as e:
            logging.warning(f"Imagem não encontrada na tentativa {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                logging.error("Não foi possível localizar o ícone iAdmin após várias tentativas.")
                raise e
    
    time.sleep(5)
    pyautogui.click(604,674)
    time.sleep(2)
    pyautogui.write('ALEXANDRE')
    time.sleep(2)
    pyautogui.click(612,778)
    time.sleep(2)
    pyautogui.write('1234')
    time.sleep(2)
    pyautogui.click(645,848)
    logging.info("[OK] Realizado login no iAdmin")
    time.sleep(10)    
    return driver



def extração_relatorio_vendas_lubrimax(driver):
    """Função para extração do relatório"""
    driver = driver
    pyautogui.click(908,229)
    time.sleep(15)
    pyautogui.click(230,200)
    time.sleep(5)
    pyautogui.click(219,231)
    time.sleep(1)
    pyautogui.click(219,231)
    time.sleep(1)
    pyautogui.click(144,299)
    time.sleep(1)
    pyautogui.click(203,293)
    time.sleep(1)
    pyautogui.click(261,268)
    time.sleep(1)
    pyautogui.click(370,198)
    time.sleep(1)
    pyautogui.click(337,359)
    time.sleep(1)
    pyautogui.click(476,199)
    time.sleep(5)
    pyautogui.click(659,194)
    time.sleep(5)
    pyautogui.click(1087,664)
    time.sleep(5)
    df = pd.read_clipboard()
    caminho_arquivo = r'C:\Projetos\Lubrimax\Vendas_Lubrimax.xlsx'
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
    df.to_excel(caminho_arquivo, index=False, engine='openpyxl')
    logging.info(f"[OK] Relatório salvo em: {caminho_arquivo}")
    pyautogui.click(751,204)
    time.sleep(1)
    pyautogui.click(1024,653)
    time.sleep(2)
    pyautogui.click(1076,223)
    time.sleep(2)
    pyautogui.click(940,652)
    time.sleep(2)
    pyautogui.click(78,703)
    time.sleep(2)
    pyautogui.click(930,677)
    return True

def extração_relatorio_vendas_adj(driver):
    """Função para extração do relatório"""
    driver = driver
    pyautogui.click(908,229)
    time.sleep(15)
    pyautogui.click(230,200)
    time.sleep(5)
    pyautogui.click(219,231)
    time.sleep(1)
    pyautogui.click(219,231)
    time.sleep(1)
    pyautogui.click(144,299)
    time.sleep(1)
    pyautogui.click(203,293)
    time.sleep(1)
    pyautogui.click(261,268)
    time.sleep(1)
    pyautogui.click(370,198)
    time.sleep(1)
    pyautogui.click(337,359)
    time.sleep(1)
    pyautogui.click(476,199)
    time.sleep(5)
    pyautogui.click(659,194)
    time.sleep(5)
    pyautogui.click(1087,664)
    time.sleep(5)
    df = pd.read_clipboard()
    caminho_arquivo = r'C:\Projetos\Lubrimax\Vendas_Lubrimax.xlsx'
    df_existente = pd.read_excel(caminho_arquivo, engine='openpyxl')
    df_completo = pd.concat([df_existente, df], ignore_index=True)
    df_completo.to_excel(caminho_arquivo, index=False, engine='openpyxl')
    logging.info(f"[OK] Relatório salvo em: {caminho_arquivo}")
    pyautogui.click(751,204)
    time.sleep(1)
    pyautogui.click(1024,653)
    time.sleep(2)
    pyautogui.click(1076,223)
    time.sleep(2)
    pyautogui.click(940,652)
    time.sleep(2)
    pyautogui.click(78,703)
    time.sleep(2)
    pyautogui.click(930,677)
    return True

def main():
    """Função principal"""
    logging.info("=" * 50)
    logging.info("🚀 Iniciando extração Lubrimax")
    logging.info("=" * 50)
    driver_lubrimax = login()
    sucesso = extração_relatorio_vendas_lubrimax(driver_lubrimax)
    if sucesso:
        logging.info("✅ Extração Lubrimax concluída com sucesso!")
    else:
        logging.error("❌ Extração falhou.") 
    driver_lubrimax.quit()
    driver_adj = login_adj()
    sucesso = extração_relatorio_vendas_adj(driver_adj)
    if sucesso:
        logging.info("✅ Extração ADJ Comercio concluída com sucesso!")
    else:
        logging.error("❌ Extração falhou.") 
    driver_adj.quit()
    
    # Atualizar banco de dados
    logging.info("=" * 50)
    logging.info("🔄 Atualizando banco de dados")
    logging.info("=" * 50)
    try:
        import atualizar_database
        sucesso_db = atualizar_database.main()
        if sucesso_db:
            logging.info("✅ Banco de dados atualizado com sucesso!")
        else:
            logging.error("❌ Falha ao atualizar banco de dados")
    except Exception as e:
        logging.error(f"❌ Erro ao atualizar banco de dados: {e}")

if __name__ == "__main__":
    main()