import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from model_engine import AutoITBAModel

def generate_charts_and_regret(output_dir="plots"):
    os.makedirs(output_dir, exist_ok=True)
    model = AutoITBAModel()
    
    # 1. Solve base and devaluation
    res_base = model.solve_model(scenario='base')
    res_dev = model.solve_model(scenario='devaluacion')
    
    # Chart 1: Profit Comparison by Year (Base vs Devaluation)
    years = [1, 2, 3, 4, 5]
    profits_base = [res_base['metrics_by_year'][t]['net_profit'] / 1e6 for t in years]
    profits_dev = [res_dev['metrics_by_year'][t]['net_profit'] / 1e6 for t in years]
    
    plt.figure(figsize=(10, 5))
    x = np.arange(len(years))
    width = 0.35
    
    plt.bar(x - width/2, profits_base, width, label='Escenario Base (REM)', color='#1F4E79')
    plt.bar(x + width/2, profits_dev, width, label='Escenario Devaluación Acelerada', color='#2CA02C')
    
    plt.xlabel('Año de Planificación', fontsize=11, fontweight='bold')
    plt.ylabel('Utilidad Neta Anual (Millones USD)', fontsize=11, fontweight='bold')
    plt.title('Comparativa de Utilidad Neta Anual: Escenario Base vs Devaluación', fontsize=13, fontweight='bold')
    plt.xticks(x, [f'Año {t}' for t in years])
    plt.legend(frameon=True)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig1_utilidad_base_vs_dev.png'), dpi=300)
    plt.close()
    
    # Chart 2: Production Mix by Model over 5 Years (Base Scenario)
    prod_by_model = {m: [] for m in model.models}
    for t in years:
        for m in model.models:
            tot = sum(res_base['production'][t][m][l, k] for l in model.lines for k in model.shifts)
            prod_by_model[m].append(tot)
            
    df_prod = pd.DataFrame(prod_by_model, index=[f'Año {t}' for t in years])
    plt.figure(figsize=(10, 6))
    bottom = np.zeros(len(years))
    colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#9013FE']
    for idx, m in enumerate(model.models):
        plt.bar(df_prod.index, df_prod[m], bottom=bottom, label=m, color=colors[idx])
        bottom += df_prod[m].values
        
    plt.xlabel('Año', fontsize=11, fontweight='bold')
    plt.ylabel('Unidades Producidas', fontsize=11, fontweight='bold')
    plt.title('Mix de Producción Anual por Modelo (Escenario Base)', fontsize=13, fontweight='bold')
    plt.legend(title='Modelo', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig2_mix_produccion_base.png'), dpi=300)
    plt.close()

    # Chart 3: Sensitivity to Inventory Holding Rate (Consigna 6)
    rates = np.linspace(0.0, 0.15, 31)
    inv_transfers = []
    profits_inv = []
    for r in rates:
        res_r = model.solve_model(scenario='base', inv_rate=r)
        tot_inv = sum(sum(res_r['inventory'][t].values()) for t in years)
        inv_transfers.append(tot_inv)
        profits_inv.append(res_r['objective_value'] / 1e6)
        
    fig, ax1 = plt.subplots(figsize=(10, 5))
    color = '#D0021B'
    ax1.set_xlabel('Tasa de Mantenimiento de Inventario (% del costo variable)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Inventario Total Transferido (Unidades)', color=color, fontsize=11, fontweight='bold')
    ax1.plot(rates * 100, inv_transfers, color=color, linewidth=2.5, marker='o', markersize=4, label='Inventario Transferido')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Annotate zero crossing
    zero_idx = np.where(np.array(inv_transfers) == 0)[0][0]
    cutoff_rate = rates[zero_idx] * 100
    ax1.axvline(x=cutoff_rate, color='black', linestyle=':', label=f'Corte: {cutoff_rate:.1f}%')
    ax1.annotate(f'Corte en {cutoff_rate:.1f}%\n(Inv = 0)', xy=(cutoff_rate, 0), xytext=(cutoff_rate + 1.5, 15000),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

    plt.title('Consigna 6: Sensibilidad del Inventario Transferido vs Tasa de Playón', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig3_sensibilidad_inventario.png'), dpi=300)
    plt.close()

    # Chart 4: Retooling Line A - Net Benefit by Year and Demand Scenario (Consigna 3)
    years_retool = [1, 2, 3, 4, 5]
    inv_val = 15e6  # using midpoint 15M USD
    
    # Base Demand
    res_no_ret_base = model.solve_model(scenario='base', pickup_demand_multiplier=1.0)
    gain_base = []
    for yr in years_retool:
        r = model.solve_model(scenario='base', pickup_demand_multiplier=1.0, retool_line_A_year=yr)
        gain_base.append((r['objective_value'] - res_no_ret_base['objective_value'] - inv_val) / 1e6)
        
    # Boom Demand
    res_no_ret_boom = model.solve_model(scenario='base', pickup_demand_multiplier=1.20)
    gain_boom = []
    for yr in years_retool:
        r = model.solve_model(scenario='base', pickup_demand_multiplier=1.20, retool_line_A_year=yr)
        gain_boom.append((r['objective_value'] - res_no_ret_boom['objective_value'] - inv_val) / 1e6)
        
    plt.figure(figsize=(10, 5))
    x = np.arange(len(years_retool))
    width = 0.35
    plt.bar(x - width/2, gain_base, width, label='Demanda Base (Inversión USD 15M)', color='#E74C3C')
    plt.bar(x + width/2, gain_boom, width, label='Boom Agropecuario +20% (Inversión USD 15M)', color='#27AE60')
    plt.axhline(0, color='black', linewidth=1)
    plt.xlabel('Año en que se realiza la Parada y Obra', fontsize=11, fontweight='bold')
    plt.ylabel('Beneficio Neto Incremental (Millones USD)', fontsize=11, fontweight='bold')
    plt.title('Consigna 3: Evaluación de Inversión y Año Óptimo de Reequipamiento Línea A', fontsize=13, fontweight='bold')
    plt.xticks(x, [f'Año {yr}' for yr in years_retool])
    plt.legend(frameon=True)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig4_reequipamiento_linea_A.png'), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 5. REGRET MATRIX (CONSIGNA 7)
    # -------------------------------------------------------------
    # Strategies (Decisions for Years 1 & 2):
    # S1: Estrategia Conservadora / Flexible (Producir localmente, no reequipar, renegociar Autonomy)
    # S2: Reequipar Línea A en Año 1 (Apostar a Pick-ups / Boom Agro)
    # S3: Importar Livianos desde China en Año 2
    #
    # Scenarios (Estados de la Naturaleza):
    # E1: Escenario Base Continuo (Demanda normal, TC REM)
    # E2: Escenario Devaluación Acelerada (TC devaluado, costos locales baratos)
    # E3: Boom Agropecuario (+20% demanda Pick-ups)
    # E4: Cierre Arancelario / Regulatorio en Año 3 (Shock de importación)
    
    # Payoff calculations (Utilidad Neta en Millones USD):
    # S1 payoffs:
    p_S1_E1 = res_base['objective_value'] / 1e6
    p_S1_E2 = res_dev['objective_value'] / 1e6
    p_S1_E3 = res_no_ret_boom['objective_value'] / 1e6
    p_S1_E4 = res_base['objective_value'] / 1e6  # immune to import shock
    
    # S2 payoffs (Reequipar Línea A en Año 1, inv 15M):
    p_S2_E1 = (model.solve_model(scenario='base', pickup_demand_multiplier=1.0, retool_line_A_year=1)['objective_value'] - 15e6) / 1e6
    p_S2_E2 = (model.solve_model(scenario='devaluacion', pickup_demand_multiplier=1.0, retool_line_A_year=1)['objective_value'] - 15e6) / 1e6
    p_S2_E3 = (model.solve_model(scenario='base', pickup_demand_multiplier=1.20, retool_line_A_year=1)['objective_value'] - 15e6) / 1e6
    p_S2_E4 = (model.solve_model(scenario='base', pickup_demand_multiplier=1.0, retool_line_A_year=1)['objective_value'] - 15e6) / 1e6
    
    # S3 payoffs (Importar China Año 2):
    p_S3_E1 = model.solve_model(scenario='base', china_import_active=True, china_import_start_year=2)['objective_value'] / 1e6
    p_S3_E2 = model.solve_model(scenario='devaluacion', china_import_active=True, china_import_start_year=2)['objective_value'] / 1e6
    p_S3_E3 = model.solve_model(scenario='base', pickup_demand_multiplier=1.20, china_import_active=True, china_import_start_year=2)['objective_value'] / 1e6
    p_S3_E4 = model.solve_model(scenario='base', china_import_active=True, china_import_start_year=2, china_stop_year=3, china_reopen_line_A=False)['objective_value'] / 1e6
    
    strategies = [
        "S1: Fabricación Local Flexible (Status Quo Optimizado)",
        "S2: Reequipamiento Línea A en Año 1 (Apuesta Pick-ups)",
        "S3: Importación Livianos China en Año 2 (Cierre Línea A)"
    ]
    scenarios_cols = [
        "E1: Base (REM)",
        "E2: Devaluación Acelerada",
        "E3: Boom Agro (+20%)",
        "E4: Cierre Regulatorio Año 3"
    ]
    
    payoffs = np.array([
        [p_S1_E1, p_S1_E2, p_S1_E3, p_S1_E4],
        [p_S2_E1, p_S2_E2, p_S2_E3, p_S2_E4],
        [p_S3_E1, p_S3_E2, p_S3_E3, p_S3_E4]
    ])
    
    df_payoffs = pd.DataFrame(payoffs, index=strategies, columns=scenarios_cols)
    
    # Regret matrix: R(i, j) = max_k(P(k, j)) - P(i, j)
    best_per_scenario = payoffs.max(axis=0)
    regret = best_per_scenario - payoffs
    df_regret = pd.DataFrame(regret, index=strategies, columns=scenarios_cols)
    df_regret['Max Regret (Arrepentimiento Máximo)'] = df_regret.max(axis=1)
    
    print("\nMATRIZ DE PAGOS (UTILIDAD EN MILLONES USD):")
    print(df_payoffs.round(2))
    
    print("\nMATRIZ DE ARREPENTIMIENTO (REGRET EN MILLONES USD):")
    print(df_regret.round(2))
    
    minimax_choice = df_regret['Max Regret (Arrepentimiento Máximo)'].idxmin()
    print(f"\nCRITERIO MINIMAX REGRET: La mejor estrategia es:\n>>> {minimax_choice} con un arrepentimiento máximo de ${df_regret.loc[minimax_choice, 'Max Regret (Arrepentimiento Máximo)']:.2f} M USD.")
    
    df_payoffs.to_csv(os.path.join(output_dir, 'matriz_pagos.csv'))
    df_regret.to_csv(os.path.join(output_dir, 'matriz_regret.csv'))
    print("Charts and matrices saved to:", output_dir)

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "plots"
    generate_charts_and_regret(out_dir)
