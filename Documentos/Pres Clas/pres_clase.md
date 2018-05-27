---
title: Algoritmo Imperialista Competitivo
subtitle: Metaheurísticas
date: Universidad de Granada
author: Pablo Baeyens Fernández
lang: es
theme: Frankfurt
colortheme: beaver
header-includes:
 - \usepackage[labelformat=empty]{caption}
colorlinks: true
---

# ICA

:::::::::::::: {.columns}
::: {.column width="50%"}
- Basado en el imperialismo y colonialismo
- Las soluciones (**países**) se dividen en **imperios** y **colonias**
- Las colonias se asimilan y los imperios compiten

![](assets/countryICA.png)
:::
::: {.column width="50%"}
![Funcionamiento del ICA](assets/visionICA.png)
:::
::::::::::::::

# Algoritmo

:::::::::::::: {.columns}
::: {.column width="40%"}
![](assets/flowchart.png)
:::
::: {.column width="60%"}
- Asimilación de colonias ![](assets/mov.png)
- Competición por las colonias ![](assets/competition.png)
- Eliminación de imperios
:::
::::::::::::::

# Comparativa


:::::::::::::: {.columns}
::: {.column width="50%"}
![$\min f = -18,55$](assets/g1.png)

:::
::: {.column width="50%"}
![Algoritmo ICA](assets/ica.png)
:::
::::::::::::::

Aplicamos ICA para minimizar $f(x) = x\sin(4x) + 1,1y\sin(2y)$.

# Comparativa

:::::::::::::: {.columns}
::: {.column width="50%"}
![Algoritmo genético](assets/Ga.png)
:::
::: {.column width="50%"}
![Algoritmo PSO](assets/pso.png)
:::
::::::::::::::

La convergencia de ICA es más rápida, aunque el número de parámetros a ajustar es mayor.


# Posibles mejoras


:::::::::::::: {.columns}
::: {.column width="40%"}

- Búsqueda local
- Revoluciones
- Adaptación de parámetros
- Asimilación en más dimensiones
:::
::: {.column width="60%"}
![](assets/revolution.png)
:::
::::::::::::::

