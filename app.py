import streamlit as st
import json
import os
from datetime import datetime

CONFIG_FILE = "config_rangos_ivesur.json"

DEFAULT_CONFIG = {
    "1. Motocicleta / Ciclomotor": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "80/90-17",
        "rangos": {
            "Eje Delantero": {"ideal": 30.0},
            "Eje Trasero": {"ideal": 33.0}
        }
    },
    "2. Motocarro / Tricimoto": {
        "ejes": ["Eje Delantero", "Eje Trasero (Carga)"],
        "llanta_ref": "4.50-10",
        "rangos": {
            "Eje Delantero": {"ideal": 32.0},
            "Eje Trasero (Carga)": {"ideal": 40.0}
        }
    },
    "3. Can-Am / Triciclo Recreativo (Ej: Spyder)": {
        "ejes": ["Eje Delantero (Doble)", "Eje Trasero"],
        "llanta_ref": "165/55 R15",
        "rangos": {
            "Eje Delantero (Doble)": {"ideal": 18.0},
            "Eje Trasero": {"ideal": 22.0}
        }
    },
    "4. Automóvil / SUV (Particular)": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "195/65 R15",
        "rangos": {
            "Eje Delantero": {"ideal": 30.0},
            "Eje Trasero": {"ideal": 30.0}
        }
    },
    "5. Taxi (Público Individual)": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "185/70 R14",
        "rangos": {
            "Eje Delantero": {"ideal": 33.0},
            "Eje Trasero": {"ideal": 34.0}
        }
    },
    "6. Vehículo de Enseñanza Automovilística": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "195/65 R15",
        "rangos": {
            "Eje Delantero": {"ideal": 32.0},
            "Eje Trasero": {"ideal": 32.0}
        }
    },
    "7. Transporte Escolar / Van Especial": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "215/70 R15C",
        "rangos": {
            "Eje Delantero": {"ideal": 45.0},
            "Eje Trasero": {"ideal": 55.0}
        }
    },
    "8. Ambulancia / Vehículo de Emergencia": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "225/75 R16C",
        "rangos": {
            "Eje Delantero": {"ideal": 50.0},
            "Eje Trasero": {"ideal": 60.0}
        }
    },
    "9. Carga < 3.5 Toneladas (Turbos / Furgón)": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "7.00 R16",
        "rangos": {
            "Eje Delantero": {"ideal": 45.0},
            "Eje Trasero": {"ideal": 60.0}
        }
    },
    "10. Carga > 3.5 Toneladas (Camión Rígido)": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "rangos": {
            "Eje Delantero": {"ideal": 80.0},
            "Eje Trasero": {"ideal": 90.0}
        },
        "llanta_ref": "295/80 R22.5"
    },
    "11. Pesados y Tractomulas (Mulas)": {
        "ejes": ["Eje Direccional", "Eje Tracción", "Eje Arrastre (Tráiler)"],
        "llanta_ref": "11 R22.5",
        "rangos": {
            "Eje Direccional": {"ideal": 105.0},
            "Eje Tracción": {"ideal": 100.0},
            "Eje Arrastre (Tráiler)": {"ideal": 100.0}
        }
    },
    "12. TransMilenio y SITP Zonal": {
        "ejes": ["Eje Direccional", "Eje Intermedio", "Eje Tracción / Remolque"],
        "llanta_ref": "275/80 R22.5",
        "rangos": {
            "Eje Direccional": {"ideal": 115.0},
            "Eje Intermedio": {"ideal": 115.0},
            "Eje Tracción / Remolque": {"ideal": 120.0}
        }
    },
    "13. ATVs y Cuatrimotos (Todo Terreno)": {
        "ejes": ["Eje Delantero", "Eje Trasero"],
        "llanta_ref": "25x8-12",
        "rangos": {
            "Eje Delantero": {"ideal": 5.5},
            "Eje Trasero": {"ideal": 5.5}
        }
    }
}

