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

## Sección 1: Formulación Formal del Modelo (MILP)

### a.i) Supuestos Más Importantes
1. **Unidad Monetaria Homogénea (USD sin descontar):** El precio de venta de todas las unidades se factura y percibe en dólares estadounidenses (USD). La función objetivo consolida todos los flujos en USD sin aplicar tasa de descuento intertemporal, optimizando el flujo de caja nominal acumulado en 5 años.
2. **Dinámica Inflacionaria y Conversión Cambiaria:** Los costos operativos de la planta radicada en Zárate (mano de obra, gastos fijos de encendido de línea y componentes nacionales de ensamble) se encuentran denominados en pesos argentinos (ARS). Se indexan anualmente al ritmo de la inflación proyectada acumulada: $	ext{FactorInflación}(t) = (1 + 0,20)^{t-1}$, arrojando los factores: Año 1: $1,0000$; Año 2: $1,2000$; Año 3: $1,4400$; Año 4: $1,7280$; Año 5: $2,0736$. Para convertirlos a dólares en cada año $t$, se divide por el tipo de cambio oficial promedio del escenario evaluado ($TC_t$).
3. **Flexibilidad y Ratio Técnico de Sustitución en Línea B (Ratio 1,2):** La Línea B posee infraestructura para soportar bastidores reforzados de pick-ups. En régimen de turno mañana puede procesar 30.000 vehículos livianos o 25.000 pick-ups al año. El ratio técnico de absorción de capacidad es $30.000 / 25.000 = 1,20$. Cada pick-up equivale a 1,20 vehículos livianos de capacidad. La restricción permite cualquier mezcla factible de producción.
4. **Capacidad y Precedencia del Turno Tarde:** La capacidad de ensamble durante el turno tarde es exactamente el **75% del turno mañana** (Línea A: 7.500 livianos/año; Línea B: 18.750 pick-ups o 22.500 livianos/año). No es admisible habilitar el turno tarde de una línea si no se encuentra previamente activo el turno mañana en esa misma línea ($y_{l, t} \le w_{l, t}$).
5. **Restricción Sindical de Peligrosidad (Operarios Compartidos):** Si al menos una línea enciende el turno tarde, se deben incorporar **5 operarios adicionales** en la sección de detalles finales por razones de peligrosidad. Estos operarios supervisan el proceso de manera conjunta para toda la planta y no se asignan por línea. Su costo se abona una sola vez en el año si $y_A(t) = 1$ o $y_B(t) = 1$.
6. **Balance de Inventario y Costo de Playón:** El inventario inicial en Año 1 es cero ($I(v, 0) = 0$). Mantener un vehículo terminado en el playón de Zárate de un año al siguiente devenga un costo anual del **25% de su costo variable unitario de fabricación** en dicho período.
7. **Diferencial de Exportación (+5% MERCOSUR):** Las pick-ups exportadas a Brasil y la región se venden a un precio 5% superior al precio de lista local por flete, seguro y prima regional de origen argentino. Los livianos no poseen demanda de exportación.

### a.ii) Definición Formal de Variables de Decisión
* $X(v, l, s, t) \ge 0$: Cantidad de vehículos del modelo $v$ ensamblados en la línea $l \in \{A, B\}$, turno $s \in \{M, T\}$, en el año $t \in \{1,\dots,5\}$.
* $sLoc(v, t) \ge 0$: Unidades vendidas del modelo $v$ en el mercado interno argentino en el año $t$.
* $sExp(v, t) \ge 0$: Unidades de pick-ups del modelo $v \in \{PB, PM, PP\}$ exportadas al MERCOSUR en el año $t$.
* $I(v, t) \ge 0$: Cantidad de vehículos del modelo $v$ almacenados en el playón al 31 de diciembre del año $t$ ($I(v, 0) = 0$).
* $wA(t), wB(t) \in \{0, 1\}$: Vale 1 si la línea A / B opera en Turno Mañana en el año $t$.
* $yA(t), yB(t) \in \{0, 1\}$: Vale 1 si la línea A / B opera en Turno Tarde en el año $t$.
* $z(t) \in \{0, 1\}$: Vale 1 si al menos una línea opera el Turno Tarde en el año $t$ (dispara los 5 operarios sindicales).

