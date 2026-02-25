import streamlit as st
import os
import time

# --- CONFIGURACION DE RUTAS ---
VAULT_DIR = "evidence_vault"
LOG_DIR = "audit_logs"

st.set_page_config(page_title="Vision-Scanner AI | Dashboard", layout="wide")

def fetch_latest_logs():
    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith(".log")]
    if not log_files:
        return "No se encontraron registros de auditoria."
    
    # Leer el log mas reciente
    latest_log = max([os.path.join(LOG_DIR, f) for f in log_files], key=os.path.getctime)
    with open(latest_log, "r") as f:
        return f.readlines()[-15:] # Ultimas 15 lineas

def main():
    st.title("🛡️ Vision-Scanner AI | Panel de Control")
    st.markdown("---")
    
    col_gallery, col_logs = st.columns([0.7, 0.3])

    with col_gallery:
        st.subheader("🖼️ Bóveda de Evidencias Biométricas")
        if os.path.exists(VAULT_DIR):
            # Listar y ordenar por fecha de creacion (mas reciente primero)
            images = [f for f in os.listdir(VAULT_DIR) if f.endswith(".jpg")]
            images.sort(key=lambda x: os.path.getctime(os.path.join(VAULT_DIR, x)), reverse=True)
            
            if images:
                grid = st.columns(3)
                for idx, img in enumerate(images[:12]): # Mostrar las ultimas 12
                    with grid[idx % 3]:
                        st.image(f"{VAULT_DIR}/{img}", use_container_width=True)
                        st.caption(f"Captura: {img}")
            else:
                st.info("Esperando deteccion de objetivos...")
        
    with col_logs:
        st.subheader("📜 Logs de Sistema")
        logs = fetch_latest_logs()
        st.code("".join(logs) if isinstance(logs, list) else logs, language="log")
        
        if st.button("🔄 Refrescar Dashboard"):
            st.rerun()

if __name__ == "__main__":
    main()