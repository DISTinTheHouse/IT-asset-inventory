import os
import json
import pandas as pd

# Ruta donde están los JSON
CARPETA_JSONS = "inventario_laptops/JSONs"

# Lista para almacenar los datos
inventario = []

for archivo in os.listdir(CARPETA_JSONS):
    if archivo.endswith(".json"):
        ruta = os.path.join(CARPETA_JSONS, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

            # Aplanamos un poco los datos para Excel
            fila = {
                "fecha": datos.get("fecha"),
                "usuario": datos.get("usuario"),
                "equipo": datos.get("nombre_equipo"),
                "dominio": datos.get("dominio_grupo"),
                "ip": datos.get("ip_local"),
                "mac": datos.get("mac_address"),
                "sistema": datos.get("sistema_operativo"),
                "version": datos.get("version_SO"),
                "procesador": datos.get("procesador"),
                "nucleos_fisicos": datos.get("nucleos_fisicos"),
                "nucleos_totales": datos.get("nucleos_totales"),
                "ram_GB": datos.get("ram_total_GB"),
                "modelo": datos.get("modelo"),
                "fabricante": datos.get("fabricante"),
                "numero_serie": datos.get("numero_serie"),
                "uptime": datos.get("uptime"),
                "num_dispositivos_disco": len(datos.get("discos", [])),  # ← nuevo
                "espacio_total_disco_GB": round(sum(d.get("total_GB", 0) for d in datos.get("discos", [])), 2)  # ← nuevo
            }

            # Info de batería (si tiene)
            bateria = datos.get("bateria")
            if bateria:
                fila["bateria_%"] = bateria.get("porcentaje")
                fila["cargando"] = bateria.get("conectado")

            # Agregar interfaces de red (sólo IPs separadas por coma)
            redes = datos.get("red", [])
            fila["interfaces_ip"] = ", ".join([r["ip"] for r in redes])

            # Agregar info de disco principal (unidad C:\ si existe)
            disco_c = next((d for d in datos.get("discos", []) if d["unidad"].startswith("C:")), None)
            if disco_c:
                fila["disco_C_total_GB"] = disco_c["total_GB"]
                fila["disco_C_usado_%"] = disco_c["porcentaje_usado"]

            inventario.append(fila)

# Guardar en Excel
df = pd.DataFrame(inventario)
df.to_excel("INVENTARIO_LAPTOPS.xlsx", index=False)

print(f"[✓] Excel generado: INVENTARIO_LAPTOPS.xlsx")
