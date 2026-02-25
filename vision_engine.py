import cv2
import logging
import sys
import os
from datetime import datetime

log_dir = "audit_logs"
evidence_dir = "evidence_vault"
os.makedirs(log_dir, exist_ok=True)
os.makedirs(evidence_dir, exist_ok=True)

log_filename = f"{log_dir}/vision_audit_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

def initialize_capture_device():
    target_index = 1 
    stream_source = cv2.VideoCapture(target_index)
    
    if not stream_source.isOpened():
        logging.error(f"Fallo critico: Interface de video inaccesible en puerto {target_index}.")
        sys.exit(1)
        
    logging.info("Stream optico inicializado. Canal de hardware establecido.")
    return stream_source

def execute_native_vision_pipeline(source):
    logging.info("Motor de inferencia y telemetria activo. Use 'q' para interrumpir.")
    
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_detector = cv2.CascadeClassifier(cascade_path)
    
    target_locked = False
    
    while True:
        status, frame = source.read()
        
        if not status:
            logging.warning("Caida de fotogramas detectada en flujo principal.")
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = face_detector.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(detections) > 0:
            if not target_locked:
                event_id = datetime.now().strftime('%Y%m%d_%H%M%S')
                logging.info(f"EVENTO DE SEGURIDAD: Objetivo fijado. ID Evento: {event_id}")
                
                # Renderizado de telemetria en frame original
                for (x, y, w, h) in detections:
                    center_x, center_y = x + w//2, y + h//2
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)
                    cv2.line(frame, (center_x - 15, center_y), (center_x + 15, center_y), (0, 255, 0), 1)
                    cv2.line(frame, (center_x, center_y - 15), (center_x, center_y + 15), (0, 255, 0), 1)
                    cv2.putText(frame, f'TGT_LOCKED_{event_id}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

                # Exportacion de evidencia fotografica
                evidence_path = f"{evidence_dir}/capture_{event_id}.jpg"
                cv2.imwrite(evidence_path, frame)
                logging.info(f"Evidencia visual consolidada en: {evidence_path}")
                
                target_locked = True
                
            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            if target_locked:
                logging.info("EVENTO DE SEGURIDAD: Objetivo fuera de rango.")
                target_locked = False
                
        cv2.imshow('Vision-Scanner-AI | Interfaz Tactica', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info("Protocolo de apagado manual iniciado.")
            break
            
    source.release()
    cv2.destroyAllWindows()
    logging.info("Hardware liberado. Fin de sesion.")

if __name__ == "__main__":
    optical_source = initialize_capture_device()
    execute_native_vision_pipeline(optical_source)