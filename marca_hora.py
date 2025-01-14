import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import datetime

# Función para comprobar si es 9:00 AM o 6:00 PM
def should_run():
    now = datetime.datetime.now()
    return (now.hour == 9 and now.minute == 0) or (now.hour == 18 and now.minute == 0)

# Bucle para verificar si es hora de ejecutar
while True:
    if should_run():
        break
    time.sleep(30)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://talana.com/es/remuneraciones/login-vue#/")

    # Ingresar usuario
    page.get_by_label("Usuario, Email o RUT").click()
    page.get_by_label("Usuario, Email o RUT").fill("")
    page.get_by_label("Usuario, Email o RUT").press("Tab")

    # Ingresar contraseña
    page.get_by_label("Contraseña").press("CapsLock")
    page.get_by_label("Contraseña").fill(".")
    page.get_by_label("Contraseña").press("CapsLock")
    page.get_by_label("Contraseña").fill(".")
    
    # Iniciar sesión
    page.get_by_role("button", name="Iniciar sesión").click()

    # Si es 9:00 AM, marca entrada
    if datetime.datetime.now().hour == 9:
        page.get_by_role("button", name="Marcar asistencia").click()
        page.locator(".q-pb-sm > .q-field > .q-field__inner > .q-field__control > .q-field__control-container > .q-field__native").click()
        page.get_by_text("Entrada").click()
        page.get_by_role("button", name="Marcar", exact=True).click()
    
    # Si es 6:00 PM, marca salida
    elif datetime.datetime.now().hour == 18:
        page.get_by_role("button", name="Marcar asistencia").click()
        page.locator(".q-pb-sm > .q-field > .q-field__inner > .q-field__control > .q-field__control-container > .q-field__native").click()
        page.get_by_text("Salida").click()
        page.get_by_role("button", name="Marcar", exact=True).click()

    # Cerrar sesión
    context.close()
    browser.close()
    
# Ejecutar el script con Playwright
with sync_playwright() as playwright:
    run(playwright)