### a.iii) Función Objetivo (Funcional Z)
$$\max Z = \sum_{t=1}^5 \left[ 	ext{Ingresos}(t) - rac{	ext{Costos en Pesos}(t)}{TC(t)} ight]$$
* $	ext{Ingresos}(t) = \sum_{v} sLoc(v, t) \cdot P_{	ext{local}}(v) + \sum_{v \in PU} sExp(v, t) \cdot [P_{	ext{local}}(v) \cdot 1,05] + 	ext{Autonomy}(t) \cdot 27.500$
* $	ext{Costos en Pesos}(t) = C_{	ext{var}}(t) + C_{	ext{inv}}(t) + C_{	ext{encendido}}(t) + C_{	ext{laboral}}(t)$
  * $C_{	ext{var}}(t) = \sum X(v, l, s, t) \cdot CV1(v) \cdot (1,20)^{t-1}$
  * $C_{	ext{inv}}(t) = \sum I(v, t) \cdot [0,25 \cdot CV1(v) \cdot (1,20)^{t-1}]$
  * $C_{	ext{encendido}}(t) = [500	ext{M} \cdot (wA+yA) + 800	ext{M} \cdot (wB+yB)] \cdot (1,20)^{t-1}$
  * $C_{	ext{laboral}}(t) = 26	ext{M} \cdot (1,20)^{t-1} \cdot [8 \cdot (wA+yA) + 10 \cdot (wB+yB) + 5 \cdot z]$

---

## Sección 2: Desarrollo Punto por Punto y Procedimientos Utilizados

---

### CONSIGNA 1: El Modelo Base a 5 Años

#### 1. ¿Cuál es la idea de negocio?
Determinar la estrategia óptima para los próximos 5 años bajo las condiciones esperadas ("Escenario Base"):
* ¿Qué turnos nos conviene prender en cada línea cada año?
* ¿Cuántas unidades fabricar de cada modelo?
* ¿Nos conviene fabricar de más y guardar autos en el playón (stock) para el año siguiente, o fabricar justo lo que se vende?

#### 2. ¿Cómo lo resuelve el código por dentro?
El script principal llama a la función `solve_model(scenario='base')` dentro de `model_engine.py`. Esto es lo que hace paso a paso:
1. **La conversión de monedas (Pesos a Dólares):**
   * Los precios de venta están fijados en dólares (USD).
   * Pero los sueldos, el costo de encender las máquinas y los insumos locales están en pesos argentinos (ARS) y aumentan un 20% anual por inflación.
   * El código hace un bucle año por año (`for t in years`) y calcula cuánto representa cada costo en dólares dividiendo por el dólar oficial de ese año (1.500, 1.750, 1.950, 2.350 y 2.800).
2. **Las "palancas" que el modelo puede mover (Variables de Decisión):**
   * *Variables binarias ($Y$ y $W\_tarde$):* Son como llaves de luz (valen 1 o 0).
     * $Y$: ¿Prendemos la Línea A a la mañana? ¿A la tarde? ¿Y la Línea B?
     * $W\_tarde$: Si alguna línea abre a la tarde, el sindicato exige contratar 5 operarios extra de peligrosidad. Esta variable se prende en 1 automáticamente si alguna línea trabaja a la tarde.
   * *Variables continuas ($X, S, I$):*
     * $X$: Cuántos autos fabricar de cada modelo en cada turno y línea.
     * $S$: Cuánto vender en el mercado local, cuánto exportar y cuánto entregar a contratos especiales (Autonomy y Agronegocios).
     * $I$: Cuántos autos quedan guardados en el playón al final de cada año.
3. **Los bucles de restricciones (Las reglas que no se pueden romper):**
   * *Bucle de Balance de Inventario:* Por cada año y por cada modelo, se asegura de que:
     $$	ext{Lo que tenía del año pasado} + 	ext{Lo que fabriqué hoy} = 	ext{Lo que vendo hoy} + 	ext{Lo que me sobra}$$
   * *Bucle de Capacidad de Máquinas:* La Línea A no puede superar 10.000 autos a la mañana ni 7.500 a la tarde. Para la Línea B se aplica la regla de que 1 pick-up equivale a 1,2 livianos de espacio en la cinta.
   * *Bucle de Jerarquía de Turnos:* No se permite abrir la tarde si la mañana de esa misma línea está apagada.
   * *Bucle de Demanda:* No podés vender más autos de los que los clientes quieren comprar.
4. **La Función Objetivo (El criterio de éxito):**
   * El código le dice al solver: *"Maximizá la suma de todos los ingresos por ventas menos todos los costos (insumos, sueldos, encendido de líneas y costo de playón)"*.

