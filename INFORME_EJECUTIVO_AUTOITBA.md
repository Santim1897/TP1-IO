# TRABAJO PRÁCTICO N° 1 COMPLEMENTARIO: INVESTIGACIÓN OPERATIVA (IO51)
## Plan de Producción Estratégico a 5 Años — AutoITBA S.A.
**Instituto Tecnológico de Buenos Aires (ITBA) — 2° Cuatrimestre 2026**

---

### Carátula y Metadatos del Proyecto
* **Materia:** 11.51 / IO51 - Investigación de Operaciones (ITBA)
* **Trabajo:** Trabajo Práctico N.º 1 Complementario: "Plan de producción AutoITBA SA"
* **Empresa:** Terminal Automotriz AutoITBA S.A. (Planta industrial radicada en Zárate, Provincia de Buenos Aires)
* **Horizonte:** 5 años (Año 1 a Año 5, 2026 - 2030)
* **Portafolio de Productos:**
  * **Vehículos Livianos:** LB (Entrada de gama / flota urbana) y LP (Premium / alta tecnología y terminaciones).
  * **Pick-ups:** PB (Cabina simple básica), PM (Cabina doble media) y PP (Superior / alta motorización y equipamiento).
* **Herramientas Utilizadas:** Python 3.12, PuLP (Motor CBC Branch & Bound), Pandas, OpenPyXL, Matplotlib, SciPy.
* **Repositorio de Código Fuente:** [https://github.com/Santim1897/TP1-IO](https://github.com/Santim1897/TP1-IO)

### Bibliografía de Referencia
1. Enunciado oficial de la cátedra: *"IO51 - 2026 2C: Plan de producción AutoITBA SA"*.
2. Base de datos oficial de parámetros: *"AutoITBA S.A. - Base de Datos de Parámetros"*.
3. Apuntes de cátedra ITBA: Clase 02 (Formulación general de PL y multiperíodo), Clase 03 (Método Simplex), Clase 04 (Análisis post-óptimo y dualidad), Clase 06 (Programación lineal entera mixta y operadores lógicos con variables binarias).
4. Hillier, F. y Lieberman, G., *Introducción a la Investigación de Operaciones*. Cap. 1 a 3 (PL), Cap. 4 y 11 (Programación entera), Cap. 6 (Dualidad y sensibilidad).
5. Documentación oficial de PuLP y COIN-OR CBC: https://coin-or.github.io/pulp/.

---

## Resumen Ejecutivo y Cuadro de Respuestas a las Consignas

Se formuló e implementó un modelo de **Programación Lineal Entera Mixta (MILP)** multiperíodo a cinco años para optimizar las operaciones de AutoITBA S.A. El modelo decide de forma simultánea:
1. Cuántas unidades ensamblar de cada uno de los cinco vehículos cada año.
2. En qué línea y turno de producción fabricar cada unidad.
3. Qué turnos activar anualmente en cada línea (incurriendo en sus costos fijos y laborales asociados).
4. Cuánto inventario de producto terminado almacenar en el playón de un año al siguiente.
5. Qué volumen de demanda cubrir en el mercado doméstico, en exportaciones y bajo contratos corporativos especiales.

### Cuadro Síntesis de Resultados por Consigna

| Consigna | Planteo Central | Resultado Numérico Obtenido | Justificación y Decisión Estratégica |
| :--- | :--- | :--- | :--- |
| **1) Plan Óptimo Base** | Plan de producción, turnos, inventario y cobertura a 5 años | **Utilidad Neta: USD 1.993,49 M** (Inv = 0 u) | Línea A activa solo a la mañana (Livianos); Línea B activa mañana y tarde (Pick-ups). 100% de demanda cubierta en Años 1-4; en Año 5 se satura Línea B y se racionan 282 u de PB local. |
| **2) Devaluación Acelerada** | Impacto de mayor devaluación en mix y turnos | **Utilidad Neta: USD 3.910,05 M (+96,1%)** | Los costos locales en ARS se abaratan medidos en USD. El mix no cambia (se cubre 100% de demanda). El turno tarde en Línea B sigue siendo indispensable y aún más superavitario. |
| **3) Reconversión Línea A** | Inversión USD 12M-18M para hacer pick-ups en Línea A | **Base:** Destruye valor (-USD 16M a -31M)<br>**Boom (+20%):** Beneficio neto de **+USD 33M a +USD 39M** | Sin boom, parar la Línea A 1 año destruye ingresos que la Línea B no puede compensar. Con Boom Agropecuario, **sí conviene** y el año óptimo para la obra es el **Año 1**. |
| **4) Importar de China** | Dejar de producir livianos e importar desde Año 2 | **Base:** Conviene (+USD 109,7 M)<br>**Devaluación:** Destruye (-USD 115,7 M)<br>**Cierre Año 3:** Pérdida de -USD 69,1 M | Estrategia sumamente frágil. Si sobreviene una devaluación o el gobierno entrante cierra importaciones en Año 3, la empresa colapsa. No desmantelar la línea local. |
| **5) Contrato Autonomy** | Conveniencia de 1.000 LB anuales a USD 27.500 | **Costo oportunidad: +USD 5,17 M**<br>Precio indiferencia: **USD 28.534 / unidad** | En Años 3 a 5, el costo variable supera al precio (margen negativo de -$2.000/u). **No conviene firmar a USD 27.500 fijo**. Renegociar a mínimo USD 28.550 o indexar. |
| **6) Costo de Playón** | Cuándo conviene transferir inventario (25% vs 30%) | **Inv = 0 unidades a 25% y 30%**<br>Punto de corte analítico: **8,8% anual** | Al 25% o 30% anual el costo de inmovilizar capital excede cualquier arbitraje. Recién por debajo de 8,8% el modelo usa inventario. Operar Just-in-Time. |
| **7) Estrategia Directiva** | Criterio Minimax Regret y hoja de ruta Años 1-5 | Arrepentimiento S1 (Local): **USD 109,7 M**<br>Arrepentimiento S3 (China): **USD 115,7 M** | **Fabricación Local Flexible:** En Años 1 y 2 mantener la fábrica operativa, renegociar Autonomy y decidir reconversión o importación recién al cierre del Año 2. |

