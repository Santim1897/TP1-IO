# TRABAJO PRÁCTICO N° 1 COMPLEMENTARIO: INVESTIGACIÓN OPERATIVA (IO51)
## Plan de Producción Estratégico a 5 Años — AutoITBA S.A.
**Instituto Tecnológico de Buenos Aires (ITBA) — 2° Cuatrimestre 2026**

---

### Resumen Ejecutivo y Metadatos del Proyecto
* **Empresa / Terminal Automotriz:** AutoITBA S.A. (Planta Industrial radicada en Zárate, Provincia de Buenos Aires).
* **Horizonte Temporal:** 5 años ($t \in \{1, 2, 3, 4, 5\}$).
* **Portafolio:** 
  * *Livianos:* LB (Entrada de gama / utilitario urbano) y LP (Premium / alta tecnología).
  * *Pick-ups:* PB (Cabina simple básica), PM (Cabina doble media) y PP (Superior / alta motorización).
* **Infraestructura:** Línea A (Livianos) y Línea B (Pick-ups y Livianos), operables en Turno Mañana y Turno Tarde.
* **Herramientas de Optimización:** Python 3.12, PuLP (Solver CBC / Simplex & Branch-and-Cut), Pandas, OpenPyXL, Matplotlib.
* **Repositorio de Código Fuente:** [https://github.com/Santim1897/TP1-IO](https://github.com/Santim1897/TP1-IO)

---

## 1. Informe Esperable por la Cátedra

### a) Modelo de Programación Lineal Entera Mixta (MILP)

#### i) Supuestos más Importantes
1. **Unidad Monetaria Homogénea (USD):** Dado que los precios de venta en el mercado local y de exportación se encuentran fijados en dólares estadounidenses y la inflación argentina genera distorsiones nominales en moneda local, toda la función objetivo y la evaluación de rentabilidad se formula y consolida en **dólares estadounidenses (USD)**.
2. **Conversión y Dinámica Macroeconómica:** Los costos expresados originalmente en pesos argentinos (ARS) —tales como salarios, costos de encendido de línea y componentes variables locales— se actualizan anualmente con una inflación del 20% anual y se convierten a dólares utilizando la cotización oficial proyectada de cada año ($TC_t$).
3. **Equivalencia de Capacidad en Línea B (Ratio 1.2):** La Línea B posee maquinaria reforzada capaz de soportar pick-ups. En régimen de turno mañana puede ensamblar 30.000 livianos o 25.000 pick-ups (o una combinación lineal de ambos). Por ende, cada pick-up consume el equivalente a **1.2 vehículos livianos** de capacidad de línea ($30.000 / 25.000 = 1.2$).
4. **Régimen de Turnos y Jerarquía:** El turno tarde opera al 75% del turno mañana debido a la menor disponibilidad de supervisión técnica y logística nocturna de proveedores. No es admisible activar el turno tarde sin tener previamente encendido el turno mañana en esa misma línea ($Y_{l, \text{Tarde}, t} \le Y_{l, \text{Mañana}, t}$).
5. **Restricción Sindical de Turno Tarde:** Si cualquiera de las dos líneas (o ambas) enciende el turno tarde, el convenio colectivo exige la contratación conjunta de **5 operarios adicionales** por motivos de peligrosidad. Estos operarios son comunes a la planta y no se duplican si ambas líneas operan a la tarde.
6. **Conservación de Flujos e Inventario (Playón):** El inventario inicial en $t=0$ es nulo. Las unidades no vendidas al término del año $t$ pueden trasladarse al año $t+1$ abonando un costo de almacenamiento y capital inmovilizado equivalente al **25% del costo variable unitario** de producción de dicho vehículo en ese año.
7. **Diferencial de Exportación (+5% MERCOSUR):** Las pick-ups exportadas al MERCOSUR perciben un sobreprecio del 5% respecto al precio de lista local, reflejando flete, seguro y la prima regional por origen argentino. Los livianos no cuentan con demanda de exportación.

---

#### ii) Variables de Decisión Elegidas
* **Variables Continuas de Producción:**
  * $X(m, l, k, t) \ge 0$: Cantidad de vehículos del modelo $m \in M$ a ensamblar en la línea $l \in L$, durante el turno $k \in K$, en el año $t \in T$.
* **Variables Binarias de Activación de Turnos:**
  * $Y(l, k, t) \in \{0, 1\}$: Vale $1$ si la línea $l \in L$ opera en el turno $k \in K$ durante el año $t \in T$; $0$ en caso contrario.
  * $W_{\text{tarde}}(t) \in \{0, 1\}$: Vale $1$ si al menos una línea opera en el Turno Tarde en el año $t \in T$; $0$ en caso contrario (activa el costo de los 5 operarios de peligrosidad).
* **Variables Continuas de Ventas y Despacho:**
  * $S_{\text{local}}(m, t) \ge 0$: Unidades vendidas en el mercado interno del modelo $m \in M$ en el año $t \in T$.
  * $S_{\text{export}}(m, t) \ge 0$: Unidades exportadas al MERCOSUR del modelo $m \in M_{pick}$ en el año $t \in T$.
  * $S_{\text{autonomy}}(t) \ge 0$: Unidades del modelo LB entregadas bajo contrato corporativo a Autonomy en el año $t \in T$.
  * $S_{\text{agro}}(t) \ge 0$: Unidades del modelo PP entregadas bajo propuesta especial a Agronegocios en el año $t \in T$ ($t \ge 2$).
* **Variables Continuas de Inventario Final:**
  * $I(m, t) \ge 0$: Cantidad de vehículos del modelo $m \in M$ almacenados en el playón al final del año $t \in T$ (con $I(m, 0) = 0$).

---

#### iii) Función Objetivo
Maximizar la **Utilidad Neta Total acumulada a lo largo del horizonte de 5 años (en USD)**:

$$\max Z = \sum_{t=1}^{5} \left[ \text{Ingresos}(t) - \text{CostosVariables}(t) - \text{CostosEncendido}(t) - \text{CostosLaborales}(t) - \text{CostosInventario}(t) \right]$$

Donde cada término se desagrega de la siguiente forma:

1. **Ingresos Totales en USD:**
$$\text{Ingresos}(t) = \sum_{m \in M} P_{\text{local}}(m) \cdot S_{\text{local}}(m, t) + \sum_{m \in M_{pick}} P_{\text{export}}(m) \cdot S_{\text{export}}(m, t) + P_{\text{autonomy}} \cdot S_{\text{autonomy}}(t) + P_{\text{agro}} \cdot S_{\text{agro}}(t)$$

2. **Costos Variables de Fabricación en USD:**
$$\text{CostosVariables}(t) = \sum_{m \in M} cv_{m, t} \sum_{l \in L} \sum_{k \in K} X(m, l, k, t)$$
$$\text{con } cv_{m, t} = \frac{CV\_ARS_{m, 1} \cdot (1.20)^{t-1}}{TC_t}$$

3. **Costos Fijos de Encendido de Línea en USD:**
$$\text{CostosEncendido}(t) = \sum_{k \in K} \left[ \frac{CF\_ARS_{A, 1} \cdot (1.20)^{t-1}}{TC_t} Y(A, k, t) + \frac{CF\_ARS_{B, 1} \cdot (1.20)^{t-1}}{TC_t} Y(B, k, t) \right]$$

4. **Costos Laborales Totales en USD:**
$$\text{CostosLaborales}(t) = \text{SalarioAnual\_USD}_t \cdot \left[ 9 \sum_{k \in K} Y(A, k, t) + 11 \sum_{k \in K} Y(B, k, t) + 5 \cdot W_{\text{tarde}}(t) \right]$$
$$\text{con } \text{SalarioAnual\_USD}_t = \frac{2.000.000 \cdot 13 \cdot (1.20)^{t-1}}{TC_t} = \frac{26.000.000 \cdot (1.20)^{t-1}}{TC_t}$$

5. **Costos de Mantenimiento de Inventario en USD:**
$$\text{CostosInventario}(t) = \sum_{m \in M} \alpha_{\text{inv}} \cdot cv_{m, t} \cdot I(m, t) \quad (\alpha_{\text{inv}} = 0.25)$$

---

#### iv) Parámetros del Modelo
A continuación se resumen los parámetros numéricos fundamentales consolidados en la base de datos:

| Parámetro / Concepto | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Factor Inflación de Costos (20% a.a.)** | 1,0000 | 1,2000 | 1,4400 | 1,7280 | 2,0736 |
| **Tipo de Cambio Escenario Base (ARS/USD)** | 1.500 | 1.750 | 1.950 | 2.350 | 2.800 |
| **Tipo de Cambio Devaluación (ARS/USD)** | 1.500 | 2.200 | 2.650 | 3.100 | 3.550 |
| **Sueldo anual x operario (ARS c/SAC)** | $26.000.000 | $31.200.000 | $37.440.000 | $44.928.000 | $53.913.600 |
| **Costo anual x operario Base (USD)** | $17.333,33 | $17.828,57 | $19.200,00 | $19.118,30 | $19.254,86 |
| **Encendido Línea A Base (USD)** | $333.333,33 | $342.857,14 | $369.230,77 | $367.659,57 | $370.285,71 |
| **Encendido Línea B Base (USD)** | $533.333,33 | $548.571,43 | $590.769,23 | $588.255,32 | $592.457,14 |
| **CV Unitario LB Base (USD)** | $26.666,67 | $27.428,57 | $29.538,46 | $29.412,77 | $29.622,86 |
| **CV Unitario LP Base (USD)** | $28.800,00 | $29.622,86 | $31.901,54 | $31.765,79 | $31.992,69 |
| **CV Unitario PB Base (USD)** | $38.333,33 | $39.428,57 | $42.461,54 | $42.280,85 | $42.582,86 |
| **CV Unitario PM Base (USD)** | $39.483,33 | $40.611,43 | $43.735,38 | $43.549,28 | $43.860,34 |
| **CV Unitario PP Base (USD)** | $40.633,33 | $41.794,29 | $45.009,23 | $44.817,70 | $45.137,83 |

* **Precios de Venta:**
  * Local (USD): LB: $30.000, LP: $35.000, PB: $45.000, PM: $50.000, PP: $57.500.
  * Exportación MERCOSUR (+5% en USD): PB: $47.250, PM: $52.500, PP: $60.375.
  * Contrato Autonomy: LB a USD 27.500 (Años 1-5, 1.000 unidades anuales).
  * Propuesta Agronegocios: PP a USD 57.500 (Años 2-5, hasta 1.500 unidades anuales).

---

#### v) Restricciones Formales

1. **Balance de Masa e Inventario ($\forall m \in M, \forall t \in T$):**
   $$I(m, t-1) + \sum_{l \in L} \sum_{k \in K} X(m, l, k, t) = \text{VentasTotales}(m, t) + I(m, t)$$
   con $I(m, 0) = 0$ y:
   * $\text{VentasTotales}(LB, t) = S_{\text{local}}(LB, t) + S_{\text{autonomy}}(t)$
   * $\text{VentasTotales}(LP, t) = S_{\text{local}}(LP, t)$
   * $\text{VentasTotales}(m, t) = S_{\text{local}}(m, t) + S_{\text{export}}(m, t) \quad \forall m \in \{PB, PM\}$
   * $\text{VentasTotales}(PP, t) = S_{\text{local}}(PP, t) + S_{\text{export}}(PP, t) + S_{\text{agro}}(t)$

2. **Capacidad de Ensamble de la Línea A ($\forall t \in T$):**
   * Turno Mañana: $\sum_{m \in M_{liv}} X(m, A, \text{Mañana}, t) \le 10.000 \cdot Y(A, \text{Mañana}, t)$
   * Turno Tarde: $\sum_{m \in M_{liv}} X(m, A, \text{Tarde}, t) \le 7.500 \cdot Y(A, \text{Tarde}, t)$
   * Exclusión de pick-ups en configuración base: $X(m, A, k, t) = 0 \quad \forall m \in M_{pick}, \forall k \in K$.

3. **Capacidad de Ensamble de la Línea B con Factor de Equivalencia ($\forall t \in T$):**
   * Turno Mañana:
     $$\sum_{m \in M_{liv}} X(m, B, \text{Mañana}, t) + 1.2 \sum_{m \in M_{pick}} X(m, B, \text{Mañana}, t) \le 30.000 \cdot Y(B, \text{Mañana}, t)$$
   * Turno Tarde:
     $$\sum_{m \in M_{liv}} X(m, B, \text{Tarde}, t) + 1.2 \sum_{m \in M_{pick}} X(m, B, \text{Tarde}, t) \le 22.500 \cdot Y(B, \text{Tarde}, t)$$

4. **Límites de Demanda y Contratos ($\forall t \in T$):**
   * Mercado Local: $S_{\text{local}}(m, t) \le \text{DemandaLocal}(m, t) \quad \forall m \in M$
   * Exportación: $S_{\text{export}}(m, t) \le \text{DemandaExport}(m, t) \quad \forall m \in M_{pick}$
   * Contrato Autonomy: $S_{\text{autonomy}}(t) = 1.000 \quad \forall t \in \{1, \dots, 5\}$
   * Propuesta Agronegocios: $S_{\text{agro}}(t) \le 1.500 \quad \forall t \ge 2 \quad (S_{\text{agro}}(1) = 0)$

5. **Lógica Operativa de Turnos y Regla Sindical ($\forall t \in T$):**
   * Jerarquía de turnos: $Y(l, \text{Tarde}, t) \le Y(l, \text{Mañana}, t) \quad \forall l \in L$
   * Activación conjunta de operarios de peligrosidad:
     $$W_{\text{tarde}}(t) \ge Y(l, \text{Tarde}, t) \quad \forall l \in L$$
     $$W_{\text{tarde}}(t) \le \sum_{l \in L} Y(l, \text{Tarde}, t)$$

6. **Condiciones de No Negatividad e Integridad:**
   $$X(m, l, k, t) \ge 0, \quad S_{\text{local}}(m, t) \ge 0, \quad S_{\text{export}}(m, t) \ge 0, \quad I(m, t) \ge 0$$
   $$Y(l, k, t) \in \{0, 1\}, \quad W_{\text{tarde}}(t) \in \{0, 1\}$$

---

#### vi) Resolución del Modelo
El modelo fue resuelto mediante el solver de programación lineal entera mixta **CBC (COIN-OR Branch and Cut)** implementado bajo la interfaz **PuLP** en Python.
* **Estado:** ÓPTIMO GLOBAL (`Optimal`).
* **Variables Totales:** 125 variables de decisión (15 binarias y 110 continuas).
* **Restricciones:** 105 ecuaciones e inecuaciones lineales.
* **Tiempo de Cómputo:** < 0.25 segundos.
* **Valor Óptimo de la Función Objetivo (Utilidad Neta Total Base):** **USD $1.993.488.792,66** (aprox. **USD 1.993,49 Millones**).

---

### b) Análisis de Sensibilidad de la Respuesta

#### i) Rangos de Nivel de Actividad
1. **Línea A (Livianos):**
   * Opera al **100% de su capacidad en Turno Mañana** en los Años 1 a 4 ($10.000$ unidades/año, produciendo exactamente la suma de $LB$ y $LP$ demandados más el contrato Autonomy).
   * En el Año 5, la demanda de livianos alcanza $2.251$ (LB) $+ 5.064,8$ (LP) $+ 1.000$ (Autonomy) $= 8.315,8$ unidades, cubriendo el $83,16\%$ de la capacidad de mañana. El Turno Tarde de la Línea A se mantiene apagado en los 5 años ($Y_{A, \text{Tarde}, t} = 0$).
2. **Línea B (Pick-ups):**
   * Opera en **régimen pleno (Mañana y Tarde)** durante todo el quinquenio ($Y_{B, \text{Mañana}, t} = 1$, $Y_{B, \text{Tarde}, t} = 1$).
   * Su capacidad combinada es de $25.000 + 18.750 = 43.750$ pick-ups anuales.
   * La demanda total de pick-ups (Local + Export + Agro) crece de $38.500$ unidades en el Año 1 hasta **$44.741,1$ unidades en el Año 5**.
   * En el Año 5 la Línea B opera al **100% de su capacidad física máxima**, obligando al modelo a racionar $282,2$ unidades de $PB$ local para priorizar las variantes de mayor margen unitario ($PP$ y $PM$).

#### ii) Rangos de Soluciones Posibles, Holguras y Cuellos de Botella
* **Cuello de Botella Primario:** Capacidad de ensamble y acabado en la Línea B en el Año 5. El precio sombra (dual value) de la capacidad de Línea B en el Año 5 es positivo y está determinado por el margen de contribución de la pick-up básica ($PB$).
* **Holgura en Línea A:** La Línea A posee una capacidad remanente ociosa en el turno tarde de $7.500$ unidades/año no utilizada, dado que el mercado de livianos está completamente abastecido y no se permite exportar livianos ni adaptarlos a pick-ups sin obra.
* **Inventario Interanual:** La holgura en inventario es nula ($I(m, t) = 0$). Con un costo de almacenamiento del 25% anual, almacenar un vehículo terminado destruye entre USD 6.666 y USD 10.600 por unidad al año, lo cual resulta prohibitivo comparado con la producción sincronizada contra demanda.

---

### c) Representación Gráfica del Proceso
El proceso de ensamble y las secciones de planta se detallan en el diagrama generado:
`plots/fig0_proceso_planta.png`.

```
                    TERMINAL AUTOMOTRIZ ZÁRATE - AUTOITBA S.A.
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [LÍNEA A: LIVIANOS]                                                                   |
|  (Cap: 10.000 M / 7.500 T)                                                              |
|       |                                                                                 |
|       +--> [Chasis: 1 op] --> [Pintura: 1 op] --> [Motor: 2 op] --> [Detalles: 5 op] --+
|                                                                         |               |
|                                                                         |               v
|  [LÍNEA B: PICK-UPS / LIV]                                              |       [PLAYÓN DE]
|  (Cap: 25k P / 30k L (M))                                               |       [DESPACHO ]
|  (Cap: 18.75k P / 22.5k L (T))                                          |       [INVENTARIO]
|       |                                                                 |               ^
|       +--> [Chasis: 1 op] --> [Pintura: 1 op] --> [Motor: 2 op] --> [Detalles: 7 op] --+
|                                                                         |
|                                                                         |
|  [TURNO TARDE - SINDICATO]                                              |
|  +5 Operarios adicionales conjuntos de supervisión por peligrosidad ----+
|                                                                                         |
+-----------------------------------------------------------------------------------------+
                                          |
                                          +--> MERCADO LOCAL (LB, LP, PB, PM, PP)
                                          +--> EXPORTACIÓN MERCOSUR (+5% USD) (PB, PM, PP)
                                          +--> CONTRATO AUTONOMY (LB - USD 27.500)
                                          +--> PROPUESTA AGRONEGOCIOS (PP - USD 57.500)
```

---

### d) Librerías Utilizadas
1. **`pulp` (v3.3.2):** Modelado algebraico declarativo y comunicación directa con el motor de optimización COIN-OR Branch-and-Cut (CBC).
2. **`pandas` (v3.0.6):** Procesamiento de matrices multidimensionales, ingesta de parámetros desde Excel y cálculo de matrices de pagos y arrepentimiento.
3. **`openpyxl` (v3.1.5):** Construcción estructurada del libro de trabajo de base de datos (`AutoITBA_Parametros.xlsx`) con estilos profesionales.
4. **`matplotlib` (v3.11.2):** Generación de gráficos analíticos de barras apiladas, sensibilidad continua de inventario, curvas de beneficio incremental y diagrama de proceso en alta resolución (300 DPI).
5. **`numpy` (v2.5.3) & `scipy` (v1.18.1):** Operaciones vectoriales, barridos de parámetros continuos y búsquedas de raíz para precios umbral de conveniencia.

---

## 2. Respuestas Detalladas a las Consignas 1 a 7

### Consigna 1: Modelo y Plan Óptimo para el Escenario Base
* **Utilidad Neta Acumulada a 5 Años:** **USD $1.993.488.792,66**
* **Plan de Activación de Turnos:**
  * **Línea A:** Opera únicamente en **Turno Mañana** ($Y_{A, \text{Mañana}, t} = 1$, $Y_{A, \text{Tarde}, t} = 0$) en los 5 años.
  * **Línea B:** Opera en **ambos turnos (Mañana y Tarde)** ($Y_{B, \text{Mañana}, t} = 1$, $Y_{B, \text{Tarde}, t} = 1$) en los 5 años.
  * **Sindicato Turno Tarde:** Se activa $W_{\text{tarde}}(t) = 1$ abonando los 5 operarios adicionales conjuntos.
* **Producción y Despacho Físico Anual:**
  * **Año 1:** Se producen $7.500$ livianos ($3.000$ LB, $4.500$ LP) en Línea A y $38.500$ pick-ups ($16.000$ PB, $11.500$ PM, $11.000$ PP) en Línea B. Abastecimiento del 100% de la demanda local, exportación y Autonomy.
  * **Años 2 a 4:** Se cubre el 100% de la demanda en todos los mercados, incorporando las $1.500$ PP anuales de Agronegocios.
  * **Año 5:** La demanda total de pick-ups ($44.741,1$ unidades) supera la capacidad máxima de la Línea B ($43.750$ unidades). El modelo despacha el 100% de $PM$, $PP$, exportaciones y agronegocios, racionando únicamente $282,2$ unidades de $PB$ en el mercado local por tener el menor margen unitario.
* **Transferencia de Inventario:** $0$ unidades transferidas entre períodos.

---

### Consigna 2: Evaluación del Escenario de Devaluación Acelerada
* **Utilidad Neta Escenario Devaluación:** **USD $3.910.054.101,41**
* **Ganancia Incremental vs Base:** **+USD $1.916.565.308,75 (+96,14%)**
* **Análisis de Mecanismos:**
  * Al estar los precios de venta indexados en USD y los costos de ensamble fijados en pesos indexados al 20% anual, la devaluación acelerada (el dólar pasa de $1.500$ a $3.550$ en lugar de $2.800$) genera una **licuación masiva de los costos en dólares**.
  * El costo variable unitario de fabricación de una pick-up básica en Año 5 cae de **USD 42.582,86** (Base) a **USD 33.586,48** (Devaluación).
* **¿Cambia el mix de producción entre mercado local y exportación?**
  * En los Años 1 a 4 no cambia: se abastece el 100% de ambos mercados.
  * En el Año 5, la devaluación aumenta el margen relativo y la competitividad, permitiendo que la planta sature aún más su capacidad para capturar toda la demanda factible. Las exportaciones siguen gozando de prioridad absoluta por el sobreprecio del 5% en dólares.
* **¿Cambia la conveniencia de activar el turno tarde?**
  * **No.** El turno tarde en Línea B sigue siendo **indispensable y altamente superavitario**. Apagar el turno tarde implicaría dejar de producir $18.750$ pick-ups al año, destruyendo cientos de millones de dólares en ingresos operativos netos frente a un costo de encendido y mano de obra que resulta insignificante en dólares devaluados.

---

### Consigna 3: Reequipamiento de la Línea A
* **Hipótesis Operativa:** Reequipar la Línea A para ensamblar pick-ups requiere parar la línea durante 1 año calendario (capacidad = 0 ese año) e invertir entre **USD 12M y USD 18M**.
* **1. Bajo Demanda Base:**
  * **No existe ningún año que justifique la inversión.**
  * El impacto operativo bruto es **negativo en todos los años** (pérdida de entre USD 1,1M y USD 13,8M antes de considerar la inversión).
  * *Motivo:* Detener la Línea A durante 1 año hace perder toda la facturación de vehículos livianos ($LB$ y $LP$), mientras que la Línea B ya posee capacidad suficiente para casi toda la demanda de pick-ups en los primeros 4 años. Al sumar la inversión de USD 12M a 18M, el proyecto destruye entre **USD 13M y USD 32M** de valor.
* **2. Bajo Boom Agropecuario (+20% en Demanda de Pick-ups):**
  * La demanda de pick-ups desborda la capacidad de Línea B desde el Año 1.
  * Si la obra se realiza en el **Año 1**:
    * Ganancia Operativa Bruta Incremental: **+USD $51.439.095,95**
    * Con inversión de USD 12M: **Beneficio Neto = +USD 39,44 M** (CONVIENE)
    * Con inversión de USD 15M: **Beneficio Neto = +USD 36,44 M** (CONVIENE)
    * Con inversión de USD 18M: **Beneficio Neto = +USD 33,44 M** (CONVIENE)
  * Realizar la obra en los Años 2 o 3 también es rentable (+USD 10M a 18M netos), pero en los Años 4 o 5 deja de convenir porque no restan suficientes años para amortizar la parada de planta.
* **Recomendación de Año Óptimo:** En caso de confirmarse el boom agropecuario, el año óptimo para ejecutar la obra es el **Año 1**, capturando cuatro años completos de ventas extraordinarias a plena capacidad dual.

---

### Consigna 4: Importación de Livianos desde China
* **Hipótesis:** Abandonar la producción local de livianos a partir del Año 2, pagar USD 8.000.000 de costo único por indemnizaciones y logística, e importar unidades CIF a Zárate (LB: USD 25.000 / LP: USD 28.000).
* **1. Evaluación bajo Escenario Base:**
  * Utilidad Sin Importar: USD $1.993,49 M | Utilidad Con Importación: USD $2.103,19 M.
  * **Beneficio Neto Incremental: +USD $109.701.958,87 (+USD 109,70 M)**.
  * *Conclusión:* **CONVIENE ROTUNDAMENTE**. El costo de importación CIF (USD 25k/28k) es muy inferior al costo variable de fabricación local en USD bajo escenario base (USD 27,4k a 29,6k para LB y USD 29,6k a 32,0k para LP), sumado al ahorro del encendido y salarios de la Línea A.
* **2. Evaluación bajo Escenario Devaluación:**
  * Utilidad Sin Importar: USD $3.910,05 M | Utilidad Con Importación: USD $3.794,39 M.
  * **Diferencia Neta: -USD $115.668.299,95 (-USD 115,67 M)**.
  * *Conclusión:* **NO CONVIENE**. Con devaluación acelerada, los costos locales se abaratan a USD 21,8k - 23,4k, tornando a la fábrica argentina mucho más competitiva que los vehículos importados a precios rígidos en dólares.
* **3. Riesgo Regulatorio (Cierre de Importaciones en Año 3):**
  * Si en Año 3 el nuevo gobierno cierra las importaciones:
    * Si la Línea A fue desmantelada irreversiblemente: la empresa pierde las ventas de livianos de los Años 3 a 5, generando una **pérdida neta de USD 69,08 Millones** frente al caso base.
    * Si la Línea A puede reabrirse: la ganancia de importar en el Año 2 compensa casi exactamente el costo de USD 8M, arrojando un resultado marginal neto de +USD 7,46 M.

---

### Consigna 5: Evaluación del Contrato con Autonomy
* **Términos:** Provisión obligatoria de 1.000 LB anuales a precio fijo de **USD 27.500** durante los 5 años.
* **Cuantificación del Costo de Oportunidad (Escenario Base):**
  * Utilidad con Contrato Autonomy: USD $1.993.488.792,66
  * Utilidad liberando la capacidad (Sin Contrato): USD $1.998.658.127,58
  * **Costo de Oportunidad / Ganancia Adicional liberando capacidad: +USD $5.169.334,92**
  * *Explicación Financiera:* En los Años 3, 4 y 5, el costo variable local de fabricación de un LB en dólares asciende a **USD 29.538,46**, **USD 29.412,77** y **USD 29.622,86**, respectivamente. Por lo tanto, entregar unidades a USD 27.500 genera una **pérdida operativa directa** de más de USD 2.000 por vehículo en los últimos tres años.
* **Precio Umbral de Conveniencia (Break-even):**
  * Resolviendo iterativamente para el precio uniforme $P_{\text{autonomy}}$ que iguale la rentabilidad de no firmar el contrato:
  * **Precio Umbral = USD $28.533,87 por unidad**.
  * Por debajo de USD 28.534, el contrato destruye valor para AutoITBA.
* **Si el contrato tuviera entregas opcionales:** A USD 27.500, la empresa solo entregaría las 1.000 unidades en los Años 1 y 2 (donde el costo es menor a USD 27.500) y vendería 0 unidades en los Años 3 a 5, alcanzando una utilidad de USD 1.999,56 M.

---

### Consigna 6: Costo de Playón y Dinámica de Inventarios
* **Impacto al 25% y 30% anual:**
  * En ambos casos, el inventario interanual óptimo es **estrictamente CERO (0 unidades)**.
  * Con márgenes unitarios saludables y capacidad suficiente en los períodos 1 a 4, abonar un sobrecosto de tenencia de entre el 25% y 30% (equivalente a más de USD 7.000 por vehículo por año) supera ampliamente cualquier beneficio especulativo de anticipar producción.
* **Barrido Continuo de Tasa ($\alpha_{\text{inv}}$):**
  * Si el costo de almacenamiento fuera **0%** (playón gratuito): el modelo transfiere **82.252,1 unidades** a lo largo del quinquenio para aprovechar tipos de cambio más bajos y nivelar la producción.
  * A una tasa de **5,0%**: se transfieren **21.328,1 unidades**.
  * **Nivel de Corte Analítico:** A partir de una tasa de **8,8% anual**, la transferencia de inventario deja de ser utilizada y cae permanentemente a **0 unidades**.

---

### Consigna 7: Recomendación Estratégica Integral para el Directorio

#### a) Clasificación Estratégica de Decisiones: Robustas vs. Contingentes

1. **Decisiones Robustas (Invariantes ante cualquier escenario razonable):**
   * **Línea B en Doble Turno Pleno:** La activación permanente de Turno Mañana y Turno Tarde en la Línea B es la decisión más rentable y sólida del negocio automotriz. Genera el núcleo del flujo de fondos de la compañía bajo cualquier combinación de tipo de cambio, demanda y costos.
   * **Prioridad Absoluta a la Exportación de Pick-ups:** Las variantes exportadas al MERCOSUR aportan una prima del 5% en dólares limpios, por lo que deben abastecerse al 100% de la cuota regional de forma incondicional.
   * **Política de Producción Just-in-Time (Playón en Cero):** No debe transferirse inventario terminado entre períodos debido al alto costo de mantenimiento en playón (> 8,8%).
   * **Aceptación de la Propuesta Agronegocios:** Vender 1.500 unidades de PP a USD 57.500 a partir del Año 2 es óptimo en todos los escenarios.

2. **Decisiones Contingentes (Altamente dependientes del entorno):**
   * **Importación desde China:** Si el escenario es Base (tipo de cambio contenido), importar livianos genera +USD 109,7M; pero si sobreviene una Devaluación Acelerada, importar destruye -USD 115,7M. Además, un cierre regulatorio en Año 3 sin capacidad de reapertura genera pérdidas por USD 69M.
   * **Reequipamiento de Línea A:** En demanda normal es inviable. Solo se vuelve extraordinariamente rentable (+USD 39M) si se materializa el Boom Agropecuario (+20% demanda pick-ups).
   * **Contrato Autonomy:** Aceptar el precio ofrecido de USD 27.500 destruye USD 5,17M. Requiere renegociación urgente.

---

#### b) Análisis de Arrepentimiento Máximo (Criterio Minimax Regret)
Se formularon y evaluaron las tres estrategias directivas para los Años 1 y 2 frente a los cuatro estados de la naturaleza:
* **S1: Fabricación Local Flexible (Status Quo Optimizado)**
* **S2: Reequipamiento de Línea A en Año 1 (Apuesta a Pick-ups)**
* **S3: Cierre de Línea A e Importación de Livianos desde China en Año 2**

##### Matriz de Pagos (Utilidad Neta Total en Millones USD):
| Estrategia / Decisión | E1: Base (REM) | E2: Devaluación Acelerada | E3: Boom Agro (+20%) | E4: Cierre Regulatorio Año 3 |
| :--- | :---: | :---: | :---: | :---: |
| **S1: Fabricación Local Flexible** | $1.993,49$ | **$3.910,05$** | $2.251,58$ | **$1.993,49$** |
| **S2: Reequipamiento Línea A en Año 1** | $1.977,37$ | $3.893,94$ | **$2.285,02$** | $1.977,37$ |
| **S3: Importación Livianos China (Año 2)**| **$2.103,19$** | $3.794,39$ | $2.361,28$ | $1.924,41$ |

##### Matriz de Arrepentimiento (Regret en Millones USD):
| Estrategia / Decisión | E1: Base | E2: Devaluación | E3: Boom Agro | E4: Cierre Reg. | **Máximo Arrepentimiento** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **S1: Fabricación Local Flexible** | $109,70$ | **$0,00$** | $33,44$ | **$0,00$** | **USD 109,70 M** *(MÍNIMO)* |
| **S2: Reequipamiento Línea A** | $125,82$ | $16,11$ | **$0,00$** | $16,12$ | **USD 125,82 M** |
| **S3: Importación desde China** | **$0,00$** | $115,67$ | $0,00$ | $69,08$ | **USD 115,67 M** |

> [!IMPORTANT]
> **Conclusión Minimax Regret:** La estrategia **S1 (Fabricación Local Flexible)** es la estrategia óptima que **minimiza el arrepentimiento máximo** (USD 109,70 M vs USD 115,67 M de importar y USD 125,82 M de reequipar). Proteger a la empresa contra el colapso por devaluación o por cierre arancelario es prioritario sobre la ganancia especulativa de corto plazo.

---

#### c) Hoja de Ruta Táctica para los Años 1 a 5
1. **Acción Inmediata sobre Contrato Autonomy (Año 1):**
   * No firmar el contrato a USD 27.500 fijo.
   * Proponer una contraoferta con un precio base de **USD 28.600** o bien incorporar una **cláusula de ajuste cuatrimestral por paridad cambiaria / costos salariales en dólares** a partir del Año 3. Si Autonomy no acepta, liberar la capacidad de Línea A.
2. **Postura ante la Importación de China (Años 1 y 2):**
   * Durante el Año 1, **mantener la producción local activa** en Línea A.
   * No asumir en Año 1 ni principios de Año 2 compromisos irreversibles de despido o reestructuración por USD 8M.
   * En el Año 2, si la política cambiaria y arancelaria se consolida sin riesgo de devaluación abrupta ni cambio de signo político adverso, evaluar la importación como esquema tercerizado sin desmantelar la línea física (manteniendo la opción de contingencia).
3. **Monitoreo del Sector Agropecuario (Años 1 y 2):**
   * Medir la tasa de crecimiento efectiva de pedidos en los concesionarios rurales durante el Año 1. Si los pedidos crecen a un ritmo sostenido del +20% (consolidación del Boom), iniciar la ingeniería de detalle para ejecutar la obra de reequipamiento de la Línea A en el Año 2 o Año 3.
4. **Preservación de Flexibilidad para Años 3 a 5:**
   * Al finalizar el ciclo electoral y conocerse el régimen macroeconómico del nuevo gobierno, AutoITBA conservará intactas sus opciones reales: operar como polo exportador hipercompetitivo (en caso de devaluación), como armador local ampliado de pick-ups (si hay boom agropecuario), o como importador selectivo de nicho (si hay apertura comercial estable).

---
*Informe elaborado conforme a las pautas metodológicas de la cátedra de Investigación Operativa — ITBA 2026.*
