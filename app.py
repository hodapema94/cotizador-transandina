import streamlit as st
import pandas as pd
import plotly.express as px

from modules.rutas import (
    listar_rutas,
    obtener_ruta,
    calcular_costo_ruta
)

from modules.cotizador import calcular_cotizacion

from modules.funciones_matematicas import (
    costo_total,
    ingreso_total,
    utilidad_total,
    puntos_equilibrio,
    maximizar_utilidad
)


# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="TransAndina | Sistema de Cotización",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# ESTILOS VISUALES
# =====================================================

st.markdown("""
<style>

    .stApp {
        background-color: #F4F7FA;
    }

    [data-testid="stSidebar"] {
        background-color: #102A43;
    }

   /* Opciones del menú de navegación */
    [data-testid="stSidebar"] [role="radiogroup"] label,
    [data-testid="stSidebar"] [role="radiogroup"] label p,
    [data-testid="stSidebar"] [role="radiogroup"] label span,
    [data-testid="stSidebar"] [role="radiogroup"] label div {
    color: #FFFFFF !important;
    opacity: 1 !important;
    }

    /* Fondo de la opción seleccionada */
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background-color: #147D64 !important;
    border-radius: 8px !important;
    }

    /* Texto de la opción seleccionada */
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p,
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) span {
    color: #FFFFFF !important;
    font-weight: 700 !important;}
    
    .main-title {
        color: #102A43;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #627D98;
        font-size: 16px;
        margin-top: 5px;
    }

    .section-title {
    color: #102A43 !important;
    font-weight: 800;
    font-size: 28px;
    margin-bottom: 5px;}

    h3, h4, h5 {
    color: #102A43 !important;
    font-weight: 700;
    }

    /* Textos descriptivos y secundarios */
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stText"] {
        color: #334E68 !important;
        font-size: 14px;}

    /* Etiquetas de formularios */
    .stApp label,
    .stApp [data-testid="stWidgetLabel"] {
        color: #102A43 !important;
        font-weight: 600;
        }

    /* Texto de ayuda */
    .stApp small {
        color: #486581 !important;
        }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #D9E2EC;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(16, 42, 67, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #627D98;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #102A43;
        font-weight: 800;
    }

    div.stButton > button {
        background-color: #147D64;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 700;
        padding: 10px;
    }

    div.stButton > button:hover {
        background-color: #0E6652;
        color: white;
    }

    /* Tarjetas de información del proyecto */
    .info-card {
        background-color: #FFFFFF !important;
        color: #102A43 !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #D9E2EC;
        margin-bottom: 12px;
    }

    /* Títulos y textos dentro de las tarjetas */
        .info-card h1,
        .info-card h2,
        .info-card h3,
        .info-card h4,
        .info-card p,
        .info-card strong,
        .info-card span,
        .info-card li {
            color: #102A43 !important;
            font-weight: 600;}

    .footer {
        text-align: center;
        color: #829AB1;
        font-size: 13px;
        padding: 15px;
    }
    /* =================================
      TEXTOS INSTITUCIONALES DEL MENÚ
    ================================= */

    /* Título principal del menú */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Encabezados y textos escritos con Markdown */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #FFFFFF !important;
    }

    /* Etiquetas de navegación */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Textos secundarios y versión */
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
  
    /* =================================
     ALERTAS DE COTIZACIÓN
    ================================= */

    /* Fondo verde para mensaje de éxito */
    [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) {
        background-color: #147D64 !important;
        border: 1px solid #0E6652 !important;
    }

    /* Fondo azul para mensaje informativo */
    [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
        background-color: #102A43 !important;
        border: 1px solid #243B53 !important;
    }

    /* Texto blanco en ambas alertas */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* Contenedores de información y mensajes personalizados */
        .stApp [data-testid="stMarkdownContainer"] .info-card p,
        .stApp [data-testid="stMarkdownContainer"] .info-card span {
            color: #FFFFFF !important;
        }

    /* Texto de los mensajes de éxito e información */
    .stApp [data-testid="stAlertContentSuccess"],
    .stApp [data-testid="stAlertContentInfo"],
    .stApp [data-testid="stAlertContentSuccess"] *,
    .stApp [data-testid="stAlertContentInfo"] * {
        color: #FFFFFF !important;
    }

    
</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def formato_pesos(valor):
    """Convierte un número a formato monetario colombiano."""
    return f"${valor:,.2f}"


def cargar_informacion_rutas():
    return listar_rutas()


def mostrar_encabezado(titulo, descripcion):
    st.markdown(
        f'<h2 class="section-title">{titulo}</h2>',
        unsafe_allow_html=True
    )
    st.caption(descripcion)


# =====================================================
# ENCABEZADO PRINCIPAL
# =====================================================

st.markdown(
    '<p class="main-title">🚛 TRANSANDINA CARGA S.A.S.</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Sistema inteligente de cotización de transporte de carga</p>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# MENÚ PRINCIPAL
# =====================================================

st.sidebar.markdown("## TRANSANDINA")
st.sidebar.caption("SISTEMA DE GESTIÓN DE FLETES")

st.sidebar.divider()

seccion = st.sidebar.radio(
    "NAVEGACIÓN",
    [
        "Cotizador",
        "Análisis matemático",
        "Rutas disponibles",
        "Información del proyecto"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Versión académica 1.0")
st.sidebar.caption("Desarrollado en Python y Streamlit")


# =====================================================
# SECCIÓN 1: COTIZADOR
# =====================================================

if seccion == "Cotizador":

    mostrar_encabezado(
        "Generar cotización",
        "Calcula una tarifa de transporte a partir de los costos estimados del recorrido."
    )

    try:

        rutas = cargar_informacion_rutas()

        if rutas.empty:
            st.warning("No existen rutas registradas.")
            st.stop()

        opciones_rutas = rutas["id_ruta"].tolist()

        nombres_rutas = {
            fila["id_ruta"]: (
                f"{fila['origen']} → {fila['destino']}"
            )
            for _, fila in rutas.iterrows()
        }

        st.markdown("#### Parámetros de cotización")

        col1, col2 = st.columns(2)

        with col1:
            id_ruta = st.selectbox(
                "Ruta de transporte",
                options=opciones_rutas,
                format_func=lambda x: nombres_rutas[x]
            )

        with col2:
            margen = st.number_input(
                "Margen comercial (%)",
                min_value=0.0,
                max_value=200.0,
                value=20.0,
                step=1.0
            )

        st.write("")

        if st.button(
            "CALCULAR TARIFA",
            type="primary",
            use_container_width=True
        ):

            resultado = calcular_cotizacion(
                int(id_ruta),
                margen
            )

            st.markdown("""
            <div style="
                background-color: #147D64;
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-weight: 600;
                margin-bottom: 15px;
            ">
                ✓ La cotización fue calculada correctamente.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Información del recorrido")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Origen",
                resultado["origen"]
            )

            col2.metric(
                "Destino",
                resultado["destino"]
            )

            col3.metric(
                "Distancia total",
                f"{resultado['distancia_km']:,.2f} km"
            )

            st.divider()

            st.markdown("#### Desglose de costos")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Costo operativo",
                    formato_pesos(resultado["costo_operativo"])
                )

                st.metric(
                    "Margen comercial",
                    f"{resultado['margen_porcentaje']:.2f}%"
                )

            with col2:
                st.metric(
                    "Costo por regla del trapecio",
                    formato_pesos(resultado["metodo_referencia"])
                )

                st.metric(
                    "Valor del margen",
                    formato_pesos(resultado["valor_margen"])
                )

            st.divider()

            st.markdown("#### Resultado de la cotización")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "TARIFA COMERCIAL SUGERIDA",
                    formato_pesos(resultado["tarifa_sugerida"])
                )

            with col2:
                st.metric(
                    "UTILIDAD ESTIMADA",
                    formato_pesos(resultado["utilidad"])
                )

            st.markdown("""
            <div style="
                background-color: #102A43;
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-weight: 500;
                line-height: 1.6;
                margin-top: 15px;
            ">
                La tarifa sugerida se obtiene aplicando el margen comercial
                sobre el costo operativo calculado mediante la regla de Simpson 1/3.
            </div>
            """, unsafe_allow_html=True)

    except Exception as error:
        st.error(f"No fue posible generar la cotización: {error}")


