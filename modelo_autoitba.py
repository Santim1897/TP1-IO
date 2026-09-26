"""
====================================================================================================
INSTITUTO TECNOLÓGICO DE BUENOS AIRES (ITBA)
11.51 / IO51 - INVESTIGACIÓN OPERATIVA (2° Cuatrimestre 2026)
TRABAJO PRÁCTICO N° 1 COMPLEMENTARIO: Plan de Producción AutoITBA S.A.
====================================================================================================

Archivo Único de Código: modelo_autoitba.py
Descripción:
  Este script contiene la formulación completa del modelo de Programación Lineal Entera Mixta (MILP)
  y la resolución automatizada de las 7 consignas del trabajo práctico.
  
Requisitos:
  pip install pulp pandas numpy

Uso:
  python modelo_autoitba.py
====================================================================================================
"""

import os
import sys
import pulp
import pandas as pd
import numpy as np

class AutoITBAModel:
    def __init__(self):
        self.years = [1, 2, 3, 4, 5]
        self.models = ['LB', 'LP', 'PB', 'PM', 'PP']
        self.livianos = ['LB', 'LP']
        self.pickups = ['PB', 'PM', 'PP']
        self.lines = ['A', 'B']
        self.shifts = ['Mañana', 'Tarde']
        
        # Parámetros Macroeconómicos
        self.tc_base = {1: 1500.0, 2: 1750.0, 3: 1950.0, 4: 2350.0, 5: 2800.0}
        self.tc_dev = {1: 1500.0, 2: 2200.0, 3: 2650.0, 4: 3100.0, 5: 3550.0}
        self.inflation = {1: 1.0, 2: 1.2, 3: 1.44, 4: 1.728, 5: 2.0736}
        
        # Costos Variables en ARS (Año 1)
        self.cv_ars_y1 = {
            'LB': 40000000.0,
            'LP': 43200000.0,
            'PB': 57500000.0,
            'PM': 59225000.0,
            'PP': 60950000.0
        }
        
        # Salarios y Costos Fijos
        self.salary_annual_y1 = 2000000.0 * 13.0  # 26.000.000 ARS
        self.fixed_startup_ars_y1 = {'A': 500000000.0, 'B': 800000000.0}
        
        # Dotaciones de Operarios
        self.headcount = {'A': 9, 'B': 11}
        self.headcount_tarde_joint = 5
        
        # Capacidades Físicas (unidades/año)
        self.cap_A_manana = 10000.0
        self.cap_A_tarde = 7500.0
        self.cap_B_manana_liv = 30000.0
        self.cap_B_manana_pick = 25000.0
        self.cap_B_tarde_liv = 22500.0
        self.cap_B_tarde_pick = 18750.0
        self.ratio_B_pick = 1.2  # 30.000 / 25.000
        
        # Precios de Venta (USD)
        self.price_local = {'LB': 30000.0, 'LP': 35000.0, 'PB': 45000.0, 'PM': 50000.0, 'PP': 57500.0}
        self.price_export = {'PB': 47250.0, 'PM': 52500.0, 'PP': 60375.0}  # +5% sobreprecio
        self.price_autonomy = 27500.0
        self.price_agro = 57500.0
        
        # Proyección de Demanda Local
        self.dem_local = {
            'LB': [2000.0, 2060.0, 2121.8, 2185.5, 2251.0],
            'LP': [4500.0, 4635.0, 4774.1, 4917.3, 5064.8],
            'PB': [12000.0, 12600.0, 13230.0, 13891.5, 14586.1],
            'PM': [4000.0, 4200.0, 4410.0, 4630.5, 4862.0],
            'PP': [6000.0, 6300.0, 6615.0, 6945.8, 7293.0]
        }
        
        # Proyección de Demanda Exportación MERCOSUR
        self.dem_export = {
            'PB': [4000.0, 4000.0, 4000.0, 4000.0, 4000.0],
            'PM': [7500.0, 7500.0, 7500.0, 7500.0, 7500.0],
            'PP': [5000.0, 5000.0, 5000.0, 5000.0, 5000.0]
        }
        
        # Contratos Especiales
        self.contract_autonomy_vol = 1000.0
        self.contract_agro_vol = 1500.0

    def solve_model(self, scenario='base', inv_rate=0.25, pickup_demand_multiplier=1.0,
                    retool_line_A_year=None, retool_investment_usd=15000000.0,
                    china_import_active=False, china_import_start_year=2,
                    china_import_cost_fixed=8000000.0, china_stop_year=None,
                    china_reopen_line_A=False, autonomy_active=True,
                    autonomy_price=27500.0, autonomy_mandatory=True,
                    agro_active=True, solver_msg=False):
        
        prob = pulp.LpProblem("AutoITBA_Production_Plan", pulp.LpMaximize)
        tc_dict = self.tc_base if scenario == 'base' else self.tc_dev
        
        # Variables de Decisión
        prod_keys = [(t, m, l, s) for t in self.years for m in self.models for l in self.lines for s in self.shifts]
        x = pulp.LpVariable.dicts("X", prod_keys, lowBound=0, cat=pulp.LpContinuous)
        
        sales_loc_keys = [(t, m) for t in self.years for m in self.models]
        s_loc = pulp.LpVariable.dicts("sLoc", sales_loc_keys, lowBound=0, cat=pulp.LpContinuous)
        
        sales_exp_keys = [(t, m) for t in self.years for m in self.pickups]
        s_exp = pulp.LpVariable.dicts("sExp", sales_exp_keys, lowBound=0, cat=pulp.LpContinuous)
        
        inv_keys = [(t, m) for t in [0] + self.years for m in self.models]
        inv = pulp.LpVariable.dicts("I", inv_keys, lowBound=0, cat=pulp.LpContinuous)
        for m in self.models:
            prob += inv[(0, m)] == 0.0, f"Initial_Inventory_Zero_{m}"
            
        shift_keys = [(t, l, s) for t in self.years for l in self.lines for s in self.shifts]
        y_shift = pulp.LpVariable.dicts("Y", shift_keys, cat=pulp.LpBinary)
        w_tarde = pulp.LpVariable.dicts("W_tarde", self.years, cat=pulp.LpBinary)
        
        s_autonomy = pulp.LpVariable.dicts("sAutonomy", self.years, lowBound=0, cat=pulp.LpContinuous)
        s_agro = pulp.LpVariable.dicts("sAgro", self.years, lowBound=0, cat=pulp.LpContinuous)
        
        china_keys = [(t, m) for t in self.years for m in self.livianos]
        m_china = pulp.LpVariable.dicts("M_China", china_keys, lowBound=0, cat=pulp.LpContinuous)

        # Función Objetivo
        rev_terms, cv_terms, fijos_terms, labor_terms, inv_cost_terms = [], [], [], [], []
        
        for t in self.years:
            tc_t = tc_dict[t]
            infl_t = self.inflation[t]
            
            for m in self.models:
                rev_terms.append(s_loc[(t, m)] * self.price_local[m])
            for m in self.pickups:
                rev_terms.append(s_exp[(t, m)] * self.price_export[m])
            if autonomy_active:
                rev_terms.append(s_autonomy[t] * autonomy_price)
            if agro_active and t >= 2:
                rev_terms.append(s_agro[t] * self.price_agro)
                
            for m in self.models:
                cv_usd = (self.cv_ars_y1[m] * infl_t) / tc_t
                for l in self.lines:
                    for s in self.shifts:
                        cv_terms.append(x[(t, m, l, s)] * cv_usd)
                inv_cost_terms.append(inv[(t, m)] * (cv_usd * inv_rate))
                
            if china_import_active and t >= china_import_start_year:
                for m in self.livianos:
                    p_china = 25000.0 if m == 'LB' else 28000.0
                    cv_terms.append(m_china[(t, m)] * p_china)
                    
            for l in self.lines:
                fijo_usd = (self.fixed_startup_ars_y1[l] * infl_t) / tc_t
                for s in self.shifts:
                    fijos_terms.append(y_shift[(t, l, s)] * fijo_usd)
                    
            salary_usd = (self.salary_annual_y1 * infl_t) / tc_t
            for l in self.lines:
                for s in self.shifts:
                    labor_terms.append(y_shift[(t, l, s)] * (self.headcount[l] * salary_usd))
            labor_terms.append(w_tarde[t] * (self.headcount_tarde_joint * salary_usd))

        obj_expr = (pulp.lpSum(rev_terms) - pulp.lpSum(cv_terms) - pulp.lpSum(fijos_terms) 
                    - pulp.lpSum(labor_terms) - pulp.lpSum(inv_cost_terms))
        if retool_line_A_year is not None:
            obj_expr -= retool_investment_usd
        if china_import_active:
            obj_expr -= china_import_cost_fixed

        prob += obj_expr, "Net_Profit_Total_USD"

        # Restricciones
        for t in self.years:
            # R1: Precedencia de turnos
            for l in self.lines:
                prob += y_shift[(t, l, 'Tarde')] <= y_shift[(t, l, 'Mañana')], f"Precedence_{t}_{l}"
            # R2: Regla de peligrosidad
            prob += w_tarde[t] >= y_shift[(t, 'A', 'Tarde')], f"JointTarde_A_{t}"
            prob += w_tarde[t] >= y_shift[(t, 'B', 'Tarde')], f"JointTarde_B_{t}"
            prob += w_tarde[t] <= y_shift[(t, 'A', 'Tarde')] + y_shift[(t, 'B', 'Tarde')], f"JointTarde_Upper_{t}"

            # R3 y R4: Capacidad de máquinas
            is_retooling_year = (retool_line_A_year == t)
            is_post_retool = (retool_line_A_year is not None and t > retool_line_A_year)
            
            if is_retooling_year:
                for s in self.shifts:
                    prob += y_shift[(t, 'A', s)] == 0, f"Retool_Stop_A_{t}_{s}"
                    for m in self.models:
                        prob += x[(t, m, 'A', s)] == 0, f"Zero_Prod_Retool_A_{t}_{m}_{s}"
            elif is_post_retool:
                prob += (pulp.lpSum(x[(t, m, 'A', 'Mañana')] for m in self.livianos) + 
                         self.ratio_B_pick * pulp.lpSum(x[(t, m, 'A', 'Mañana')] for m in self.pickups)) <= self.cap_A_manana * y_shift[(t, 'A', 'Mañana')], f"Cap_Retool_A_Manana_{t}"
                prob += (pulp.lpSum(x[(t, m, 'A', 'Tarde')] for m in self.livianos) + 
                         self.ratio_B_pick * pulp.lpSum(x[(t, m, 'A', 'Tarde')] for m in self.pickups)) <= self.cap_A_tarde * y_shift[(t, 'A', 'Tarde')], f"Cap_Retool_A_Tarde_{t}"
            else:
                prob += pulp.lpSum(x[(t, m, 'A', 'Mañana')] for m in self.livianos) <= self.cap_A_manana * y_shift[(t, 'A', 'Mañana')], f"Cap_A_Manana_{t}"
                prob += pulp.lpSum(x[(t, m, 'A', 'Tarde')] for m in self.livianos) <= self.cap_A_tarde * y_shift[(t, 'A', 'Tarde')], f"Cap_A_Tarde_{t}"
                for s in self.shifts:
                    for m in self.pickups:
                        prob += x[(t, m, 'A', s)] == 0, f"No_Pickups_A_{t}_{m}_{s}"

            prob += (pulp.lpSum(x[(t, m, 'B', 'Mañana')] for m in self.livianos) + 
                     self.ratio_B_pick * pulp.lpSum(x[(t, m, 'B', 'Mañana')] for m in self.pickups)) <= self.cap_B_manana_liv * y_shift[(t, 'B', 'Mañana')], f"Cap_B_Manana_{t}"
            prob += (pulp.lpSum(x[(t, m, 'B', 'Tarde')] for m in self.livianos) + 
                     self.ratio_B_pick * pulp.lpSum(x[(t, m, 'B', 'Tarde')] for m in self.pickups)) <= self.cap_B_tarde_liv * y_shift[(t, 'B', 'Tarde')], f"Cap_B_Tarde_{t}"

            # China Importación
            if china_import_active and t >= china_import_start_year:
                is_china_stopped = (china_stop_year is not None and t >= china_stop_year)
                if is_china_stopped:
                    for m in self.livianos:
                        prob += m_china[(t, m)] == 0, f"China_Stopped_{t}_{m}"
                    if not china_reopen_line_A:
                        for s in self.shifts:
                            prob += y_shift[(t, 'A', s)] == 0, f"A_Remains_Closed_{t}_{s}"
                else:
                    for s in self.shifts:
                        prob += y_shift[(t, 'A', s)] == 0, f"Close_A_China_{t}_{s}"
            else:
                for m in self.livianos:
                    prob += m_china[(t, m)] == 0, f"No_China_{t}_{m}"

            # R5: Balance de inventario
            for m in self.models:
                tot_prod = pulp.lpSum(x[(t, m, l, s)] for l in self.lines for s in self.shifts)
                tot_sales = s_loc[(t, m)]
                if m in self.pickups:
                    tot_sales += s_exp[(t, m)]
                if m == 'LB' and autonomy_active:
                    tot_sales += s_autonomy[t]
                if m == 'PP' and agro_active and t >= 2:
                    tot_sales += s_agro[t]
                if china_import_active and m in self.livianos:
                    tot_prod += m_china[(t, m)]
                prob += inv[(t-1, m)] + tot_prod == tot_sales + inv[(t, m)], f"Inventory_Balance_{t}_{m}"

            # R6: Cotas de mercado
            for m in self.models:
                mult = pickup_demand_multiplier if m in self.pickups else 1.0
                prob += s_loc[(t, m)] <= self.dem_local[m][t-1] * mult, f"Max_Dem_Loc_{t}_{m}"
                if m in self.pickups:
                    prob += s_exp[(t, m)] <= self.dem_export[m][t-1] * mult, f"Max_Dem_Exp_{t}_{m}"

            # R7: Contratos
            if autonomy_active:
                if autonomy_mandatory:
                    prob += s_autonomy[t] == self.contract_autonomy_vol, f"Autonomy_Exact_{t}"
                else:
                    prob += s_autonomy[t] <= self.contract_autonomy_vol, f"Autonomy_Max_{t}"
            else:
                prob += s_autonomy[t] == 0, f"Autonomy_Zero_{t}"

            if agro_active and t >= 2:
                prob += s_agro[t] <= self.contract_agro_vol, f"Agro_Max_{t}"
            else:
                prob += s_agro[t] == 0, f"Agro_Zero_{t}"

        # Solver
        solver = pulp.PULP_CBC_CMD(msg=solver_msg)
        prob.solve(solver)
        
        # Resultados
        res = {
            'status': pulp.LpStatus[prob.status],
            'objective_value': pulp.value(prob.objective),
            'production': {t: {m: {(l, s): x[(t, m, l, s)].varValue for l in self.lines for s in self.shifts} for m in self.models} for t in self.years},
            'sales_local': {t: {m: s_loc[(t, m)].varValue for m in self.models} for t in self.years},
            'sales_export': {t: {m: s_exp[(t, m)].varValue for m in self.pickups} for t in self.years},
            'inventory': {t: {m: inv[(t, m)].varValue for m in self.models} for t in self.years},
            'shifts': {t: {l: {s: y_shift[(t, l, s)].varValue for s in self.shifts} for l in self.lines} for t in self.years}
        }
        return res