#### 3. ¿Qué resultado arroja y qué significa?
* **Ganancia total acumulada a 5 años:** **USD 1.993,49 Millones** (o USD 1.916,30 M sin agronegocios).
* **Línea A (Livianos):** Trabaja solo en Turno Mañana. Nunca hace falta prender el turno tarde porque la demanda de livianos es chica y la mañana alcanza de sobra.
* **Línea B (Pick-ups):** Trabaja a doble turno pleno (Mañana y Tarde) todos los 5 años. Las pick-ups dejan mucho más margen de ganancia, por lo que conviene explotar la línea al máximo.
* **Inventario (Playón):** Da cero (0 unidades) en todos los años. Tener autos parados en el playón cuesta un 25% anual de su valor, lo cual es carísimo; el modelo concluye que lo más inteligente es una producción Just-in-Time (fabricar y despachar en el mismo año).

---

### CONSIGNA 2: Evaluación de Devaluación Acelerada

#### 1. ¿Cuál es la idea de negocio?
Evaluar qué le pasa a la empresa si la economía argentina sufre una devaluación más fuerte de lo previsto (el dólar pasa de $1.500 en el Año 1 a $3.550 en el Año 5, en vez de los $2.800 del caso base). Las preguntas centrales de la cátedra son:
1. ¿Aumenta o disminuye la ganancia neta?
2. ¿Cambia la conveniencia de activar el turno tarde?
3. ¿Cambia la proporción de autos que vendemos en Argentina versus lo que exportamos al MERCOSUR?

#### 2. ¿Cómo lo resuelve el código por dentro?
En `run_experiments.py`:
1. **Reutiliza el mismo motor:** Llama a `model.solve_model(scenario='devaluacion')`.
2. **Cambia el vector de Tipo de Cambio:** En lugar de dividir los costos en pesos por el sendero base, usa el sendero devaluado:
   * Año 1: $1.500
   * Año 2: $2.200 (en vez de $1.750)
   * Año 3: $2.650 (en vez de $1.950)
   * Año 4: $3.100 (en vez de $2.350)
   * Año 5: $3.550 (en vez de $2.800)
3. **El efecto matemático:** Como los ingresos de la empresa están en dólares fijos, pero gran parte de los costos operativos están en pesos con inflación del 20%, un dólar más alto hace que los costos medidos en dólares se licúen (se hagan mucho más chicos). Por ejemplo, en el Año 5 fabricar una pick-up básica pasa de costar USD 42.583 en el caso base a costar USD 33.586 en el escenario devaluado.
4. **Comparación automática:** El código compara las métricas clave de ambos escenarios:
   `diff_dev = res_dev['objective_value'] - res_base['objective_value']`
   Itera año por año comparando los turnos activos y los totales vendidos en el mercado local y de exportación.

#### 3. ¿Qué conclusiones arroja la Consigna 2?
1. **Impacto en la ganancia:** La utilidad casi se duplica, saltando de USD 1.993,49 M a **USD 3.910,05 M (+96,14% de ganancia extra)**. Al ser una industria con costos locales en pesos e ingresos en dólares, la devaluación la vuelve enormemente rentable.
2. **¿Conviene prender el turno tarde?** Sí, con más razón que nunca. Si en el caso base ya era rentable, con costos salariales licuados en dólares el turno tarde de la Línea B es una máquina de generar margen neto. Apagarlo sería un error gravísimo.
3. **¿Cambia el mix local vs exportación?**
   * En los Años 1 a 4, la fábrica abastece el 100% de ambos mercados.
   * En el Año 5, la demanda total de pick-ups supera el tope físico de la Línea B (43.750 camionetas). Ante este cuello de botella, el modelo prioriza siempre al 100% las exportaciones, porque pagan un sobreprecio del 5% en dólares limpios, y ajusta apenas 282 unidades de la pick-up básica en el mercado local (por ser la de menor margen).

---

### CONSIGNA 3: Reequipamiento de la Línea A a Pick-ups

#### 1. ¿Cuál es la idea de negocio?
El gerente operativo quiere adaptar la Línea A para ensamblar pick-ups, aprovechando que es el segmento más rentable. La obra exige parar la Línea A durante 1 año entero (capacidad = 0) e invertir entre USD 12M y USD 18M.
* ¿Existe algún escenario que justifique la inversión durante los 5 años?
* ¿Cambia si la demanda de pick-ups crece un +20% por un boom del campo?
* ¿Cuál es el año óptimo para realizar la obra?

