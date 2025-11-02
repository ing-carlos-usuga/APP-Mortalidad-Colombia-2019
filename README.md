Carlos Jesús Úsuga Rozo
Maestría en Inteligencia Artificial – Universidad de La Salle
Enlace de render

https://usuga-act4-app-mortalidad-colombia-2019.onrender.com
Enlace de github
https://github.com/ing-carlos-usuga/APP-Mortalidad-Colombia-2019
Introducción del proyecto
Esta aplicación web interactiva permite analizar la mortalidad en Colombia durante el año 2019, utilizando datos del DANE. A través de gráficos dinámicos y tablas estadísticas desarrolladas con Dash y Plotly, el usuario puede visualizar patrones de mortalidad por departamento, sexo, grupo de edad y causas principales.

Objetivo
Objetivo principal es ofrecer una herramienta analítica que permita:
Explorar y comprender la distribución de muertes por regiones y factores demográficos.


Identificar tendencias mensuales, grupos de edad con mayor incidencia y principales causas de muerte.


Proveer un recurso educativo analitico que pueda ser visualizado en la nube  y localmente
Estructura del proyecto
│
<img width="346" height="555" alt="Captura de pantalla 2025-11-02 a la(s) 2 58 42 p m" src="https://github.com/user-attachments/assets/18b2c9ef-41d0-4b30-929d-04cdd52e97b1" />

Requisitos
Versión de Python: 3.12 o superior
Librerías necesarias (requirements.txt):
dash==2.17.1
pandas==2.2.2
numpy==1.26.4
plotly==5.24.1
openpyxl==3.1.5
gunicorn==21.2.0


Software y tecnologías utilizadas
Python 3.12 
Dash & Plotly Express – Visualización interactiva de datos
Pandas – Manipulación y análisis de datos
OpenPyXL – Lectura de archivos Excel
Gunicorn – Servidor de producción (para Render)
Render – Plataforma de despliegue web


 Despliegue en Render (PaaS)
Crear un nuevo repositorio en GitHub y subir los archivos del proyecto.


En Render.com:


Crear un nuevo servicio web.


Conectar tu cuenta de GitHub y seleccionar el repositorio.


Elegir Python como entorno.


Configurar los archivos base:


Procfile debe contener:

 web: gunicorn app:server

Asegurar que 
requirements.txt y PYTHON_VERSION estén en la raíz.


Render instalará automáticamente las dependencias y ejecutará el comando de inicio.


Tras la compilación, la aplicación estará disponible en una URL pública 
https://usuga-act4-app-mortalidad-colombia-2019.onrender.com

Ejecución local
Clonar el repositorio
git clone https://github.com/ing-carlos-usuga/APP-Mortalidad-Colombia-2019.git
cd APP-Mortalidad-Colombia-2019
Instalar dependencias
pip install -r requirements.txt
Ejecutar la aplicación
python app.py

Abrir en el navegador
http://127.0.0.1:8050


Visualizaciones principales
La aplicación incluye los siguientes componentes interactivos:
Distribución de muertes por departamento (barras)


Evolución mensual de muertes (líneas)


Top 5 ciudades más violentas (X95 – homicidios)


Ciudades con menor índice de mortalidad (circular)


Tabla de las 10 principales causas de muerte


Muertes por sexo y departamento (barras apiladas)


Histograma por grupo de edad (según GRUPO_EDAD1 del DANE)


Imágenes de soporte:
Configuración de la versión de python para que no se ejecute automáticamente.

<img width="521" height="188" alt="Captura de pantalla 2025-11-02 a la(s) 2 34 03 p m" src="https://github.com/user-attachments/assets/8b77ff3e-14c3-481c-9261-445cd9bfb852" />




imagen iniciando en render la aplicación:

<img width="599" height="287" alt="Captura de pantalla 2025-11-02 a la(s) 2 55 21 p m" src="https://github.com/user-attachments/assets/ff3d9a5d-ac00-49db-bcfb-63095a68d65c" />


Cargando la aplicación localmente:


<img width="1408" height="783" alt="Captura de pantalla 2025-11-02 a la(s) 2 38 17 p m" src="https://github.com/user-attachments/assets/43e5dc66-8167-4bc4-9604-7263d83bc947" />

<img width="1401" height="661" alt="Captura de pantalla 2025-11-02 a la(s) 2 38 26 p m" src="https://github.com/user-attachments/assets/fc0d8cbf-adec-4a1f-a2ed-4ece8d7e4644" />

<img width="1414" height="688" alt="Captura de pantalla 2025-11-02 a la(s) 2 38 35 p m" src="https://github.com/user-attachments/assets/c62d4c14-a6a5-41c8-98ac-ce56bb51d1a5" />

<img width="1412" height="666" alt="Captura de pantalla 2025-11-02 a la(s) 2 38 43 p m" src="https://github.com/user-attachments/assets/d9bdfc6b-db69-4c7e-b7eb-578debaf5ec4" />

<img width="1406" height="633" alt="Captura de pantalla 2025-11-02 a la(s) 2 38 51 p m" src="https://github.com/user-attachments/assets/a6cb1584-c291-4627-9a96-4647d13b276f" />

<img width="1411" height="560" alt="Captura de pantalla 2025-11-02 a la(s) 2 38 58 p m" src="https://github.com/user-attachments/assets/34ec844e-0642-4a3d-a3e6-eb26a65574b0" />





