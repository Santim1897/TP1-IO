import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_plant_process(output_path="plots/fig0_proceso_planta.png"):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, "Diagrama de Flujo del Proceso Productivo - AutoITBA S.A.", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1F4E79')
    ax.text(6, 7.1, "Terminal Automotriz Zárate - Configuración de Líneas, Secciones y Turnos", 
            ha='center', va='center', fontsize=10, style='italic', color='#555555')

    # Styles
    box_blue = dict(boxstyle="round,pad=0.4", fc="#D9E1F2", ec="#2F5597", lw=1.5)
    box_green = dict(boxstyle="round,pad=0.4", fc="#E2EFDA", ec="#385723", lw=1.5)
    box_orange = dict(boxstyle="round,pad=0.4", fc="#FCE4D6", ec="#C65911", lw=1.5)
    box_gray = dict(boxstyle="round,pad=0.4", fc="#F2F2F2", ec="#7F7F7F", lw=1.5)
    box_red = dict(boxstyle="round,pad=0.4", fc="#F8CBAD", ec="#C00000", lw=2)

    # 4 Consecutive Sections
    sections = [
        ("Sección 1:\nChasis\n(Automatizado)", 2.0),
        ("Sección 2:\nPintura\n(Automatizado)", 4.5),
        ("Sección 3:\nMotor\n(Técnicos)", 7.0),
        ("Sección 4:\nDetalles Finales\n(Cuello de Botella)", 9.5)
    ]
    
    # Headers for stages
    for title, x_pos in sections:
        ax.text(x_pos, 6.2, title, ha='center', va='center', fontsize=9, fontweight='bold', bbox=box_gray)

    # Line A track
    ax.text(0.6, 4.8, "LÍNEA A\nLivianos (LB, LP)\nCap: 10k Mañana\n7.5k Tarde", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=box_blue)
    
    # Line A Section Dotaciones
    ax.text(2.0, 4.8, "1 Operario\nSupervisión", ha='center', va='center', fontsize=8, bbox=box_blue)
    ax.text(4.5, 4.8, "1 Operario\nSupervisión", ha='center', va='center', fontsize=8, bbox=box_blue)
    ax.text(7.0, 4.8, "2 Operarios\nTécnicos", ha='center', va='center', fontsize=8, bbox=box_blue)
    ax.text(9.5, 4.8, "5 Operarios\nAcabados", ha='center', va='center', fontsize=8, bbox=box_blue)
    
    # Line A Arrows
    for x_start in [1.3, 2.7, 5.2, 7.7]:
        ax.annotate('', xy=(x_start + 0.6, 4.8), xytext=(x_start, 4.8),
                    arrowprops=dict(arrowstyle="->", color="#2F5597", lw=1.5))

    # Line B track
    ax.text(0.6, 3.0, "LÍNEA B\nPick-ups y Livianos\nCap: 25k P / 30k L (M)\n18.75k P / 22.5k L (T)", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=box_green)
    
    # Line B Section Dotaciones
    ax.text(2.0, 3.0, "1 Operario\nSupervisión", ha='center', va='center', fontsize=8, bbox=box_green)
    ax.text(4.5, 3.0, "1 Operario\nSupervisión", ha='center', va='center', fontsize=8, bbox=box_green)
    ax.text(7.0, 3.0, "2 Operarios\nTécnicos", ha='center', va='center', fontsize=8, bbox=box_green)
    ax.text(9.5, 3.0, "7 Operarios\nAcabados", ha='center', va='center', fontsize=8, bbox=box_green)

    # Line B Arrows
    for x_start in [1.3, 2.7, 5.2, 7.7]:
        ax.annotate('', xy=(x_start + 0.6, 3.0), xytext=(x_start, 3.0),
                    arrowprops=dict(arrowstyle="->", color="#385723", lw=1.5))

    # Sindicato Box (Turno Tarde)
    ax.text(9.5, 1.8, "Dotación Sindical Conjunta (Turno Tarde):\n+5 Operarios de Peligrosidad (Supervisión común)", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color="#C00000", bbox=box_red)
    
    # Connections to Sindicato
    ax.annotate('', xy=(9.5, 2.4), xytext=(9.5, 2.1),
                arrowprops=dict(arrowstyle="->", color="#C00000", lw=1.5, ls="--"))
    ax.annotate('', xy=(9.5, 4.2), xytext=(9.5, 2.1),
                arrowprops=dict(arrowstyle="->", color="#C00000", lw=1.5, ls="--"))

    # Playón de Inventario y Distribución
    ax.text(11.2, 3.9, "PLAYÓN /\nDESPACHO\n\n• Mercado Local\n• Exportación\n• Autonomy\n• Agronegocios", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=box_orange)

    ax.annotate('', xy=(10.5, 3.9), xytext=(10.1, 4.8),
                arrowprops=dict(arrowstyle="->", color="#2F5597", lw=1.5))
    ax.annotate('', xy=(10.5, 3.9), xytext=(10.1, 3.0),
                arrowprops=dict(arrowstyle="->", color="#385723", lw=1.5))

    # Summary footer info
    summary_text = (
        "Totales Dotación Base: Línea A = 9 operarios/turno | Línea B = 11 operarios/turno | "
        "Turno Tarde: +5 operarios conjuntos\n"
        "Costos de Encendido por Turno: Línea A = ARS 500M/año | Línea B = ARS 800M/año (actualizados por inflación del 20% anual)"
    )
    ax.text(6, 0.6, summary_text, ha='center', va='center', fontsize=8, 
            bbox=dict(boxstyle="square,pad=0.5", fc="#FFFFFF", ec="#CCCCCC"))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print("Process diagram saved to:", output_path)

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "plots/fig0_proceso_planta.png"
    draw_plant_process(out)
