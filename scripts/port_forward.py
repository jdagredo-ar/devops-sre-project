import subprocess
import sys
import time

# Definimos los túneles necesarios: Servicio de K8s, puerto local y puerto del pod
TUNNELS = [
    {"name": "Grafana", "service": "svc/grafana-svc", "local": 30300, "remote": 3000},
    {"name": "Prometheus", "service": "svc/prometheus-svc", "local": 30090, "remote": 9090},
    {"name": "Backend", "service": "svc/backend-svc", "local": 30080, "remote": 8000},
]


def start_tunnel(tunnel):
  cmd = [
      "kubectl",
      "port-forward",
      tunnel["service"],
      f"{tunnel['local']}:{tunnel['remote']}",
  ]
  print(
      f"[*] Iniciando túnel para {tunnel['name']} en http://localhost:{tunnel['local']}"
  )
  while True:
    try:
      process = subprocess.Popen(
          cmd,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
      )
      # Mantenemos el proceso vivo y leemos errores si se cae
      stdout, stderr = process.communicate()
      if process.returncode != 0:
        print(
            f"[!] El túnel de {tunnel['name']} se desconectó. Reiniciando en 5"
            f" segundos... Error: {stderr.strip()}"
        )
        time.sleep(5)
    except Exception as e:
      print(f"[X] Error en {tunnel['name']}: {e}")
      time.sleep(5)


if __name__ == "__main__":
  import threading

  print("🚀 Levantando la automatización de túneles SRE para Kubernetes...")

  threads = []
  for t in TUNNELS:
    thread = threading.Thread(target=start_tunnel, args=(t,), daemon=True)
    thread.start()
    threads.append(thread)
    time.sleep(1)  # Pequeño respiro entre hilos

  print(
      "\n✨ ¡Todos los túneles están corriendo en segundo plano! Presiona Ctrl+C"
      " para salir.\n"
  )

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print(
        "\n🛑 Deteniendo los túneles de observabilidad. ¡Hasta la próxima!"
    )
    sys.exit(0)