# =====================================================
# SECCIÓN 2: ANÁLISIS MATEMÁTICO
# =====================================================

elif seccion == "Análisis matemático":

    mostrar_encabezado(
        "Análisis financiero y matemático",
        "Evalúa el comportamiento de los costos, ingresos y utilidades de la empresa."
    )

    cantidad_viajes = st.slider(
        "Selecciona la cantidad de viajes mensuales",
        min_value=0,
        max_value=150,
        value=65
    )

    costo = costo_total(cantidad_viajes)
    ingreso = ingreso_total(cantidad_viajes)
    utilidad = utilidad_total(cantidad_viajes)

    st.markdown("#### Indicadores financieros")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Costo total",
        f"${costo:,.2f} millones"
    )

    col2.metric(
        "Ingresos totales",
        f"${ingreso:,.2f} millones"
    )

    col3.metric(
        "Utilidad",
        f"${utilidad:,.2f} millones"
    )

    st.caption(
        "Los valores de este análisis están expresados en millones de pesos."
    )

    st.divider()

    cantidades = list(range(0, 151))

    datos = pd.DataFrame({
        "Viajes": cantidades,
        "Costos": [costo_total(q) for q in cantidades],
        "Ingresos": [ingreso_total(q) for q in cantidades],
        "Utilidad": [utilidad_total(q) for q in cantidades]
    })

    st.markdown("#### Comportamiento de costos e ingresos")

    grafica = px.line(
        datos,
        x="Viajes",
        y=["Costos", "Ingresos"],
        labels={
            "value": "Millones de pesos",
            "variable": "Concepto",
            "Viajes": "Cantidad de viajes mensuales"
        },
        title="Comparación de costos e ingresos",
        template="plotly_white",
        color_discrete_sequence=["#E67E22", "#147D64"]
    )

    grafica.update_layout(
        legend_title="Indicador",
        hovermode="x unified"
    )

    st.plotly_chart(
        grafica,
        use_container_width=True
    )

    st.markdown("#### Comportamiento de la utilidad")

    grafica_utilidad = px.line(
        datos,
        x="Viajes",
        y="Utilidad",
        labels={
            "Utilidad": "Millones de pesos",
            "Viajes": "Cantidad de viajes mensuales"
        },
        title="Utilidad según cantidad de viajes",
        template="plotly_white",
        color_discrete_sequence=["#2563EB"]
    )

    grafica_utilidad.add_hline(
        y=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Punto de utilidad cero"
    )

    grafica_utilidad.add_vline(
        x=cantidad_viajes,
        line_dash="dot",
        line_color="#64748B",
        annotation_text=f"{cantidad_viajes} viajes"
    )

    st.plotly_chart(
        grafica_utilidad,
        use_container_width=True
    )

    st.divider()

    st.markdown("#### Puntos de equilibrio")

    equilibrios = puntos_equilibrio()

    col1, col2 = st.columns(2)

    for numero, punto in enumerate(equilibrios):

        if numero == 0:
            col1.metric(
                "Primer punto de equilibrio",
                f"{punto:.2f} viajes"
            )
        elif numero == 1:
            col2.metric(
                "Segundo punto de equilibrio",
                f"{punto:.2f} viajes"
            )

    st.caption(
        "En los puntos de equilibrio, los ingresos son iguales a los costos "
        "y la utilidad es cero."
    )

    st.divider()

    st.markdown("#### Optimización de la utilidad")

    optimizacion = maximizar_utilidad()

    col1, col2 = st.columns(2)

    col1.metric(
        "Máximo matemático aproximado",
        f"{optimizacion['viajes_optimos']:.2f} viajes"
    )

    col2.metric(
        "Utilidad máxima",
        f"${optimizacion['utilidad_maxima']:,.4f} millones"
    )

    st.markdown(
        f"""
        <div style="
            background-color: #147D64;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 15px;
            margin-bottom: 15px;
        ">
            ✓ Para una operación con viajes enteros, el modelo recomienda
            {optimizacion['viajes_enteros']} viajes mensuales.
        </div>
        """,
        unsafe_allow_html=True
)