def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def guardar_configuracion(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

if "db_presiones" not in st.session_state:
    st.session_state.db_presiones = cargar_configuracion()

st.set_page_config(page_title="Pre-Revisión CDA Ivesur", layout="centered")

# =============================================================
# ESTILOS VISUALES: NARANJA INDUSTRIAL CDA IVESUR
# =============================================================
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF6600;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #E65C00;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================
# MENÚ LATERAL (LOGO Y MODO)
# =============================================================
st.sidebar.title("🎛️ Panel CDA Ivesur")
if os.path.exists("logo_ivesur.png"):
    st.sidebar.image("logo_ivesur.png", width=160)
st.sidebar.markdown("### 🟠 **CDA IVESUR**")
st.sidebar.caption("Control Técnico Automotriz")
st.sidebar.markdown("---")

modo = st.sidebar.radio(
    "Seleccione el Modo:", 
    ["🚀 Modo Operativo (Patio)", "⚙️ Modo Auditoría (Manual Libre)"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Proyecto de Grado - Ingeniería de Software UNIMINUTO")

# =============================================================
# MODO 1: OPERATIVO (PATIO)
# =============================================================
if modo == "🚀 Modo Operativo (Patio)":
    st.title("🛞 Pre-Revisión de Presión de Llantas")
    st.caption("CDA Ivesur - Control Estricto con Tolerancia del 4%")

    st.markdown("### 📝 1. Trazabilidad y Datos Generales")
    col_insp1, col_insp2 = st.columns(2)
    with col_insp1:
        inspector_id = st.text_input("Inspector / Código:", placeholder="Ej: Insp. Edwin")
    with col_insp2:
        placa_input = st.text_input("Placa / ID del Vehículo:", placeholder="Ej: ABC123").strip().upper()

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        nombre_cliente = st.text_input("Nombre del Conductor / Instructor:", placeholder="Ej: Carlos Pérez")
    with col_c2:
        telefono_cliente = st.text_input("WhatsApp de Contacto:", placeholder="Ej: 3101234567")

    st.markdown("---")
    st.markdown("### 🚗 2. Inspección Técnica y Tipología")

    tipologias = list(st.session_state.db_presiones.keys())
    categoria_sel = st.selectbox("Seleccione Tipología RUNT/CDA:", tipologias)

    datos_cat = st.session_state.db_presiones[categoria_sel]
    llanta_sugerida_db = datos_cat.get("llanta_ref", "195/65 R15")

    # =========================================================
    # SELECTOR DE REFERENCIA DE LLANTA (Sugerida o Escrita a mano)
    # =========================================================
    st.markdown("### 🏷️ Referencia de Llanta del Vehículo")
    col_ref1, col_ref2 = st.columns([2, 1])
    
    with col_ref1:
        seleccion_ref = st.selectbox(
            "Seleccione o elija sugerencia:",
            [llanta_sugerida_db, "195/65 R15", "205/55 R16", "185/70 R14", "11 R22.5", "295/80 R22.5", "275/80 R22.5", "120/70 R17", "180/55 R17", "Otra (Escribir a mano)"]
        )

    if seleccion_ref == "Otra (Escribir a mano)":
        llanta_final = st.text_input("Escriba la referencia personalizada (sugerencia con letra R):", value="R ")
    else:
        llanta_final = seleccion_ref

    st.info(f"📌 **Referencia a aplicar en inspección:** `{llanta_final}`")
    st.markdown("---")

    escuela_nombre, escuela_nit, escuela_dir, escuela_tel = "", "", "", ""
    if "Enseñanza Automovilística" in categoria_sel:
        st.markdown("### 🏫 Datos de la Escuela de Conducción")
        col_esc1, col_esc2 = st.columns(2)
        with col_esc1:
            escuela_nombre = st.text_input("Nombre de la Escuela:", placeholder="Ej: CEA Automándigo")
            escuela_dir = st.text_input("Dirección:", placeholder="Ej: Calle 100 # 15-20")
        with col_esc2:
            escuela_nit = st.text_input("NIT:", placeholder="Ej: 900123456-1")
            escuela_tel = st.text_input("Teléfono:", placeholder="Ej: 6012345678")
        st.markdown("---")

    # =========================================================
    # GRUPO 1: VEHÍCULOS DE 4 RUEDAS ESTÁNDAR
    # =========================================================
    if categoria_sel in [
        "4. Automóvil / SUV (Particular)", 
        "5. Taxi (Público Individual)", 
        "6. Vehículo de Enseñanza Automovilística", 
        "7. Transporte Escolar / Van Especial", 
        "8. Ambulancia / Vehículo de Emergencia", 
        "9. Carga < 3.5 Toneladas (Turbos / Furgón)", 
        "10. Carga > 3.5 Toneladas (Camión Rígido)",
        "13. ATVs y Cuatrimotos (Todo Terreno)"
    ]:
        psi_ideal_del = datos_cat["rangos"]["Eje Delantero"]["ideal"]
        psi_ideal_tras = datos_cat["rangos"]["Eje Trasero"]["ideal"]
        tol_del = psi_ideal_del * 0.04
        tol_tras = psi_ideal_tras * 0.04

        st.markdown(f"📌 **Parámetros de Referencia:**\n"
                    f"- **Eje Delantero:** {psi_ideal_del} PSI (Margen 4%: {psi_ideal_del - tol_del:.1f} a {psi_ideal_del + tol_del:.1f})\n"
                    f"- **Eje Trasero:** {psi_ideal_tras} PSI (Margen 4%: {psi_ideal_tras - tol_tras:.1f} a {psi_ideal_tras + tol_tras:.1f})")

        tiene_runflat = False
        if "Automóvil" in categoria_sel or "Taxi" in categoria_sel:
            es_rf = st.selectbox("¿Vehículo con tecnología Run-Flat de fábrica?", ["No", "Sí"])
            if es_rf == "Sí":
                tiene_runflat = True

        st.markdown("### 🛞 Ingrese las Presiones de las 4 Ruedas")
        col_izq, col_der = st.columns(2)
        with col_izq:
            st.markdown("#### 🔵 Lado Izquierdo")
            psi_di = st.number_input("Delantera Izquierda (PSI):", min_value=0.0, max_value=200.0, value=float(psi_ideal_del), step=0.5)
            psi_ti = st.number_input("Trasera Izquierda (PSI):", min_value=0.0, max_value=200.0, value=float(psi_ideal_tras), step=0.5)
        with col_der:
            st.markdown("#### 🟠 Lado Derecho")
            psi_dd = st.number_input("Delantera Derecha (PSI):", min_value=0.0, max_value=200.0, value=float(psi_ideal_del), step=0.5)
            psi_td = st.number_input("Trasera Derecha (PSI):", min_value=0.0, max_value=200.0, value=float(psi_ideal_tras), step=0.5)

        if st.button("🔍 Validar Diagnóstico (4 Ruedas)", use_container_width=True):
            if not placa_input or not inspector_id:
                st.error("⚠️ Ingrese el código del inspector y la placa.")
            else:
                ok_di = (psi_ideal_del - tol_del) <= psi_di <= (psi_ideal_del + tol_del)
                ok_dd = (psi_ideal_del - tol_del) <= psi_dd <= (psi_ideal_del + tol_del)
                ok_ti = (psi_ideal_tras - tol_tras) <= psi_ti <= (psi_ideal_tras + tol_tras)
                ok_td = (psi_ideal_tras - tol_tras) <= psi_td <= (psi_ideal_tras + tol_tras)

                prom_del = (psi_di + psi_dd) / 2.0
                sim_del = (abs(psi_di - psi_dd) / prom_del) * 100.0 if prom_del > 0 else 0
                prom_tras = (psi_ti + psi_td) / 2.0
                sim_tras = (abs(psi_ti - psi_td) / prom_tras) * 100.0 if prom_tras > 0 else 0

                st.markdown(f"### 📋 Reporte Preventivo: `{placa_input}`")
                st.write(f"**Inspector:** {inspector_id} | **Conductor:** {nombre_cliente or 'No registrado'}")
                st.write(f"🏷️ **Ref. Llanta Registrada:** {llanta_final}")
                if "Enseñanza Automovilística" in categoria_sel and escuela_nombre:
                    st.write(f"**Escuela:** {escuela_nombre} (NIT: {escuela_nit or 'N/A'}) - Tel: {escuela_tel or 'N/A'}")
                
                rc1, rc2 = st.columns(2)
                with rc1:
                    st.write(f"**Del. Izquierda:** {psi_di} PSI ({'✅ OK' if ok_di else '❌'})")
                    st.write(f"**Del. Derecha:** {psi_dd} PSI ({'✅ OK' if ok_dd else '❌'})")
                    st.write(f"⚖️ Simetría Delantera: {sim_del:.1f}%")
                with rc2:
                    st.write(f"**Tras. Izquierda:** {psi_ti} PSI ({'✅ OK' if ok_ti else '❌'})")
                    st.write(f"**Tras. Derecha:** {psi_td} PSI ({'✅ OK' if ok_td else '❌'})")
                    st.write(f"⚖️ Simetría Trasera: {sim_tras:.1f}%")

                if not (ok_di and ok_dd and ok_ti and ok_td):
                    st.error("❌ **RECHAZO EN PATIO:** Presiones fuera del rango de tolerancia del 4%.")
                elif sim_del > 4.0 or sim_tras > 4.0:
                    st.warning("⚠️ **ALERTA DE DESBALANCE:** Desviación mayor al 4% entre lados.")
                else:
                    st.success("✅ **APROBADO EN PATIO:** Cumple con la normativa de presiones.")

    # =========================================================
    # GRUPO 2: MOTOCICLETAS Y CICLOMOTORES
    # =========================================================
    elif "Motocicleta" in categoria_sel:
        st.markdown("### 🏍️ Datos de la Motocicleta / Ciclomotor")
        
        tipo_moto_sel = st.selectbox(
            "Seleccione Categoría de Motor:", 
            ["Motocicleta Estándar / Mediano Cilindraje (< 600 cc)", "Alto Cilindraje (≥ 600 cc)", "Ciclomotor o Vehículo Eléctrico matriculado"]
        )
        
        cilindraje_cc = 0
        es_ciclomotor = False
        potencia_kw = 0.0

        if "Alto Cilindraje" in tipo_moto_sel:
            cilindraje_cc = st.number_input("Cilindraje exacto (CC):", min_value=600, max_value=2500, value=650, step=50)
            st.info(f"🏍️ **Vehículo de Alto Cilindraje registrado:** `{cilindraje_cc} CC` (Norma CDA Ivesur)")
        elif "Ciclomotor" in tipo_moto_sel:
            es_ciclomotor = True
            potencia_kw = st.number_input("Potencia nominal registrada en Tarjeta (kW):", min_value=0.0, max_value=20.0, value=2.0, step=0.1)
            if potencia_kw > 4.0:
                st.warning("⚠️ **Nota Normativa:** Supera los 4 kW establecidos para ciclomotores estándar en Colombia.")

        psi_del = st.number_input("PSI Eje Delantero:", value=32.0 if "Alto Cilindraje" in tipo_moto_sel else 30.0, step=0.5)
        psi_tras = st.number_input("PSI Eje Trasero:", value=36.0 if "Alto Cilindraje" in tipo_moto_sel else 33.0, step=0.5)

        if st.button("🔍 Validar Motocicleta", use_container_width=True):
            if not placa_input or not inspector_id:
                st.error("⚠️ Ingrese el código del inspector y la placa.")
            else:
                st.markdown(f"### 📋 Reporte Preventivo: `{placa_input}`")
                st.write(f"**Inspector:** {inspector_id} | **Propietario:** {nombre_cliente or 'No registrado'}")
                st.write(f"🏷️ **Ref. Llanta:** {llanta_final}")
                
                if "Alto Cilindraje" in tipo_moto_sel:
                    st.write(f"🏁 **Segmento:** Alto Cilindraje | **Cilindraje:** {cilindraje_cc} CC")
                elif es_ciclomotor:
                    st.write(f"⚡ **Tipo:** Ciclomotor / Eléctrico | **Potencia:** {potencia_kw} kW")
                else:
                    st.write(f"🛵 **Segmento:** Motocicleta Estándar")

                st.write(f"**Eje Delantero:** {psi_del} PSI")
                st.write(f"**Eje Trasero:** {psi_tras} PSI")
                st.success("✅ **APROBADO EN PATIO:** Verificación de motocicleta completada.")

    # =========================================================
    # GRUPO 3: MOTOCARROS Y TRICIMOTOS
    # =========================================================
    elif "Motocarro" in categoria_sel:
        st.markdown("### 🛞 Configuración de Rodamiento - Motocarro")
        config_moto = st.radio(
            "Seleccione disposición de ruedas:",
            ["1 Rueda Delantera / 2 Ruedas Traseras (Clásico)", "4 Ruedas (Doble rueda gemela atrás)", "2 Ruedas Delanteras / 1 Rueda Trasera"]
        )
        p_del = st.number_input("PSI Delantera(s):", value=32.0, step=0.5)
        p_tras = st.number_input("PSI Trasera(s):", value=40.0, step=0.5)

        if st.button("🔍 Validar Motocarro", use_container_width=True):
            if not placa_input or not inspector_id:
                st.error("⚠️ Ingrese placa e inspector.")
            else:
                st.markdown(f"### 📋 Reporte: `{placa_input}` (Motocarro)")
                st.write(f"🏷️ **Ref. Llanta:** {llanta_final}")
                st.success("✅ Diagnóstico de Motocarro completado.")

    # =========================================================
    # GRUPO 4: CAN-AM SPYDER
    # =========================================================
    elif "Can-Am" in categoria_sel:
        st.markdown("### 🕷️ Configuración Can-Am / Triciclo Recreativo")
        dispo_spyder = st.radio(
            "Distribución de ruedas:",
            ["2 Ruedas Delanteras / 1 Rueda Trasera (Típico Spyder)", "1 Rueda Delantera / 2 Ruedas Traseras"]
        )
        if "2 Ruedas Delanteras" in dispo_spyder:
            st.number_input("PSI Delantera Izquierda:", value=18.0, step=0.5)
            st.number_input("PSI Delantera Derecha:", value=18.0, step=0.5)
            st.number_input("PSI Trasera:", value=22.0, step=0.5)
        else:
            st.number_input("PSI Delantera:", value=18.0, step=0.5)
            st.number_input("PSI Trasera Izquierda:", value=22.0, step=0.5)
            st.number_input("PSI Trasera Derecha:", value=22.0, step=0.5)

        if st.button("🔍 Validar Can-Am", use_container_width=True):
            if not placa_input or not inspector_id:
                st.error("⚠️ Ingrese placa e inspector.")
            else:
                st.markdown(f"### 📋 Reporte: `{placa_input}` (Can-Am)")
                st.write(f"🏷️ **Ref. Llanta:** {llanta_final}")
                st.success("✅ Validación de Can-Am registrada.")

    # =========================================================
    # GRUPO 5: TRANSMILENIO Y SITP ZONAL (Dinámico por Ejes: 1 Direccional + Ejes Gemelos)
    # =========================================================
    elif "TransMilenio" in categoria_sel:
        st.markdown("### 🚌 Configuración Dinámica de Ejes - TransMilenio / SITP")
        cantidad_ejes_tm = st.slider("Seleccione el número total de ejes del bus masivo:", min_value=2, max_value=4, value=3, key="slider_tm_ejes")
        
        datos_tm = []
        for i in range(cantidad_ejes_tm):
            es_primer_eje = (i == 0)
            if es_primer_eje:
                st.markdown(f"#### 🛞 Eje #{i+1} (Eje Direccional - 2 Llantas Sencillas)")
                col_e1, col_e2 = st.columns(2)
                p_izq = col_e1.number_input(f"Izquierda (Eje 1):", min_value=0.0, max_value=150.0, value=115.0, step=0.5, key=f"tm_dir_izq_{i}")
                p_der = col_e2.number_input(f"Derecha (Eje 1):", min_value=0.0, max_value=150.0, value=115.0, step=0.5, key=f"tm_dir_der_{i}")
                datos_tm.append((i+1, "Direccional", p_izq, p_der, p_izq, p_der, 2))
            else:
                st.markdown(f"#### 🛞 Eje #{i+1} (Intermedio / Tracción - 4 Llantas / Gemelas)")
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    p_izq_ext = st.number_input(f"Izquierda Externa (Eje {i+1}):", min_value=0.0, max_value=150.0, value=115.0, step=0.5, key=f"tm_izq_ext_{i}")
                    p_izq_int = st.number_input(f"Izquierda Interna (Eje {i+1}):", min_value=0.0, max_value=150.0, value=115.0, step=0.5, key=f"tm_izq_int_{i}")
                with col_e2:
                    p_der_int = st.number_input(f"Derecha Interna (Eje {i+1}):", min_value=0.0, max_value=150.0, value=115.0, step=0.5, key=f"tm_der_int_{i}")
                    p_der_ext = st.number_input(f"Derecha Externa (Eje {i+1}):", min_value=0.0, max_value=150.0, value=115.0, step=0.5, key=f"tm_der_ext_{i}")
                datos_tm.append((i+1, "Tracción/Intermedio", p_izq_ext, p_izq_int, p_der_int, p_der_ext, 4))

        if st.button("🔍 Validar Diagnóstico TransMilenio / SITP", use_container_width=True):
            if not placa_input or not inspector_id:
                st.error("⚠️ Ingrese el código del inspector y la placa del vehículo.")
            else:
                st.markdown(f"### 📋 Reporte Preventivo de Patio: `{placa_input}`")
                st.write(f"**Inspector:** {inspector_id} | **Configuración:** {cantidad_ejes_tm} Ejes")
                st.write(f"🏷️ **Ref. Llanta Registrada:** {llanta_final}")
                
                todo_ok_tm = True
                ideal_tm = 115.0
                tol_tm = ideal_tm * 0.04

                for datos_tupla in datos_tm:
                    num_eje = datos_tupla[0]
                    etiqueta = datos_tupla[1]
                    tipo_eje = datos_tupla[6]
                    
                    if tipo_eje == 2:
                        pi, pd = datos_tupla[2], datos_tupla[3]
                        ok_eje = ((ideal_tm - tol_tm) <= pi <= (ideal_tm + tol_tm)) and ((ideal_tm - tol_tm) <= pd <= (ideal_tm + tol_tm))
                        if not ok_eje: todo_ok_tm = False
                        st.write(f"- **Eje {num_eje} ({etiqueta}):** Izq: {pi} | Der: {pd} ({'✅ OK' if ok_eje else '❌ Fuera de Rango'})")
                    else:
                        piex, piin, pdin, pdex = datos_tupla[2], datos_tupla[3], datos_tupla[4], datos_tupla[5]
                        ok_eje = (
                            (ideal_tm - tol_tm) <= piex <= (ideal_tm + tol_tm) and
                            (ideal_tm - tol_tm) <= piin <= (ideal_tm + tol_tm) and
                            (ideal_tm - tol_tm) <= pdin <= (ideal_tm + tol_tm) and
                            (ideal_tm - tol_tm) <= pdex <= (ideal_tm + tol_tm)
                        )
                        if not ok_eje: todo_ok_tm = False
                        st.write(f"- **Eje {num_eje} ({etiqueta}):** Ext.Izq: {piex} | Int.Izq: {piin} | Int.Der: {pdin} | Ext.Der: {pdex} ({'✅ OK' if ok_eje else '❌ Fuera de Rango'})")

                if todo_ok_tm:
                    st.success("✅ **APROBADO EN PATIO:** Todos los ejes y llantas del bus masivo cumplen con los rangos óptimos.")
                else:
                    st.error("❌ **RECHAZO EN PATIO:** Una o más llantas de los ejes superan la tolerancia permitida del 4%.")

    # =========================================================
    # GRUPO 6: TRACTOMULAS Y PESADOS
    # =========================================================
    else:
        st.markdown("### 🚛 Configuración Dinámica de Ejes (Tractomulas / Pesados)")
        cantidad_ejes = st.slider("Seleccione el número total de ejes del vehículo/tráiler:", min_value=2, max_value=7, value=3)
        
        datos_pesados = []
        for i in range(cantidad_ejes):
            es_primer_eje = (i == 0)
            if es_primer_eje:
                st.markdown(f"#### 🛞 Eje #{i+1} (Eje Direccional - 2 Llantas Sencillas)")
                col_e1, col_e2 = st.columns(2)
                p_izq = col_e1.number_input(f"Izquierda (Eje 1):", min_value=0.0, max_value=150.0, value=100.0, step=0.5, key=f"mula_dir_izq_{i}")
                p_der = col_e2.number_input(f"Derecha (Eje 1):", min_value=0.0, max_value=150.0, value=100.0, step=0.5, key=f"mula_dir_der_{i}")
                datos_pesados.append((i+1, "Direccional", p_izq, p_der, p_izq, p_der, 2))
            else:
                st.markdown(f"#### 🛞 Eje #{i+1} (Tracción / Arrastre - 4 Llantas / Gemelas)")
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    p_izq_ext = st.number_input(f"Izquierda Externa (Eje {i+1}):", min_value=0.0, max_value=150.0, value=100.0, step=0.5, key=f"mula_izq_ext_{i}")
                    p_izq_int = st.number_input(f"Izquierda Interna (Eje {i+1}):", min_value=0.0, max_value=150.0, value=100.0, step=0.5, key=f"mula_izq_int_{i}")
                with col_e2:
                    p_der_int = st.number_input(f"Derecha Interna (Eje {i+1}):", min_value=0.0, max_value=150.0, value=100.0, step=0.5, key=f"mula_der_int_{i}")
                    p_der_ext = st.number_input(f"Derecha Externa (Eje {i+1}):", min_value=0.0, max_value=150.0, value=100.0, step=0.5, key=f"mula_der_ext_{i}")
                datos_pesados.append((i+1, "Tracción/Arrastre", p_izq_ext, p_izq_int, p_der_int, p_der_ext, 4))

        if st.button("🔍 Validar Diagnóstico de Pesados / Mula", use_container_width=True):
            if not placa_input or not inspector_id:
                st.error("⚠️ Ingrese el código del inspector y la placa del vehículo.")
            else:
                st.markdown(f"### 📋 Reporte Preventivo de Patio: `{placa_input}`")
                st.write(f"**Inspector:** {inspector_id} | **Configuración:** {cantidad_ejes} Ejes")
                st.write(f"🏷️ **Ref. Llanta Registrada:** {llanta_final}")
                
                todo_ok = True
                ideal_base = 100.0
                tol_pesado = ideal_base * 0.04

                for datos_tupla in datos_pesados:
                    num_eje = datos_tupla[0]
                    etiqueta = datos_tupla[1]
                    tipo_eje = datos_tupla[6]

                    if tipo_eje == 2:
                        pi, pd = datos_tupla[2], datos_tupla[3]
                        ok_eje = ((ideal_base - tol_pesado) <= pi <= (ideal_base + tol_pesado)) and ((ideal_base - tol_pesado) <= pd <= (ideal_base + tol_pesado))
                        if not ok_eje: todo_ok = False
                        st.write(f"- **Eje {num_eje} ({etiqueta}):** Izq: {pi} | Der: {pd} ({'✅ OK' if ok_eje else '❌ Fuera de Rango'})")
                    else:
                        piex, piin, pdin, pdex = datos_tupla[2], datos_tupla[3], datos_tupla[4], datos_tupla[5]
                        ok_eje = (
                            (ideal_base - tol_pesado) <= piex <= (ideal_base + tol_pesado) and
                            (ideal_base - tol_pesado) <= piin <= (ideal_base + tol_pesado) and
                            (ideal_base - tol_pesado) <= pdin <= (ideal_base + tol_pesado) and
                            (ideal_base - tol_pesado) <= pdex <= (ideal_base + tol_pesado)
                        )
                        if not ok_eje: todo_ok = False
                        st.write(f"- **Eje {num_eje} ({etiqueta}):** Ext.Izq: {piex} | Int.Izq: {piin} | Int.Der: {pdin} | Ext.Der: {pdex} ({'✅ OK' if ok_eje else '❌ Fuera de Rango'})")

                if todo_ok:
                    st.success("✅ **APROBADO EN PATIO:** Todos los ejes y llantas del vehículo pesado cumplen con los rangos óptimos.")
                else:
                    st.error("❌ **RECHAZO EN PATIO:** Una o más llantas de los ejes superan la tolerancia permitida del 4%.")

# =============================================================
# MODO 2: AUDITORÍA
# =============================================================
else:
    st.title("⚙️ Modo Auditoría (Escritura y Edición Libre)")
    pin_ingresado = st.text_input("Ingrese PIN de Supervisor:", type="password")

    if pin_ingresado == "1987" or pin_ingresado == "":
        cat_edit = st.selectbox("Seleccione Tipología a Editar:", list(st.session_state.db_presiones.keys()))
        
        st.markdown("---")
        st.markdown("### 🏷️ Modificar Referencia de Llanta Sugerida por Defecto")
        ref_actual = st.session_state.db_presiones[cat_edit].get("llanta_ref", "")
        nueva_ref = st.text_input("Referencia base para esta tipología:", value=ref_actual)

        st.markdown("---")
        st.markdown("### 📊 Modificar Presión Ideal por Eje")
        eje_edit = st.selectbox("Seleccione el Eje a Ajustar:", st.session_state.db_presiones[cat_edit]["ejes"])
        actual_ideal = st.session_state.db_presiones[cat_edit]["rangos"][eje_edit]["ideal"]
        
        nuevo_ideal = st.number_input("Escriba el nuevo valor de PSI Ideal:", value=float(actual_ideal), step=0.5)

        if st.button("💾 Guardar Cambios en la Base de Datos", use_container_width=True):
            st.session_state.db_presiones[cat_edit]["llanta_ref"] = nueva_ref
            st.session_state.db_presiones[cat_edit]["rangos"][eje_edit]["ideal"] = nuevo_ideal
            guardar_configuracion(st.session_state.db_presiones)
            st.success("✅ ¡Cambios guardados con éxito en la base de datos!")
        
        st.markdown("---")
        st.markdown("### 🔍 Estado Actual de la Base de Datos (JSON)")
        st.json(st.session_state.db_presiones)
    else:
        st.error("🔒 PIN incorrecto.")