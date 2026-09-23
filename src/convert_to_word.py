import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_styled_document(docx_path="INFORME_EJECUTIVO_AUTOITBA.docx"):
    doc = docx.Document()
    
    # Page setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Color palette
    COLOR_PRIMARY = RGBColor(31, 78, 121)     # ITBA Navy Blue #1F4E79
    COLOR_SECONDARY = RGBColor(47, 85, 151)   # Slate Blue #2F5597
    COLOR_DARK = RGBColor(38, 38, 38)         # Charcoal text
    COLOR_MUTED = RGBColor(89, 89, 89)        # Gray
    
    # -------------------------------------------------------------
    # HEADER / PORTADA
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("INSTITUTO TECNOLÓGICO DE BUENOS AIRES (ITBA)")
    run_inst.font.name = "Calibri"
    run_inst.font.size = Pt(12)
    run_inst.font.bold = True
    run_inst.font.color.rgb = COLOR_SECONDARY
    
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_dept = p_dept.add_run("Departamento de Ingeniería Industrial — 11.51 / IO51 Investigación de Operaciones")
    run_dept.font.name = "Calibri"
    run_dept.font.size = Pt(10.5)
    run_dept.font.color.rgb = COLOR_MUTED
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(6)
    run_title = p_title.add_run("TRABAJO PRÁCTICO N° 1 COMPLEMENTARIO\nPlan de Producción Estratégico — AutoITBA S.A.")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    run_sub = p_sub.add_run("Optimización Matemática a 5 Años, Análisis de Sensibilidad y Estrategia Directiva (2026-2030)")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = COLOR_DARK
    
    # Metadata Box
    table_meta = doc.add_table(rows=4, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Materia:", "11.51 / IO51 - Investigación Operativa (2° Cuatrimestre 2026)"),
        ("Terminal Automotriz:", "AutoITBA S.A. (Planta Zárate, Buenos Aires)"),
        ("Herramientas:", "Python 3.12, PuLP (Solver CBC), Pandas, OpenPyXL"),
        ("Repositorio GitHub:", "https://github.com/Santim1897/TP1-IO")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = table_meta.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.text = k
        cell_v.text = v
        cell_k.paragraphs[0].runs[0].font.bold = True
        cell_k.paragraphs[0].runs[0].font.color.rgb = COLOR_PRIMARY
        cell_v.paragraphs[0].runs[0].font.color.rgb = COLOR_DARK
        set_cell_background(cell_k, "F2F2F2")
        set_cell_background(cell_v, "FAFAFA")
        set_cell_margins(cell_k, 60, 60, 100, 100)
        set_cell_margins(cell_v, 60, 60, 100, 100)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(18)
    
    # -------------------------------------------------------------
    # RESUMEN EJECUTIVO
    # -------------------------------------------------------------
    h1 = doc.add_heading("Resumen Ejecutivo", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "Se formuló y resolvió un modelo de Programación Lineal Entera Mixta (MILP) para planificar la producción, "
        "asignación de turnos, almacenamiento interanual y abastecimiento de mercado de la terminal automotriz AutoITBA S.A. "
        "durante un horizonte de cinco años (Año 1 a Año 5). El modelo busca maximizar la Utilidad Neta Total consolidada en "
        "dólares estadounidenses (USD), incorporando la dinámica inflacionaria del 20% anual y matrices de tipo de cambio oficial."
    )
    
    doc.add_paragraph(
        "Bajo el Escenario Base, la Utilidad Neta acumulada alcanza USD 1.993,49 Millones (USD 1.916,30 Millones sin contrato optativo adicional de agronegocios). "
        "El plan óptimo establece operar la Línea A únicamente en Turno Mañana (abasteciendo el 100% de la demanda de livianos) "
        "y la Línea B en Turno Mañana y Turno Tarde a pleno régimen (dedicada exclusivamente a pick-ups). No se traslada inventario terminado "
        "entre períodos debido al elevado costo financiero y logístico de playón (25% anual)."
    )
    
    # Summary Table of Consignas
    h2_sum = doc.add_heading("Síntesis de Respuestas a las Consignas", level=2)
    h2_sum.runs[0].font.color.rgb = COLOR_SECONDARY
    
    table_sum = doc.add_table(rows=8, cols=4)
    table_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Consigna", "Tema Analizado", "Resultado Cuantitativo", "Decisión Recomendada"]
    for i, h in enumerate(headers):
        cell = table_sum.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell, 80, 80, 100, 100)
        
    consignas_res = [
        ("1. Plan Óptimo Base", "Producción, turnos y cobertura a 5 años", "Utilidad: USD 1.993,49 M (Inv = 0)", "Línea A Mañana; Línea B Mañana+Tarde. 100% demanda cubierta."),
        ("2. Devaluación", "Impacto de tipo de cambio acelerado", "Utilidad: USD 3.910,05 M (+96,1%)", "Costos en pesos se licúan en USD. Turno tarde es aún más rentable."),
        ("3. Reequipamiento", "Inversión USD 12M-18M para pick-ups en Línea A", "Base: Inviable (-USD 16M a -31M)\nBoom (+20%): +USD 33M a +39M", "No reequipar en demanda normal. Con Boom Agropecuario, hacer la obra en Año 1."),
        ("4. Importación China", "Reemplazo de livianos locales desde Año 2", "Base: +USD 109,7 M\nDevaluación: -USD 115,7 M\nCierre Año 3: -USD 69,1 M", "No desmantelar la planta local. Riesgo regulatorio y cambiario extremo."),
        ("5. Contrato Autonomy", "1.000 LB anuales a USD 27.500 fijo", "Costo oportunidad: +USD 5,17 M\nPrecio umbral: USD 28.534/u", "A USD 27.500 da pérdida en Años 3-5. Renegociar a > USD 28.550 o liberar capacidad."),
        ("6. Costo de Playón", "Sensibilidad al costo de inventario (25%-30%)", "Inv = 0 a 25% y 30%\nCorte analítico: 8,8% anual", "Operar Just-in-Time. Guardar stock solo conviene si la tasa fuera inferior al 8,8%."),
        ("7. Estrategia Directiva", "Robustez vs contingencia (Minimax Regret)", "Arrepentimiento S1: USD 109,7 M\nArrepentimiento S3: USD 115,7 M", "Fabricación Local Flexible: No asumir compromisos irreversibles en Años 1 y 2.")
    ]
    for row_idx, data_row in enumerate(consignas_res, start=1):
        for col_idx, text in enumerate(data_row):
            cell = table_sum.rows[row_idx].cells[col_idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F2F5F9")
            set_cell_margins(cell, 60, 60, 80, 80)
            
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # SECCIÓN A: MODELO DE PROGRAMACIÓN LINEAL
    # -------------------------------------------------------------
    h_a = doc.add_heading("a) Modelo de Programación Lineal Entera Mixta (MILP)", level=1)
    h_a.runs[0].font.color.rgb = COLOR_PRIMARY
    
    # i) Supuestos
    h_ai = doc.add_heading("i) Supuestos más Importantes", level=2)
    h_ai.runs[0].font.color.rgb = COLOR_SECONDARY
    
    supuestos = [
        "Unidad Monetaria Homogénea (USD): Dado que los precios de venta locales y de exportación se encuentran fijados en dólares estadounidenses y la economía argentina experimenta inflación en moneda local, toda la función objetivo y evaluación financiera se consolida en USD sin descontar (el enunciado no provee tasa de descuento intertemporal).",
        "Indexación y Conversión de Costos en Pesos: Los costos operativos originalmente en ARS (mano de obra, encendido de línea y componentes variables locales) se indexan anualmente al ritmo de la inflación proyectada del 20% anual y se convierten a dólares dividiendo por el tipo de cambio oficial del año t (TC_t).",
        "Equivalencia de Capacidad en Línea B (Ratio 1.2): La Línea B es flexible y puede ensamblar 30.000 livianos o 25.000 pick-ups por turno mañana. Por ende, cada pick-up consume técnicamente 1,2 veces la capacidad de un liviano (30.000 / 25.000 = 1,2).",
        "Régimen de Turnos y Jerarquía: El turno tarde opera al 75% de la capacidad del turno mañana debido a menor dotación de supervisores e insumos logísticos nocturnos. No es admisible activar el turno tarde sin tener encendido previamente el turno mañana en esa misma línea.",
        "Regla Sindical de Peligrosidad: Si al menos una línea opera en el turno tarde, se activa la exigencia colectiva de contratar 5 operarios adicionales comunes de supervisión de peligrosidad. Estos operarios se pagan una sola vez si hay turno tarde en planta.",
        "Ecuación de Continuidad y Playón: El inventario inicial en Año 1 es cero. Las unidades no comercializadas pueden trasladarse al período siguiente pagando un 25% anual del costo variable unitario de fabricación de dicho vehículo.",
        "Prima de Exportación (+5% MERCOSUR): Las pick-ups exportadas perciben un adicional del 5% sobre el precio de lista local por flete, seguro y prima regional de origen argentino."
    ]
    for s in supuestos:
        p = doc.add_paragraph(s, style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        
    # ii) Variables
    h_aii = doc.add_heading("ii) Variables de Decisión Elegidas", level=2)
    h_aii.runs[0].font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "Se adoptó un esquema donde la producción, ventas e inventarios se representan como variables continuas (divisibilidad), "
        "mientras que las decisiones de encendido de líneas y turnos se modelan mediante variables binarias:"
    )
    
    table_var = doc.add_table(rows=8, cols=4)
    table_var.alignment = WD_TABLE_ALIGNMENT.CENTER
    var_headers = ["Variable", "Tipo", "Dimensión", "Significado Económico / Operativo"]
    for i, h in enumerate(var_headers):
        cell = table_var.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell, 80, 80, 100, 100)
        
    var_rows = [
        ("X(m, l, k, t)", "Continua (>=0)", "70 variables", "Unidades producidas del modelo m en la línea l, turno k, año t."),
        ("S_local(m, t)", "Continua (>=0)", "25 variables", "Unidades vendidas en el mercado local del modelo m en el año t."),
        ("S_export(m, t)", "Continua (>=0)", "15 variables", "Unidades exportadas al MERCOSUR del modelo m (pick-ups) en el año t."),
        ("I(m, t)", "Continua (>=0)", "25 variables", "Inventario en playón del modelo m al cierre del año t (I(m, 0) = 0)."),
        ("wA(t), wB(t)", "Binaria {0, 1}", "10 variables", "Vale 1 si la línea A / B opera en Turno Mañana en el año t; 0 si no."),
        ("yA(t), yB(t)", "Binaria {0, 1}", "10 variables", "Vale 1 si la línea A / B opera en Turno Tarde en el año t; 0 si no."),
        ("z(t)", "Binaria {0, 1}", "5 variables", "Vale 1 si al menos una línea opera el Turno Tarde (activa los 5 operarios extra).")
    ]
    for row_idx, r in enumerate(var_rows, start=1):
        for col_idx, text in enumerate(r):
            cell = table_var.rows[row_idx].cells[col_idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F2F5F9")
            set_cell_margins(cell, 60, 60, 80, 80)

    # iii) Función Objetivo
    h_aiii = doc.add_heading("iii) Función Objetivo (Funcional Z)", level=2)
    h_aiii.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p_fo = doc.add_paragraph()
    p_fo.add_run("MAX Z = ∑ [ Ingresos(t) - Costos_USD(t) ]\n").font.bold = True
    p_fo.add_run("Donde:\n")
    p_fo.add_run("• Ingresos(t) = ∑ S_local(m,t)·P_local(m) + ∑ S_export(m,t)·(P_local(m)·1.05) + Contrato_Autonomy(t)\n")
    p_fo.add_run("• Costos_USD(t) = [ Costo_Variable_ARS(t) + Costo_Inventario_ARS(t) + Costo_Encendido_ARS(t) + Costo_Laboral_ARS(t) ] / TC(t)\n")
    p_fo.add_run("  - Costo_Variable_ARS(t) = ∑ X(m,l,k,t) · CV1(m) · (1.20)^(t-1)\n")
    p_fo.add_run("  - Costo_Inventario_ARS(t) = ∑ I(m,t) · 0.25 · CV1(m) · (1.20)^(t-1)\n")
    p_fo.add_run("  - Costo_Encendido_ARS(t) = [ 500M·(wA+yA) + 800M·(wB+yB) ] · (1.20)^(t-1)\n")
    p_fo.add_run("  - Costo_Laboral_ARS(t) = 26M · [ 8·(wA+yA) + 10·(wB+yB) + 5·z ] · (1.20)^(t-1)")
    set_cell_background(doc.add_table(rows=1, cols=1).rows[0].cells[0], "F9FBFD")

    # iv) Parámetros
    h_aiv = doc.add_heading("iv) Parámetros del Modelo", level=2)
    h_aiv.runs[0].font.color.rgb = COLOR_SECONDARY
    
    table_par = doc.add_table(rows=13, cols=6)
    table_par.alignment = WD_TABLE_ALIGNMENT.CENTER
    par_headers = ["Parámetro / Concepto", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
    for i, h in enumerate(par_headers):
        cell = table_par.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell, 60, 60, 80, 80)
        
    par_rows = [
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
    for row_idx, r in enumerate(par_rows, start=1):
        for col_idx, text in enumerate(r):
            cell = table_par.rows[row_idx].cells[col_idx]
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(9.0)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F2F5F9")
            set_cell_margins(cell, 40, 40, 60, 60)

    # v) Restricciones
    h_av = doc.add_heading("v) Restricciones del Modelo", level=2)
    h_av.runs[0].font.color.rgb = COLOR_SECONDARY
    
    restricciones = [
        ("R1. Precedencia de Turnos:", "yA(t) <= wA(t)  y  yB(t) <= wB(t) (no se abre la tarde sin la mañana)."),
        ("R2. Lógica de Peligrosidad (z):", "z(t) >= yA(t), z(t) >= yB(t), z(t) <= yA(t) + yB(t) (activa los 5 operarios de peligrosidad si hay turno tarde)."),
        ("R3. Capacidad Línea A:", "∑ X(m, A, Mañana, t) <= 10.000·wA(t)  y  ∑ X(m, A, Tarde, t) <= 7.500·yA(t)."),
        ("R4. Capacidad Mixta Línea B:", "[ ∑ X_liv / 30.000 + ∑ X_pick / 25.000 ] <= 1.0·wB(t) (Mañana) y <= 0.75·yB(t) (Tarde). Ratio 1.2."),
        ("R5. Balance de Inventarios:", "I(m, t-1) + Producción(m, t) = Ventas_Local(m, t) + Export(m, t) + Autonomy(m, t) + I(m, t)."),
        ("R6. Topes de Demanda y Contratos:", "Ventas_Local <= DemandaLocal(t); Export <= DemandaExport; Autonomy = 1.000 LB anuales.")
    ]
    for name, desc in restricciones:
        p = doc.add_paragraph()
        r_name = p.add_run(name + " ")
        r_name.font.bold = True
        r_name.font.color.rgb = COLOR_PRIMARY
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
    # SECCIÓN 2: RESPUESTAS DETALLADAS A LAS CONSIGNAS
    # -------------------------------------------------------------
    h_cons = doc.add_heading("2. Respuestas Detalladas a las Consignas 1 a 7", level=1)
    h_cons.runs[0].font.color.rgb = COLOR_PRIMARY
    
    # Consigna 1
    h_c1 = doc.add_heading("Consigna 1: Plan Óptimo para el Escenario Base", level=2)
    h_c1.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "El modelo arroja una Utilidad Neta Total acumulada de USD 1.993,49 Millones en los cinco años. "
        "El turno mañana se enciende en ambas líneas los 5 años, mientras que el turno tarde se activa exclusivamente en la Línea B los 5 años. "
        "No se transfiere inventario terminado entre períodos (I = 0). En los Años 1 a 4 se cubre el 100% de la demanda en todos los canales. "
        "En el Año 5, la demanda de pick-ups satura la Línea B y se priorizan las versiones de mayor margen (PP y PM), racionando 282 unidades de PB local."
    )
    plot_mix = os.path.join("plots", "fig2_mix_produccion_base.png")
    if os.path.exists(plot_mix):
        doc.add_picture(plot_mix, width=Inches(6.0))
        p_cap = doc.add_paragraph("Figura 2: Mix de Producción Anual por Modelo a lo largo de los 5 Años (Escenario Base).")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # Consigna 2
    h_c2 = doc.add_heading("Consigna 2: Evaluación del Escenario de Mayor Devaluación", level=2)
    h_c2.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Bajo una devaluación acelerada (TC pasa a 2.200, 2.650, 3.100 y 3.550), la Utilidad Neta se incrementa un +96,1% hasta alcanzar "
        "USD 3.910,05 Millones (ganancia extraordinaria de +USD 1.916,57 M). La causa es la licuación de los costos operativos en pesos frente "
        "a ingresos dolarizados estables.\n"
        "• ¿Cambia el mix local/exportación? NO, se sigue cubriendo el 100% de la demanda en ambos mercados.\n"
        "• ¿Cambia la conveniencia del turno tarde? NO, el turno tarde en la Línea B es sumamente superavitario y se mantiene activo los 5 años."
    )
    plot_dev = os.path.join("plots", "fig1_utilidad_base_vs_dev.png")
    if os.path.exists(plot_dev):
        doc.add_picture(plot_dev, width=Inches(6.0))
        p_cap = doc.add_paragraph("Figura 3: Comparativa de Utilidad Neta Anual entre Escenario Base y Devaluación Acelerada.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # Consigna 3
    h_c3 = doc.add_heading("Consigna 3: Reequipamiento de la Línea A a Pick-ups", level=2)
    h_c3.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "Reequipar la Línea A para pick-ups exige parar la línea 1 año e invertir entre USD 12M y 18M.\n"
        "• Demanda Base: NO CONVIENE EN NINGÚN AÑO. Parar la Línea A un año implica perder la venta de hasta 10.000 livianos, destruyendo entre USD 13M y 31M.\n"
        "• Boom Agropecuario (+20% demanda pick-ups): SÍ CONVIENE rotundamente. Si la obra se realiza en el Año 1, aporta un beneficio neto de entre "
        "+USD 33,4M y +USD 39,4M descontando la inversión. El año óptimo es el Año 1."
    )
    plot_retool = os.path.join("plots", "fig4_reequipamiento_linea_A.png")
    if os.path.exists(plot_retool):
        doc.add_picture(plot_retool, width=Inches(6.0))
        p_cap = doc.add_paragraph("Figura 4: Beneficio Neto Incremental de la Reconversión de Línea A según el Año de Ejecución.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # Consigna 4
    h_c4 = doc.add_heading("Consigna 4: Importación de Livianos desde China", level=2)
    h_c4.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Escenario Base: Conviene ampliamente (+USD 109,70 M de ahorro neto), ya que el CIF (USD 25k/28k) es menor al costo variable local (USD 27,4k-29,6k).\n"
        "• Escenario Devaluación: NO CONVIENE (-USD 115,67 M de pérdida), ya que la devaluación abarata la producción nacional a USD 21,8k-23,4k.\n"
        "• Riesgo Regulatorio (Cierre en Año 3): Si se cierran importaciones y la línea fue desmantelada irreversiblemente, se pierden USD 69,08 M frente a seguir produciendo. "
        "Si la línea puede reabrirse, la ganancia se desploma a apenas +USD 7,46 M (se pagaron USD 8M de transición para ganar un solo año)."
    )

    # Consigna 5
    h_c5 = doc.add_heading("Consigna 5: Evaluación del Contrato con Autonomy", level=2)
    h_c5.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Cuantificación del Costo de Oportunidad: El contrato a USD 27.500 fijo DESTRUYE USD 5,17 Millones de valor frente a no firmarlo.\n"
        "• Causa Financiera: En los Años 3, 4 y 5, el costo variable local de fabricar un LB es de USD 29.538, USD 29.413 y USD 29.623, arrojando margen operativo negativo.\n"
        "• Precio Umbral de Indiferencia: El precio mínimo que hace conveniente el contrato es USD 28.534 por unidad. Por debajo de ese valor destruye caja."
    )

    # Consigna 6
    h_c6 = doc.add_heading("Consigna 6: Costo de Playón y Transferencia de Inventarios", level=2)
    h_c6.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Al 25% y 30% anual: Se transfieren CERO (0) unidades en todos los años. Subir la tasa del 25% al 30% no genera ningún impacto.\n"
        "• Punto de Corte Analítico: La transferencia interanual recién aparece por debajo de una tasa del 8,8% anual (a 5% se transfieren 21.328 unidades). "
        "A cualquier costo mayor a ~8,8%, el modelo opera en régimen Just-in-Time."
    )
    plot_inv = os.path.join("plots", "fig3_sensibilidad_inventario.png")
    if os.path.exists(plot_inv):
        doc.add_picture(plot_inv, width=Inches(6.0))
        p_cap = doc.add_paragraph("Figura 5: Curva de Sensibilidad del Inventario Transferido vs Tasa de Mantenimiento en Playón.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.size = Pt(9.5)

    # Consigna 7
    h_c7 = doc.add_heading("Consigna 7: Recomendación Estratégica Integral (Minimax Regret)", level=2)
    h_c7.runs[0].font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph(
        "• Decisiones Robustas: Mantener Línea B en doble turno pleno los 5 años; abastecer 100% de la exportación; política de cero inventario interanual.\n"
        "• Decisiones Contingentes: Importación desde China y reconversión de Línea A dependen totalmente del tipo de cambio y de la demanda agraria.\n"
        "• Análisis Minimax Regret: La estrategia de Fabricación Local Flexible (S1) presenta el mínimo arrepentimiento máximo (USD 109,7 M vs USD 115,7 M de importar y USD 125,8 M de reequipar).\n"
        "• Hoja de Ruta Táctica: En Años 1 y 2 mantener la fábrica operativa en Zárate sin asumir costos irreversibles de despido o inversión; renegociar el precio con Autonomy a > USD 28.550; y evaluar la reconversión o importación recién al cierre del Año 2 una vez clarificado el nuevo régimen político-económico."
    )

    doc.save(docx_path)
    print(f"Document successfully created at: {docx_path}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "INFORME_EJECUTIVO_AUTOITBA.docx"
    create_styled_document(out)
