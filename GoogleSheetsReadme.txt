Para que funcione el Google Sheets, tiene que estar corriendo el script FlaskApi.py y ngrok.exe .
Pasos:
1-Correr FlaskApi.py en consola con el comando:
	python FlaskApi.py
2-Correr ngrok.exe y en su consola, el comando:
	ngrok http 80
ngrok mostrara en consola cual es la url con la que se permitir� conectarse desde Google Sheets a la Api. En la funci�n getUrlNgrok() del App Script, se tendr� que cambiar el valor de url a la proporcionada por ngrok.