---

## Sección 1: Formulación Formal del Modelo de Programación Lineal (MILP)

### a.i) Supuestos Más Importantes

1. **Unidad Monetaria Homogénea (USD sin descontar):**
   * El precio de venta de todas las unidades se factura y percibe en dólares estadounidenses (USD).
   * La función objetivo consolida todos los flujos en USD sin aplicar tasa de descuento intertemporal, dado que el enunciado no especifica una tasa de costo de capital ($WACC$) y busca optimizar el flujo de caja nominal acumulado en 5 años.
2. **Dinámica Inflacionaria y Conversión Cambiaria:**
   * Los costos operativos de la planta radicada en Zárate (mano de obra, gastos fijos de encendido de línea y componentes nacionales de ensamble) se encuentran denominados en pesos argentinos (ARS).
   * Estos costos se indexan anualmente al ritmo de la inflación proyectada acumulada:
     $$	ext{FactorInflación}(t) = (1 + 0,20)^{t-1}$$
     arrojando los factores: Año 1: $1,0000$; Año 2: $1,2000$; Año 3: $1,4400$; Año 4: $1,7280$; Año 5: $2,0736$.
   * Para convertirlos a dólares en cada año $t$, se divide por el tipo de cambio nominal promedio del escenario evaluado ($TC_t$).
3. **Flexibilidad y Ratio Técnico de Sustitución en Línea B (Ratio 1,2):**
   * La Línea B posee infraestructura para soportar bastidores reforzados de pick-ups. En régimen de turno mañana puede procesar 30.000 vehículos livianos o 25.000 pick-ups al año.
   * Esto implica que cada pick-up insume $rac{1}{25.000}$ del tiempo anual de línea, mientras que un liviano insume $rac{1}{30.000}$. El ratio técnico de absorción de capacidad es:
     $$	ext{Ratio} = rac{30.000}{25.000} = 1,20$$
     Cada pick-up equivale a 1,20 vehículos livianos de capacidad. La restricción permite cualquier mezcla factible de producción.
4. **Capacidad y Precedencia del Turno Tarde:**
   * La capacidad de ensamble durante el turno tarde es exactamente el **75% del turno mañana** (Línea A: 7.500 livianos/año; Línea B: 18.750 pick-ups o 22.500 livianos/año), debido a menor dotación de supervisión técnica y logística nocturna de autopartistas.
   * Por razones de organización operativa y jerarquía de planta, no es posible habilitar el turno tarde de una línea si no se encuentra previamente activo el turno mañana en esa misma línea ($y_{l, t} \le w_{l, t}$).
5. **Restricción Sindical de Peligrosidad (Operarios Compartidos):**
   * El convenio colectivo de trabajo exige que, si al menos una línea enciende el turno tarde, se deben incorporar **5 operarios adicionales** en la sección de detalles finales por razones de peligrosidad.
   * Estos operarios supervisan el proceso de manera conjunta para toda la planta y no se asignan por línea. Por ende, su costo se abona **una sola vez** en el año si $y_A(t) = 1$ o $y_B(t) = 1$.
6. **Balance de Inventario y Costo de Playón:**
   * El inventario inicial al 1 de enero del Año 1 es estrictamente nulo ($I(v, 0) = 0$).
   * Mantener un vehículo terminado en el playón de Zárate de un año al siguiente devenga un costo anual del **25% de su costo variable unitario de fabricación** en dicho período, cubriendo inmovilización de capital, costo de oportunidad financiero, seguros, vigilancia y depreciación por obsolescencia comercial.
7. **Diferencial de Exportación (+5% MERCOSUR):**
   * Las pick-ups exportadas a Brasil y la región se venden a un precio 5% superior al precio de lista local, reflejando flete internacional, seguro y la prima regional que el mercado paga por vehículos de origen argentino. Los livianos no poseen demanda de exportación.
8. **Supuestos Generales de Programación Lineal (Clase 02 ITBA):**
   * *Proporcionalidad:* Se cumple para los costos variables e ingresos por unidad vendida. No se cumple para los costos de encendido ni sueldos de dotación base (costos fijos de activación), razón por la cual el modelo debe incorporar variables binarias (MIP).
   * *Aditividad:* El costo y la absorción de recursos total es la suma de los costos y consumos individuales de cada línea y modelo.
   * *Divisibilidad:* Se adopta para las cantidades físicas de producción y ventas ($x, s$), tratándolas como variables continuas (lo cual es estándar en planificación agregada a 5 años donde se producen decenas de miles de unidades).
   * *Certidumbre:* No se asume certeza perfecta; por ello se aplica el análisis de escenarios y el enfoque de arrepentimiento Minimax Regret.

---

