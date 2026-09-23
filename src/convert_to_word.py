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

def format_table(table, col_widths=None, header_bg="1F4E79", zebra=True):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, cell in enumerate(table.rows[0].cells):
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, 100, 100, 120, 120)
    for r_idx, row in enumerate(table.rows[1:], start=1):
        for c_idx, cell in enumerate(row.cells):
            cell.paragraphs[0].runs[0].font.size = Pt(9.0)
            if zebra and r_idx % 2 == 1:
                set_cell_background(cell, "F2F5F9")
            set_cell_margins(cell, 60, 60, 100, 100)

def create_complete_word_doc(docx_path="INFORME_EJECUTIVO_AUTOITBA.docx"):
    doc = docx.Document()
    
    # Page setup - Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    COLOR_PRIMARY = RGBColor(31, 78, 121)     # ITBA Navy Blue #1F4E79
    COLOR_SECONDARY = RGBColor(47, 85, 151)   # Slate Blue #2F5597
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
    r_sub = p_sub.add_run("Optimización Matemática (MILP), Demostraciones Analíticas y Recomendación Estratégica (2026-2030)")
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
    h1 = doc.add_heading("Resumen Ejecutivo y Cuadro de Respuestas", level=1)
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
        ("1. Plan Óptimo Base", "Producción, turnos y cobertura a 5 años", "Utilidad: USD 1.916,3 M / 1.993,5 M (Inv = 0)", "Línea A Mañana; Línea B Mañana y Tarde. 100% demanda cubierta."),
        ("2. Devaluación", "Impacto de tipo de cambio acelerado", "Utilidad: USD 3.779,1 M (+96,1%)", "Costos en pesos se licúan en USD. Turno tarde en Línea B es indispensable."),
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

    # Función Objetivo
    doc.add_heading("a.iii) Función Objetivo (Funcional Z)", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    p_fo = doc.add_paragraph()
    p_fo.add_run("MAX Z = ∑ [ Ingresos(t) - Costos_USD(t) ]\n").font.bold = True
    p_fo.add_run("• Ingresos(t) = ∑ sLoc(v,t)·P_local(v) + ∑ sExp(v,t)·[P_local(v)·1.05] + Autonomy(t)·27.500\n")
    p_fo.add_run("• Costos_USD(t) = [ C_var(t) + C_inv(t) + C_encendido(t) + C_laboral(t) ] / TC(t)\n")
    p_fo.add_run("  - C_var(t) = ∑ X(v,l,s,t) · CV1(v) · (1.20)^(t-1)\n")
    p_fo.add_run("  - C_inv(t) = ∑ I(v,t) · 0.25 · CV1(v) · (1.20)^(t-1)\n")
    p_fo.add_run("  - C_encendido(t) = [ 500M·(wA+yA) + 800M·(wB+yB) ] · (1.20)^(t-1)\n")
    p_fo.add_run("  - C_laboral(t) = 26M · [ 8·(wA+yA) + 10·(wB+yB) + 5·z ] · (1.20)^(t-1)")

    # Parámetros
    doc.add_heading("a.iv) Parámetros del Modelo", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
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
    doc.add_heading("a.v) Restricciones Formales (135 Ecuaciones)", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
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
    # SECCIÓN 2: DESARROLLO ANALÍTICO Y RESPUESTAS A LAS CONSIGNAS
    # -------------------------------------------------------------
    h_sec2 = doc.add_heading("Sección 2: Demostraciones Analíticas y Consignas 1 a 7", level=1)
    h_sec2.runs[0].font.color.rgb = COLOR_PRIMARY

    # Consigna 1
    doc.add_heading("Consigna 1: Formulación y Plan Óptimo para el Escenario Base", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Planteo y Modelo Conceptual:\n"
        "La empresa enfrenta un problema de asignación de capacidad con costos fijos escalonados. La Línea B tiene un costo fijo "
        "de encendido anual muy superior al de la Línea A (800 M ARS vs 500 M ARS), y sus operarios demandan salarios más elevados por la mayor dotación "
        "(10 operarios vs 8). Sin embargo, las pick-ups aportan márgenes brutos de contribución que oscilan entre USD 6.667 y USD 16.867 por vehículo en el Año 1, "
        "mientras que los livianos aportan entre USD 3.333 (LB) y USD 6.200 (LP)."
    )
    doc.add_paragraph(
        "2. Resultados Numéricos:\n"
        "Al ejecutar el algoritmo Simplex y Branch & Bound con PuLP / CBC:\n"
        "• Utilidad Neta Total a 5 Años: USD 1.916.300.845 (sin propuesta adicional de agronegocios) o USD 1.993.488.793 (con propuesta de agronegocios).\n"
        "• Turnos Activos: Línea A opera solo turno mañana los 5 años (wA=1, yA=0). Línea B opera en doble turno mañana y tarde los 5 años (wB=1, yB=1).\n"
        "• Inventario en Playón: 0 unidades en todos los años."
    )
    
    # Table 1: Financial breakdown
    table_c1 = doc.add_table(rows=5, cols=7)
    c1_h = ["Concepto Financiero", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5", "Total Acumulado"]
    for i, h in enumerate(c1_h):
        table_c1.rows[0].cells[i].text = h
    c1_data = [
        ("Tipo de Cambio (ARS/USD)", "1.500", "1.750", "1.950", "2.350", "2.800", "—"),
        ("Ingresos Totales (USD)", "$2.214,6 M", "$2.275,4 M", "$2.339,1 M", "$2.405,8 M", "$2.475,7 M", "$11.710,7 M"),
        ("Costos Totales (USD)", "-$1.725,9 M", "-$1.825,2 M", "-$2.022,0 M", "-$2.072,2 M", "-$2.149,1 M", "-$9.794,4 M"),
        ("Utilidad Neta (USD)", "$488,7 M", "$450,2 M", "$317,1 M", "$333,6 M", "$326,7 M", "$1.916,3 M")
    ]
    for r_idx, r_data in enumerate(c1_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c1.rows[r_idx].cells[c_idx].text = val
    format_table(table_c1)

    plot_mix = os.path.join("plots", "fig2_mix_produccion_base.png")
    if os.path.exists(plot_mix):
        doc.add_picture(plot_mix, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 2: Mix de Producción Anual por Modelo a lo largo de los 5 Años (Escenario Base).")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_paragraph(
        "3. Interpretación Económica y Fenómeno de Compresión de Margen:\n"
        "Aunque el volumen físico vendido crece año tras año (de 46.000 a 51.557 vehículos), la utilidad anual cae de USD 489 M a USD 327 M. "
        "Esto no es un problema de volumen sino de margen: los costos aumentan al 20% anual en pesos, mientras que el tipo de cambio oficial del REM "
        "se devalúa a un ritmo menor en los años 2 a 4. El tipo de cambio se atrasa frente a la inflación de costos, comprimiendo el margen unitario en dólares."
    )

    # Consigna 2
    doc.add_heading("Consigna 2: Evaluación del Escenario de Mayor Devaluación", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Mecanismo de Transmisión Económica:\n"
        "Al devaluarse el peso de manera acelerada (1.500 -> 2.200 -> 2.650 -> 3.100 -> 3.550), la conversión de los costos operativos en pesos "
        "hacia dólares se reduce drásticamente: Costo_USD(t) = Costos_ARS(t) / TC(t). Los ingresos permanecen constantes por estar fijados contractualmente en USD. "
        "Por ende, la Utilidad Neta a 5 años casi se duplica, pasando de USD 1.916,3 M a USD 3.779,1 M (+97,2%)."
    )
    
    table_c2 = doc.add_table(rows=6, cols=6)
    c2_h = ["Métrica / Margen Unitario", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
    for i, h in enumerate(c2_h):
        table_c2.rows[0].cells[i].text = h
    c2_data = [
        ("Utilidad Base (USD M)", "$488,7", "$450,2", "$317,1", "$333,6", "$326,7"),
        ("Utilidad Devaluación (USD M)", "$488,7", "$823,5", "$851,2", "$835,0", "$780,7"),
        ("Margen LB Base (USD)", "$3.333", "$2.571", "$462", "$587", "$377"),
        ("Margen LB Devaluación (USD)", "$3.333", "$8.182", "$8.264", "$7.703", "$6.635"),
        ("Margen PP Devaluación (USD)", "$16.867", "$24.255", "$24.380", "$23.525", "$21.898")
    ]
    for r_idx, r_data in enumerate(c2_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c2.rows[r_idx].cells[c_idx].text = val
    format_table(table_c2)

    plot_dev = os.path.join("plots", "fig1_utilidad_base_vs_dev.png")
    if os.path.exists(plot_dev):
        doc.add_picture(plot_dev, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 3: Comparativa de Utilidad Neta Anual entre Escenario Base y Devaluación Acelerada.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_paragraph(
        "2. Respuestas a la Dirección:\n"
        "• ¿Cambia el mix local/exportación? NO. La empresa ya abastece el 100% de la demanda local y de exportación en ambos escenarios. La relación la fija el mercado.\n"
        "• ¿Cambia la conveniencia del turno tarde? NO. Se vuelve aún más rentable mantener el turno tarde en la Línea B: sus costos en dólares bajan y aporta 18.750 pick-ups de alto margen."
    )

    # Consigna 3
    doc.add_heading("Consigna 3: Reequipamiento de la Línea A a Pick-ups", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Planteo y Modelo Conceptual:\n"
        "Se evalúa reequipar la Línea A para ensamblar pick-ups parando la línea 1 año (wA = yA = 0 en ese año) e invirtiendo entre USD 12M y 18M. "
        "A partir del año siguiente, la línea puede ensamblar pick-ups (capacidad de 8.333 u/año mañana y 6.250 u/año tarde)."
    )
    
    table_c3 = doc.add_table(rows=6, cols=6)
    c3_h = ["Año de Obra", "Neto Base (12M)", "Neto Base (18M)", "Neto Boom (12M)", "Neto Boom (15M)", "Neto Boom (18M)"]
    for i, h in enumerate(c3_h):
        table_c3.rows[0].cells[i].text = h
    c3_data = [
        ("Obra Año 1", "-$16,4 M", "-$22,4 M", "+$19,0 M", "+$16,0 M", "+$13,0 M"),
        ("Obra Año 2", "-$20,5 M", "-$26,5 M", "+$4,6 M", "+$1,6 M", "-$1,4 M"),
        ("Obra Año 3", "-$17,5 M", "-$23,5 M", "+$10,8 M", "+$7,8 M", "+$4,8 M"),
        ("Obra Año 4", "-$21,5 M", "-$27,5 M", "-$7,7 M", "-$10,7 M", "-$13,7 M"),
        ("Obra Año 5", "-$23,3 M", "-$29,3 M", "-$24,5 M", "-$27,5 M", "-$30,5 M")
    ]
    for r_idx, r_data in enumerate(c3_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c3.rows[r_idx].cells[c_idx].text = val
    format_table(table_c3)

    plot_ret = os.path.join("plots", "fig4_reequipamiento_linea_A.png")
    if os.path.exists(plot_ret):
        doc.add_picture(plot_ret, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 4: Beneficio Neto Incremental de la Reconversión de Línea A según el Año de Ejecución.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    doc.add_paragraph(
        "2. Conclusiones Analíticas:\n"
        "• Demanda Base: NO CONVIENE EN NINGÚN AÑO. Parar la Línea A hace perder las ventas de 7.500 livianos mientras que la Línea B ya alcanza "
        "para todas las pick-ups hasta el Año 4. La inversión destruye entre USD 16M y 31M de caja.\n"
        "• Boom Agropecuario (+20%): SÍ CONVIENE rotundamente. La demanda salta a 46.200 pick-ups, saturando la Línea B.\n"
        "• Año Óptimo: AÑO 1. Permite aprovechar 4 años completos de ventas extraordinarias con una ganancia neta de entre +USD 13,0M y +USD 19,0M.\n"
        "• Umbral Mínimo: El boom de demanda debe ser de al menos +17% sostenido para justificar la obra."
    )

    # Consigna 4
    doc.add_heading("Consigna 4: Importación de Livianos desde China", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Planteo y Modelo Conceptual:\n"
        "Se evalúa sustituir la fabricación local de livianos por importación CIF desde China desde el Año 2, asumiendo un costo único de transición de "
        "USD 8.000.000 por indemnizaciones y logística. CIF Zárate: LB = USD 25.000, LP = USD 28.000."
    )
    
    table_c4 = doc.add_table(rows=5, cols=4)
    c4_h = ["Alternativa Evaluada", "Base (M USD)", "Devaluación (M USD)", "Impacto Incremental vs Local"]
    for i, h in enumerate(c4_h):
        table_c4.rows[0].cells[i].text = h
    c4_data = [
        ("Seguir Produciendo Localmente", "$1.916,3 M", "$3.779,1 M", "Base de comparación ($0,0)"),
        ("Importar Livianos desde Año 2", "$2.025,9 M", "$3.663,4 M", "Base: +$109,6 M | Deval: -$115,7 M"),
        ("Cierre en Año 3 (Línea Reabrible)", "$1.923,7 M", "$3.779,1 M", "+$7,4 M (Marginal)"),
        ("Cierre en Año 3 (Cierre Irreversible)", "$1.847,2 M", "$3.779,1 M", "-$69,1 M (PÉRDIDA GRAVE)")
    ]
    for r_idx, r_data in enumerate(c4_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c4.rows[r_idx].cells[c_idx].text = val
    format_table(table_c4)

    doc.add_paragraph(
        "2. Explicación Económica de las Dos Fuerzas:\n"
        "• En Escenario Base: Conviene ampliamente (+USD 109,6 M) por dos vías: menor costo unitario (LB sale USD 25k importado vs USD 27,4k-29,6k local) "
        "y ahorro de costos fijos de encendido y salarios de Línea A (708 M ARS del año 1, equivalentes a ~USD 500k anuales).\n"
        "• En Escenario Devaluación: Se da vuelta por completo (-USD 115,7 M de pérdida). Producir localmente pasa a costar USD 21.800 para LB, "
        "mucho más barato que los USD 25.000 fijos de importación.\n"
        "• Riesgo Regulatorio en Año 3: Si el nuevo gobierno cierra aduanas y la línea fue desmantelada, la empresa pierde las ventas de los Años 3 a 5 (-USD 69,1 M). "
        "La recomendación es NO adoptar esta estrategia en el Año 1."
    )

    # Consigna 5
    doc.add_heading("Consigna 5: Evaluación del Contrato con Autonomy", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Demostración Matemática del Costo de Oportunidad:\n"
        "El contrato estipula 1.000 unidades anuales de LB a precio fijo de USD 27.500 durante los 5 años.\n"
        "• Utilidad con contrato: USD 1.916.300.845\n"
        "• Utilidad liberando la capacidad (sin contrato): USD 1.921.470.180\n"
        "• Costo de Oportunidad: +USD 5.169.335 (+USD 5,17 M). El contrato destruye valor."
    )
    
    table_c5 = doc.add_table(rows=5, cols=7)
    c5_h = ["Concepto", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5", "Total 5 Años"]
    for i, h in enumerate(c5_h):
        table_c5.rows[0].cells[i].text = h
    c5_data = [
        ("Precio Contrato (USD/u)", "$27.500", "$27.500", "$27.500", "$27.500", "$27.500", "—"),
        ("Costo Variable LB (USD/u)", "$26.667", "$27.429", "$29.538", "$29.413", "$29.623", "—"),
        ("Margen Unitario (USD/u)", "+$833", "+$71", "-$2.038", "-$1.913", "-$2.123", "-$5.170 / u"),
        ("Aporte Anual (1.000 u)", "+$833.000", "+$71.000", "-$2.038.000", "-$1.913.000", "-$2.123.000", "-$5.170.000")
    ]
    for r_idx, r_data in enumerate(c5_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c5.rows[r_idx].cells[c_idx].text = val
    format_table(table_c5)

    doc.add_paragraph(
        "2. Deducción del Precio de Indiferencia (USD 28.534):\n"
        "Como la Línea A opera con holgura de capacidad (75% a 83%), el contrato no desplaza capacidad de otros modelos. Su pérdida es puramente de margen de precio. "
        "Dado que Z es perfectamente lineal en el precio del contrato (cada dólar extra aporta 1.000 u x 5 años = USD 5.000):\n"
        "P_indiferencia = 27.500 + (5.169.335 / 5.000) = 27.500 + 1.033,87 = USD 28.533,87 (redondeado: USD 28.534).\n"
        "Este precio coincide exactamente con el costo variable promedio de los 5 años: (26.667 + 27.429 + 29.538 + 29.413 + 29.623) / 5 = USD 28.534.\n"
        "Recomendación: Renegociar a mínimo USD 28.550 o indexar; si no, rechazar el contrato."
    )

    # Consigna 6
    doc.add_heading("Consigna 6: Costo de Playón y Transferencia de Inventarios", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Condición Analítica de Arbitraje Intertemporal:\n"
        "Para que convenga fabricar una unidad en el año t y guardarla para el año t+1 pagando la tasa h, se debe cumplir:\n"
        "cv(t)·(1 + h) / e(t) <= cv(t+1) / e(t+1)   ===>   h <= [ (cv(t+1)/e(t+1)) / (cv(t)/e(t)) ] - 1\n"
        "El incremento porcentual del costo unitario en dólares del año 2 al 3 es del +7,7%. Por ende, para tasas h superiores al 7,7%-8,8%, el costo de guardar "
        "supera cualquier ahorro de fabricación anticipada."
    )
    
    table_c6 = doc.add_table(rows=7, cols=3)
    c6_h = ["Tasa de Mantenimiento (h)", "Inventario Total Transferido", "Comportamiento del Modelo"]
    for i, h in enumerate(c6_h):
        table_c6.rows[0].cells[i].text = h
    c6_data = [
        ("0,0% (Almacenamiento gratis)", "91.252 unidades", "Nivelación masiva de carga entre períodos."),
        ("1,0% a 5,0%", "61.429 a 22.546 unidades", "Traslado activo de pick-ups y livianos."),
        ("8,0% a 8,1%", "4.302 unidades", "Solo transfiere 4.302 livianos del año 2 al 3."),
        ("8,2% a 8,8%", "0,0 unidades", "PUNTO DE CORTE ANALÍTICO (El inventario cae a cero)."),
        ("25,0% (Tasa Base)", "0,0 unidades", "Cero inventario (Régimen Just-in-Time estricto)."),
        ("30,0% (Tasa Sensibilidad)", "0,0 unidades", "Cero inventario (Sin ningún impacto en la utilidad).")
    ]
    for r_idx, r_data in enumerate(c6_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c6.rows[r_idx].cells[c_idx].text = val
    format_table(table_c6)

    plot_inv = os.path.join("plots", "fig3_sensibilidad_inventario.png")
    if os.path.exists(plot_inv):
        doc.add_picture(plot_inv, width=Inches(5.5))
        p_cap = doc.add_paragraph("Figura 5: Curva de Sensibilidad del Inventario Transferido vs Tasa de Mantenimiento en Playón.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # Consigna 7
    doc.add_heading("Consigna 7: Recomendación Estratégica Integral (Minimax Regret)", level=2).runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "1. Planteo Formal del Criterio Minimax Regret de Savage:\n"
        "Se evalúa el arrepentimiento máximo de comprometer cada decisión estratégica hoy frente a los 4 estados posibles de la economía. "
        "El arrepentimiento R(i, j) = max_k P(k, j) - P(i, j) mide cuánto dinero dejó de ganar la empresa respecto a la mejor decisión que pudo haber tomado "
        "conociendo el escenario de antemano."
    )
    
    table_c7 = doc.add_table(rows=5, cols=6)
    c7_h = ["Estrategia / Decisión", "E1: Base", "E2: Deval.", "E3: Boom", "E4: Cierre Reg.", "Arrepentimiento Máximo"]
    for i, h in enumerate(c7_h):
        table_c7.rows[0].cells[i].text = h
    c7_data = [
        ("S1: Plan Base Local", "$109,6 M", "$0,0 M", "$18,9 M", "$0,0 M", "USD 109,6 M"),
        ("S2: Reequipar Línea A (Año 1)", "$126,0 M", "$16,2 M", "$0,0 M", "$16,4 M", "USD 126,0 M"),
        ("S3: Importar China (Año 2)", "$0,0 M", "$115,7 M", "$0,0 M", "$69,1 M", "USD 115,7 M"),
        ("S_E: Opciones Abiertas (Esperar)", "$15,4 M", "$0,0 M", "$0,0 M", "$0,0 M", "USD 15,4 M (ÓPTIMO)")
    ]
    for r_idx, r_data in enumerate(c7_data, start=1):
        for c_idx, val in enumerate(r_data):
            table_c7.rows[r_idx].cells[c_idx].text = val
    format_table(table_c7)

    doc.add_paragraph(
        "2. Hoja de Ruta Táctica para los Años 1 a 5:\n"
        "• Año 1: Operar según el Plan Base (Línea A mañana, Línea B doble turno). Renegociar con Autonomy a > USD 28.550 (o liberar capacidad). "
        "No comprometer ni los USD 12M de obra ni los USD 8M de importación.\n"
        "• Años 1 y 2: Seguir la demanda real del agro (umbral es +17%) y el tipo de cambio real frente a las elecciones.\n"
        "• Cierre de Año 2: Con las variables despejadas, decidir reconversión o importación con mínimo riesgo."
    )

    doc.save(docx_path)
    print(f"Complete Word document successfully updated at: {docx_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "INFORME_EJECUTIVO_AUTOITBA.docx"
    create_complete_word_doc(out)