#### 2. ¿Cómo lo resuelve el código por dentro?
En `model_engine.py` y `run_experiments.py`:
1. Se parametriza el año de obra `retool_line_A_year` $\in \{1, 2, 3, 4, 5\}$.
2. En el año de obra $t$, se fija forzosamente $wA(t) = yA(t) = 0$ (parada total de planta).
3. A partir del año $t+1$, se habilita a la Línea A para fabricar pick-ups aplicando el factor de equivalencia (capacidad 8.333 pick-ups/año mañana y 6.250 tarde).
4. Se descuenta la inversión (USD 12M, 15M o 18M) del funcional y se corre para demanda base y para demanda con boom (+20% en pick-ups).

#### 3. ¿Qué resultado arroja y qué significa?
* **Demanda Base: NO CONVIENE EN NINGÚN AÑO.** La ganancia operativa incremental es negativa en todos los años (pierde entre USD 4,4M y 11,3M antes de inversión, y entre USD 16M y 31M neta). Parar la Línea A hace perder 7.500 livianos, y la Línea B ya alcanzaba para todas las pick-ups hasta el Año 4.
* **Boom Agropecuario (+20%): SÍ CONVIENE rotundamente.** La demanda salta a 46.200 pick-ups, desbordando la Línea B.
* **Año Óptimo:** **AÑO 1.** Aporta una ganancia neta de entre **+USD 13,0M y +USD 19,0M** neta de inversión, permitiendo aprovechar 4 años completos de capacidad dual expandida.

---

### CONSIGNA 4: Importación de Livianos desde China

#### 1. ¿Cuál es la idea de negocio?
Evaluar si AutoITBA debe cerrar la producción local de livianos a partir del Año 2 y reemplazarla por autos importados desde China a precio CIF (LB: USD 25.000 / LP: USD 28.000), pagando USD 8.000.000 de costo único por indemnizaciones y logística.
* ¿Conviene en escenario base? ¿Y con devaluación?
* ¿Qué pasa si el nuevo gobierno cierra las importaciones en el Año 3?

#### 2. ¿Cómo lo resuelve el código por dentro?
1. Se activan variables de importación $M_{	ext{china}}(m, t)$ para $m \in \{LB, LP\}$ a partir de $t \ge 2$.
2. Se fuerza a cero la producción local de livianos en la planta ($X = 0$).
3. Al cerrar la Línea A, el modelo ahorra automáticamente sus costos fijos de encendido y salarios ($708	ext{ M ARS}$ del Año 1).
4. Se introduce el riesgo regulatorio fijando $M_{	ext{china}} = 0$ a partir de $t \ge 3$, evaluando si la Línea A puede reabrirse o si queda cerrada irreversiblemente.

#### 3. ¿Qué resultado arroja y qué significa?
* **Escenario Base: Conviene (+USD 109,7 M de ganancia neta).** Importar a USD 25k/28k es más barato que fabricar localmente a USD 27,4k-29,6k, sumado al ahorro de costos fijos de Línea A.
* **Escenario Devaluación: NO CONVIENE (-USD 115,7 M de pérdida).** La devaluación abarata los costos locales a USD 21,8k-23,4k, volviendo a la fábrica nacional mucho más competitiva que los autos chinos en dólares fijos.
* **Riesgo Regulatorio en Año 3:** Si se cierran importaciones y la línea fue desmantelada, la empresa pierde **USD 69,1 M**; si la línea es reabrible, la ganancia se desploma a apenas **+USD 7,4 M** (se pagaron USD 8M de transición para ganar un solo año). No conviene desmantelar la fábrica.

---

### CONSIGNA 5: Evaluación del Contrato con Autonomy

#### 1. ¿Cuál es la idea de negocio?
Autonomy ofrece comprar 1.000 unidades anuales de LB a precio fijo de USD 27.500 durante los 5 años.
* Área comercial: Lo defiende por estabilidad de volumen.
* Área financiera: Dice que ocupa capacidad y compromete rentabilidad.
* Preguntas: ¿Cuál es el costo de oportunidad? ¿A qué precio umbral deja de convenir?