# =====================================================
# SECCIÓN 3: RUTAS DISPONIBLES
# =====================================================

elif seccion == "Rutas disponibles":

    mostrar_encabezado(
        "Administración de rutas",
        "Consulta los recorridos registrados y sus costos estimados."
    )

    try:

        rutas = listar_rutas()

        if rutas.empty:
            st.warning("No existen rutas registradas.")
            st.stop()

        st.markdown("#### Recorridos registrados")

        st.dataframe(
            rutas,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.markdown("#### Detalle del recorrido")

        id_ruta = st.selectbox(
            "Selecciona una ruta",
            options=rutas["id_ruta"].tolist(),
            format_func=lambda x: (
                f"{rutas.loc[rutas['id_ruta'] == x, 'origen'].iloc[0]} "
                f"→ "
                f"{rutas.loc[rutas['id_ruta'] == x, 'destino'].iloc[0]}"
            ),
            key="ruta_detalle"
        )

        detalle = obtener_ruta(int(id_ruta))

        st.dataframe(
            detalle,
            use_container_width=True,
            hide_index=True
        )

        resultado = calcular_costo_ruta(int(id_ruta))

        col1, col2 = st.columns(2)

        col1.metric(
            "Costo estimado por Simpson",
            formato_pesos(resultado["costo_simpson"])
        )

        col2.metric(
            "Costo estimado por trapecio",
            formato_pesos(resultado["costo_trapecio"])
        )

    except Exception as error:
        st.error(f"No fue posible consultar las rutas: {error}")


# =====================================================
# SECCIÓN 4: INFORMACIÓN DEL PROYECTO
# =====================================================


elif seccion == "Información del proyecto":

    mostrar_encabezado(
        "Acerca del sistema",
        "Información general sobre el desarrollo y los fundamentos matemáticos."
    )

    # Información general del proyecto
    st.markdown(
        """
        <div style="
            background-color: #FFFFFF;
            color: #102A43;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #D9E2EC;
            margin-bottom: 15px;
        ">
            <h3 style="color: #102A43; font-weight: 800; margin-top: 0;">
                ¿Qué es TransAndina Carga S.A.S.?
            </h3>
            <p style="color: #334E68; font-size: 15px; line-height: 1.7;">
                Este proyecto consiste en desarrollar una herramienta informática
                que permita estimar tarifas de transporte de carga por carretera,
                utilizando métodos numéricos y modelos matemáticos.
            </p>
            <p style="color: #334E68; font-size: 15px; line-height: 1.7; margin-bottom: 0;">
                Su propósito es aplicar conceptos de cálculo integral y diferencial
                para apoyar el análisis de costos, ingresos y rentabilidad.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Métodos matemáticos utilizados
    st.markdown("#### Métodos matemáticos utilizados")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="
                background-color: #FFFFFF;
                color: #102A43;
                padding: 22px;
                border-radius: 12px;
                border: 1px solid #D9E2EC;
                margin-bottom: 12px;
            ">
                <h4 style="color: #102A43;">1. Regla de Simpson 1/3</h4>
                <p style="color: #334E68; line-height: 1.6;">
                    Aproxima el costo total del recorrido mediante integración numérica.
                </p>
                <h4 style="color: #102A43;">2. Regla del trapecio</h4>
                <p style="color: #334E68; line-height: 1.6;">
                    Calcula una segunda aproximación para comparar los resultados.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="
                background-color: #FFFFFF;
                color: #102A43;
                padding: 22px;
                border-radius: 12px;
                border: 1px solid #D9E2EC;
                margin-bottom: 12px;
            ">
                <h4 style="color: #102A43;">3. Cálculo diferencial</h4>
                <p style="color: #334E68; line-height: 1.6;">
                    Permite analizar costos, ingresos y utilidades marginales.
                </p>
                <h4 style="color: #102A43;">4. Optimización</h4>
                <p style="color: #334E68; line-height: 1.6;">
                    Identifica la cantidad de viajes que maximiza la utilidad mensual.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Tecnologías utilizadas
    st.markdown("#### Tecnologías utilizadas")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Lenguaje", "Python")
    col2.metric("Interfaz", "Streamlit")
    col3.metric("Datos", "Pandas")
    col4.metric("Cálculo", "NumPy")
    col5.metric("Gráficas", "Plotly")

    st.divider()

    # Objetivo del proyecto
    st.markdown("#### Objetivo del proyecto")

    st.markdown(
        """
        <div style="
            background-color: #FFFFFF;
            color: #334E68;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #D9E2EC;
            font-size: 15px;
            line-height: 1.7;
        ">
            Demostrar cómo los conceptos matemáticos pueden convertirse
            en soluciones informáticas que apoyen la toma de decisiones
            en una empresa de transporte de carga.
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.divider()

st.markdown(
    '<p class="footer">TRANSANDINA CARGA S.A.S. | '
    'Sistema de cotización de transporte | Proyecto académico</p>',
    unsafe_allow_html=True
)