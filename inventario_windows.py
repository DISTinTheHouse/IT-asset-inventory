import platform
import psutil
import socket
import uuid
import json
import datetime
import os
import getpass
import subprocess

def clear_console():
    os.system("cls" if platform.system() == "Windows" else "clear")

def get_bios_info():
    try:
        manufacturer = subprocess.check_output("wmic computersystem get manufacturer", shell=True).decode().split("\n")[1].strip()
        model = subprocess.check_output("wmic computersystem get model", shell=True).decode().split("\n")[1].strip()
        serial = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
        return {
            "fabricante": manufacturer,
            "modelo": model,
            "numero_serie": serial
        }
    except:
        return {}

def get_network_interfaces():
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                interfaces.append({
                    "interfaz": interface,
                    "ip": addr.address
                })
    return interfaces

def get_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot_time
    return str(uptime)

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "porcentaje": battery.percent,
                "conectado": battery.power_plugged
            }
    except:
        return None

def get_system_info():
    bios = get_bios_info()
    info = {
        "fecha": str(datetime.datetime.now()),
        "usuario": getpass.getuser(),
        "nombre_equipo": socket.gethostname(),
        "dominio_grupo": os.getenv('USERDOMAIN'),
        "ip_local": socket.gethostbyname(socket.gethostname()),
        "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1]),
        "sistema_operativo": platform.system(),
        "version_SO": platform.version(),
        "release_SO": platform.release(),
        "arquitectura": platform.machine(),
        "procesador": platform.processor(),
        "nucleos_fisicos": psutil.cpu_count(logical=False),
        "nucleos_totales": psutil.cpu_count(logical=True),
        "ram_total_GB": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "fabricante": bios.get("fabricante"),
        "modelo": bios.get("modelo"),
        "numero_serie": bios.get("numero_serie"),
        "uptime": get_uptime(),
        "bateria": get_battery_info(),
        "discos": [],
        "red": get_network_interfaces()
    }

    for part in psutil.disk_partitions():
        if "cdrom" in part.opts or part.fstype == '':
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            info["discos"].append({
                "unidad": part.device,
                "montaje": part.mountpoint,
                "tipo": part.fstype,
                "total_GB": round(usage.total / (1024 ** 3), 2),
                "usado_GB": round(usage.used / (1024 ** 3), 2),
                "libre_GB": round(usage.free / (1024 ** 3), 2),
                "porcentaje_usado": usage.percent
            })
        except PermissionError:
            continue

    return info

if __name__ == "__main__":
    clear_console()
    print("==============================")
    print("   INVENTARIO DE EQUIPO")
    print("==============================\n")

    data = get_system_info()
    filename = f"INVENTARIO_{socket.gethostname()}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"[✓] Inventario generado con éxito.")
    print(f"[📁] Archivo creado: {filename}")
    print("\nPuede cerrar esta ventana o presione ENTER para salir.")
    input()