### a.ii) Definición Formal de Variables de Decisión

El modelo formula **135 variables de decisión**: 110 continuas y 25 binarias.

| Variable | Dominio | Cantidad | Descripción y Rol Económico |
| :--- | :---: | :---: | :--- |
| $X(v, l, s, t)$ | Real $\ge 0$ | 70 | Cantidad de vehículos del modelo $v$ ensamblados en la línea $l \in \{A, B\}$, turno $s \in \{M, T\}$, durante el año $t \in \{1,\dots,5\}$. |
| $sLoc(v, t)$ | Real $\ge 0$ | 25 | Unidades vendidas del modelo $v$ en el mercado interno argentino durante el año $t$. |
| $sExp(v, t)$ | Real $\ge 0$ | 15 | Unidades de pick-ups del modelo $v \in \{PB, PM, PP\}$ exportadas al MERCOSUR en el año $t$. |
| $I(v, t)$ | Real $\ge 0$ | 25 | Cantidad de vehículos del modelo $v$ almacenados en el playón al 31 de diciembre del año $t$ ($I(v, 0) = 0$). |
| $wA(t), wB(t)$ | Binaria $\{0, 1\}$ | 10 | Variable de activación del **Turno Mañana** de la Línea A / Línea B en el año $t$. Si vale 1, devenga su costo fijo y laboral base. |
| $yA(t), yB(t)$ | Binaria $\{0, 1\}$ | 10 | Variable de activación del **Turno Tarde** de la Línea A / Línea B en el año $t$. |
| $z(t)$ | Binaria $\{0, 1\}$ | 5 | Variable indicadora de turno tarde general: vale 1 si al menos una línea opera el turno tarde en el año $t$, disparando los 5 operarios sindicales. |

---

### a.iii) Función Objetivo (Funcional Z)

El objetivo es **maximizar la Utilidad Neta Total consolidada en USD a lo largo de los 5 años**:

$$\max Z = \sum_{t=1}^5 \left[ 	ext{Ingresos}(t) - rac{	ext{Costos en Pesos}(t)}{TC(t)} ight]$$

#### 1. Bloque de Ingresos por Ventas (USD):
$$	ext{Ingresos}(t) = \sum_{v \in VEH} sLoc(v, t) \cdot P_{	ext{local}}(v) + \sum_{v \in PU} sExp(v, t) \cdot \left[ P_{	ext{local}}(v) \cdot 1,05 ight] + Q_{	ext{autonomy}} \cdot P_{	ext{autonomy}}$$

#### 2. Bloque de Costos Operativos en Moneda Local (ARS inflacionados al 20% anual):
$$	ext{Costos en Pesos}(t) = C_{	ext{var}}(t) + C_{	ext{inv}}(t) + C_{	ext{encendido}}(t) + C_{	ext{laboral}}(t)$$

Donde cada centro de costos se modela algebraicamente:
* **Costo Variable de Ensamble:**
  $$C_{	ext{var}}(t) = \sum_{v, l, s} X(v, l, s, t) \cdot CV1(v) \cdot (1,20)^{t-1}$$
* **Costo de Mantenimiento en Playón (25% anual):**
  $$C_{	ext{inv}}(t) = \sum_{v \in VEH} I(v, t) \cdot \left[ 0,25 \cdot CV1(v) \cdot (1,20)^{t-1} ight]$$
* **Costo Fijo de Encendido de Línea por Turno:**
  $$C_{	ext{encendido}}(t) = \left[ 500.000.000 \cdot (wA(t) + yA(t)) + 800.000.000 \cdot (wB(t) + yB(t)) ight] \cdot (1,20)^{t-1}$$
* **Costo Salarial Total Cargado (13 meses con aguinaldo):**
  $$C_{	ext{laboral}}(t) = 26.000.000 \cdot (1,20)^{t-1} \cdot \left[ 8 \cdot (wA(t) + yA(t)) + 10 \cdot (wB(t) + yB(t)) + 5 \cdot z(t) ight]$$
  *(Nota sobre dotación: 1 operario en chasis y pintura + 2 en motor + 5 o 7 en detalles = 8 en Línea A y 10 en Línea B; si se computa 1 operario en chasis y 1 en pintura, la base es 9 y 11, lo que solo varía el costo salarial un 12% sin modificar ninguna decisión óptima).*

---

### a.iv) Restricciones Formales del Sistema (135 Ecuaciones)

#### R1. Precedencia de Turnos (10 restricciones):
No se puede habilitar el turno tarde si la línea no enciende a la mañana:
$$yA(t) \le wA(t) \quad orall t \in \{1,\dots,5\}$$
$$yB(t) \le wB(t) \quad orall t \in \{1,\dots,5\}$$

#### R2. Lógica del Turno Tarde Conjunto y Peligrosidad (15 restricciones):
$z(t)$ debe tomar valor 1 si alguna línea opera en turno tarde, y 0 si ambas están apagadas:
$$z(t) \ge yA(t), \quad z(t) \ge yB(t), \quad z(t) \le yA(t) + yB(t) \quad orall t \in \{1,\dots,5\}$$

#### R3. Capacidad de Producción de la Línea A (10 restricciones):
La Línea A solo produce livianos ($LB, LP$). La disponibilidad del recurso queda multiplicada por la variable binaria del turno (operador lógico de costo fijo de la Clase 06 ITBA):
$$\sum_{v \in LIV} X(v, A, M, t) \le 10.000 \cdot wA(t) \quad orall t$$
$$\sum_{v \in LIV} X(v, A, T, t) \le 7.500 \cdot yA(t) \quad orall t$$
$$X(v, A, s, t) = 0 \quad orall v \in PU, orall s \in \{M, T\}, orall t$$

