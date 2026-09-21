# TP1 - Investigación Operativa: Plan de Producción AutoITBA S.A.
**Instituto Tecnológico de Buenos Aires (ITBA) — 2° Cuatrimestre 2026**

Este repositorio contiene la resolución completa, formalización matemática, implementación computacional, análisis de sensibilidad y recomendaciones estratégicas para el **Trabajo Práctico N° 1 Complementario: "Plan de producción AutoITBA SA"**.

---

## 📁 Estructura del Repositorio

```text
TP1-IO/
├── data/
│   └── AutoITBA_Parametros.xlsx   <- Base de datos completa en Excel (7 pestañas)
├── plots/
│   ├── fig0_proceso_planta.png     <- Diagrama de flujo de planta, secciones y dotaciones
│   ├── fig1_utilidad_base_vs_dev.png <- Comparación de utilidades: Base vs Devaluación
│   ├── fig2_mix_produccion_base.png  <- Mix de producción anual por modelo (Escenario Base)
│   ├── fig3_sensibilidad_inventario.png <- Barrido continuo de tasa de playón (Corte ~8.8%)
│   ├── fig4_reequipamiento_linea_A.png  <- Beneficio neto incremental de la obra en Línea A
│   ├── matriz_pagos.csv            <- Matriz de pagos por estrategia y escenario (USD M)
│   └── matriz_regret.csv           <- Matriz de arrepentimiento y criterio Minimax Regret
├── src/
│   ├── __init__.py
│   ├── generate_excel.py           <- Generador automatizado de la base de datos Excel
│   ├── model_engine.py             <- Motor central de optimización MILP en PuLP (CBC)
│   ├── run_experiments.py          <- Ejecución sistemática de Consignas 1 a 7
│   ├── generate_charts.py          <- Generación de gráficos analíticos y matrices de decisión
│   └── draw_process.py             <- Generación del diagrama gráfico de planta
├── INFORME_EJECUTIVO_AUTOITBA.md   <- Informe académico y directivo exhaustivo
├── main.py                         <- Script maestro de ejecución punta a punta
├── requirements.txt                <- Dependencias del entorno de Python
└── README.md                       <- Documentación principal del repositorio
```

---

## 🚀 Instalación y Ejecución Rápida

### Requisitos Previos
* Python 3.10 o superior.

### 1. Clonar e instalar dependencias
```bash
git clone https://github.com/Santim1897/TP1-IO.git
cd TP1-IO
pip install -r requirements.txt
```

### 2. Ejecutar todo el proyecto
Para correr el modelo de optimización, regenerar las figuras y reproducir todas las consignas:
```bash
python main.py
```

---

## 📊 Resumen de Resultados Principales

| Consigna | Problema Analizado | Resultado Clave | Decisión Recomendada |
| :--- | :--- | :--- | :--- |
| **1. Modelo Base** | Plan de producción a 5 años | Utilidad Neta: **USD $1.993,49 M** | Línea A Mañana (Livianos); Línea B Mañana+Tarde (Pick-ups). Playón = 0. |
| **2. Devaluación** | Escenario Devaluación Acelerada | Utilidad Neta: **USD $3.910,05 M (+96,14%)** | Costos locales se abaratan en USD. Turno tarde es aún más rentable. |
| **3. Reequipamiento** | Adaptar Línea A a Pick-ups (USD 12-18M) | Inviable en demanda base. Con Boom Agro (+20%): **+USD 39,44 M netos** | Realizar la obra en **Año 1** únicamente si se confirma el boom agropecuario. |
| **4. Importación China** | Reemplazar livianos locales desde Año 2 | Base: **+USD 109,70 M** / Devaluación: **-USD 115,67 M** / Cierre: **-USD 69,08 M** | No desmantelar la línea local. Riesgo regulatorio y cambiario crítico. |
| **5. Contrato Autonomy**| 1.000 LB anuales a USD 27.500 | Costo de oportunidad: **+USD 5,17 M**. Precio umbral: **USD 28.533,87** | Renegociar precio a > USD 28.550 o liberar capacidad en Años 3 a 5. |
| **6. Costo Playón** | Tasa inventario (25% vs 30% vs barrido) | Inventario = 0 a 25% y 30%. Tasa de corte: **8,8% anual** | Producción sincronizada contra demanda (Just-in-Time). |
| **7. Estrategia Minimax**| Decisión robusta vs contingente en Años 1-2 | Arrepentimiento Máximo S1: **USD 109,70 M** (mínimo) vs S3: USD 115,67 M | **Fabricación Local Flexible**: Preservar opciones abiertas para Años 3 a 5. |

---

## 📖 Informe Académico y Directivo Completo
El detalle formal de la formulación matemática (conjuntos, variables, función objetivo, restricciones), análisis de sensibilidad de la respuesta, supuestos económicos y respuestas a las consignas se encuentra en:
👉 [**INFORME_EJECUTIVO_AUTOITBA.md**](INFORME_EJECUTIVO_AUTOITBA.md)
