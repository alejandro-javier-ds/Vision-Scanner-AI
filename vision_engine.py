import cv2
import logging
import sys
import os
import time
import pyodbc
import mediapipe as mp
from datetime import datetime

CAPTURE_INTERVAL = 5.0
VAULT_DIR = "evidence_vault"
os.makedirs(VAULT_DIR, exist_ok=True)

SQL_CONFIG = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=(localdb)\\MSSQLLocalDB;" 
    "Database=VisionSecurityDB;"
    "Trusted_Connection=yes;"
)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("audit_logs/vision_audit.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def register_biometric_event(filename: str, absolute_path: str):
    try:
        connection = pyodbc.connect(SQL_CONFIG)
        cursor = connection.cursor()
        statement = "INSERT INTO BiometricAudit (ImageFilename, ImagePath) VALUES (?, ?)"
        cursor.execute(statement, (filename, absolute_path))
        connection.commit()
        logging.info("SQL_SYNC: Event record committed to BiometricAudit table.")
        connection.close()
    except Exception as error:
        logging.error(f"SQL_ERROR: Synchronization failed. Details: {str(error)}")

def run_biometric_service(video_source: cv2.VideoCapture):
    logging.info("Biometric service initialized. SQL persistence enabled.")
    
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
    
    last_capture_time = time.time() - CAPTURE_INTERVAL
    
    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True) as mesh:
        while True:
            ret, frame = video_source.read()
            if not ret: break
            
            current_time = time.time()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, 
                        landmarks, 
                        mp_face_mesh.FACEMESH_TESSELATION, 
                        drawing_spec, 
                        drawing_spec
                    )
                
                if (current_time - last_capture_time) >= CAPTURE_INTERVAL:
                    timestamp = datetime.now().strftime('%H%M%S')
                    file_name = f"biometric_cap_{timestamp}.jpg"
                    file_path = os.path.abspath(f"{VAULT_DIR}/{file_name}")
                    
                    cv2.imwrite(file_path, frame)
                    logging.info(f"IO_SYSTEM: Evidence saved at {file_name}")
                    
                    register_biometric_event(file_name, file_path)
                    last_capture_time = current_time
            
            cv2.imshow('Vision-Scanner-AI | Production Environment', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Service termination requested by user.")
                break

    video_source.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream = cv2.VideoCapture(1)
    if stream.isOpened():
        run_biometric_service(stream)
    else:
        logging.error("Hardware error: Failed to bind optical sensor.")