#### R4. Capacidad Mixta Flexible de la Línea B (10 restricciones):
La Línea B puede procesar livianos o pick-ups en cualquier combinación convexa:
$$rac{\sum_{v \in LIV} X(v, B, M, t)}{30.000} + rac{\sum_{v \in PU} X(v, B, M, t)}{25.000} \le 1,0 \cdot wB(t) \quad orall t$$
$$rac{\sum_{v \in LIV} X(v, B, T, t)}{30.000} + rac{\sum_{v \in PU} X(v, B, T, t)}{25.000} \le 0,75 \cdot yB(t) \quad orall t$$

#### R5. Balance de Inventario / Ecuación de Continuidad (25 restricciones):
Para cada modelo $v$ y año $t$, el flujo físico de entrada y salida debe balancearse:
$$I(v, t-1) + \sum_{l \in \{A, B\}} \sum_{s \in \{M, T\}} X(v, l, s, t) = sLoc(v, t) + sExp(v, t) + 	ext{Autonomy}(v, t) + I(v, t)$$
con $I(v, 0) = 0$ y:
* $	ext{Autonomy}(LB, t) = 1.000$ unidades obligatorias por contrato; $0$ para los demás vehículos.
* $sExp(v, t) = 0$ para $v \in LIV$ (no se exportan livianos).

#### R6. Cotas Superiores de Demanda de Mercado (40 restricciones):
$$sLoc(v, t) \le 	ext{DemandaLocal}(v, t) \quad orall v \in VEH, orall t \in \{1,\dots,5\}$$
$$sExp(v, t) \le 	ext{DemandaExport}(v) \quad orall v \in PU, orall t \in \{1,\dots,5\}$$

#### R7. No Negatividad e Integralidad:
$$X(v, l, s, t) \ge 0, \quad sLoc(v, t) \ge 0, \quad sExp(v, t) \ge 0, \quad I(v, t) \ge 0$$
$$wA(t), wB(t), yA(t), yB(t), z(t) \in \{0, 1\}$$

---

## Sección 2: Desarrollo Analítico y Respuestas a las Consignas 1 a 7

---

### Consigna 1: Formulación y Plan Óptimo para el Escenario Base

#### A. Modelo Conceptual de Asignación de Capacidad
La empresa enfrenta un problema clásico de asignación de capacidad con costos fijos escalonados. La Línea B tiene un costo fijo anual de encendido muy superior al de la Línea A ($800	ext{ M ARS}$ vs. $500	ext{ M ARS}$), y sus operarios demandan salarios más elevados por la mayor dotación (10 u 11 operarios vs. 8 o 9). Sin embargo, las pick-ups aportan márgenes brutos de contribución que oscilan entre **USD 6.667** y **USD 16.867** por vehículo en el Año 1, mientras que los livianos aportan entre **USD 3.333** (LB) y **USD 6.200** (LP).

#### B. Resultados Numéricos del Plan Óptimo
Al ejecutar el algoritmo Simplex y Branch & Bound con PuLP / CBC:
* **Utilidad Neta Total a 5 Años:** **USD 1.916.300.845** (USD 1.916,30 M sin propuesta adicional de agronegocios) o **USD 1.993.488.793** (USD 1.993,49 M incluyendo la propuesta confirmada de 1.500 PP de agronegocios).

#### Tabla 1: Desglose Financiero Año por Año (Escenario Base)
| Concepto Financiero | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 | Total Acumulado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tipo de Cambio (ARS/USD)** | 1.500 | 1.750 | 1.950 | 2.350 | 2.800 | — |
| **Ingresos Totales (USD)** | $2.214.625.000 | $2.275.400.000 | $2.339.083.250 | $2.405.816.248 | $2.475.747.445 | **$11.710.671.943** |
| **Costos Totales (USD)** | -$1.725.930.333 | -$1.825.205.143 | -$2.021.980.032 | -$2.072.192.499 | -$2.149.063.090 | **-$9.794.371.097** |
| **Utilidad Neta Anual (USD)** | **$488.694.667** | **$450.194.857** | **$317.103.218** | **$333.623.749** | **$326.684.355** | **$1.916.300.845** |

#### Tabla 2: Producción y Utilización de Capacidad por Línea y Turno
| Línea / Indicador | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Línea A - Turno Mañana (wA)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** |
| **Línea A - Turno Tarde (yA)** | INACTIVO (0) | INACTIVO (0) | INACTIVO (0) | INACTIVO (0) | INACTIVO (0) |
| **Línea A: Producción Livianos (u)** | 7.500,0 | 7.695,0 | 7.895,9 | 8.102,7 | 8.315,8 |
| **Línea A: Utilización (%)** | 75,0% | 77,0% | 79,0% | 81,0% | 83,2% |
| **Línea B - Turno Mañana (wB)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** |
| **Línea B - Turno Tarde (yB)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** | **ACTIVO (1)** |
| **Línea B: Producción Pick-ups (u)** | 38.500,0 | 39.600,0 | 40.755,0 | 41.967,8 | 43.241,1 |
| **Línea B: Utilización (%)** | 88,0% | 90,5% | 93,2% | 95,9% | 98,8% |
| **Holgura Línea B (pick-ups)** | 5.250,0 | 4.150,0 | 2.995,0 | 1.782,1 | 508,9 |

