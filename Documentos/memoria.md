---
title: "Algoritmo Imperialista Competitivo"
author: Pablo Baeyens Fernández
subtitle: Metaheurísticas
date: \today
documentclass: scrartcl
classoption: oneside
lang: es
header-includes:
- \usepackage{algorithm}
- \usepackage[noend]{algorithmic}
- \input{assets/spanishAlgorithmic}
- \usepackage{caption}
- \usepackage{graphicx}
- \usepackage{sidecap}
- \usepackage{changepage}
colorlinks: true
bibliography: assets/bibliografía.bib
biblio-style: apalike
link-citations: true
citation-style: assets/estilo.csl
numbersections: true
toc: true
tocdepth: 2
---

\newpage
  
# Introducción

Los problemas de optimización uniobjetivo en variables reales consisten en, dados $n \in \mathbb{N}$ y un *dominio* $\Omega \subseteq \mathbb{R}^d$ hallar un mínimo global de una función $F:\Omega \to \mathbb{R}$ llamada *función objetivo*. Una *solución* es un vector $x \in \mathbb{R}^d$ y su *calidad* es el valor $F(x)$.

Este problema no es en general tratable de forma exacta; una función objetivo arbitraria puede no tener buenas propiedades analíticas o ser altamente multimodal, lo que impide el uso de técnicas basadas en el análisis como el uso del gradiente descendiente. 
En su lugar intentamos aplicar metaheurísticas que intentan resolver estos problemas de forma general utilizando heurísticas, con frecuencia inspiradas en la naturaleza o en otros fenómenos.

En este documento analizamos una familia de metaheurísticas concreta y evaluamos su comportamiento sobre las funciones objetivo definidas para la competición CEC 2014 [@CEC2014].
En concreto utilizamos una adaptación de las mismas a NumPy que he implementado junto con Ignacio Aguilera Martos [@cec2014NumPy].

# Metodología

Para el análisis del algoritmo he trabajado a partir de una versión del algoritmo implementada en NumPy para Python 3 [@JJSrra].
He modificado el algoritmo de tal manera que fuera más sencillo trabajar con el y he hecho modificaciones a partir de este.
Para el análisis del algoritmo original he mantenido los parámetros originales que se utilizan en [@implICA].
He analizado su comportamiento con la modificación de parámetros en función de los parámetros en la sección [Posibles modificaciones].

He ejecutado cada versión del algoritmo implementada en las primeras 20 funciones de la competición CEC2014 en dimensiones 10 y 30 y presento los resultados en una tabla que contiene el resultado medio obtenido así como la desviación típica de 25 ejecuciones de cada algoritmo en cada función.

El número de evaluaciones de la función de evaluación es de $10000\cdot \mathrm{dim}$ donde $\mathrm{dim}$ es la dimensión (10 o 30).
Los resultados pueden reproducirse ejecutando el script `ICAMain.py` en el que he fijado la semilla `73` de NumPy para asegurar la reproducibilidad de los resultados.

Los resultados analizados también están disponibles en el fichero en formato libre `Resultados.ods` junto con este documento.
La pestaña `D10` incluye los resultados en dimensión 10, la pestaña `D30` los resultados en dimensión 30 y la pestaña `Resumen` incluye una tabla resumen.

# Algoritmo imperialista competitivo

El *algoritmo imperialista competitivo* (ICA por sus siglas del inglés) es un algoritmo evolutivo basado en poblaciones[@LucasImperialistcompetitivealgorithm2017]. Es un algoritmo aplicable a problemas de optimización en variables reales para funciones definidas sobre un convexo de cualquier dimensión. 
También se han propuesto versiones para problemas discretos [@Behnamiandiscretecolonialcompetitive2011].

La inspiración del algoritmo viene del fenómeno histórico del imperialismo y el colonialismo.
Las soluciones son *países* que se dividen en *colonias* e *imperialistas*; las colonias se *asimilan* hacia los imperialistas y los imperialistas compiten entre sí por las colonias. El proceso fundamental de búsqueda de soluciones es la asimilación, que produce cruces entre el imperialista y sus colonias.

Abstrayendo esta interpretación podemos verlo como un algoritmo de optimización por enjambre de partículas con varias subpoblaciones (los imperialistas junto con sus colonias) que propone una forma de interacción entre estas poblaciones (la competición imperialista).

Es un algoritmo que ha sido utilizado para diversas aplicaciones industriales [@HosseinisurveyImperialistCompetitive2014] y desde su publicación original se han propuesto varias mejoras o versiones alternativas del algoritmo que mejoran sus resultados [@AbdiGICAImperialistcompetitive2017][@LinInteractionEnhancedImperialist2012][@AbdechiriAdaptiveImperialistCompetitive2010][@LinImprovingImperialistCompetitive2013][@RamezaniSocialBasedAlgorithmSBA2013].

En este documento trabajo a partir de la versión del algoritmo para más de dos dimensiones implementada en [@implICA].


## Algoritmo original

