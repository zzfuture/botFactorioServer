import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

# Launch the browser with the cache enabled
chrome_options = Options()
chrome_options.add_argument('--disk-cache')
driver = webdriver.Chrome(options=chrome_options)

# Load a web page
driver.get('https://www.google.com/')

# Wait for the page to load
time.sleep(5)

# Print the page load time
print(driver.execute_script('return performance.timing.loadEventEnd - performance.timing.navigationStart'))

# Close the browser
driver.quit()

bot = commands.Bot(command_prefix="!", intents=intents)

async def obtener_estado_servidor(html):
    soup = BeautifulSoup(html, 'html.parser')
    etiqueta_estado = soup.find('div', class_='ui small bottom right attached label')
    
    if etiqueta_estado and 'Stopped' in etiqueta_estado.text:
        return 'Apagado'
    
    etiqueta_ip = soup.find('div', class_='center aligned content')
    if etiqueta_ip:
        ip = etiqueta_ip.find_next('div').text.strip()
        return f'Funcionando (IP: {ip})'
    
    return 'Estado desconocido'

async def server():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disk-cache')
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(options=chrome_options)

    usuario = "ikerfdoas@gmail.com"
    contraseña = "1975jeIE"

    try:
        driver.get("https://hostfactor.io/")
        wait = WebDriverWait(driver, 10)
        
        login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Log In')]")))
        login_button.click()

        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
        username_input.send_keys(usuario)

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        password_input.send_keys(contraseña)

        login_submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_submit_button.click()
        
        time.sleep(3)  # Esperar a que cargue la página
        
        cards_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ui.cards .ui.card"))
        )
        
        cards_elements[0].click()
        html_del_elemento = cards_elements[0].get_attribute("outerHTML")
        
        return driver, html_del_elemento
    
    except Exception as e:
        print(f'Error al interactuar con el sitio web: {str(e)}')
        driver.quit()
        return None, None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def fstatus(ctx):
    driver, html_del_elemento = await server()
    
    if driver and html_del_elemento:
        estado_funcionando = await obtener_estado_servidor(html_del_elemento)
        await ctx.author.send(estado_funcionando)
        print(estado_funcionando)
        # await ctx.send(estado_funcionando)
        driver.quit()

@bot.command()
async def frun(ctx):
    driver, _ = await server()
    
    if driver:
        await ctx.author.send("Server iniciándose...")

        try:
            # Esperar a que aparezca el botón "Start" en el popup
            start_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Start')]"))
            )
            start_button.click()

            # Esperar a que se complete el inicio (se muestra "Ready")
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Ready')]"))
            )
            
            estado = await obtener_estado_servidor(driver.page_source)
            await ctx.send(f'Servidor {estado}')
            
        except Exception as e:
            print(f'Error al iniciar el servidor: {str(e)}')
            await ctx.send(f'Error al iniciar el servidor: {str(e)}')
        
        driver.quit()
import tokenDiscord
bot.run(tokenDiscord.rtoken(), prefix="/")