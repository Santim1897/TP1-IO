import os
import sys
import pandas as pd
import numpy as np

# Ensure model engine is accessible
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from model_engine import AutoITBAModel

def run_all():
    model = AutoITBAModel()
    
    print("================================================================================")
    print("CONSIGNA 1: MODELO BASE (5 AÑOS)")
    print("================================================================================")
    res_base = model.solve_model(scenario='base')
    print(f"Status: {res_base['status']}")
    print(f"Utilidad Neta Total (USD): ${res_base['objective_value']:,.2f}")
    
    # Yearly breakdown
    for t in [1, 2, 3, 4, 5]:
        print(f"\n--- AÑO {t} (TC = {model.tc_base[t]} ARS/USD) ---")
        print("Turnos activos:")
        for l in model.lines:
            for k in model.shifts:
                val = res_base['shifts'][t][l][k]
                if val > 0.5:
                    print(f"  - Línea {l}, Turno {k}: ACTIVO")
        print(f"W_tarde: {res_base['w_tarde'][t]}")
        
        print("Producción por modelo y línea:")
        for m in model.models:
            prod_A = sum(res_base['production'][t][m]['A', k] for k in model.shifts)
            prod_B = sum(res_base['production'][t][m]['B', k] for k in model.shifts)
            tot_prod = prod_A + prod_B
            print(f"  {m:2s}: Total={tot_prod:8.1f} | Línea A={prod_A:8.1f} | Línea B={prod_B:8.1f}")
            
        print("Ventas y Demanda:")
        for m in model.models:
            v_loc = res_base['sales_local'][t][m]
            d_loc = model.dem_local[m][t-1]
            print(f"  {m:2s} Local: {v_loc:8.1f} / {d_loc:8.1f} ({v_loc/d_loc*100:.1f}%)", end="")
            if m in model.pickups:
                v_exp = res_base['sales_export'][t][m]
                d_exp = model.dem_export[m][t-1]
                print(f" | Export: {v_exp:8.1f} / {d_exp:8.1f} ({v_exp/d_exp*100:.1f}%)", end="")
            if m == 'LB':
                print(f" | Autonomy: {res_base['sales_autonomy'][t]:8.1f} / 1000", end="")
            if m == 'PP' and t >= 2:
                print(f" | Agro: {res_base['sales_agro'][t]:8.1f} / 1500", end="")
            print()
            
        print("Inventario final:", {m: f"{res_base['inventory'][t][m]:.1f}" for m in model.models})
        metrics = res_base['metrics_by_year'][t]
        print(f"Financiero: Ingresos=${metrics['revenue']:,.0f} | CV=${metrics['cost_variable']:,.0f} | Fijos=${metrics['cost_fixed_startup']:,.0f} | Laboral=${metrics['cost_labor']:,.0f} | Utilidad=${metrics['net_profit']:,.0f}")

    print("\n================================================================================")
    print("CONSIGNA 2: EVALUACIÓN DEVALUACIÓN (ESCENARIO BASE VS DEVALUACIÓN)")
    print("================================================================================")
    res_dev = model.solve_model(scenario='devaluacion')
    print(f"Status Devaluación: {res_dev['status']}")
    print(f"Utilidad Neta Base:        ${res_base['objective_value']:,.2f}")
    print(f"Utilidad Neta Devaluación: ${res_dev['objective_value']:,.2f}")
    diff_dev = res_dev['objective_value'] - res_base['objective_value']
    print(f"Diferencia (Dev - Base):   ${diff_dev:,.2f} ({diff_dev/res_base['objective_value']*100:+.2f}%)")
    
    print("\nComparación de Turnos y Producción:")
    for t in [1, 2, 3, 4, 5]:
        print(f"\nAño {t}:")
        print(f"  Turnos Base: Línea A={res_base['shifts'][t]['A']}, Línea B={res_base['shifts'][t]['B']}")
        print(f"  Turnos Dev:  Línea A={res_dev['shifts'][t]['A']}, Línea B={res_dev['shifts'][t]['B']}")
        tot_loc_base = sum(res_base['sales_local'][t][m] for m in model.models)
        tot_exp_base = sum(res_base['sales_export'][t][m] for m in model.pickups)
        tot_loc_dev = sum(res_dev['sales_local'][t][m] for m in model.models)
        tot_exp_dev = sum(res_dev['sales_export'][t][m] for m in model.pickups)
        print(f"  Ventas Base -> Local: {tot_loc_base:,.1f}, Export: {tot_exp_base:,.1f}")
        print(f"  Ventas Dev  -> Local: {tot_loc_dev:,.1f}, Export: {tot_exp_dev:,.1f}")
        
    print("\n================================================================================")
    print("CONSIGNA 3: REEQUIPAMIENTO LÍNEA A")
    print("================================================================================")
    # Testing retooling year 1 to 5, at base demand and boom agro (+20%)
    for boom_name, mult in [("Demanda Base", 1.0), ("Boom Agro (+20% Demanda Pick-ups)", 1.20)]:
        print(f"\n--- {boom_name} ---")
        res_no_retool = model.solve_model(scenario='base', pickup_demand_multiplier=mult, retool_line_A_year=None)
        base_profit = res_no_retool['objective_value']
        print(f"Sin reequipamiento: Utilidad Bruta = ${base_profit:,.2f}")
        
        for y_retool in [1, 2, 3, 4, 5]:
            res_ret = model.solve_model(scenario='base', pickup_demand_multiplier=mult, retool_line_A_year=y_retool, retool_investment_usd=0.0)
            gross_profit = res_ret['objective_value']
            gross_gain = gross_profit - base_profit
            print(f"  Obra en Año {y_retool}: Ganancia Bruta Operativa Incremental = ${gross_gain:,.2f}")
            for inv in [12000000.0, 15000000.0, 18000000.0]:
                net_gain = gross_gain - inv
                print(f"    Inv ${inv/1e6:.0f}M -> Beneficio Neto = ${net_gain:,.2f} | {'CONVIENE' if net_gain > 0 else 'NO CONVIENE'}")

    print("\n================================================================================")
    print("CONSIGNA 4: IMPORTACIÓN DESDE CHINA")
    print("================================================================================")
    # Base scenario
    res_china_base = model.solve_model(scenario='base', china_import_active=True, china_import_start_year=2, china_import_cost_fixed=8000000.0)
    print(f"Escenario Base:")
    print(f"  Sin Importar (Base): ${res_base['objective_value']:,.2f}")
    print(f"  Con Importación:     ${res_china_base['objective_value']:,.2f}")
    diff_china_base = res_china_base['objective_value'] - res_base['objective_value']
    print(f"  Diferencia:          ${diff_china_base:,.2f} -> {'CONVIENE' if diff_china_base > 0 else 'NO CONVIENE'}")
    
    # Devaluacion scenario
    res_china_dev = model.solve_model(scenario='devaluacion', china_import_active=True, china_import_start_year=2, china_import_cost_fixed=8000000.0)
    print(f"\nEscenario Devaluación:")
    print(f"  Sin Importar (Dev):  ${res_dev['objective_value']:,.2f}")
    print(f"  Con Importación:     ${res_china_dev['objective_value']:,.2f}")
    diff_china_dev = res_china_dev['objective_value'] - res_dev['objective_value']
    print(f"  Diferencia:          ${diff_china_dev:,.2f} -> {'CONVIENE' if diff_china_dev > 0 else 'NO CONVIENE'}")

    # Risk: Cierre de importaciones en Año 3
    print("\nRiesgo Regulatorio: Cierre de importaciones en Año 3")
    # Subcase A: Importaciones se cierran en Año 3 y NO se puede reabrir Línea A (se pierden livianos años 3-5)
    res_china_risk_closed = model.solve_model(scenario='base', china_import_active=True, china_import_start_year=2, china_stop_year=3, china_reopen_line_A=False, china_import_cost_fixed=8000000.0)
    print(f"  Cierre en Año 3 (Sin reapertura Línea A): ${res_china_risk_closed['objective_value']:,.2f} (Pérdida vs Base: ${res_china_risk_closed['objective_value'] - res_base['objective_value']:,.2f})")
    # Subcase B: Importaciones se cierran en Año 3 pero se reabre Línea A
    res_china_risk_reopen = model.solve_model(scenario='base', china_import_active=True, china_import_start_year=2, china_stop_year=3, china_reopen_line_A=True, china_import_cost_fixed=8000000.0)
    print(f"  Cierre en Año 3 (Con reapertura Línea A): ${res_china_risk_reopen['objective_value']:,.2f} (Pérdida vs Base: ${res_china_risk_reopen['objective_value'] - res_base['objective_value']:,.2f})")

    print("\n================================================================================")
    print("CONSIGNA 5: CONTRATO AUTONOMY")
    print("================================================================================")
    # What if Autonomy is freed up? (autonomy_active = False)
    res_no_autonomy = model.solve_model(scenario='base', autonomy_active=False)
    print(f"Utilidad con Contrato Autonomy (USD 27,500): ${res_base['objective_value']:,.2f}")
    print(f"Utilidad liberando capacidad (Sin Autonomy):  ${res_no_autonomy['objective_value']:,.2f}")
    cost_oportunidad = res_no_autonomy['objective_value'] - res_base['objective_value']
    print(f"Diferencia (Sin Autonomy - Con Autonomy):     ${cost_oportunidad:,.2f}")
    if cost_oportunidad > 0:
        print(f"  -> Conviene liberar la capacidad: costo de oportunidad positivo de ${cost_oportunidad:,.2f}")
    else:
        print(f"  -> El contrato genera una ganancia neta incremental de ${-cost_oportunidad:,.2f} respecto a no tenerlo.")
        
    # Find break-even price (precio umbral de conveniencia)
    # Binary search or sweep
    low_p = 10000.0
    high_p = 35000.0
    target_obj = res_no_autonomy['objective_value']
    for _ in range(30):
        mid_p = (low_p + high_p) / 2.0
        res_mid = model.solve_model(scenario='base', autonomy_price=mid_p, autonomy_mandatory=True)
        if res_mid['objective_value'] >= target_obj:
            high_p = mid_p
        else:
            low_p = mid_p
    threshold_price = (low_p + high_p) / 2.0
    print(f"Precio umbral de conveniencia para Autonomy: ${threshold_price:,.2f} USD/unidad")
    
    # Also evaluate if autonomy is optional (<= 1000) at 27500
    res_opt_autonomy = model.solve_model(scenario='base', autonomy_mandatory=False, autonomy_price=27500.0)
    print(f"Si el contrato fuera opcional (vender hasta 1000 unidades si conviene a USD 27,500):")
    print(f"  Utilidad: ${res_opt_autonomy['objective_value']:,.2f}")
    print(f"  Unidades vendidas a Autonomy por año:", [res_opt_autonomy['sales_autonomy'][t] for t in [1, 2, 3, 4, 5]])

    print("\n================================================================================")
    print("CONSIGNA 6: COSTO DE PLAYÓN E INVENTARIO")
    print("================================================================================")
    # Check rate 25% vs 30%
    res_inv_25 = model.solve_model(scenario='base', inv_rate=0.25)
    res_inv_30 = model.solve_model(scenario='base', inv_rate=0.30)
    print(f"Tasa 25%: Utilidad = ${res_inv_25['objective_value']:,.2f} | Inventario total = {sum(sum(res_inv_25['inventory'][t].values()) for t in [1, 2, 3, 4, 5])}")
    print(f"Tasa 30%: Utilidad = ${res_inv_30['objective_value']:,.2f} | Inventario total = {sum(sum(res_inv_30['inventory'][t].values()) for t in [1, 2, 3, 4, 5])}")
    
    # Check in what situations inventory is used:
    # Let's test with tighter capacity (e.g. Turno Tarde not available or capacity constrained)
    # Or test continuous rate sweep
    rates = np.linspace(0.0, 0.40, 41)
    inv_use = []
    for r in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        res_r = model.solve_model(scenario='base', inv_rate=r)
        tot_inv = sum(sum(res_r['inventory'][t].values()) for t in [1, 2, 3, 4, 5])
        print(f"  Tasa {r*100:4.1f}%: Inventario total transferido = {tot_inv:,.1f} unidades | Utilidad = ${res_r['objective_value']:,.2f}")

    print("\n================================================================================")
    print("CONSIGNA 7: ANÁLISIS ESTRATÉGICO Y MATRIZ DE REGRET")
    print("================================================================================")
    # Compare key decisions across Base, Devaluacion, Boom Agro, China Open, China Ban
    print("Calculando matriz de pagos y arrepentimiento...")

if __name__ == "__main__":
    run_all()