En esta sección describimos el algoritmo original tal y como aparece en la versión en MATLAB implementada por los autores [@implICA]. Esta versión arregla algunos errores del algoritmo original. El pseudocódigo del algoritmo es el siguiente:

\input{algos/algoGeneral}

donde $\alpha, z, R_\mathrm{Inicial}$ y nDécadas son parámetros ajustables. Las funciones del algoritmo hacen lo siguiente:

**CreaImperiosIniciales** construye de forma uniforme países y toma los mejores como imperialistas:
El número de imperialistas ($N_\mathrm{imp}$) y de países totales ($N$) se fijan como parámetros.
Sea $c_i$ el coste del imperialista $i$-ésimo, $c_\mathrm{máx} = \max_{1 \leq j \leq N_\mathrm{imp}} c_j$.
Cada imperialista se lleva un número de colonias $\mathrm{NC}_i$ en función de su poder $P_i$:
\begin{equation*}
  P_i = \begin{cases}
  1,\!3 c_\mathrm{máx} - c_i & \text{si } c_\mathrm{máx} > 0 \\
  0,\!7 c_\mathrm{máx} - c_i & \text{si } c_\mathrm{máx}\leq 0
  \end{cases}, \quad
\mathrm{NC}_i = \left[ \left|\frac{P_i}{\sum_1^{N_\mathrm{imp}} P_j}\right| (N - N_\mathrm{imp})\right]
\end{equation*}
Esta fórmula evita un problema en el algoritmo que hacía que el peor imperialista no tuviera ninguna colonia.

**AsimilaColonias** *asimila* las colonias hacia su imperialista; para cada colonia $c$ con imperialista asociado $e$ toma $\delta \sim U([0,\beta]^d)$ un vector aleatorio donde $\beta$ es un parámetro y actualiza:
$c \leftarrow c + \delta(e-c)$

**PoseeImperio** coloca como imperialista a la mejor colonia si esta supera en calidad al imperialista.
A continuación se actualiza el coste total del imperio en función del coste de las colonias.

Finalmente **CompeticiónImperialista** toma la peor colonia del peor imperialista y se la da aleatoriamente a otro imperialista con selección por ruleta en función del coste normalizado $E_i$:
$E_i = \max( \mathrm{CosteTotal}(e_j)) - \mathrm{CosteTotal}(e_i)$.


## Versiones alternativas

En esta sección describo brevemente 4 versiones alternativas y mejoras que han sido propuestas en la literatura relativa a este algoritmo:

*ICA with globalization mechanism (GICA)* [@AbdiGICAImperialistcompetitive2017]
: propone algunas modificaciones para aumentar la relación entre los imperios:

  1. La asimilación se hace parcialmente hacia el mejor imperialista y no sólo hacia al que pertenece la colonia
  2. Implementa mecanismo de cruce aritmético entre imperialistas y sustituye a los imperialistas si encuentra una mejor solución
  3. Implementa un mecanismo de cruce entre las colonias de un mismo imperio mediante una combinación convexa aleatoria

\newpage

*Interaction Enhanced ICA* [@LinInteractionEnhancedImperialist2012]
: propone dos variantes: en primer lugar ICAAI que construye un "imperialista artificial" haciendo una suma ponderada de los imperialistas existentes (dando más peso al mejor imperialista) e intenta sustituir el peor imperialista por este. En segundo lugar ICACI cruza los imperialistas entre sí y los reemplaza si hay mejora. El paper encuentra que ICAAI suele dar mejores resultados que ICACI en general, y estos mejoran los resultados del algoritmo ICA original así como al PSO.


*Adaptive ICA (AICA)* [@AbdechiriAdaptiveImperialistCompetitive2010]
: propone modificar de forma adaptativa el ángulo de rotación del proceso de asimilación de colonias en función de la diversidad existente en el imperio. Para ello calcula la diversidad existente en la población en mediante la función de densidad de la normal multivariante. A partir de este dato modifica el ángulo de rotación de la asimilación; esto hace que aumente o disminuya la diversidad de la población, evitando así la convergencia prematura.
Esta versión adaptativa no es aplicable a la versión que consideramos en este trabajo ya que el ángulo de rotación no existe en más de dos dimensiones.

*Improving ICA with Local Search for Global Optimization* [@LinImprovingImperialistCompetitive2013]
: propone aplicar búsqueda local a todos los imperialistas o sólo al mejor de ellos y compara estos con una versión de ICA.
Usando el mismo número de evaluaciones de la función objetivo obtiene mejores resultados en el caso de aplicar búsqueda local a todos los imperialistas.


# Análisis del algoritmo

## Comportamiento en cada función y frente a DE

\begin{table}[H]
\begin{center}
\begin{tabular}{c|ccc|ccc}
  & \multicolumn{3}{c}{\textsc{dim = 10}} & \multicolumn{3}{c}{\textsc{dim = 30}} \\