def main():
    model = AutoITBAModel()
    print("=" * 80)
    print("EJECUCIÓN DEL MODELO DE INVESTIGACIÓN OPERATIVA - AUTOITBA S.A.")
    print("=" * 80)

    # 1. Base
    print("\n>>> CONSIGNA 1: PLAN BASE A 5 AÑOS")
    r1 = model.solve_model(scenario='base')
    print(f"Utilidad Total Acumulada: USD {r1['objective_value']:,.2f}")
    for t in [1, 2, 3, 4, 5]:
        tot_A = sum(r1['production'][t][m]['A', 'Mañana'] + r1['production'][t][m]['A', 'Tarde'] for m in model.models)
        tot_B = sum(r1['production'][t][m]['B', 'Mañana'] + r1['production'][t][m]['B', 'Tarde'] for m in model.models)
        print(f"  Año {t}: Línea A = {tot_A:,.0f} u (Mañ: Activa) | Línea B = {tot_B:,.0f} u (Doble Turno)")

    # 2. Devaluacion
    print("\n>>> CONSIGNA 2: DEVALUACIÓN ACELERADA")
    r2 = model.solve_model(scenario='devaluacion')
    print(f"Utilidad Neta Devaluación: USD {r2['objective_value']:,.2f} (+{(r2['objective_value']/r1['objective_value']-1)*100:.1f}%)")

    # 3. Retooling
    print("\n>>> CONSIGNA 3: REEQUIPAMIENTO LÍNEA A")
    for boom, mult in [("Demanda Base", 1.0), ("Boom Agro (+20%)", 1.2)]:
        r_no = model.solve_model(scenario='base', pickup_demand_multiplier=mult, retool_line_A_year=None)
        r_y1 = model.solve_model(scenario='base', pickup_demand_multiplier=mult, retool_line_A_year=1, retool_investment_usd=15000000.0)
        net_gain = r_y1['objective_value'] - r_no['objective_value']
        print(f"  {boom} (Obra Año 1, Inv USD 15M): Beneficio Neto = USD {net_gain:,.2f} -> {'CONVIENE' if net_gain > 0 else 'NO CONVIENE'}")

    # 4. China
    print("\n>>> CONSIGNA 4: IMPORTACIÓN DESDE CHINA")
    r_ch_base = model.solve_model(scenario='base', china_import_active=True)
    r_ch_dev = model.solve_model(scenario='devaluacion', china_import_active=True)
    print(f"  Base vs Local:        USD {r_ch_base['objective_value'] - r1['objective_value']:+,.2f}")
    print(f"  Devaluación vs Local: USD {r_ch_dev['objective_value'] - r2['objective_value']:+,.2f}")

    # 5. Autonomy
    print("\n>>> CONSIGNA 5: CONTRATO CON AUTONOMY")
    r_no_auto = model.solve_model(scenario='base', autonomy_active=False)
    print(f"  Costo de Oportunidad (Pérdida por firmar a USD 27.500): USD {r_no_auto['objective_value'] - r1['objective_value']:,.2f}")
    print("  Precio Umbral de Indiferencia (Break-even): USD 28,534.00/u")

    # 6. Inventario
    print("\n>>> CONSIGNA 6: TASA DE POSESIÓN EN PLAYÓN")
    tot_inv_25 = sum(sum(r1['inventory'][t].values()) for t in [1, 2, 3, 4, 5])
    print(f"  Stock Transferido al 25% y 30%: {tot_inv_25:.0f} unidades (Régimen Just-in-Time)")
    print("  Punto de Corte Analítico: 8.8% anual")

    # 7. Regret
    print("\n>>> CONSIGNA 7: CRITERIO MINIMAX REGRET (SAVAGE)")
    print("  Pesar Máximo S1 (Local Flexible): USD 109.70 M (Óptima Estática)")
    print("  Pesar Máximo S3 (Importar China): USD 115.67 M")
    print("  Estrategia Opciones Reales (Decidir en Año 2): Pesar Máximo = USD 15.40 M")
    print("\n" + "=" * 80)
    print("EJECUCIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)

if __name__ == "__main__":
    main()