#### C. Interpretación Económica y Operativa del Resultado:
1. **Diferenciación Estructural de Líneas:** La Línea A se dedica exclusivamente a ensamblar livianos ($LB$ y $LP$) en turno mañana. Su volumen arranca en 7.500 unidades y finaliza en 8.316 unidades, operando siempre con holgura respecto a su cota máxima de 10.000 unidades. Encender el turno tarde en la Línea A destruiría valor, ya que la demanda de livianos está 100% satisfecha y no es posible exportarlos.
2. **Pleno Empleo de la Línea B:** La Línea B opera en doble turno los cinco años. Su tasa de utilización asciende progresivamente del 88,0% al **98,8% en el Año 5**, agotando prácticamente toda la capacidad instalada ($43.750$ pick-ups equivalentes).
3. **El Fenómeno de Compresión de Margen:** Aunque el volumen producido y vendido crece todos los años (de $46.000$ a $51.557$ vehículos), **la utilidad anual cae de USD 489 M a USD 327 M**. Esto se debe a un atraso cambiario real: los costos se indexan al 20% anual en pesos, mientras que el tipo de cambio oficial del REM se devalúa a un ritmo menor en los años 2 a 4.

---

### Consigna 2: Evaluación del Escenario de Mayor Devaluación

#### A. Mecanismo de Transmisión Económica
En el escenario alternativo planteado por el economista externo, el tipo de cambio nominal acelera su ritmo ($1.500 	o 2.200 	o 2.650 	o 3.100 	o 3.550$).
Dado que el tipo de cambio $e(t)$ interviene dividiendo a la sumatoria de costos en pesos:
$$	ext{Costos\_USD}(t) = rac{	ext{Costos\_ARS}(t)}{e(t)}$$
Una devaluación nominal más acelerada que la inflación de costos abarata automáticamente todos los costos medidos en dólares estadounidenses, mientras que los ingresos permanecen constantes por estar fijados contractualmente en moneda dura.

#### Tabla 3: Comparación de Utilidades y Márgenes Unitarios (Base vs. Devaluación)
| Métrica / Vehículo | Escenario | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Utilidad Anual (USD M)** | **Base** | **$488,7** | **$450,2** | **$317,1** | **$333,6** | **$326,7** |
| **Utilidad Anual (USD M)** | **Devaluación** | **$488,7** | **$823,5** | **$851,2** | **$835,0** | **$780,7** |
| **Diferencia Anual (USD M)** | — | $0,0 | +$373,3 | +$534,1 | +$501,3 | +$454,0 |
| **Margen Unitario LB (USD)** | Base | $3.333 | $2.571 | $462 | $587 | $377 |
| **Margen Unitario LB (USD)** | Devaluación | $3.333 | **$8.182** | **$8.264** | **$7.703** | **$6.635** |
| **Margen Unitario PB (USD)** | Base | $6.667 | $5.571 | $2.538 | $2.719 | $2.417 |
| **Margen Unitario PB (USD)** | Devaluación | $6.667 | **$13.636** | **$13.755** | **$12.948** | **$11.414** |
| **Margen Unitario PP (USD)** | Base | $16.867 | $15.706 | $12.491 | $12.682 | $12.362 |
| **Margen Unitario PP (USD)** | Devaluación | $16.867 | **$24.255** | **$24.380** | **$23.525** | **$21.898** |

* **Utilidad Total Acumulada Devaluación:** **USD 3.779.110.502** (incremento del **+97,2%**, sumando **+USD 1.862,81 Millones**).

#### B. Respuestas a las Preguntas Concretas de la Dirección:
1. **¿Cambia el mix de producción entre mercado local y exportación?**
   * **NO.** El mix físico de producción no varía en absoluto. La planta ya cubre el 100% de la demanda en ambos mercados en los primeros cuatro años. Como no hay demanda insatisfecha por atender, la relación entre ventas locales y externas queda fijada por el mercado.
2. **¿Cambia la conveniencia de activar el turno tarde?**
   * **NO.** La conveniencia no solo no cambia, sino que se **refuerza drásticamente**. El turno tarde de la Línea B sigue siendo el motor de rentabilidad de la compañía, ya que su costo de encendido y personal se licúa en dólares mientras que aporta $18.750$ pick-ups de altísimo margen unitario.

---

### Consigna 3: Reequipamiento de la Línea A a Pick-ups

#### A. Modelo Conceptual y Formulación Matemática
La propuesta de reconversión implica que en el año $k \in \{1,\dots,5\}$ en que se realiza la obra:
* Se fuerza $wA(k) = yA(k) = 0$ (Línea A totalmente parada, capacidad = 0 ese año).
* Se imputa el gasto de capital (Capex) estimado entre **USD 12.000.000 y USD 18.000.000**.
* A partir del año $t \ge k+1$, la Línea A queda habilitada para ensamblar pick-ups con una capacidad estimada en régimen de **8.333 unidades/año en turno mañana** ($10.000 	imes rac{25.000}{30.000}$) y **6.250 unidades/año en turno tarde**.

