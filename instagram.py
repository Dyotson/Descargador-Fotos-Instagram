from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests


# ¿Vas a una cuenta privada o a una cuenta publica?
print("Descargador de fotos de Instagram automatico")
print("1.- Cuenta Publica")
print("2.- Cuenta Privada (Se necesitan credenciales)")
opt = int(input('¿Vas a descargar de una cuenta publica o privada? Escribe el numero a continuacion: '))
print("Cargando Webdriver...")

# Ingresar a cuenta de Instagram
driver = webdriver.Firefox()
if opt == 2:
    user = input('Ingresa tu usuario: ')
    pas = input('Ingresa tu contraseña: ')
    print("Cargando...")
    driver.get('https://www.instagram.com')
    time.sleep(3)
    usuario = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
    contrasena = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
    boton = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
    usuario.send_keys(user)
    contrasena.send_keys(pas)
    boton.click()

# Ir a la pagina de interes (Perfil)
driver.get(input('Ingrese el link del perfil de Instagram que quieras descargar (Ej: https://www.instagram.com/usuario/): '))
time.sleep(5)
print("Obteniendo fotografias... (Esto puede tardar un poco)")
links = []
SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    link = driver.find_elements_by_css_selector('.v1Nh3.kIKUG._bz0w')
    for i in link:
        awa = i.find_element_by_tag_name('a')
        lol = awa.get_attribute('href')
        if lol not in links:
            links.append(lol)

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Ir link por link y descargar imagen.
print("Fotografias obtenidas! Empezando a descargar... (Por favor mantener el webdriver en primer plano y no cerrarlo!)")
o = 1
for elements in links:
    driver.get(elements)
    time.sleep(3)
    foto = driver.find_element_by_css_selector('.FFVAD')
    src = foto.get_attribute('src')
    print("Descargando: " + str(src))
    with open(str(o) + '.jpg', 'wb') as handle:
        response = requests.get(src, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    o += 1

print("Fotos descargadas!")
# Cerrar el driver
driver.close()
