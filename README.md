# Vision-Scanner-AI 🛡️

Sistema de monitoreo biométrico avanzado con procesamiento de visión artificial en tiempo real, persistencia de datos en SQL Server y dashboard analítico.

## 🚀 Arquitectura del Sistema
El proyecto implementa un pipeline de datos distribuido en tres capas:
1. **Percepción:** Inferencia de malla facial (468 puntos) mediante MediaPipe.
2. **Persistencia:** Auditoría de eventos en SQL Server (LocalDB) con integridad relacional.
3. **Presentación:** Interfaz web interactiva desarrollada en Streamlit.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.11
- **Visión:** OpenCV & MediaPipe
- **Base de Datos:** SQL Server (ODBC Driver 17)
- **Dashboard:** Streamlit

## 📂 Estructura del Proyecto
- `vision_engine.py`: Motor principal de inferencia y sincronización SQL.
- `dashboard.py`: Panel de control para visualización de evidencias.
- `evidence_vault/`: Almacenamiento local de capturas JPG.
- `audit_logs/`: Registros técnicos de ejecución.

## 📊 Base de Datos
El sistema utiliza una tabla de auditoría `BiometricAudit` con el siguiente esquema:
- `EventID`: Identificador único incremental.
- `CaptureTimestamp`: Marca de tiempo del evento.
- `ImageFilename`: Referencia al archivo físico.
- `ImagePath`: Ruta absoluta para trazabilidad.

## 🔧 Instalación
1. Clonar el repositorio.
2. Crear ambiente virtual: `python -m venv venv`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Ejecutar motor: `python vision_engine.py`.
5. Lanzar dashboard: `streamlit run dashboard.py`.