import os
import sys

def main():
    print("=" * 80)
    print("AUTOITBA S.A. - TRABAJO PRÁCTICO N° 1 DE INVESTIGACIÓN OPERATIVA")
    print("Planificación Estratégica de Producción a 5 Años (2026-2030)")
    print("ITBA - 2026 2C")
    print("=" * 80)
    
    # 1. Ensure Excel database exists
    excel_path = os.path.join("data", "AutoITBA_Parametros.xlsx")
    if not os.path.exists(excel_path):
        print(f"\n[1/3] Generando base de datos Excel en {excel_path}...")
        from src.generate_excel import build_excel
        build_excel(excel_path)
    else:
        print(f"\n[1/3] Base de datos Excel encontrada en {excel_path}.")
        
    # 2. Run Process Flowchart and Visualizations
    print("\n[2/3] Generando diagramas de proceso y gráficos analíticos...")
    from src.draw_process import draw_plant_process
    draw_plant_process(os.path.join("plots", "fig0_proceso_planta.png"))
    
    from src.generate_charts import generate_charts_and_regret
    generate_charts_and_regret(output_dir="plots")
    
    # 3. Run all experiments and display results
    print("\n[3/3] Ejecutando modelo de optimización para todas las consignas...")
    from src.run_experiments import run_all
    run_all()
    
    print("\n" + "=" * 80)
    print("EJECUCIÓN COMPLETADA EXITOSAMENTE.")
    print("Ver informe detallado en: INFORME_EJECUTIVO_AUTOITBA.md")
    print("=" * 80)

if __name__ == "__main__":
    main()