\textbf{F} &  \textbf{Media} &  \textbf{Desviación} & \textbf{\#} &  \textbf{Media} & \textbf{Desviación} & \textbf{\#}  \\ \hline
1 & 4,81$\cdot 10^{4}$ & 8,37$\cdot 10^{4}$ & 13 & 1,99$\cdot 10^{6}$ & 2,10$\cdot 10^{6}$ & 13 \\
2 & 3,79$\cdot 10^{2}$ & 1,57$\cdot 10^{3}$ & 13 & 5,66$\cdot 10^{4}$ & 3,77$\cdot 10^{4}$ & 14 \\
3 & 3,34$\cdot 10^{0}$ & 4,99$\cdot 10^{0}$ & 11 & 7,56$\cdot 10^{2}$ & 8,72$\cdot 10^{2}$ & 11 \\
4 & 1,87$\cdot 10^{1}$ & 1,71$\cdot 10^{1}$ & 11 & 9,66$\cdot 10^{1}$ & 5,26$\cdot 10^{1}$ & 14 \\
5 & 2,01$\cdot 10^{1}$ & 1,13$\cdot 10^{-1}$ & 14 & 2,03$\cdot 10^{1}$ & 3,50$\cdot 10^{-1}$ & 12 \\
6 & 5,29$\cdot 10^{0}$ & 1,60$\cdot 10^{0}$ & 17 & 3,09$\cdot 10^{1}$ & 3,55$\cdot 10^{0}$ & 17 \\
7 & 3,64$\cdot 10^{-1}$ & 2,17$\cdot 10^{-1}$ & 14 & 1,32$\cdot 10^{-1}$ & 6,56$\cdot 10^{-2}$ & 12 \\
8 & 2,51$\cdot 10^{1}$ & 9,35$\cdot 10^{0}$ & 17 & 1,35$\cdot 10^{2}$ & 3,05$\cdot 10^{1}$ & 17 \\
9 & 2,44$\cdot 10^{1}$ & 9,36$\cdot 10^{0}$ & 17 & 1,53$\cdot 10^{2}$ & 2,60$\cdot 10^{1}$ & 17 \\
10 & 6,92$\cdot 10^{2}$ & 2,81$\cdot 10^{2}$ & 17 & 3,66$\cdot 10^{3}$ & 7,19$\cdot 10^{2}$ & 17 \\
11 & 8,31$\cdot 10^{2}$ & 2,17$\cdot 10^{2}$ & 17 & 3,93$\cdot 10^{3}$ & 6,78$\cdot 10^{2}$ & 16 \\
12 & 5,13$\cdot 10^{-1}$ & 2,28$\cdot 10^{-1}$ & 14 & 1,28$\cdot 10^{0}$ & 4,07$\cdot 10^{-1}$ & 15 \\
13 & 2,58$\cdot 10^{-1}$ & 1,06$\cdot 10^{-1}$ & 12 & 4,78$\cdot 10^{-1}$ & 1,63$\cdot 10^{-1}$ & 12 \\
14 & 2,60$\cdot 10^{-1}$ & 1,46$\cdot 10^{-1}$ & 11 & 2,89$\cdot 10^{-1}$ & 3,17$\cdot 10^{-2}$ & 9 \\
15 & 1,55$\cdot 10^{0}$ & 6,87$\cdot 10^{-1}$ & 13 & 2,55$\cdot 10^{1}$ & 1,03$\cdot 10^{1}$ & 14 \\
16 & 3,12$\cdot 10^{0}$ & 3,89$\cdot 10^{-1}$ & 17 & 1,25$\cdot 10^{1}$ & 3,80$\cdot 10^{-1}$ & 15 \\
17 & 4,91$\cdot 10^{2}$ & 2,76$\cdot 10^{2}$ & 11 & 1,37$\cdot 10^{4}$ & 1,46$\cdot 10^{4}$ & 10 \\
18 & 5,47$\cdot 10^{1}$ & 4,94$\cdot 10^{1}$ & 6 & 2,90$\cdot 10^{2}$ & 1,21$\cdot 10^{2}$ & 11 \\
19 & 4,45$\cdot 10^{0}$ & 1,31$\cdot 10^{0}$ & 17 & 2,39$\cdot 10^{1}$ & 1,69$\cdot 10^{1}$ & 14 \\
20 & 5,16$\cdot 10^{1}$ & 3,43$\cdot 10^{1}$ & 11 & 4,94$\cdot 10^{2}$ & 1,33$\cdot 10^{2}$ & 10 \\
\end{tabular}
\end{center}
\caption{Resultados de ICA original en las 20 primeras funciones de CEC2014 para dimensión 10 y 30.
"\#" indica la posición en la que habría quedado el algoritmo en CEC2014 en esa función (17 si es peor que todos los competidores)}
\label{resOriginal}
\end{table}


En esta sección analizo el comportamiento del algoritmo original en las distintas funciones de las competición CEC2014. En primer lugar pueden consultarse las tablas de resultados del algoritmo imperialista competitivo en dimensión 10 y 30 en \ref{resOriginal}.


En **dimensión 10** el comportamiento de los algoritmos de evolución diferencial es claramente mejor que el del algoritmo imperialista competitivo en su versión original (ver Figura 2).
En particular los algoritmos de evolución diferencial alcanzan el mínimo en las funciones 1,2,3 mientras que el algoritmo imperialista competitivo se queda varios órdenes de magnitud por encima.
El algoritmo presenta sin embargo un buen comportamiento en algunas de las funciones.
En particular alcanza resultados similares a los algoritmos de evolución diferencial en las funciones 4-6 y 12-16 (un subconjunto de las funciones multimodales).

\begin{figure}[H]
\label{compde}
\begin{adjustwidth}{-1in}{-1in} 
\centering
\includegraphics[width=1.3\textwidth]{img/ComparacionDE.png}
\end{adjustwidth}
\caption{Valor de mejor solución para algoritmos DE vs algoritmo original en \textbf{dimensión 10}.
La escala del eje Y es logarítmica para apreciar mejor las diferencias. \\
\texttt{ica} es el algoritmo imperialista competitivo y \texttt{debin}, \texttt{deexp} son los algoritmos de DE.}
\end{figure}


\begin{figure}[H]
\label{compde30}
\begin{adjustwidth}{-1in}{-1in} 
\centering
\includegraphics[width=1.2\textwidth]{img/ComparacionDE30.png}
\end{adjustwidth}
\caption{Valor de mejor solución para algoritmos DE vs algoritmo original en \textbf{dimensión 30}.
La escala del eje Y es logarítmica para apreciar mejor las diferencias. \\
\texttt{ica} es el algoritmo imperialista competitivo y \texttt{debin}, \texttt{deexp} son los algoritmos de DE.}
\end{figure}

En **dimensión 30** sorprendentemente el algoritmo imperialista competitivo supera a los algoritmos de evolución diferencial en todas las funciones multimodales exceptuando la 10 (ver Figura 3).
En las funciones unimodales (1,2,3) sigue siendo superado por DE pero en las híbridas las soluciones son comparables o mejores.

Si analizamos las definiciones de las funciones de CEC2014 (disponibles en [@liang2013problem]) vemos que el algoritmo parece presentar un buen comportamiento en **funciones multimodales e híbridas no separables en alta dimensión** mientras que su comportamiento es pésimo en funciones unimodales o funciones híbridas cuando la dimensión es inferior.

## Importancia de las distintas partes

Para analizar el comportamiento he analizado su rendimiento eliminando algunos de los pasos: la posesión del imperio, la revolución y la competición imperialista. Como se describe en [Metodología y reproducibilidad] tomo la media de 25 ejecuciones.

Para este análisis me restrinjo a dimensión 10.
Los resultados del algoritmo eliminando cada componente pueden verse en la figura (\ref{comp}):

\begin{figure}[H]
\label{comp}
\begin{adjustwidth}{-1in}{-1in} 
\centering
\includegraphics[width=1.3\textwidth]{img/AnalisisComponentes.png}
\end{adjustwidth}
\caption{Valor de mejor solución para cada función eliminando componentes en \textbf{dimensión 10}.
La escala del eje Y es logarítmica para apreciar mejor las diferencias. \\
\texttt{original} es el algoritmo original, \texttt{norev}, \texttt{nopos} y \texttt{nocomp} eliminan las revoluciones, la posesión de imperio y la competición respectivamente.}
\end{figure}

Como vemos en la figura el aspecto más importante del algoritmo es la **operación de posesión** que actualiza el imperialista. Esto tiene sentido ya que esta operación es crucial para el buen funcionamiento de la asimilación: en otro caso sólo estaríamos haciendo movimientos aleatorios. 
Eliminar la operación de **competición imperialista** también parece empeorar de forma significativa el rendimiento del algoritmo, en espacial en las funciones 1,2 y 3.

La operación de **revolución** (añadida posteriormente por los autores en su implementación en MATLAB pero no presente en el paper original) parece tener efectos más modestos sobre los resultados del algoritmo. En algunas funciones como 17,18 y 20 el algoritmo de revolución presente resultados ligeramente mejores.

## Convergencia del algoritmo

Para analizar el por qué del comportamiento del algoritmo he analizado la evolución del coste de la función objetivo en la mejor solución de la población respecto del número de evaluaciones. 
Como ejemplo representativo vemos el caso de la función $f_{11}$.

\begin{SCfigure}
\centering
\includegraphics[width=0.7\textwidth]{img/GraficaConvOriginal11.png}
\caption*{Figura 2: \\ Mejor solución en función del número de evaluaciones para ICA original con $f_{11}$ en dimensión 10}
\end{SCfigure}

Como vemos la función se estanca en un mínimo local rápidamente; a partir de la evaluación 10000 no consigue escapar de este hasta el final de la ejecución. 
Este comportamiento se reproduce en casi todas las funciones de la competición: tras un porcentaje pequeño de las evaluaciones el algoritmo se estanca en un mínimo local.
Por tanto el ámbito de mejora principal del algoritmo se encuentra en el aumento de la exploración del espacio de soluciones.

# Posibles modificaciones

He probado multitud de posibles mejoras del algoritmo y he descartado aquellas que ejecutadas en dimensión 10 con 3 ejecuciones por cada función no daban mejores resultados medios que el algoritmo original (salvo la versión memética que he analizado más extensamente por completitud).
Discuto brevemente las mejoras descartadas en la sección [Modificaciones descartadas].

Para aquellas con las que sí se obtenía una mejora significativa he hecho una ejecución completa con la misma semilla que el algoritmo ICA original.
Discuto estas mejoras en la sección [Modificaciones analizadas].

En términos generales, los aspectos que he considerado para la modificación del algoritmo son:

1. Cambios en la asimilación de las colonias
2. Cambios en el proceso o frecuencia de revolución o el ajuste de este parámetro
3. Cambios en el proceso de competición imperialista

## Modificaciones descartadas

Dentro de los cambios en la asimilación de colonias he probado o considerado algunas versiones alternativas para comprender el funcionamiento del algoritmo e intentar mejorarlo. En particular he considerado y descartado:

1. Un proceso de asimilación determinista equivalente al cruce aritmético
2. Un proceso de asimilación en el que la distribución de la que se muestrea $\delta$ no es una distribución uniforme, sesgando esta distribución hacia la mitad del intervalo o haciéndolo de forma adaptativa en función de la bondad de la colonia.
3. Una variante elitista en la cual una colonia es asimilada sólo si mejora su evaluación.
4. Una variante de la asimilación en la que el cruce se realiza también hacia el mejor imperialista.
5. Ajuste de parámetros en la versión original del algoritmo. En concreto he intentado aumentar y reducir el tamaño de la población y el número de imperialistas o modificar la constante del proceso de asimilación.

En ninguno de estos casos se han apreciado diferencias significativas respecto de los resultados del algoritmo imperialista competitivo original o los resultados han sido peores. 
Esto nos indica que el hecho que impide el buen funcionamiento del algoritmo en algunas de las funciones no está relacionado con el proceso de asimilación o los parámetros (que parecen haber sido ajustados adecuadamente por los autores).

## Modificaciones analizadas

Las modificaciones que he elegido para analizar han sido la hibridación del algoritmo incluyendo búsquedas locales (simulando el proceso de [@LinImprovingImperialistCompetitive2013]) y una versión que modifica la asimilación haciéndola similar a un cruce de Differential Evolution aunque conservando las subpoblaciones.

### Versión memética

He intentado reproducir los resultados de [@LinImprovingImperialistCompetitive2013] incluyendo una búsqueda local para mejorar los imperialistas. En concreto he considerado las dos versiones descritas:

1. Una versión que añade búsqueda local al mejor imperialista
2. Una versión que añade búsqueda local a todos los imperialistas

He considerado 3 versiones de búsqueda local: Solis-Wets implementada por Daniel Molina y dos versiones de búsqueda local implementadas en la biblioteca de Python SciPy.
La búsqueda local que mejores resultados ha producido es la búsqueda local L-BFGS-B del paquete SciPy [@minimizemethodLBFGSB].

Con esta búsqueda local he considerado las dos opciones de hibridación.
Para intentar hallar el equilibrio entre iteraciones dedicadas a la búsqueda local y al algoritmo imperialista he ejecutado el algoritmo con distintos números de evaluaciones máximas para la búsqueda local, desde 100 evaluaciones hasta 10000 en dimensión 10. Como estadistico que resume cómo de bueno es el algoritmo con ese número de iteraciones he utilizado la suma de los resultados en las funciones 2 a 20. 
He excluido la función 1 ya que da resultados muy variables.

El resultado puede verse en la siguiente figura.

\includegraphics[width=1\textwidth]{img/sumaVsnevals.png}

Como vemos en todos los casos el algoritmo original es varios órdenes de magnitud mejor respecto de este estadístico por lo que los resultados que aparecen en [@LinImprovingImperialistCompetitive2013] no se reproducen para este conjunto de funciones.
Una posible explicación es que este paper analizaba los resultados en funciones de baja dimensión y por tanto los resultados no son generalizables a las funciones consideradas en la competición.
Otra posibilidad que las búsquedas locales consideradas no sean lo suficientemente eficaces.
Como ejemplo, los resultados para 1000 evaluaciones de ambas variantes pueden encontrarse en el documento de resultados para dimensión 10. En todos los casos la versión original supera a estas versiones meméticas.

### ICA DE

He implementado una versión del proceso de asimilación que reproduce el algoritmo de Evolución Diferencial en cada imperio. En concreto la fórmula considerada para actualizar la componente i-ésima de una colonia $x_{i,G}$ es:

$$v_{i,G} = x_{i,G} + F(x_{\operatorname{imperialista},G} - x_{i,G}) + F(x_{r1,G} - x_{r2,G})$$

donde $x_{r1,G}$ y $x_{r2,G}$ son colonias distintas escogidas de forma uniforme de entre las colonias de un imperialista y $x_{\operatorname{imperialista},G}$ es el imperialista al que pertenece la colonia considerada.
Si una coordenada se sale de los límites del dominio en lugar de eso se queda en el borde.

Utilizando esta fórmula construimos una nueva colonia posible siguiendo la fórmula del algoritmo de evolución diferencial:

$$u_{j,i,G} = \begin{cases}v_{j,i,G} & \text{ si } \mathrm{rand}(0,1) \leq \mathrm{CR} \text{ o } j = j_{\mathrm{rand}}\\x_{j,i,G} & \text{ en otro caso}\end{cases}$$

Y actualizamos la colonia $x_{i,G}$ por $u_{i,G}$ en caso de que esta sea mejor.
El resto de aspectos del algoritmo se conservan, esto es, lo único que se modifica es la función $\mathrm{AsimilaColonias}$ que pasa a realizar el proceso descrito en esta sección y algunos parámetros.

Los parámetros del algoritmo original establecen 8 imperialistas y 80 países, lo que supone una población demasiado pequeña para los algoritmos de evolución diferencial. 
Además antes de ser eliminado un imperio puede llegar a tener sólo una o dos colonias, lo que impide la aplicación de este algoritmo.

Por esto he aumentado el número de países a 100 conservando los imperialistas y he modificado el umbral a partir del cuál un imperio es demasiado pequeño para continuar y es absorbido por el resto.

Con estas modificaciones los resultados son los siguientes:

\begin{table}[H]
\begin{center}
\begin{adjustwidth}{-0.8in}{-0.8in}
\resizebox{1.3\textwidth}{!}{%
\begin{tabular}{c|ccc|ccc|ccc|ccc}
& \multicolumn{6}{c}{\textsc{dim = 10}} & \multicolumn{6}{c}{\textsc{dim = 30}} \\
& \multicolumn{3}{c}{ICA Original} & \multicolumn{3}{c}{ICA DE} & \multicolumn{3}{c}{ICA Original} & \multicolumn{3}{c}{ICA DE}  \\
\textbf{F} &  \textbf{$\bar{x}$} &  \textbf{$\sigma$} & \textbf{\#}  &  \textbf{$\bar{x}$} &  \textbf{$\sigma$} & \textbf{\#} &  \textbf{$\bar{x}$} & \textbf{$\sigma$} & \textbf{\#}   &  \textbf{$\bar{x}$} &  \textbf{$\sigma$} & \textbf{\#} \\ \hline
1 & 4,81$\cdot10^{4}$ & 8,37$\cdot10^{4}$ & 13 & 4,25$\cdot10^{2}$ & 1,10$\cdot10^{3}$ & 8 & 1,99$\cdot10^{6}$ & 2,10$\cdot10^{6}$ & 13 & 3,41$\cdot10^{6}$ & 2,56$\cdot10^{6}$ & 13 \\
2 & 3,79$\cdot10^{2}$ & 1,57$\cdot10^{3}$ & 13 & 1,70$\cdot10^{0}$ & 7,66$\cdot10^{0}$ & 11 & 5,66$\cdot10^{4}$ & 3,77$\cdot10^{4}$ & 14 & 9,54$\cdot10^{3}$ & 7,05$\cdot10^{3}$ & 13 \\
3 & 3,34$\cdot10^{0}$ & 4,99$\cdot10^{0}$ & 11 & 8,98$\cdot 10^{-1}$ & 1,87$\cdot10^{0}$ & 10 & 7,56$\cdot10^{2}$ & 8,72$\cdot10^{2}$ & 11 & 2,74$\cdot10^{3}$ & 1,59$\cdot10^{3}$ & 11 \\
4 & 1,87$\cdot10^{1}$ & 1,71$\cdot10^{1}$ & 11 & 1,85$\cdot10^{1}$ & 1,73$\cdot10^{1}$ & 11 & 9,66$\cdot10^{1}$ & 5,26$\cdot10^{1}$ & 14 & 1,30$\cdot10^{2}$ & 1,97$\cdot10^{1}$ & 15 \\
5 & 2,01$\cdot10^{1}$ & 1,13$\cdot 10^{-1}$ & 14 & 1,95$\cdot10^{1}$ & 4,06$\cdot10^{0}$ & 8 & 2,03$\cdot10^{1}$ & 3,50$\cdot 10^{-1}$ & 12 & 2,09$\cdot10^{1}$ & 5,41$\cdot 10^{-1}$ & 16 \\
6 & 5,29$\cdot10^{0}$ & 1,60$\cdot10^{0}$ & 17 & 1,52$\cdot 10^{-1}$ & 4,18$\cdot 10^{-1}$ & 10 & 3,09$\cdot10^{1}$ & 3,55$\cdot10^{0}$ & 17 & 9,81$\cdot10^{0}$ & 2,14$\cdot10^{0}$ & 11 \\
7 & 3,64$\cdot 10^{-1}$ & 2,17$\cdot 10^{-1}$ & 14 & 5,39$\cdot 10^{-1}$ & 2,70$\cdot 10^{-1}$ & 10 & 1,32$\cdot 10^{-1}$ & 6,56$\cdot 10^{-1}$ & 12 & 3,70$\cdot 10^{-1}$ & 3,18$\cdot 10^{-1}$ & 9 \\
8 & 2,51$\cdot10^{1}$ & 9,35$\cdot10^{0}$ & 17 & 3,99$\cdot10^{0}$ & 1,90$\cdot10^{0}$ & 10 & 1,35$\cdot10^{2}$ & 3,05$\cdot10^{1}$ & 17 & 5,48$\cdot10^{1}$ & 1,37$\cdot10^{1}$ & 13 \\
9 & 2,44$\cdot10^{1}$ & 9,36$\cdot10^{0}$ & 17 & 8,52$\cdot10^{0}$ & 5,08$\cdot10^{0}$ & 9 & 1,53$\cdot10^{2}$ & 2,60$\cdot10^{1}$ & 17 & 5,70$\cdot10^{1}$ & 1,46$\cdot10^{1}$ & 9 \\
10 & 6,92$\cdot10^{2}$ & 2,81$\cdot10^{2}$ & 17 & 1,83$\cdot10^{2}$ & 1,03$\cdot10^{2}$ & 13 & 3,66$\cdot10^{3}$ & 7,19$\cdot10^{2}$ & 17 & 1,87$\cdot10^{3}$ & 6,93$\cdot10^{2}$ & 13 \\
11 & 8,31$\cdot10^{2}$ & 2,17$\cdot10^{2}$ & 17 & 3,59$\cdot10^{2}$ & 3,00$\cdot10^{2}$ & 11 & 3,93$\cdot10^{3}$ & 6,78$\cdot10^{2}$ & 16 & 4,27$\cdot10^{3}$ & 1,93$\cdot10^{3}$ & 16 \\
12 & 5,13$\cdot 10^{-1}$ & 2,28$\cdot 10^{-1}$ & 14 & 8,95$\cdot 10^{-1}$ & 1,79$\cdot 10^{-1}$ & 15 & 1,28$\cdot10^{0}$ & 4,07$\cdot 10^{-1}$ & 15 & 2,40$\cdot10^{0}$ & 2,22$\cdot 10^{-1}$ & 17 \\
13 & 2,58$\cdot 10^{-1}$ & 1,06$\cdot 10^{-1}$ & 12 & 1,13$\cdot 10^{-1}$ & 5,33$\cdot 10^{-1}$ & 9 & 4,78$\cdot 10^{-1}$ & 1,63$\cdot 10^{-1}$ & 12 & 3,17$\cdot 10^{-1}$ & 7,64$\cdot 10^{-1}$ & 10 \\
14 & 2,60$\cdot 10^{-1}$ & 1,46$\cdot 10^{-1}$ & 11 & 1,09$\cdot 10^{-1}$ & 4,41$\cdot 10^{-1}$ & 4 & 2,89$\cdot 10^{-1}$ & 3,17$\cdot 10^{-1}$ & 9 & 3,48$\cdot 10^{-1}$ & 1,58$\cdot 10^{-1}$ & 13 \\
15 & 1,55$\cdot10^{0}$ & 6,87$\cdot 10^{-1}$ & 13 & 1,66$\cdot10^{0}$ & 2,50$\cdot 10^{-1}$ & 13 & 2,55$\cdot10^{1}$ & 1,03$\cdot10^{1}$ & 14 & 8,86$\cdot10^{0}$ & 4,11$\cdot10^{0}$ & 10 \\
16 & 3,12$\cdot10^{0}$ & 3,89$\cdot 10^{-1}$ & 17 & 2,06$\cdot10^{0}$ & 4,20$\cdot 10^{-1}$ & 8 & 1,25$\cdot10^{1}$ & 3,80$\cdot 10^{-1}$ & 15 & 1,11$\cdot10^{1}$ & 4,85$\cdot 10^{-1}$ & 11 \\
17 & 4,91$\cdot10^{2}$ & 2,76$\cdot10^{2}$ & 11 & 1,47$\cdot10^{2}$ & 8,35$\cdot10^{1}$ & 7 & 1,37$\cdot10^{4}$ & 1,46$\cdot10^{4}$ & 10 & 2,30$\cdot10^{4}$ & 2,61$\cdot10^{4}$ & 10 \\
18 & 5,47$\cdot10^{1}$ & 4,94$\cdot10^{1}$ & 6 & 2,14$\cdot10^{1}$ & 1,70$\cdot10^{1}$ & 8 & 2,90$\cdot10^{2}$ & 1,21$\cdot10^{2}$ & 11 & 2,69$\cdot10^{2}$ & 5,85$\cdot10^{2}$ & 11 \\
19 & 4,45$\cdot10^{0}$ & 1,31$\cdot10^{0}$ & 17 & 7,31$\cdot 10^{-1}$ & 6,13$\cdot 10^{-1}$ & 8 & 2,39$\cdot10^{1}$ & 1,69$\cdot10^{1}$ & 14 & 1,02$\cdot10^{1}$ & 1,75$\cdot10^{0}$ & 12 \\
20 & 5,16$\cdot10^{1}$ & 3,43$\cdot10^{1}$ & 11 & 4,86$\cdot10^{0}$ & 4,08$\cdot10^{0}$ & 6 & 4,94$\cdot10^{2}$ & 1,33$\cdot10^{2}$ & 10 & 6,42$\cdot10^{2}$ & 7,42$\cdot10^{2}$ & 10 \\
   &                   & \textbf{Mediana}           & 13,5 &                 &   \textbf{Mediana}         & 9,5 &                 & \textbf{Mediana}           & 14 &  & \textbf{Mediana} & 11,5
\end{tabular}}
\end{adjustwidth}
\end{center}
\caption{Resultados de ICA e ICA DE en las 20 primeras funciones de CEC2014 para dimensión 10 y 30.
"\#" indica la posición en la que habría quedado el algoritmo en CEC2014 en esa función (17 si es peor que todos los competidores).
Calculo la posición mediana para comparar.}
\label{resDE}
\end{table}

Como vemos en ambas dimensiones la mejora es significativa, tanto en resultado medio y posición media del algoritmo como en la disminución de la desviación típica, lo que nos da un comportamiento más consistente.
La mejora es bastante más significativa en el caso de baja dimensión ya que como vimos en el caso de dimensión 30 en la sección [Comportamiento en cada función y frente a DE] el comportamiento frente a DE es igualado en esta dimensión por el algoritmo original. 
En la siguiente figura podemos ver una comparación gráfica de los resultados en dimensión 10.

\begin{figure}[H]
\label{compde}
\centering
\includegraphics[width=0.9\textwidth]{img/icade.png}
\caption{Valor de mejor solución para algoritmo original vs algoritmo ICA-DE en \textbf{dimensión 10}.
La escala del eje Y es logarítmica para apreciar mejor las diferencias.}
\end{figure}

El algoritmo mejora su comportamiento en las funciones unimodales aunque no llega a igualar el comportamiento de DE.

# Resumen y conclusiones

El algoritmo imperialista competitivo es un algoritmo evolutivo basado en poblaciones que mantiene varias subpoblaciones (imperios) en los cuales las soluciones de menor calidad (colonias) se acercan a las de mayor calidad (imperios).
Además consta de un mecanismo de interacción entre poblaciones que permite a los imperios competir por las colonias.

En su versión original se propuso para 2 dimensiones y posteriormente se diseñó una versión para una cantidad arbitraria de dimensiones.
En este trabajo analizamos su comportamiento en las 20 primeras funciones de CEC2014 para 10 y 30 dimensiones y el por qué de este.
Concluimos que su comportamiento es aceptable para las funciones 5 y 12-16 de la competición CEC2014 e incluso supera en dimensión 30 a DE, aunque en dimensión 10 es superado por ambas versiones en casi todas las categorías y tiene un comportamiento muy inestable en las funciones unimodales.

Tras analizar el comportamiento de la convergencia vemos que se estanca rápidamente en mínimos locales y no es capaz de escapar de estos.

Como posibles soluciones exploré varios tipos de mejoras y he estudiado con detalle dos de ellas; una que ha sido estudiada previamente en la literatura de este algoritmo (versión memética) y otra versión de construcción propia inspirada en los algoritmos de evolución diferencial pero manteniendo la esencia de la competición imperialista.

En el primer caso (algoritmos meméticos) no logramos reproducir los resultados de la literatura, posiblemente debido a que el paper original explora los resultados en dos dimensiones. Incluso en el mejor de los casos el resultado obtenido suele ser mucho peor que el del algoritmo original ya que el algoritmo se estanca aún más fácilmente.

En el segundo caso (algoritmo inspirado en la evolución diferencial) conseguimos mejoras importantes respecto del algoritmo original conservando algunas de las características que lo definen: mantenemos las distintas subpoblaciones, la competición imperialista entre ellas y las revoluciones.
El algoritmo así obtenido mejora su posición mediana en la competición CEC2014 aunque no llega a reproducir los resultados del estado del arte.

Como conclusión final por tanto podemos observar que el algoritmo imperialista competitivo, como muchos de los algoritmos basados en poblaciones no está a la altura ni en su versión original ni en la versión modificada de algunos de los competidores de CEC2014. No obstante la versión mejorada hibridada con la evolución diferencial apunta a que hay posibilidades de mejora del algoritmo para hacerlo más competitivo y posiblemente la investigación en este campo pueda producir mejores resultados de los obtenidos en este trabajo.

# Referencias