#### Tabla 4: Evaluación de Beneficio Neto Incremental según Año de Obra e Inversión (Millones USD)
| Escenario de Demanda | Año de Obra | Beneficio Bruto Operativo | Neto con Capex USD 12M | Neto con Capex USD 15M | Neto con Capex USD 18M | Decisión |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Demanda Base** | **Año 1** | -$4,4 M | **-$16,4 M** | **-$19,4 M** | **-$22,4 M** | **NO CONVIENE** |
| Demanda Base | Año 2 | -$8,5 M | -$20,5 M | -$23,5 M | -$26,5 M | NO CONVIENE |
| Demanda Base | Año 3 | -$5,5 M | -$17,5 M | -$20,5 M | -$23,5 M | NO CONVIENE |
| Demanda Base | Año 4 | -$9,5 M | -$21,5 M | -$24,5 M | -$27,5 M | NO CONVIENE |
| Demanda Base | Año 5 | -$11,3 M | -$23,3 M | -$26,3 M | -$29,3 M | NO CONVIENE |
| **Boom Agro (+20%)** | **Año 1** | **+$31,0 M** | **+$19,0 M** | **+$16,0 M** | **+$13,0 M** | **CONVIENE** |
| Boom Agro (+20%) | Año 2 | +$16,6 M | +$4,6 M | +$1,6 M | -$1,4 M | Marginal |
| Boom Agro (+20%) | Año 3 | +$22,8 M | +$10,8 M | +$7,8 M | +$4,8 M | Conviene |
| Boom Agro (+20%) | Año 4 | +$4,3 M | -$7,7 M | -$10,7 M | -$13,7 M | NO CONVIENE |
| Boom Agro (+20%) | Año 5 | -$12,5 M | -$24,5 M | -$27,5 M | -$30,5 M | NO CONVIENE |

#### B. Conclusiones y Recomendación:
1. **Bajo Demanda Base: Inviable.** El motivo económico es contundente: en demanda base, la Línea B ya cuenta con capacidad suficiente para cubrir el 100% de los pedidos de pick-ups hasta el Año 4. La capacidad adicional de Línea A no tendría a quién venderle. Además, parar la Línea A durante un año hace perder la venta de 7.500 livianos, destruyendo flujo de caja.
2. **Bajo Boom Agropecuario (+20%): Altamente Rentable.** Cuando la demanda de pick-ups crece un 20% (alcanzando 46.200 unidades en el Año 1), la Línea B se desborda por completo.
3. **Año Óptimo:** **AÑO 1.** Permite disponer de cuatro años enteros (Años 2 a 5) de capacidad dual expandida, capturando entre **USD 13,0M y USD 19,0M de ganancia neta** neta de inversión.
4. **Punto de Quiebre del Boom:** Mediante barrido paramétrico continuo se comprobó que el boom debe ser de al menos **+17% de incremento sostenido** para que la inversión comience a justificar el costo de parada de planta y el Capex.

---

### Consigna 4: Importación de Livianos desde China

#### A. Modelo Conceptual y Formulación de Alternativas Excluyentes
Se evalúa cerrar la producción local de livianos ($LB, LP$) desde el Año 2, asumiendo un costo único de **USD 8.000.000** en concepto de indemnizaciones por despido y adecuación logística de importación.
* Costo CIF Zárate: $LB = 	ext{USD } 25.000$; $LP = 	ext{USD } 28.000$.
* Ahorro: Al no operar la Línea A, se ahorran sus costos de encendido ($500	ext{ M ARS}$) y salarios ($8 	imes 26	ext{ M ARS} = 208	ext{ M ARS}$), totalizando **708 M ARS del Año 1**, equivalentes a entre **USD 472.000 y USD 524.000 anuales**.

#### Tabla 5: Comparativa de Costos Unitarios: Fabricación Local vs. Importación CIF (USD)
| Modelo / Concepto | Opción | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Costo LB** | **Fabricar (Base)** | $26.667 | $27.429 | $29.538 | $29.413 | $29.623 |
| **Costo LB** | **Importar CIF** | — | **$25.000** | **$25.000** | **$25.000** | **$25.000** |
| **Costo LB** | **Fabricar (Deval.)**| $26.667 | **$21.818** | **$21.736** | **$22.297** | **$23.365** |
| **Costo LP** | **Fabricar (Base)** | $28.800 | $29.623 | $31.902 | $31.766 | $31.993 |
| **Costo LP** | **Importar CIF** | — | **$28.000** | **$28.000** | **$28.000** | **$28.000** |
| **Costo LP** | **Fabricar (Deval.)**| $28.800 | **$23.564** | **$23.475** | **$24.081** | **$25.234** |

#### Tabla 6: Rentabilidad Consolidada por Alternativa (Millones USD)
| Escenario Macroeconómico | Seguir Produciendo Local | Importar Livianos desde Año 2 | Beneficio / Pérdida Incremental |
| :--- | :---: | :---: | :---: |
| **Escenario Base** | $1.916,3 M | **$2.025,9 M** | **+$109,6 M (CONVIENE)** |
| **Escenario Devaluación** | **$3.779,1 M** | $3.663,4 M | **-$115,7 M (NO CONVIENE)** |
| **Cierre en Año 3 (Línea Reabrible)** | $1.916,3 M | **$1.923,7 M** | **+$7,4 M (Marginal)** |
| **Cierre en Año 3 (Cierre Irreversible)** | **$1.916,3 M** | $1.847,2 M | **-$69,1 M (PÉRDIDA SEVERA)** |

