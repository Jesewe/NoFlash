import pymem, time, requests
import pymem.process
from threading import Thread

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
m_flFlashMaxAlpha = int(response["netvars"]["m_flFlashMaxAlpha"])


try:
	pm = pymem.Pymem("csgo.exe")
	client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
except:
	ctypes.windll.user32.MessageBoxW (None, 'Не удалось получить доступ к процессу - csgo.exe.', 'Сбой', 0)
	sys.exit()


def NoFlash():
    while True:
        player = pm.read_int(client + dwLocalPlayer)
        if player:
            flash_value = player + m_flFlashMaxAlpha
            if flash_value:
                pm.write_float(flash_value, float(0))
        time.sleep(1)


Thread(target=NoFlash).start()