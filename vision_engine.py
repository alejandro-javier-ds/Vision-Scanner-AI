import cv2
import logging
import sys
import os
import time
import mediapipe as mp
from datetime import datetime

CAPTURE_INTERVAL_SECONDS = 5.0
LOG_DIRECTORY = "audit_logs"
VAULT_DIRECTORY = "evidence_vault"

for directory in [LOG_DIRECTORY, VAULT_DIRECTORY]:
    os.makedirs(directory, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIRECTORY}/vision_audit_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def initialize_optical_sensor(target_index: int = 1) -> cv2.VideoCapture:
    capture_stream = cv2.VideoCapture(target_index)
    if not capture_stream.isOpened():
        logging.error(f"Hardware binding failed on port {target_index}.")
        sys.exit(1)
    logging.info("Optical sensor synchronization complete.")
    return capture_stream

def execute_biometric_pipeline(video_stream: cv2.VideoCapture) -> None:
    logging.info(f"Biometric engine active. Auto-capture interval: {CAPTURE_INTERVAL_SECONDS}s.")
    
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing_utils = mp.solutions.drawing_utils
    render_spec = mp_drawing_utils.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
    
    last_capture_timestamp = time.time() - CAPTURE_INTERVAL_SECONDS
    
    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as mesh_model:
        while True:
            frame_status, raw_frame = video_stream.read()
            if not frame_status:
                logging.warning("Video stream integrity lost (Frame drop).")
                break
                
            current_timestamp = time.time()
            rgb_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)
            inference_results = mesh_model.process(rgb_frame)
            
            if inference_results.multi_face_landmarks:
                for face_landmarks in inference_results.multi_face_landmarks:
                    mp_drawing_utils.draw_landmarks(
                        image=raw_frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=render_spec,
                        connection_drawing_spec=render_spec
                    )
                
                if (current_timestamp - last_capture_timestamp) >= CAPTURE_INTERVAL_SECONDS:
                    event_hash = datetime.now().strftime('%H%M%S')
                    evidence_filepath = f"{VAULT_DIRECTORY}/biometric_{event_hash}.jpg"
                    cv2.imwrite(evidence_filepath, raw_frame)
                    logging.info(f"Biometric evidence consolidated: {evidence_filepath}")
                    last_capture_timestamp = current_timestamp
            
            cv2.imshow('Vision-Scanner-AI | Active Monitoring', raw_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Manual interrupt signal received.")
                break
                
    video_stream.release()
    cv2.destroyAllWindows()
    logging.info("Hardware resources released.")

if __name__ == "__main__":
    sensor_stream = initialize_optical_sensor()
    execute_biometric_pipeline(sensor_stream)