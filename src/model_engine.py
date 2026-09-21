import os
import pulp
import pandas as pd
import numpy as np

class AutoITBAModel:
    def __init__(self, excel_path=None):
        self.excel_path = excel_path
        self.years = [1, 2, 3, 4, 5]
        self.models = ['LB', 'LP', 'PB', 'PM', 'PP']
        self.livianos = ['LB', 'LP']
        self.pickups = ['PB', 'PM', 'PP']
        self.lines = ['A', 'B']
        self.shifts = ['Mañana', 'Tarde']
        
        # Load parameters
        self.load_parameters()

    def load_parameters(self):
        if self.excel_path and os.path.exists(self.excel_path):
            # Read from Excel
            xls = pd.ExcelFile(self.excel_path)
            df_macro = pd.read_excel(xls, 'Macro_y_TipoCambio')
            df_cap = pd.read_excel(xls, 'Capacidad_Dotacion')
            df_costs = pd.read_excel(xls, 'Costos_Operativos')
            df_dem = pd.read_excel(xls, 'Demanda_y_Precios')
            
        # Standard parameters
        self.tc_base = {1: 1500.0, 2: 1750.0, 3: 1950.0, 4: 2350.0, 5: 2800.0}
        self.tc_dev = {1: 1500.0, 2: 2200.0, 3: 2650.0, 4: 3100.0, 5: 3550.0}
        self.inflation = {1: 1.0, 2: 1.2, 3: 1.44, 4: 1.728, 5: 2.0736}
        
        # Cost parameters (Year 1 ARS)
        self.cv_ars_y1 = {
            'LB': 40000000.0,
            'LP': 43200000.0,
            'PB': 57500000.0,
            'PM': 59225000.0,
            'PP': 60950000.0
        }
        
        self.salary_monthly_y1 = 2000000.0
        self.salary_annual_y1 = self.salary_monthly_y1 * 13.0  # 26,000,000 ARS
        
        self.fixed_startup_ars_y1 = {
            'A': 500000000.0,
            'B': 800000000.0
        }
        
        # Headcounts
        self.headcount = {
            'A': 9,  # 1 chasis + 1 pintura + 2 motor + 5 detalles
            'B': 11  # 1 chasis + 1 pintura + 2 motor + 7 detalles
        }
        self.headcount_tarde_joint = 5
        
        # Capacities (units/year)
        self.cap_A_manana = 10000.0
        self.cap_A_tarde = 7500.0
        self.cap_B_manana_liv = 30000.0
        self.cap_B_manana_pick = 25000.0
        self.cap_B_tarde_liv = 22500.0
        self.cap_B_tarde_pick = 18750.0
        self.ratio_B_pick = 1.2  # 30000 / 25000
        
        # Prices (USD)
        self.price_local = {
            'LB': 30000.0,
            'LP': 35000.0,
            'PB': 45000.0,
            'PM': 50000.0,
            'PP': 57500.0
        }
        self.price_export = {
            'PB': 47250.0,
            'PM': 52500.0,
            'PP': 60375.0
        }
        self.price_autonomy = 27500.0
        self.price_agro = 57500.0
        
        # Demands (Year 1 to 5)
        # Local growth: 3% livianos, 5% pick-ups
        self.dem_local = {
            'LB': [2000.0, 2060.0, 2121.8, 2185.5, 2251.0],
            'LP': [4500.0, 4635.0, 4774.1, 4917.3, 5064.8],
            'PB': [12000.0, 12600.0, 13230.0, 13891.5, 14586.1],
            'PM': [4000.0, 4200.0, 4410.0, 4630.5, 4862.0],
            'PP': [6000.0, 6300.0, 6615.0, 6945.8, 7293.0]
        }
        
        # Export constant
        self.dem_export = {
            'PB': [4000.0, 4000.0, 4000.0, 4000.0, 4000.0],
            'PM': [7500.0, 7500.0, 7500.0, 7500.0, 7500.0],
            'PP': [5000.0, 5000.0, 5000.0, 5000.0, 5000.0]
        }
        
        # Special contracts
        self.contract_autonomy_vol = 1000.0  # LB years 1-5
        self.contract_agro_vol = 1500.0      # PP years 2-5

    def solve_model(self,
                    scenario='base',              # 'base' or 'devaluacion'
                    inv_rate=0.25,                # inventory cost rate
                    autonomy_mandatory=True,      # whether autonomy is a commitment
                    autonomy_price=None,          # override autonomy price
                    autonomy_active=True,         # whether autonomy is enabled
                    agro_active=True,             # whether agronegocios is enabled
                    pickup_demand_multiplier=1.0, # for boom agro (+20% -> 1.20)
                    retool_line_A_year=None,      # year Line A is stopped for retooling (1-5), or None
                    retool_investment_usd=0.0,    # investment cost in USD
                    china_import_active=False,    # whether China import is enabled
                    china_import_start_year=2,    # year China import starts
                    china_import_cost_fixed=8000000.0, # one-time transition cost
                    china_stop_year=None,         # year China imports are halted (e.g. 3)
                    china_reopen_line_A=False     # if Line A can reopen after China ban
                    ):
        
        tc = self.tc_base if scenario == 'base' else self.tc_dev
        p_autonomy = self.price_autonomy if autonomy_price is None else autonomy_price
        
        prob = pulp.LpProblem(f"AutoITBA_{scenario}", pulp.LpMaximize)
        
        # Variables
        # Production X(m, l, k, t)
        X = {}
        for m in self.models:
            for l in self.lines:
                for k in self.shifts:
                    for t in self.years:
                        X[m, l, k, t] = pulp.LpVariable(f"X_{m}_{l}_{k}_{t}", lowBound=0, cat=pulp.LpContinuous)
                        
        # Shift activation Y(l, k, t)
        Y = {}
        for l in self.lines:
            for k in self.shifts:
                for t in self.years:
                    Y[l, k, t] = pulp.LpVariable(f"Y_{l}_{k}_{t}", cat=pulp.LpBinary)
                    
        # Evening shift indicator W_tarde(t)
        W_tarde = {}
        for t in self.years:
            W_tarde[t] = pulp.LpVariable(f"W_tarde_{t}", cat=pulp.LpBinary)
            
        # Sales Local and Export
        S_local = {}
        for m in self.models:
            for t in self.years:
                S_local[m, t] = pulp.LpVariable(f"S_local_{m}_{t}", lowBound=0, cat=pulp.LpContinuous)
                
        S_export = {}
        for m in self.pickups:
            for t in self.years:
                S_export[m, t] = pulp.LpVariable(f"S_export_{m}_{t}", lowBound=0, cat=pulp.LpContinuous)
                
        # Contracts
        S_autonomy = {}
        for t in self.years:
            S_autonomy[t] = pulp.LpVariable(f"S_autonomy_{t}", lowBound=0, cat=pulp.LpContinuous)
            
        S_agro = {}
        for t in self.years:
            S_agro[t] = pulp.LpVariable(f"S_agro_{t}", lowBound=0, cat=pulp.LpContinuous)
            
        # Inventory I(m, t)
        I = {}
        for m in self.models:
            for t in [0] + self.years:
                if t == 0:
                    I[m, t] = 0.0  # Initial inventory is 0
                else:
                    I[m, t] = pulp.LpVariable(f"I_{m}_{t}", lowBound=0, cat=pulp.LpContinuous)
                    
        # Optional: China imports (Consigna 4)
        M_china = {}
        for m in self.livianos:
            for t in self.years:
                M_china[m, t] = pulp.LpVariable(f"M_china_{m}_{t}", lowBound=0, cat=pulp.LpContinuous)

        # -------------------------------------------------------------
        # OBJECTIVE FUNCTION
        # -------------------------------------------------------------
        rev_terms = []
        cost_terms = []
        
        for t in self.years:
            # Revenues
            # Local sales
            for m in self.models:
                rev_terms.append(self.price_local[m] * S_local[m, t])
            # Export sales
            for m in self.pickups:
                rev_terms.append(self.price_export[m] * S_export[m, t])
            # Contracts
            if autonomy_active:
                rev_terms.append(p_autonomy * S_autonomy[t])
            if agro_active and t >= 2:
                rev_terms.append(self.price_agro * S_agro[t])
                
            # Costs
            # Variable production costs
            for m in self.models:
                cv_usd = (self.cv_ars_y1[m] * self.inflation[t]) / tc[t]
                for l in self.lines:
                    for k in self.shifts:
                        cost_terms.append(cv_usd * X[m, l, k, t])
                        
            # Fixed startup costs
            cf_A_usd = (self.fixed_startup_ars_y1['A'] * self.inflation[t]) / tc[t]
            cf_B_usd = (self.fixed_startup_ars_y1['B'] * self.inflation[t]) / tc[t]
            for k in self.shifts:
                cost_terms.append(cf_A_usd * Y['A', k, t])
                cost_terms.append(cf_B_usd * Y['B', k, t])
                
            # Labor costs
            sal_usd = (self.salary_annual_y1 * self.inflation[t]) / tc[t]
            for k in self.shifts:
                cost_terms.append(self.headcount['A'] * sal_usd * Y['A', k, t])
                cost_terms.append(self.headcount['B'] * sal_usd * Y['B', k, t])
            # Evening joint surcharge
            cost_terms.append(self.headcount_tarde_joint * sal_usd * W_tarde[t])
            
            # Inventory holding costs
            for m in self.models:
                cv_usd = (self.cv_ars_y1[m] * self.inflation[t]) / tc[t]
                h_usd = inv_rate * cv_usd
                cost_terms.append(h_usd * I[m, t])
                
            # China import costs (Consigna 4)
            if china_import_active and t >= china_import_start_year:
                cif_cost = {'LB': 25000.0, 'LP': 28000.0}
                for m in self.livianos:
                    cost_terms.append(cif_cost[m] * M_china[m, t])
                    
        # Fixed one-time costs
        total_revenue = pulp.lpSum(rev_terms)
        total_cost = pulp.lpSum(cost_terms)
        
        constant_penalty = 0.0
        if retool_line_A_year is not None:
            constant_penalty += retool_investment_usd
        if china_import_active:
            constant_penalty += china_import_cost_fixed
            
        prob += total_revenue - total_cost - constant_penalty, "Total_Profit_USD"
        
        # -------------------------------------------------------------
        # CONSTRAINTS
        # -------------------------------------------------------------
        for t in self.years:
            # 1. Inventory Balance
            for m in self.models:
                # Inflow: Inventory t-1 + Local Production + Imports (if any)
                inflow = I[m, t-1] + pulp.lpSum(X[m, l, k, t] for l in self.lines for k in self.shifts)
                if china_import_active and m in self.livianos and t >= china_import_start_year:
                    inflow += M_china[m, t]
                    
                # Outflow: Sales + Inventory t
                outflow = S_local[m, t] + I[m, t]
                if m in self.pickups:
                    outflow += S_export[m, t]
                if m == 'LB' and autonomy_active:
                    outflow += S_autonomy[t]
                if m == 'PP' and agro_active and t >= 2:
                    outflow += S_agro[t]
                    
                prob += inflow == outflow, f"InvBalance_{m}_{t}"
                
            # 2. Demand Limits
            for m in self.models:
                prob += S_local[m, t] <= self.dem_local[m][t-1] * (pickup_demand_multiplier if m in self.pickups else 1.0), f"DemLocal_{m}_{t}"
            for m in self.pickups:
                prob += S_export[m, t] <= self.dem_export[m][t-1] * pickup_demand_multiplier, f"DemExport_{m}_{t}"
                
            # Contracts
            if autonomy_active:
                if autonomy_mandatory:
                    prob += S_autonomy[t] == self.contract_autonomy_vol, f"Contract_Autonomy_{t}"
                else:
                    prob += S_autonomy[t] <= self.contract_autonomy_vol, f"Contract_Autonomy_Max_{t}"
            else:
                prob += S_autonomy[t] == 0, f"Contract_Autonomy_Zero_{t}"
                
            if agro_active:
                if t >= 2:
                    prob += S_agro[t] <= self.contract_agro_vol, f"Contract_Agro_Max_{t}"
                else:
                    prob += S_agro[t] == 0, f"Contract_Agro_Zero_{t}"
            else:
                prob += S_agro[t] == 0, f"Contract_Agro_Zero_{t}"

            # China Import restrictions
            if not china_import_active or t < china_import_start_year:
                for m in self.livianos:
                    prob += M_china[m, t] == 0, f"NoChinaImport_{m}_{t}"
            elif china_stop_year is not None and t >= china_stop_year:
                for m in self.livianos:
                    prob += M_china[m, t] == 0, f"ChinaImportStopped_{m}_{t}"

            # If China import active, does company abandon local production of livianos from year 2?
            if china_import_active and t >= china_import_start_year:
                if not (china_stop_year is not None and t >= china_stop_year and china_reopen_line_A):
                    # Abandon local production of livianos
                    for m in self.livianos:
                        for l in self.lines:
                            for k in self.shifts:
                                prob += X[m, l, k, t] == 0, f"AbandonLivianos_{m}_{l}_{k}_{t}"

            # 3. Line Retooling logic (Consigna 3)
            # If Line A is retooled in retool_line_A_year:
            # During retool year, capacity of Line A = 0
            # After retool year, Line A can produce pick-ups!
            is_retool_year = (retool_line_A_year == t)
            is_post_retool = (retool_line_A_year is not None and t > retool_line_A_year)
            
            # Line A Capacity
            if is_retool_year:
                for k in self.shifts:
                    prob += Y['A', k, t] == 0, f"LineA_ShutDown_{k}_{t}"
                    for m in self.models:
                        prob += X[m, 'A', k, t] == 0, f"LineA_ZeroProd_{m}_{k}_{t}"
            else:
                if not is_post_retool:
                    # Line A only livianos
                    for m in self.pickups:
                        for k in self.shifts:
                            prob += X[m, 'A', k, t] == 0, f"LineA_NoPickups_{m}_{k}_{t}"
                    # Capacity livianos
                    prob += pulp.lpSum(X[m, 'A', 'Mañana', t] for m in self.livianos) <= self.cap_A_manana * Y['A', 'Mañana', t], f"Cap_A_Manana_{t}"
                    prob += pulp.lpSum(X[m, 'A', 'Tarde', t] for m in self.livianos) <= self.cap_A_tarde * Y['A', 'Tarde', t], f"Cap_A_Tarde_{t}"
                else:
                    # Line A retooled! Can produce livianos and pick-ups
                    # Ratio: 1 pick-up = 1.2 livianos equivalent
                    prob += (pulp.lpSum(X[m, 'A', 'Mañana', t] for m in self.livianos) + 
                             self.ratio_B_pick * pulp.lpSum(X[m, 'A', 'Mañana', t] for m in self.pickups)
                             <= self.cap_A_manana * Y['A', 'Mañana', t]), f"Cap_A_Retooled_Manana_{t}"
                    prob += (pulp.lpSum(X[m, 'A', 'Tarde', t] for m in self.livianos) + 
                             self.ratio_B_pick * pulp.lpSum(X[m, 'A', 'Tarde', t] for m in self.pickups)
                             <= self.cap_A_tarde * Y['A', 'Tarde', t]), f"Cap_A_Retooled_Tarde_{t}"

            # Line B Capacity
            prob += (pulp.lpSum(X[m, 'B', 'Mañana', t] for m in self.livianos) + 
                     self.ratio_B_pick * pulp.lpSum(X[m, 'B', 'Mañana', t] for m in self.pickups)
                     <= self.cap_B_manana_liv * Y['B', 'Mañana', t]), f"Cap_B_Manana_{t}"
            prob += (pulp.lpSum(X[m, 'B', 'Tarde', t] for m in self.livianos) + 
                     self.ratio_B_pick * pulp.lpSum(X[m, 'B', 'Tarde', t] for m in self.pickups)
                     <= self.cap_B_tarde_liv * Y['B', 'Tarde', t]), f"Cap_B_Tarde_{t}"

            # 4. Turn Hierarchy and Union rules
            for l in self.lines:
                prob += Y[l, 'Tarde', t] <= Y[l, 'Mañana', t], f"ShiftHierarchy_{l}_{t}"
                prob += W_tarde[t] >= Y[l, 'Tarde', t], f"UnionW_Tarde_LB_{l}_{t}"
            prob += W_tarde[t] <= pulp.lpSum(Y[l, 'Tarde', t] for l in self.lines), f"UnionW_Tarde_UB_{t}"

        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        status_str = pulp.LpStatus[prob.status]
        obj_val = pulp.value(prob.objective) if status_str == 'Optimal' else None
        
        # Extract detailed solution if optimal
        results = {
            'status': status_str,
            'objective_value': obj_val,
            'production': {},
            'sales_local': {},
            'sales_export': {},
            'sales_autonomy': {},
            'sales_agro': {},
            'inventory': {},
            'shifts': {},
            'w_tarde': {},
            'imports_china': {},
            'metrics_by_year': {}
        }
        
        if status_str == 'Optimal':
            for t in self.years:
                results['shifts'][t] = {l: {k: Y[l, k, t].varValue for k in self.shifts} for l in self.lines}
                results['w_tarde'][t] = W_tarde[t].varValue
                results['sales_autonomy'][t] = S_autonomy[t].varValue
                results['sales_agro'][t] = S_agro[t].varValue
                
                results['sales_local'][t] = {m: S_local[m, t].varValue for m in self.models}
                results['sales_export'][t] = {m: S_export[m, t].varValue for m in self.pickups}
                results['inventory'][t] = {m: I[m, t].varValue for m in self.models}
                results['imports_china'][t] = {m: M_china[m, t].varValue for m in self.livianos}
                
                results['production'][t] = {}
                for m in self.models:
                    results['production'][t][m] = {
                        (l, k): X[m, l, k, t].varValue for l in self.lines for k in self.shifts
                    }
                    
                # Calculate annual revenues and costs
                rev_y = sum(self.price_local[m] * S_local[m, t].varValue for m in self.models)
                rev_y += sum(self.price_export[m] * S_export[m, t].varValue for m in self.pickups)
                if autonomy_active:
                    rev_y += p_autonomy * S_autonomy[t].varValue
                if agro_active and t >= 2:
                    rev_y += self.price_agro * S_agro[t].varValue
                    
                cv_y = sum(
                    ((self.cv_ars_y1[m] * self.inflation[t]) / tc[t]) * sum(X[m, l, k, t].varValue for l in self.lines for k in self.shifts)
                    for m in self.models
                )
                cf_y = sum(
                    ((self.fixed_startup_ars_y1[l] * self.inflation[t]) / tc[t]) * sum(Y[l, k, t].varValue for k in self.shifts)
                    for l in self.lines
                )
                sal_usd = (self.salary_annual_y1 * self.inflation[t]) / tc[t]
                labor_y = sum(
                    self.headcount[l] * sal_usd * sum(Y[l, k, t].varValue for k in self.shifts)
                    for l in self.lines
                ) + self.headcount_tarde_joint * sal_usd * W_tarde[t].varValue
                
                inv_y = sum(
                    inv_rate * ((self.cv_ars_y1[m] * self.inflation[t]) / tc[t]) * I[m, t].varValue
                    for m in self.models
                )
                
                import_cost_y = 0.0
                if china_import_active and t >= china_import_start_year:
                    cif_cost = {'LB': 25000.0, 'LP': 28000.0}
                    import_cost_y = sum(cif_cost[m] * M_china[m, t].varValue for m in self.livianos)
                    
                profit_y = rev_y - cv_y - cf_y - labor_y - inv_y - import_cost_y
                
                results['metrics_by_year'][t] = {
                    'revenue': rev_y,
                    'cost_variable': cv_y,
                    'cost_fixed_startup': cf_y,
                    'cost_labor': labor_y,
                    'cost_inventory': inv_y,
                    'cost_import': import_cost_y,
                    'net_profit': profit_y
                }
                
        return results

if __name__ == "__main__":
    model = AutoITBAModel()
    res = model.solve_model(scenario='base')
    print("Base Model Status:", res['status'])
    print("Base Total Profit USD:", f"${res['objective_value']:,.2f}")
    for t in [1, 2, 3, 4, 5]:
        print(f"\n--- Year {t} ---")
        print("Shifts:", res['shifts'][t])
        print("W_tarde:", res['w_tarde'][t])
        print("Metrics:", {k: f"${v:,.0f}" for k, v in res['metrics_by_year'][t].items()})