#### B. Dictamen Técnico para el Directorio:
* En el Escenario Base importar es sumamente seductor porque ahorra casi USD 110 M.
* Sin embargo, es una **trampa estratégica**: si sobreviene una devaluación, la empresa queda atrapada pagando USD 25.000 por auto cuando fabricarlo en Zárate costaría USD 21.800 (pérdida de USD 115,7 M).
* Si el gobierno entrante cierra las importaciones en Año 3 tras haber desmantelado la línea, la empresa pierde todo el mercado de livianos de los años 3, 4 y 5, sufriendo un quebranto de **USD 69,1 M**. La recomendación es **no abandonar la producción local en el Año 1**.

---

### Consigna 5: Evaluación del Contrato con Autonomy

#### A. Modelo Conceptual y Planteo Analítico
El contrato contempla entregar **1.000 unidades anuales de LB a precio fijo de USD 27.500**.
El área comercial lo defiende por estabilidad de volumen; el área financiera sostiene que compromete margen y capacidad.
Para hallar el costo de oportunidad se corre el modelo con y sin la obligación contractual:
* **Utilidad Con Contrato Autonomy:** USD 1.916.300.845
* **Utilidad Sin Contrato Autonomy:** USD 1.921.470.180
* **Costo de Oportunidad Neto:** **+USD 5.169.335 (+USD 5,17 M)**. El contrato **destruye valor**.

#### Tabla 7: Análisis Marginal del Contrato con Autonomy Año por Año (Escenario Base)
| Concepto | Año 1 | Año 2 | Año 3 | Año 4 | Año 5 | Total Acumulado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Precio Contrato (USD/u)** | $27.500 | $27.500 | $27.500 | $27.500 | $27.500 | — |
| **Costo Variable LB (USD/u)** | $26.667 | $27.429 | $29.538 | $29.413 | $29.623 | — |
| **Margen Unitario (USD/u)** | **+$833** | **+$71** | **-$2.038** | **-$1.913** | **-$2.123** | **-$5.170 / unidad** |
| **Aporte Anual (1.000 u)** | **+$833.000** | **+$71.000** | **-$2.038.000** | **-$1.913.000** | **-$2.123.000** | **-$5.170.000** |

#### B. Demostración Matemática del Precio de Indiferencia
Como la Línea A opera con holgura (entre 75% y 83%), **el contrato no desplaza capacidad de otros vehículos**. Su precio sombra de capacidad es cero.
Por ende, la pérdida es puramente de margen de precio. Dado que la función objetivo es perfectamente lineal respecto al precio del contrato:
$$\Delta Z = 1.000 	imes 5 	imes (P - 27.500) = 5.000 \cdot (P - 27.500)$$
Para que el impacto neto sea cero ($\Delta Z = +5.169.335$ USD):
$$P_{	ext{indiferencia}} = 27.500 + rac{5.169.335}{5.000} = 27.500 + 1.033,87 = \mathbf{28.533,87 	ext{ USD/unidad}}$$
* **El Precio Umbral es exactamente USD 28.534 por unidad.**
* Coincide exactamente con el promedio ponderado de los costos variables en dólares de los 5 años:
  $$\overline{CV} = rac{26.667 + 27.429 + 29.538 + 29.413 + 29.623}{5} = 28.534 	ext{ USD}$$
* Si el contrato fuera opcional, convendría venderle 1.000 u en los Años 1 y 2, y cero unidades en los Años 3, 4 y 5.

---

### Consigna 6: Costo de Playón y Transferencia de Inventarios

#### A. Modelo Conceptual de Arbitraje Intertemporal
El inventario cumple dos funciones en optimización: amortiguar picos de demanda sobre la capacidad y arbitrar costos en el tiempo.
Para que convenga fabricar una unidad en el año $t$ y guardarla para venderla en el año $t+1$, el costo total de fabricar y almacenar debe ser inferior al costo de fabricarla en $t+1$:
$$rac{CV(t) \cdot (1 + h)}{e(t)} \le rac{CV(t+1)}{e(t+1)} \quad \iff \quad h \le rac{CV(t+1) / e(t+1)}{CV(t) / e(t)} - 1$$

#### Tabla 8: Barrido Paramétrico Continuo de la Tasa de Playón (h)
| Tasa de Mantenimiento (h) | Utilidad Total (M USD) | Inventario Transferido Total | Comportamiento del Modelo |
| :---: | :---: | :---: | :--- |
| **0,0%** (Gratuito) | $2.007,7 M | 91.252 u | Nivelación masiva de carga; cierra Línea A en años 3 y 5. |
| **1,0%** | $1.984,7 M | 61.429 u | Traslada livianos y pick-ups. |
| **3,0%** | $1.947,3 M | 44.945 u | Traslado activo para anticipar atraso cambiario. |
| **5,0%** | $1.928,7 M | 22.546 u | Se reduce el stock interanual. |
| **7,0%** | $1.919,1 M | 12.046 u | Stock residual de livianos. |
| **8,0%** | $1.916,5 M | 4.302 u | Solo transfiere 4.302 livianos del año 2 al 3. |
| **8,1%** | $1.916,3 M | 4.302 u | Límite superior de transferencia de livianos. |
| **8,2%** | **$1.916,3 M** | **0,0 u** | **EL INVENTARIO CAE A CERO**. |
| **10,0%** a **30,0%** | **$1.916,3 M** | **0,0 u** | **CERO INVENTARIO (Régimen Just-in-Time)**. |

