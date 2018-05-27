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
colorlinks: true
bibliography: assets/bibliografía.bib
biblio-style: apalike
link-citations: true
citation-style: assets/estilo.csl
numbersections: true
toc: true
---

\newpage

# Introducción

Los problemas de optimización uniobjetivo en variables reales consisten en, dados $n \in \mathbb{N}$ y un *dominio* $\Omega \subseteq \mathbb{R}^n$ hallar un mínimo global de una función $F:\Omega \to \mathbb{R}$ llamada *función objetivo*. Una *solución* es un vector $x \in \mathbb{R}^n$ y su *calidad* es el valor $F(x)$.

Este problema no es en general tratable de forma exacta; una función objetivo arbitraria puede no tener buenas propiedades analíticas o ser altamente multimodal, lo que impide el uso de técnicas basadas en el análisis como el uso del gradiente descendiente. 
En su lugar intentamos aplicar metaheurísticas que intentan resolver estos problemas de forma general utilizando heurísticas, con frecuencia inspiradas en la naturaleza o en otros fenómenos.

En este documento analizamos una familia de metaheurísticas concreta y evaluamos su comportamiento sobre las funciones objetivo definidas para la competición CEC 2014 [@CEC2014].
En concreto utilizamos una adaptación de las mismas a NumPy que he implementado junto con Ignacio Aguilera Martos [@cec2014NumPy].


# Algoritmo imperialista competitivo

El *algoritmo imperialista competitivo* (ICA por sus siglas del inglés) es un algoritmo evolutivo basado en poblaciones[@LucasImperialistcompetitivealgorithm2017]. Es un algoritmo aplicable a problemas de optimización en variables reales para funciones definidas sobre un convexo de cualquier dimensión. 
También se han propuesto versiones para problemas discretos [@Behnamiandiscretecolonialcompetitive2011].

La inspiración del algoritmo viene del fenómeno histórico del imperialismo y el colonialismo.
Las soluciones son *países* que se dividen en *colonias* e *imperialistas*; las colonias se *asimilan* hacia los imperialistas y los imperialistas compiten entre sí por las colonias. El proceso fundamental de búsqueda de soluciones es la asimilación, que produce cruces entre el imperialista y sus colonias.

Abstrayendo esta interpretación podemos verlo como un algoritmo de optimización por enjambre de partículas con varias subpoblaciones (los imperialistas junto con sus colonias) que propone una forma de interacción entre estas poblaciones (la competición imperialista).

Es un algoritmo que ha sido utilizado para diversas aplicaciones industriales [@HosseinisurveyImperialistCompetitive2014] y desde su publicación original se han propuesto varias mejoras o versiones alternativas del algoritmo que mejoran sus resultados [@AbdiGICAImperialistcompetitive2017][@LinInteractionEnhancedImperialist2012][@AbdechiriAdaptiveImperialistCompetitive2010][@LinImprovingImperialistCompetitive2013][@RamezaniSocialBasedAlgorithmSBA2013].

## Algoritmo original

En esta sección describimos el algoritmo original tal y como aparece en la versión en MATLAB implementada por los autores [@implICA]. Esta versión introduce ya el concepto de revolución que no aparece en el paper original y subsana algunos errores así que he considerado que era una versión más adecuada para empezar a trabajar.

El pseudocódigo del algoritmo es el siguiente:

\input{algos/algoGeneral}

donde $\alpha, z, R_\mathrm{Inicial}$ y nDécadas son parámetros ajustables.
En primer lugar la función CreaImperiosIniciales construye de forma uniforme países y toma los mejores como imperialistas 

## Versiones alternativas

En esta sección describo brevemente 4 versiones alternativas y mejoras que han sido propuestas en la literatura relativa a este algoritmo:

*ICA with globalization mechanism (GICA)* [@AbdiGICAImperialistcompetitive2017]
: propone algunas modificaciones para aumentar la relación entre los imperios:

  1. La asimilación se hace parcialmente hacia el mejor imperialista y no sólo hacia al que pertenece la colonia
  2. Implementa mecanismo de cruce aritmético entre imperialistas y sustituye a los imperialistas si encuentra una mejor solución
  3. Implementa un mecanismo de cruce entre las colonias de un mismo imperio mediante una combinación convexa aleatoria


*Interaction Enhanced ICA* [@LinInteractionEnhancedImperialist2012]
: propone dos variantes: en primer lugar ICAAI que construye un imperialista artifical haciendo una suma ponderada de los imperialistas existentes (dando más peso al mejor imperialista) e intenta sustituir el mejor imperialista por este. En segundo lugar ICACI cruza los imperialistas entre sí y los reemplaza si hay mejora. El paper encuentra que ICAAI suele dar mejores resultados que ICACI en general, y estos mejoran los resultados del algoritmo ICA original así como al PSO.


*Adaptive ICA (AICA)* [@AbdechiriAdaptiveImperialistCompetitive2010]
: propone modificar de forma adaptativa el ángulo de rotación del proceso de asimilación de colonias en función de la diversidad existente en el imperio. Para ello calcula la diversidad existente en la población en mediante la función de densidad de la normal multivariante. A partir de este dato modifica el ángulo de rotación de la asimilación; esto hace que aumente o disminuya la diversidad de la población, evitando así la convergencia prematura.

*Improving ICA with Local Search for Global Optimization* [@LinImprovingImperialistCompetitive2013]
: propone aplicar búsqueda local a todos los imperialistas o sólo al mejor de ellos y compara estos con una versión de ICA.
Usando el mismo número de evaluaciones de la función objetivo obtiene mejores resultados en el caso de aplicar búsqueda local a todos los imperialistas.

# Análisis del algoritmo


# Mejoras implementadas

# Análisis de las mejoras

# Conclusiones

\newpage

# Referencias
