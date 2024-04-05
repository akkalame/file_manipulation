from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import pandas as pd
import re
from pathlib import Path

app = Flask(__name__,template_folder='app/templates', static_folder='app/static')

delimeter = {
	"tab": "\t", 
	",": ",",
	":":":",
	";":";",
	"line":"\n"
}

# Ruta para cargar el formulario HTML
@app.route('/')
def index():
	return render_template('index.html')

# Ruta para manejar la solicitud POST del formulario
@app.route('/process', methods=['POST'])
def process():
	try:
		
		fileA = request.files['fileA']
		fileB = request.files['fileB']
		sep = request.form['separator']
		tempRoute = os.getcwd()+"\\app\\temp\\"
		mkdir(tempRoute)
		# Guardar los archivos temporales
		fileA.save(tempRoute+fileA.filename)
		
		fileB.save(tempRoute+fileB.filename)

		fileCName = os.path.splitext(fileA.filename)[0] + "-output."+os.path.splitext(fileA.filename)[1]
		
		# Llamar a la función cleanFile
		msg, indicator = cleanFile(tempRoute+fileA.filename, tempRoute+fileB.filename, sep, fileCName)

		# Eliminar los archivos temporales
		os.remove(tempRoute+fileA.filename)
		os.remove(tempRoute+fileB.filename)

		if not msg:
			return send_file(fileCName, as_attachment=True)
		return render_template('index.html', message=msg, msgIndicator=indicator)
	except Exception as e:
		return str(e)
	
def cleanFile(fileA, fileB, sep, fileC, encoding="utf-8"):
	try:
		sep = delimeter[sep]
		sep=","
		# Determinar la extensión de los archivos
		extA = os.path.splitext(fileA)[1]
		extB = os.path.splitext(fileB)[1]

		# Leer archivos CSV o archivos de texto según la extensión
		if extA == '.csv':
			df_a = pd.read_csv(fileA, delimiter=sep)
		elif extA == '.txt':
			if sep == "\n":
				# Leer el archivo de texto línea por línea y dividir cada línea usando el salto de línea como separador
				with open(fileA, 'r', encoding=encoding) as f:
					lines = [line.strip() for line in f]
				df_a = pd.DataFrame(lines)
			else:
				df_a = pd.read_csv(fileA, sep=sep, header=None)

		if extB == '.csv':
			df_b = pd.read_csv(fileB, sep=sep)
		elif extB == '.txt':
			if sep == "\n":
				# Leer el archivo de texto línea por línea y dividir cada línea usando el salto de línea como separador
				with open(fileB, 'r', encoding=encoding) as f:
					lines = [line.strip() for line in f]
				df_b = pd.DataFrame(lines)
			else:
				df_b = pd.read_csv(fileB, sep=sep, header=None)
		
		if sep == "\n":
			# Eliminar las filas de df_a que se encuentran en df_b
			df_resultado = df_a.merge(df_b, indicator=True, how='outer').loc[lambda x : x['_merge'] == 'left_only'].drop(columns='_merge')
		else:
			df_resultado = df_a.merge(df_b, indicator=True, how='outer').loc[lambda x: x['_merge'] == 'left_only'].drop(columns='_merge')
			#df_resultado = df_a[~df_a.isin(df_b)].dropna()

		# Guardar el resultado en un nuevo archivo CSV con el delimitador de tabulación
		df_resultado.to_csv(fileC, index=False, encoding="utf-8", sep=sep)
		return None, ""
	except pd.errors.ParserError as e:
		return parse_pandas_error_message(str(e))
	except Exception as e:
		return str(e)


def parse_pandas_error_message(error_message):
	# Expresión regular para buscar el número esperado de campos y el número real de campos en el mensaje de error
	invalidNumFields = r"Expected (\d+) fields in line (\d+), saw (\d+)"
	
	indicator = "error-message"
	if re.search(invalidNumFields, error_message):
		match = re.search(invalidNumFields, error_message)
		expected_fields = int(match.group(1))
		line_number = int(match.group(2))
		actual_fields = int(match.group(3))
		
		msg = f"Error al analizar el archivo CSV: Se esperaban {expected_fields} campos en la línea {line_number}, pero se encontraron {actual_fields}. Por favor, revisa la estructura del archivo y asegúrate de que esté formateado correctamente."
	else:
		msg = "Error al analizar el archivo: No se pudo determinar el problema específico. Por favor, revisa el archivo y asegúrate de que esté formateado correctamente."
	return msg, indicator

if __name__ == '__main__':
	app.run(debug=True)


def mkdir(path):
	carpeta = Path(path)
	if not carpeta.exists():
		try:
			carpeta.mkdir()
		except:
			pass

