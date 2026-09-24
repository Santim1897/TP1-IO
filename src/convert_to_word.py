import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_table(table, header_bg="1F4E79", zebra=True):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell in table.rows[0].cells:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, 100, 100, 120, 120)
    for r_idx, row in enumerate(table.rows[1:], start=1):
        for cell in row.cells:
            cell.paragraphs[0].runs[0].font.size = Pt(9.0)
            if zebra and r_idx % 2 == 1:
                set_cell_background(cell, "F2F5F9")
            set_cell_margins(cell, 60, 60, 100, 100)

def create_complete_word_doc(docx_path="INFORME_EJECUTIVO_AUTOITBA.docx"):
    doc = docx.Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    COLOR_PRIMARY = RGBColor(31, 78, 121)     # ITBA Navy Blue
    COLOR_SECONDARY = RGBColor(47, 85, 151)   # Slate Blue
    COLOR_DARK = RGBColor(38, 38, 38)
    COLOR_MUTED = RGBColor(89, 89, 89)
    
    # -------------------------------------------------------------
    # PORTADA
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("INSTITUTO TECNOLÓGICO DE BUENOS AIRES (ITBA)")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_SECONDARY
    
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("Departamento de Ingeniería Industrial — 11.51 / IO51 Investigación de Operaciones")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = COLOR_MUTED
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(24)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("TRABAJO PRÁCTICO N° 1 COMPLEMENTARIO\nPlan de Producción Estratégico — AutoITBA S.A.")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(28)
    r_sub = p_sub.add_run("Optimización Matemática (MILP), Procedimientos de Código Paso a Paso y Verificación de Respuestas")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_DARK
    
    # Metadata Table
    table_meta = doc.add_table(rows=5, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Materia:", "11.51 / IO51 - Investigación Operativa (2° Cuatrimestre 2026)"),
        ("Terminal Automotriz:", "AutoITBA S.A. (Planta Zárate, Buenos Aires)"),
        ("Horizonte de Evaluación:", "5 Años (Año 1 a Año 5 / 2026 - 2030)"),
        ("Herramientas:", "Python 3.12, PuLP (Solver CBC / Branch & Bound), Pandas, OpenPyXL"),
        ("Repositorio Oficial:", "https://github.com/Santim1897/TP1-IO")
    ]
    for idx, (k, v) in enumerate(meta):
        row = table_meta.rows[idx]
        row.cells[0].text = k
        row.cells[1].text = v
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.color.rgb = COLOR_PRIMARY
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = COLOR_DARK
        set_cell_background(row.cells[0], "F2F2F2")
        set_cell_background(row.cells[1], "FAFAFA")
        set_cell_margins(row.cells[0], 60, 60, 100, 100)
        set_cell_margins(row.cells[1], 60, 60, 100, 100)
        
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # RESUMEN EJECUTIVO Y TABLA DE CONSIGNAS
    # -------------------------------------------------------------
    h1 = doc.add_heading("Resumen Ejecutivo y Cuadro de Respuestas a las Consignas", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "Se formuló y resolvió un modelo de Programación Lineal Entera Mixta (MILP) multiperíodo para optimizar las operaciones "
        "de AutoITBA S.A. a lo largo de un horizonte de 5 años. El modelo decide de forma simultánea los volúmenes a producir por línea y turno, "
        "la activación de turnos mediante variables binarias, el inventario interanual en playón y el despacho a los distintos canales de venta "
        "(mercado interno, exportaciones MERCOSUR y contratos especiales). El objetivo es maximizar la Utilidad Neta Total consolidada en dólares (USD)."
    )
    
    table_sum = doc.add_table(rows=8, cols=4)
    sum_headers = ["Consigna", "Planteo Central", "Resultado Cuantitativo", "Decisión Recomendada"]
    for i, h in enumerate(sum_headers):
        table_sum.rows[0].cells[i].text = h
    sum_data = [
        ("1. Plan Óptimo Base", "Producción, turnos y cobertura a 5 años", "Utilidad: USD 1.993,49 M (Inv = 0)", "Línea A Mañana; Línea B Mañana y Tarde. 100% demanda cubierta."),
        ("2. Devaluación", "Impacto de tipo de cambio acelerado", "Utilidad: USD 3.910,05 M (+96,1%)", "Costos en pesos se licúan en USD. Turno tarde en Línea B es indispensable."),
        ("3. Reequipamiento", "Inversión USD 12M-18M para pick-ups en Línea A", "Base: Inviable (-USD 16M a -31M)\nBoom (+20%): +USD 33M a +39M", "No reequipar en demanda normal. Con Boom Agropecuario, hacer la obra en Año 1."),
        ("4. Importación China", "Reemplazo de livianos locales desde Año 2", "Base: +USD 109,7 M\nDevaluación: -USD 115,7 M\nCierre Año 3: -USD 69,1 M", "No desmantelar la planta local. Riesgo regulatorio y cambiario extremo."),
        ("5. Contrato Autonomy", "1.000 LB anuales a USD 27.500 fijo", "Costo oportunidad: +USD 5,17 M\nPrecio indiferencia: USD 28.534/u", "A USD 27.500 da pérdida en Años 3-5. Renegociar a > USD 28.550 o liberar capacidad."),
        ("6. Costo de Playón", "Sensibilidad al costo de inventario (25%-30%)", "Inv = 0 a 25% y 30%\nCorte analítico: 8,8% anual", "Operar Just-in-Time. Guardar stock solo conviene si la tasa fuera inferior al 8,8%."),
        ("7. Estrategia Directiva", "Robustez vs contingencia (Minimax Regret)", "Arrepentimiento S1: USD 109,7 M\nArrepentimiento S3: USD 115,7 M", "Fabricación Local Flexible: No asumir compromisos irreversibles en Años 1 y 2.")
    ]
    for r_idx, row_data in enumerate(sum_data, start=1):
        for c_idx, val in enumerate(row_data):
            table_sum.rows[r_idx].cells[c_idx].text = val
    format_table(table_sum)

    doc.add_page_break()
    
    # -------------------------------------------------------------
    # SECCIÓN 1: FORMULACIÓN FORMAL DEL MODELO (MILP)
    # -------------------------------------------------------------
    h_sec1 = doc.add_heading("Sección 1: Formulación Formal del Modelo (MILP)", level=1)
    h_sec1.runs[0].font.color.rgb = COLOR_PRIMARY
    
    # Supuestos
    doc.add_heading("a.i) Supuestos Más Importantes", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    sup = [
        "Unidad Monetaria Homogénea (USD sin descontar): El precio de venta se percibe en dólares y la función objetivo consolida todos los flujos en USD sin aplicar tasa de descuento intertemporal.",
        "Indexación y Conversión de Costos en Pesos: Los costos operativos en Zárate se indexan anualmente al ritmo de la inflación proyectada del 20% anual: FactorInflacion(t) = (1.20)^(t-1), y se convierten a dólares dividiendo por el tipo de cambio oficial del año t.",
        "Flexibilidad y Ratio de Sustitución en Línea B (Ratio 1,2): La Línea B puede ensamblar 30.000 livianos o 25.000 pick-ups por turno mañana. Cada pick-up equivale a 1,20 livianos de absorción de capacidad (30.000 / 25.000 = 1,20).",
        "Capacidad y Precedencia del Turno Tarde: El turno tarde opera al 75% del turno mañana. No se puede activar el turno tarde sin tener previamente encendido el turno mañana en esa misma línea (yA <= wA, yB <= wB).",
        "Regla Sindical de Peligrosidad (Operarios Compartidos): Si al menos una línea opera el turno tarde, se incorporan 5 operarios adicionales comunes en detalles finales. Su costo se abona una sola vez en el año si hay turno tarde en planta.",
        "Balance de Inventario y Costo de Playón: El inventario inicial en Año 1 es cero. Mantener un vehículo en playón de un año a otro devenga un costo del 25% de su costo variable de fabricación en dicho año.",
        "Diferencial de Exportación (+5% MERCOSUR): Las pick-ups exportadas perciben un sobreprecio del 5% sobre el precio de lista local por flete, seguro y prima regional."
    ]
    for s in sup:
        doc.add_paragraph(s, style='List Bullet')

    # Variables
    doc.add_heading("a.ii) Definición Formal de Variables de Decisión", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    table_var = doc.add_table(rows=8, cols=4)
    v_headers = ["Variable", "Dominio", "Cantidad", "Descripción y Rol Económico"]
    for i, h in enumerate(v_headers):
        table_var.rows[0].cells[i].text = h
    v_rows = [
        ("X(v, l, s, t)", "Real >= 0", "70", "Unidades del vehículo v ensambladas en línea l, turno s, año t."),
        ("sLoc(v, t)", "Real >= 0", "25", "Unidades del modelo v vendidas en el mercado interno en el año t."),
        ("sExp(v, t)", "Real >= 0", "15", "Unidades de pick-ups exportadas al MERCOSUR en el año t."),
        ("I(v, t)", "Real >= 0", "25", "Inventario en playón del modelo v al cierre del año t (I(v, 0) = 0)."),
        ("wA(t), wB(t)", "Binaria {0, 1}", "10", "Vale 1 si se activa el Turno Mañana de la Línea A / B en el año t."),
        ("yA(t), yB(t)", "Binaria {0, 1}", "10", "Vale 1 si se activa el Turno Tarde de la Línea A / B en el año t."),
        ("z(t)", "Binaria {0, 1}", "5", "Vale 1 si al menos una línea opera el Turno Tarde (activa los 5 operarios extra).")
    ]
    for r_idx, r_data in enumerate(v_rows, start=1):
        for c_idx, val in enumerate(r_data):
            table_var.rows[r_idx].cells[c_idx].text = val
    format_table(table_var)

    # Parámetros
    doc.add_heading("a.iii) Parámetros del Modelo", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    table_par = doc.add_table(rows=13, cols=6)
    p_headers = ["Parámetro / Concepto", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
    for i, h in enumerate(p_headers):
        table_par.rows[0].cells[i].text = h
    p_rows = [
        ("Inflación acumulada (20% a.a.)", "1,0000", "1,2000", "1,4400", "1,7280", "2,0736"),
        ("Tipo de Cambio Base (ARS/USD)", "1.500", "1.750", "1.950", "2.350", "2.800"),
        ("Tipo de Cambio Devaluación (ARS/USD)", "1.500", "2.200", "2.650", "3.100", "3.550"),
        ("Sueldo anual por operario (ARS)", "$26.000.000", "$31.200.000", "$37.440.000", "$44.928.000", "$53.913.600"),
        ("Encendido Línea A (USD Base)", "$333.333", "$342.857", "$369.231", "$367.660", "$370.286"),
        ("Encendido Línea B (USD Base)", "$533.333", "$548.571", "$590.769", "$588.255", "$592.457"),
        ("CV Unitario LB (USD Base)", "$26.667", "$27.429", "$29.538", "$29.413", "$29.623"),
        ("CV Unitario LP (USD Base)", "$28.800", "$29.623", "$31.902", "$31.766", "$31.993"),
        ("CV Unitario PB (USD Base)", "$38.333", "$39.429", "$42.462", "$42.281", "$42.583"),
        ("CV Unitario PM (USD Base)", "$39.483", "$40.611", "$43.735", "$43.549", "$43.860"),
        ("CV Unitario PP (USD Base)", "$40.633", "$41.794", "$45.009", "$44.818", "$45.138"),
        ("Precios de Lista Local (USD)", "LB: 30.000", "LP: 35.000", "PB: 45.000", "PM: 50.000", "PP: 57.500")
    ]
    for r_idx, r_data in enumerate(p_rows, start=1):
        for c_idx, val in enumerate(r_data):
            table_par.rows[r_idx].cells[c_idx].text = val
    format_table(table_par)

    # Restricciones
    doc.add_heading("a.iv) Restricciones Formales (135 Ecuaciones)", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    restricciones = [
        ("R1. Precedencia de Turnos (10 ec.):", "yA(t) <= wA(t)  y  yB(t) <= wB(t) (no se puede activar el turno tarde sin la mañana)."),
        ("R2. Lógica de Peligrosidad (15 ec.):", "z(t) >= yA(t), z(t) >= yB(t), z(t) <= yA(t) + yB(t) (dispara los 5 operarios de peligrosidad si hay tarde)."),
        ("R3. Capacidad Línea A (10 ec.):", "∑ X(v, A, M, t) <= 10.000·wA(t)  y  ∑ X(v, A, T, t) <= 7.500·yA(t). X(pickups, A) = 0."),
        ("R4. Capacidad Mixta Línea B (10 ec.):", "[ ∑ X_liv / 30.000 + ∑ X_pick / 25.000 ] <= 1.0·wB(t) (Mañana) y <= 0.75·yB(t) (Tarde). Ratio 1.2."),
        ("R5. Balance de Masa / Inventario (25 ec.):", "I(v, t-1) + ∑ X(v, l, s, t) = sLoc(v, t) + sExp(v, t) + Autonomy(v, t) + I(v, t)."),
        ("R6. Cotas de Demanda y Contratos (40 ec.):", "sLoc <= DemandaLocal(t); sExp <= DemandaExport; Autonomy = 1.000 LB anuales.")
    ]
    for name, desc in restricciones:
        p = doc.add_paragraph()
        r = p.add_run(name + " ")
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        p.add_run(desc)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECCIÓN C: REPRESENTACIÓN GRÁFICA DEL PROCESO
    # -------------------------------------------------------------
    h_c = doc.add_heading("c) Representación Gráfica del Proceso Productivo", level=1)
    h_c.runs[0].font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "A continuación se presenta el diagrama esquemático de la planta industrial de AutoITBA S.A. en Zárate, "
        "mostrando las cuatro secciones consecutivas (Chasis, Pintura, Motor y Detalles Finales), las dotaciones de operarios, "
        "la regla sindical de turno tarde y el flujo hacia el playón de despacho:"
    )
    plot_proc = os.path.join("plots", "fig0_proceso_planta.png")
    if os.path.exists(plot_proc):
        doc.add_picture(plot_proc, width=Inches(6.5))
        p_cap = doc.add_paragraph("Figura 1: Diagrama de Flujo del Proceso Productivo y Asignación Laboral por Línea y Turno.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECCIÓN 2: DESARROLLO ANALÍTICO Y PROCEDIMIENTOS UTILIZADOS
    # -------------------------------------------------------------
    h_sec2 = doc.add_heading("Sección 2: Procedimientos de Código Paso a Paso y Verificación de Respuestas", level=1)
    h_sec2.runs[0].font.color.rgb = COLOR_PRIMARY

    # CONSIGNA 1
    doc.add_heading("CONSIGNA 1: El Modelo Base a 5 Años", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Determinar la estrategia óptima para los próximos 5 años bajo las condiciones esperadas (\"Escenario Base\"):\n"
        "• ¿Qué turnos nos conviene prender en cada línea cada año?\n"
        "• ¿Cuántas unidades fabricar de cada modelo?\n"
        "• ¿Nos conviene fabricar de más y guardar autos en el playón (stock) para el año siguiente, o fabricar justo lo que se vende?"
    )
    
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "El script principal llama a la función solve_model(scenario='base') dentro de model_engine.py. Esto es lo que hace paso a paso:\n\n"
        "1. La conversión de monedas (Pesos a Dólares):\n"
        "   • Los precios de venta están fijados en dólares (USD).\n"
        "   • Pero los sueldos, el costo de encender las máquinas y los insumos locales están en pesos argentinos (ARS) y aumentan un 20% anual por inflación.\n"
        "   • El código hace un bucle año por año (for t in years) y calcula cuánto representa cada costo en dólares dividiendo por el dólar oficial de ese año (1.500, 1.750, 1.950, 2.350 y 2.800).\n\n"
        "2. Las 'palancas' que el modelo puede mover (Variables de Decisión):\n"
        "   • Variables binarias (Y y W_tarde): Son como llaves de luz (valen 1 o 0).\n"
        "     - Y: ¿Prendemos la Línea A a la mañana? ¿A la tarde? ¿Y la Línea B?\n"
        "     - W_tarde: Si alguna línea abre a la tarde, el sindicato exige contratar 5 operarios extra de peligrosidad. Esta variable se prende en 1 automáticamente si alguna línea trabaja a la tarde.\n"
        "   • Variables continuas (X, S, I):\n"
        "     - X: Cuántos autos fabricar de cada modelo en cada turno y línea.\n"
        "     - S: Cuánto vender en el mercado local, cuánto exportar y cuánto entregar a contratos especiales (Autonomy y Agronegocios).\n"
        "     - I: Cuántos autos quedan guardados en el playón al final de cada año.\n\n"
        "3. Los bucles de restricciones (Las reglas que no se pueden romper):\n"
        "   • Bucle de Balance de Inventario: Por cada año y por cada modelo, asegura que:\n"
        "     Lo que tenía del año pasado + Lo que fabriqué hoy = Lo que vendo hoy + Lo que me sobra\n"
        "   • Bucle de Capacidad de Máquinas: La Línea A no puede superar 10.000 autos a la mañana ni 7.500 a la tarde. Para la Línea B se aplica la regla de que 1 pick-up equivale a 1,2 livianos de espacio en la cinta.\n"
        "   • Bucle de Jerarquía de Turnos: No se permite abrir la tarde si la mañana de esa misma línea está apagada.\n"
        "   • Bucle de Demanda: No podés vender más autos de los que los clientes quieren comprar.\n\n"
        "4. La Función Objetivo (El criterio de éxito):\n"
        "   • El código le dice al solver: \"Maximizá la suma de todos los ingresos por ventas menos todos los costos (insumos, sueldos, encendido de líneas y costo de playón)\"."
    )
    
    doc.add_heading("3. ¿Qué resultado arroja y qué significa?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Ganancia total acumulada a 5 años: USD 1.993,49 Millones (o USD 1.916,30 M sin agronegocios).\n"
        "• Línea A (Livianos): Trabaja solo en Turno Mañana. Nunca hace falta prender el turno tarde porque la demanda de livianos es chica y la mañana alcanza de sobra.\n"
        "• Línea B (Pick-ups): Trabaja a doble turno pleno (Mañana y Tarde) todos los 5 años. Las pick-ups dejan mucho más margen de ganancia, por lo que conviene explotar la línea al máximo.\n"
        "• Inventario (Playón): Da cero (0 unidades) en todos los años. Tener autos parados en el playón cuesta un 25% anual de su valor, lo cual es carísimo; el modelo concluye que lo más inteligente es una producción Just-in-Time (fabricar y despachar en el mismo año)."
    )
    
    plot_mix = os.path.join("plots", "fig2_mix_produccion_base.png")
    if os.path.exists(plot_mix):
        doc.add_picture(plot_mix, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 2: Mix de Producción Anual por Modelo a lo largo de los 5 Años (Escenario Base).")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # CONSIGNA 2
    doc.add_heading("CONSIGNA 2: Evaluación de Devaluación Acelerada", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Evaluar qué le pasa a la empresa si la economía argentina sufre una devaluación más fuerte de lo previsto "
        "(el dólar pasa de $1.500 en el Año 1 a $3.550 en el Año 5, en vez de los $2.800 del caso base). Las preguntas centrales de la cátedra son:\n"
        "1. ¿Aumenta o disminuye la ganancia neta?\n"
        "2. ¿Cambia la conveniencia de activar el turno tarde?\n"
        "3. ¿Cambia la proporción de autos que vendemos en Argentina versus lo que exportamos al MERCOSUR?"
    )
    
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "En run_experiments.py:\n"
        "1. Reutiliza el mismo motor: Llama a model.solve_model(scenario='devaluacion').\n"
        "2. Cambia el vector de Tipo de Cambio: En lugar de dividir los costos en pesos por el sendero base, usa el sendero devaluado:\n"
        "   • Año 1: $1.500\n"
        "   • Año 2: $2.200 (en vez de $1.750)\n"
        "   • Año 3: $2.650 (en vez de $1.950)\n"
        "   • Año 4: $3.100 (en vez de $2.350)\n"
        "   • Año 5: $3.550 (en vez de $2.800)\n"
        "3. El efecto matemático: Como los ingresos de la empresa están en dólares fijos, pero gran parte de los costos operativos están en pesos con inflación del 20%, "
        "un dólar más alto hace que los costos medidos en dólares se licúen (se hagan mucho más chicos). Por ejemplo, en el Año 5 fabricar una pick-up básica "
        "pasa de costar USD 42.583 en el caso base a costar USD 33.586 en el escenario devaluado.\n"
        "4. Comparación automática: El código compara las métricas clave de ambos escenarios calculando diff_dev = res_dev['objective_value'] - res_base['objective_value'] "
        "e itera año por año comparando los turnos activos y los totales vendidos en el mercado local y de exportación."
    )
    
    doc.add_heading("3. ¿Qué conclusiones arroja la Consigna 2?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Impacto en la ganancia: La utilidad casi se duplica, saltando de USD 1.993,49 M a USD 3.910,05 M (+96,14% de ganancia extra). "
        "Al ser una industria con costos locales en pesos e ingresos en dólares, la devaluación la vuelve enormemente rentable.\n"
        "2. ¿Conviene prender el turno tarde? Sí, con más razón que nunca. Si en el caso base ya era rentable, con costos salariales licuados en dólares "
        "el turno tarde de la Línea B es una máquina de generar margen neto. Apagarlo sería un error gravísimo.\n"
        "3. ¿Cambia el mix local vs exportación?\n"
        "   • En los Años 1 a 4, la fábrica abastece el 100% de ambos mercados.\n"
        "   • En el Año 5, la demanda total de pick-ups supera el tope físico de la Línea B (43.750 camionetas). Ante este cuello de botella, el modelo prioriza siempre al 100% las exportaciones, "
        "porque pagan un sobreprecio del 5% en dólares limpios, y ajusta apenas 282 unidades de la pick-up básica en el mercado local (por ser la de menor margen)."
    )
    
    plot_dev = os.path.join("plots", "fig1_utilidad_base_vs_dev.png")
    if os.path.exists(plot_dev):
        doc.add_picture(plot_dev, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 3: Comparativa de Utilidad Neta Anual entre Escenario Base y Devaluación Acelerada.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # CONSIGNA 3
    doc.add_heading("CONSIGNA 3: Reequipamiento de la Línea A a Pick-ups", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "El gerente operativo quiere adaptar la Línea A para ensamblar pick-ups, aprovechando que es el segmento más rentable. "
        "La obra exige parar la Línea A durante 1 año entero (capacidad = 0 ese año) e invertir entre USD 12M y USD 18M.\n"
        "• ¿Existe algún escenario que justifique la inversión durante los 5 años?\n"
        "• ¿Cambia si la demanda de pick-ups crece un +20% por un boom del campo?\n"
        "• ¿Cuál es el año óptimo para realizar la obra?"
    )
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "En model_engine.py y run_experiments.py:\n"
        "1. Se parametriza el año de obra retool_line_A_year en cada uno de los 5 años posibles.\n"
        "2. En el año de obra t, se fija forzosamente wA(t) = yA(t) = 0 (parada total de planta en Línea A).\n"
        "3. A partir del año t+1, se habilita a la Línea A para fabricar pick-ups aplicando el factor de equivalencia (capacidad 8.333 pick-ups/año mañana y 6.250 tarde).\n"
        "4. Se descuenta la inversión (USD 12M, 15M o 18M) del funcional y se corre para demanda base y para demanda con boom (+20% en pick-ups)."
    )
    doc.add_heading("3. ¿Qué resultado arroja y qué significa?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Demanda Base: NO CONVIENE EN NINGÚN AÑO. Parar la Línea A hace perder 7.500 livianos mientras que la Línea B ya alcanzaba para todas las pick-ups hasta el Año 4. "
        "La inversión destruye entre USD 16M y 31M de caja.\n"
        "• Boom Agropecuario (+20%): SÍ CONVIENE rotundamente. La demanda salta a 46.200 pick-ups, saturando la Línea B.\n"
        "• Año Óptimo: AÑO 1. Aporta una ganancia neta de entre +USD 13,0M y +USD 19,0M neta de inversión, permitiendo aprovechar 4 años completos de capacidad dual expandida."
    )
    plot_ret = os.path.join("plots", "fig4_reequipamiento_linea_A.png")
    if os.path.exists(plot_ret):
        doc.add_picture(plot_ret, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 4: Beneficio Neto Incremental de la Reconversión de Línea A según el Año de Ejecución.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # CONSIGNA 4
    doc.add_heading("CONSIGNA 4: Importación de Livianos desde China", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Evaluar si AutoITBA debe cerrar la producción local de livianos a partir del Año 2 y reemplazarla por autos importados desde China a precio CIF "
        "(LB: USD 25.000 / LP: USD 28.000), pagando USD 8.000.000 de costo único por indemnizaciones y logística.\n"
        "• ¿Conviene en escenario base? ¿Y con devaluación?\n"
        "• ¿Qué pasa si el nuevo gobierno cierra las importaciones en el Año 3?"
    )
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Se activan variables de importación M_china(m, t) para m in {LB, LP} a partir de t >= 2.\n"
        "2. Se fuerza a cero la producción local de livianos en la planta (X = 0).\n"
        "3. Al cerrar la Línea A, el modelo ahorra automáticamente sus costos fijos de encendido y salarios (708 M ARS del Año 1).\n"
        "4. Se introduce el riesgo regulatorio fijando M_china = 0 a partir de t >= 3, evaluando si la Línea A puede reabrirse o si queda cerrada irreversiblemente."
    )
    doc.add_heading("3. ¿Qué resultado arroja y qué significa?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Escenario Base: Conviene (+USD 109,7 M de ganancia neta). Importar a USD 25k/28k es más barato que fabricar localmente a USD 27,4k-29,6k, sumado al ahorro de costos fijos de Línea A.\n"
        "• Escenario Devaluación: NO CONVIENE (-USD 115,7 M de pérdida). La devaluación abarata los costos locales a USD 21,8k-23,4k, volviendo a la fábrica nacional mucho más competitiva.\n"
        "• Riesgo Regulatorio en Año 3: Si se cierran importaciones y la línea fue desmantelada, la empresa pierde USD 69,1 M; si la línea es reabrible, la ganancia se desploma a apenas +USD 7,4 M. "
        "No conviene desmantelar la fábrica."
    )

    # CONSIGNA 5
    doc.add_heading("CONSIGNA 5: Evaluación del Contrato con Autonomy", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Autonomy ofrece comprar 1.000 unidades anuales de LB a precio fijo de USD 27.500 durante los 5 años.\n"
        "• Área comercial: Lo defiende por estabilidad de volumen.\n"
        "• Área financiera: Dice que ocupa capacidad y compromete rentabilidad.\n"
        "• Preguntas: ¿Cuál es el costo de oportunidad? ¿A qué precio umbral deja de convenir?"
    )
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Se resuelve el modelo con la restricción obligatoria S_autonomy(t) = 1.000.\n"
        "2. Se resuelve el modelo liberando la capacidad (S_autonomy(t) = 0).\n"
        "3. Se resta la utilidad de ambos escenarios para hallar el costo de oportunidad: Costo Oportunidad = Z_sin - Z_con.\n"
        "4. Se calcula el precio de indiferencia analítico aprovechando que la función objetivo es perfectamente lineal respecto al precio del contrato."
    )
    doc.add_heading("3. ¿Qué resultado arroja y qué significa?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• El contrato destruye USD 5,17 Millones de valor.\n"
        "• ¿Por qué? No es por falta de capacidad (la Línea A opera al 75%-83%). La pérdida es de margen puro: en los Años 3, 4 y 5 fabricar un LB cuesta USD 29.538, USD 29.413 y USD 29.623. "
        "Venderlo a USD 27.500 genera una pérdida operativa directa de más de USD 2.000 por vehículo en esos años.\n"
        "• Precio Umbral de Indiferencia: USD 28.534 por unidad. Es el costo variable promedio ponderado de los 5 años. Por debajo de USD 28.534, el contrato destruye caja."
    )

    # CONSIGNA 6
    doc.add_heading("CONSIGNA 6: Costo de Playón y Transferencia de Inventarios", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "La empresa puede fabricar de más y guardar vehículos en el playón pagando un 25% anual de su costo variable.\n"
        "• ¿En qué casos el modelo decide transferir inventario?\n"
        "• ¿Qué ocurre si la tasa sube al 30%?\n"
        "• ¿A qué nivel de costo la transferencia deja de ser utilizada?"
    )
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Se evalúa la condición de arbitraje intertemporal: [CV(t) * (1 + h) / TC(t)] <= [CV(t+1) / TC(t+1)].\n"
        "2. Se realiza un barrido paramétrico continuo de la tasa h desde 0% hasta 30% con pasos de 0,5% y 1,0%.\n"
        "3. En cada iteración se suma el inventario total guardado para detectar el punto de anulación exacta."
    )
    doc.add_heading("3. ¿Qué resultado arroja y qué significa?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Al 25% y 30%: Cero (0) inventario transferido. Subir la tasa al 30% no genera ningún impacto porque al 25% ya no convenía guardar stock.\n"
        "• Punto de corte analítico: El inventario desaparece por completo a partir del 8,1% - 8,8% anual.\n"
        "• Significado: Para tasas mayores al ~8,8%, el costo financiero de tener autos parados supera cualquier beneficio de anticipar producción. AutoITBA debe operar en régimen Just-in-Time."
    )
    plot_inv = os.path.join("plots", "fig3_sensibilidad_inventario.png")
    if os.path.exists(plot_inv):
        doc.add_picture(plot_inv, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 5: Curva de Sensibilidad del Inventario Transferido vs Tasa de Mantenimiento en Playón.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # CONSIGNA 7
    doc.add_heading("CONSIGNA 7: Recomendación Estratégica Integral (Minimax Regret)", level=2).runs[0].font.color.rgb = COLOR_PRIMARY
    doc.add_heading("1. ¿Cuál es la idea de negocio?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Presentar una recomendación integral al directorio distinguiendo decisiones robustas vs contingentes, y definir una estrategia que minimice el arrepentimiento "
        "en los Años 1 y 2 dejando opciones abiertas para los Años 3 a 5."
    )
    doc.add_heading("2. ¿Cómo lo resuelve el código por dentro?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Se formula la matriz de pagos cruzando las estrategias directivas contra los cuatro escenarios posibles (Base, Devaluación, Boom Agro y Cierre de Aduana).\n"
        "2. Se calcula la Matriz de Arrepentimiento (Regret de Savage): R(i, j) = max_k P(k, j) - P(i, j).\n"
        "3. Se selecciona la estrategia con el menor arrepentimiento máximo (Minimax Regret)."
    )
    doc.add_heading("3. ¿Qué resultado arroja y qué significa?", level=3).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Decisiones Robustas: Línea B en doble turno los 5 años; abastecer 100% exportaciones; inventario cero.\n"
        "• Decisiones Contingentes: Importación de China y reconversión de Línea A.\n"
        "• Criterio Minimax Regret:\n"
        "  - Plan Base Local (S1): Arrepentimiento Máximo = USD 109,7 M\n"
        "  - Importar desde China (S3): Arrepentimiento Máximo = USD 115,7 M\n"
        "  - Estrategia de Opciones Abiertas (Esperar Año 2): Arrepentimiento Máximo = USD 15,4 M (Óptimo Global)\n"
        "• Hoja de Ruta: Operar localmente en Año 1, renegociar con Autonomy a > USD 28.550, no incurrir en costos irreversibles en Años 1 y 2, "
        "y decidir reconversión o importación al cierre del Año 2 con el nuevo gobierno y régimen cambiario definidos."
    )
    
    doc.save(docx_path)
    print(f"Complete Word document successfully updated at: {docx_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "INFORME_EJECUTIVO_AUTOITBA.docx"
    create_complete_word_doc(out)
