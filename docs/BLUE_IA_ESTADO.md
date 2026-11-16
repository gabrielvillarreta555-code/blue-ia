# Blue IA — Estado de investigación y continuidad

**Actualizado:** 2026-11-16  
**Responsable:** Blue Lab Studios  
**Naturaleza:** bitácora de continuidad; los resultados históricos aquí resumidos proceden de reportes y conversaciones previas, **no se han reejecutado ni auditado contra artefactos originales en este repositorio**.

## Cómo retomar desde un chat nuevo
1. Leer este documento primero.
2. Distinguir **resultado medido**, **decisión de Dirección**, **protocolo aprobado** y **propuesta**.
3. Consultar los artefactos originales antes de afirmar reproducibilidad; si no están en este repositorio, pedir sus rutas o enlaces.
4. Al terminar cada investigación, añadir una entrada fechada con hipótesis, método, datos/semillas, resultados, limitaciones, decisión, siguiente paso y enlaces a código/PR/checkpoints. Actualizar la sección «Estado actual»; no sobrescribir el historial.
5. No convertir una propuesta en experimento ejecutado ni una prueba sintética en una capacidad demostrada en producción.

## Visión
Desarrollar una IA propia (Blue), aprendiendo desde neuronas artificiales, entrenamiento, memoria y razonamiento, sin limitarse a integrar APIs de modelos existentes. Prioridad científica: generalización y aprendizaje continuo medibles. Los experimentos de recuperación externa no equivalen a cambios en pesos neuronales.

## Estado actual — 2026-11-16
- **Blue Neural:** BN-ILP-001 a BN-ILP-005 reportados; resultados mixtos, sin demostrar aprendizaje continuo robusto. **BN-ILP-006 no consta como ejecutado**.
- **Blue Memory (BM-001):** protocolo de diseño autorizado, ejecución no confirmada.
- **Blue Reasoning (BR-001):** protocolo de diseño autorizado, ejecución no confirmada.
- **Blue Efficiency:** comparación batch 1 vs 32 propuesta, ejecución no confirmada.
- **Producción:** no autorizar integración de los métodos experimentales sin evidencia adicional.
- **Repositorios:** este repositorio contiene experimentos anteriores de Blue IA con Qwen en Colab; **no asumir que los experimentos BN-ILP viven aquí**. Ver README para el alcance real del código.

## Blue Neural — registro histórico resumido

### BN-ILP-001
MLP A→B, con/sin repetición. Sin replay: A inicial 71,25%; combinaciones retenidas 24,69%; A tras B 39,38%; B 60%. Con replay: A inicial 68,13%; combinaciones retenidas 13,13%; A tras B 79,38%; B 35%. Baseline vecino más cercano: A inicial 75,63%; combinaciones retenidas 53,75%; A tras B 71,88%; B 80%. **No se alcanzó generalización objetivo ≥60%.**

### BN-ILP-002
Auditoría de identificabilidad: 64 combinaciones excluidas pueden etiquetarse mediante funciones incompatibles, ambas consistentes con entrenamiento. Se detectó desequilibrio de replay. **Auditoría, no prueba de mejora.**

### BN-ILP-003
Cinco semillas; replay 0/1/3. Generalización 30,31/29,69/35,62%; A después de B 54,37/62,50/75,62%; B 46,88/46,25/45%. **Ninguna variante alcanzó generalización ≥60%.**

### BN-ILP-004
Supuesto XOR-afín explícito, datos equilibrados, cinco semillas emparejadas. Generalización A retenida tras A: media 69,06%. Después de B: sin replay A 49,38%, B 52,5%, olvido 18,12 puntos; replay 1 A 49,38%, B 50,62%; replay 3 A 63,12%, B 50,62%, olvido 4,38 puntos. Solo 2/5 semillas alcanzaron conjuntamente los umbrales iniciales. Solapamiento de 28–36 patrones/semilla con un conjunto anterior: **no reclamar benchmark independiente**.

### BN-ILP-005
Control B-only, cinco semillas: B desde cero 60,0% (2/5 semillas ≥60%); A→B sin replay 52,5% (1/5); A→B con replay 50,62% (0/5). Resultados B-only por semilla: 59,38%, 68,75%, 53,12%, 50%, 68,75%. Algunas trayectorias colapsaron a una sola clase; gradientes muestreados no nulos. **B ya es inestable por sí sola; hay indicios de interferencia desde A.** Meta futura: B ≥60% en 4/5 semillas.

