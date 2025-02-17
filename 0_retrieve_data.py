import requests

url = 'https://climate.appstate.edu/Data/Met/Chacaltaya/Chacaltaya_hr.dat'

outfile = 'data_hr.dat'
response = requests.get(url)


# Descargar el archivo
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(outfile, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Archivo descargado como {outfile}")
else:
    print(f"Error al descargar el archivo: {response.status_code}")