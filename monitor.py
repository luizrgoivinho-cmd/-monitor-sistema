import psutil
import time

print("=== Monitor de sistemas ===")

while True:
	cpu  = psutil.cpu_percent(interval=1)
	memoria = psutil.virtual_memory()

	print(f"Uso da CPU: {cpu}%")
	print(f"Uso da memória RAM: {memoria.percent}%")

	if cpu >80:
		print("ALERTA: uso elevado da CPU!")

	if memoria.percent > 80:
		print("ALERTA: uso elevado da memória!")
	
	print("-" * 30)
	time.sleep(1)