### BN-ILP-006 — protocolo aprobado condicionalmente, ejecución no confirmada
Comparar SGD LR=0,1 con 128 pasos (histórico), LR=0,1 con 256 pasos y LR=0,05 con 128 pasos, modificando una variable cada vez; cinco semillas emparejadas, mismas particiones y MLP. Curvas train/validación; test retenido solo al final, sin selección por test. Presupuesto máximo: 1.920 actualizaciones nuevas, 45 s CPU, 90 s pared, 1 GiB RAM, 120 KiB de persistencia.

**Bloqueo de almacenamiento reportado:** 151.552 bytes libres vs mínimo 225.280. Se autorizó exclusivamente borrar el archivo de caché regenerable `/home/agent/.cache/matplotlib/fontlist-v390.json` tras verificar que es archivo regular y no enlace, y volver a medir espacio e integridad. No se autorizó borrar otros archivos. No afirmar que esta limpieza o entrenamiento ocurrió sin registro.

## Blue Memory / Blue Reasoning / Efficiency
- **BC-011 (reporte histórico):** demostración sintética de enseñar, recuperar, revocar y devolver «desconocido». Es recuperación externa, **no entrenamiento de pesos**.
- **BM-001 (diseño):** memoria externa con versiones, validez, procedencia y revocación. Comparar búsqueda exacta, léxica y filtro de validez. Límites propuestos: 30 s CPU, 128 MiB RAM, 64 KiB persistencia.
- **BR-001 (diseño):** distinguir fuentes correlacionadas de evidencia independiente, calibrar abstención en casos sintéticos; comparar mayoría simple, Sócrates y política experimental. Límites propuestos: 30 s CPU, 128 MiB RAM, 64 KiB persistencia.
- **Sócrates (reporte histórico):** abstención ante conflicto sintético con traza; no demuestra verificación general en el mundo real.
- **Blue Efficiency (propuesta):** inferencia CPU batch 1 frente a batch 32 sobre checkpoints existentes, comprobar identidad de predicciones; ≤30 s CPU, ≤1 GiB RAM, ≤32 KiB persistencia.
- Dirección autorizó **diseñar** BM-001 y BR-001 con particiones independientes y métricas prefijadas, **no su ejecución ni integración en producción**.

## Decisiones de Dirección
- BN-005 (línea previa k-WTA/EWC/routing/DER++): rechazado por no superar consistentemente DER++; resultados históricos sintético 53,68%, dígitos 49,17%, frente a controles con replay y DER++.
- BN-006 (línea previa): modificaciones solicitadas; priorizar aprendizaje continuo, criterios de éxito y recursos.
- BN-ILP-006: protocolo autorizado **solo bajo condiciones de recursos e integridad**.
- BM-001/BR-001: preparación de protocolos, no ejecución.
- No inflar resultados; preservar separación entre ciencia experimental y producto.

## Próximo paso recomendado
1. Localizar los informes originales, código, semillas, particiones y checkpoints BN-ILP; enlazarlos aquí. No reconstruir números ausentes.
2. Comprobar si se resolvió el bloqueo de disco y si BN-ILP-006 llegó a ejecutarse.
3. Si no, ejecutar únicamente cuando se cumplan las condiciones aprobadas; publicar tabla por semilla y curvas.
4. Preparar protocolos BM-001 y BR-001 para revisión, sin tratarlos como resultados.
5. Al cerrar cada trabajo, actualizar esta bitácora **en el mismo PR o commit de investigación**.

## Plantilla para nuevas entradas
```md
### AAAA-MM-DD — ID — título
Estado: propuesta | protocolo | ejecutado | auditado | rechazado
Pregunta / hipótesis:
Método y datos:
Semillas y particiones:
Resultados (con unidades):
Comparación y limitaciones:
Decisión:
Siguiente acción:
Artefactos (rutas, commits, PR, fuentes):
```

## Política de actualización
Este archivo es el **índice de continuidad**; informes extensos deben ir a `docs/investigaciones/<ID>.md`. No registrar secretos, datos personales ni conversaciones privadas. Mantener un resumen compacto y referencias a evidencia; Git conserva el historial de versiones.