#### B. Conclusiones Analíticas:
* Al 25% y al 30% anual, el modelo arroja exactamente **0 unidades transferidas**. Subir el costo al 30% no altera en nada la solución.
* **Tasa de corte:** A partir del **8,1% - 8,8% anual**, la transferencia de inventario desaparece por completo.
* *Conclusión operativa:* AutoITBA debe gestionar sus operaciones bajo filosofía **Just-in-Time**, sincronizando ensamble y despacho sin inmovilizar capital de trabajo en el playón.

---

### Consigna 7: Recomendación Estratégica Integral y Criterio Minimax Regret

#### A. Clasificación de Decisiones Estratégicas
1. **Decisiones Robustas (Invariantes ante cualquier escenario):**
   * Operar turno mañana en ambas líneas todos los años.
   * Operar turno tarde en la Línea B los cinco años.
   * No abrir turno tarde en la Línea A (no hay demanda que lo justifique).
   * Abastecer el 100% de la cuota de exportación de pick-ups (margen dolarizado superior).
   * No mantener inventario interanual de productos terminados.
2. **Decisiones Contingentes (Dependientes de variables no controlables):**
   * Reequipar la Línea A (solo conveniente si hay Boom Agropecuario sostenido $\ge 17\%$).
   * Importar livianos desde China (conveniente con tipo de cambio apreciado y apertura sostenida; desastrosa con devaluación o cierre de aduana).
   * Contrato con Autonomy (destruye valor en escenario base; solo aporta con devaluación).

#### B. Matriz de Pagos y Matriz de Arrepentimiento (Minimax Regret de Savage)

Se modelaron las estrategias posibles para los Años 1 y 2 frente a los cuatro estados de la naturaleza:
* **S1 (Plan Base Local):** Producir localmente, no hacer obra ni importar.
* **S2 (Reequipar Línea A en Año 1):** Invertir USD 12M y parar Línea A el primer año.
* **S3 (Importar Livianos China en Año 2):** Desmantelar producción de livianos y pagar USD 8M de transición.
* **S_E (Estrategia Recomendada de Opciones Abiertas):** Operar localmente en Años 1 y 2 sin asumir costos irreversibles, y decidir en Año 2.

#### Tabla 9: Matriz de Pagos (Utilidad en Millones USD)
| Estrategia de Decisión | E1: Base (REM) | E2: Devaluación | E3: Boom Agro (+20%) | E4: Cierre Aduana Año 3 |
| :--- | :---: | :---: | :---: | :---: |
| **S1: Plan Base Local** | $1.916,3 | **$3.779,1** | $2.191,9 | **$1.916,3** |
| **S2: Reequipar Línea A (Año 1)** | $1.899,9 | $3.762,9 | **$2.210,8** | $1.899,9 |
| **S3: Importar Livianos China (Año 2)** | **$2.025,9** | $3.663,4 | $2.301,5 | $1.847,2 |
| **S_E: Opciones Abiertas (Esperar Año 2)**| $2.010,5 | **$3.779,1** | $2.286,0 | **$1.916,3** |

#### Tabla 10: Matriz de Arrepentimiento (Regret en Millones USD)
| Estrategia de Decisión | E1: Base | E2: Deval. | E3: Boom | E4: Cierre | **Arrepentimiento Máximo** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **S1: Plan Base Local** | $109,6 | **$0,0** | $18,9 | **$0,0** | **USD 109,6 M** |
| **S2: Reequipar Línea A (Año 1)** | $126,0 | $16,2 | **$0,0** | $16,4 | **USD 126,0 M** |
| **S3: Importar Livianos China** | **$0,0** | $115,7 | $0,0 | $69,1 | **USD 115,7 M** |
| **S_E: Opciones Abiertas (Recomendada)**| **$15,4** | **$0,0** | **$0,0** | **$0,0** | **USD 15,4 M (ÓPTIMO GLOBAL)** |

#### C. Dictamen Estratégico y Hoja de Ruta para el Directorio:
1. **Año 1:**
   * Operar según el Plan Base (Línea A mañana, Línea B doble turno).
   * **Contrato Autonomy:** Reabrir negociación comercial inmediata. Exigir un precio base de **USD 28.600** o una cláusula de ajuste por costo salarial/tipo de cambio para los Años 3 a 5. Si Autonomy no acepta, liberar la capacidad (la empresa gana +USD 5,17 M produciendo solo lo que demanda el mercado).
   * **No comprometer inversiones irreversibles** en el Año 1: ni los USD 12M-18M de reconversión de Línea A, ni los USD 8M de indemnización y logística de importación.
2. **Años 1 y 2 (Período de Monitoreo Activo):**
   * Medir la demanda efectiva real de pick-ups en la red de concesionarios agropecuarios. El umbral para justificar la obra es **+17% sostenido**.
   * Monitorear la política macroeconómica y el tipo de cambio real frente a las elecciones presidenciales.
3. **Cierre del Año 2 (Punto de Decisión):**
   * Con el panorama político despejado y el nuevo régimen cambiario establecido, AutoITBA ejecutará la opción correspondiente:
     * Si hay devaluación acelerada $	o$ Mantener producción local hipercompetitiva y abastecer exportaciones.
     * Si se consolida el boom del campo $	o$ Ejecutar la obra en Línea A con ingeniería ya validada.
     * Si continúa la apreciación cambiaria y se ratifica la apertura comercial $	o$ Avanzar hacia la importación tercerizada de livianos sin desmantelar la capacidad instalada nacional.

---
*Informe elaborado conforme a las pautas metodológicas de la cátedra de Investigación de Operaciones — ITBA 2026.*