#### 2. ¿Cómo lo resuelve el código por dentro?
1. Se resuelve el modelo con la restricción obligatoria $S_{	ext{autonomy}}(t) = 1.000$.
2. Se resuelve el modelo liberando la capacidad ($S_{	ext{autonomy}}(t) = 0$).
3. Se resta la utilidad de ambos escenarios para hallar el costo de oportunidad: $	ext{Costo Oportunidad} = Z_{	ext{sin}} - Z_{	ext{con}}$.
4. Se calcula el precio de indiferencia analítico aprovechando que la función objetivo es perfectamente lineal respecto al precio del contrato.

#### 3. ¿Qué resultado arroja y qué significa?
* **El contrato destruye USD 5,17 Millones de valor.**
* **¿Por qué?** No es por falta de capacidad (la Línea A opera al 75%-83%). La pérdida es de margen puro: en los Años 3, 4 y 5 fabricar un LB cuesta USD 29.538, USD 29.413 y USD 29.623. Venderlo a USD 27.500 genera una pérdida operativa directa de más de USD 2.000 por vehículo en esos años.
* **Precio Umbral de Indiferencia:** **USD 28.534 por unidad.** Es el costo variable promedio ponderado de los 5 años. Por debajo de USD 28.534, el contrato destruye caja.

---

### CONSIGNA 6: Costo de Playón y Transferencia de Inventarios

#### 1. ¿Cuál es la idea de negocio?
La empresa puede fabricar de más y guardar vehículos en el playón pagando un 25% anual de su costo variable.
* ¿En qué casos el modelo decide transferir inventario?
* ¿Qué ocurre si la tasa sube al 30%?
* ¿A qué nivel de costo la transferencia deja de ser utilizada?

#### 2. ¿Cómo lo resuelve el código por dentro?
1. Se evalúa la condición de arbitraje intertemporal: $rac{CV(t) \cdot (1 + h)}{TC(t)} \le rac{CV(t+1)}{TC(t+1)}$.
2. Se realiza un barrido paramétrico continuo de la tasa $h$ desde 0% hasta 30% con pasos de 0,5% y 1,0%.
3. En cada iteración se suma el inventario total guardado $\sum_{v, t} I(v, t)$ para detectar el punto de anulación exacta.

#### 3. ¿Qué resultado arroja y qué significa?
* **Al 25% y 30%: Cero (0) inventario transferido.** Subir la tasa al 30% no genera ningún impacto porque al 25% ya no convenía guardar stock.
* **Punto de corte analítico:** El inventario desaparece por completo a partir del **8,1% - 8,8% anual**.
* **Significado:** Para tasas mayores al ~8,8%, el costo financiero de tener autos parados supera cualquier beneficio de anticipar producción. AutoITBA debe operar en régimen **Just-in-Time**.

---

### CONSIGNA 7: Recomendación Estratégica Integral (Minimax Regret)

#### 1. ¿Cuál es la idea de negocio?
Presentar una recomendación integral al directorio distinguiendo decisiones robustas vs contingentes, y definir una estrategia que minimice el arrepentimiento en los Años 1 y 2 dejando opciones abiertas para los Años 3 a 5.

#### 2. ¿Cómo lo resuelve el código por dentro?
1. Se formula la matriz de pagos cruzando las estrategias directivas contra los cuatro escenarios posibles (Base, Devaluación, Boom Agro y Cierre de Aduana).
2. Se calcula la Matriz de Arrepentimiento (Regret de Savage):
   $$R(i, j) = \max_k P(k, j) - P(i, j)$$
3. Se selecciona la estrategia con el menor arrepentimiento máximo (Minimax Regret).

#### 3. ¿Qué resultado arroja y qué significa?
* **Decisiones Robustas:** Línea B en doble turno los 5 años; abastecer 100% exportaciones; inventario cero.
* **Decisiones Contingentes:** Importación de China y reconversión de Línea A.
* **Criterio Minimax Regret:**
  * Plan Base Local (S1): Arrepentimiento Máximo = **USD 109,7 M**
  * Importar desde China (S3): Arrepentimiento Máximo = **USD 115,7 M**
  * Estrategia de Opciones Abiertas (Esperar Año 2): Arrepentimiento Máximo = **USD 15,4 M (Óptimo Global)**
* **Hoja de Ruta:** Operar localmente en Año 1, renegociar con Autonomy a > USD 28.550, no incurrir en costos irreversibles en Años 1 y 2, y decidir reconversión o importación al cierre del Año 2 con el nuevo gobierno y régimen cambiario definidos.

---
*Informe elaborado conforme a las pautas metodológicas de la cátedra de Investigación de Operaciones — ITBA 2026.*
