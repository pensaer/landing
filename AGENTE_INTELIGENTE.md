# Agente Inteligente de Generación de Landings

## Descripción

`watch_and_generate.py` es un agente que monitorea cambios en el proyecto y ejecuta automáticamente el pipeline completo de generación de landing pages.

## Características

### 🔍 Monitoreo Inteligente

- **Detecta cambios en `gen_landings.py`** → Regenera automáticamente todas las landings
- **Detecta cambios en carpetas de unidades** → Cuando se agregan/eliminan unidades
- **Timeout de inactividad** → Ejecuta al menos cada 1 hora (prevención de desincronización)

### ⚙️ Pipeline Automático

Cuando detecta cambios, ejecuta en orden:

1. `python gen_landings.py` → Genera 41 landing pages HTML + fichas HTML
2. `python gen_pdfs.py` → Convierte fichas HTML → PDF
3. `python gen_index.py` → Regenera index.html
4. `git add -A && git commit && git push` → Sincroniza con GitHub

### 📊 Comportamiento

```
┌─────────────────────────────────────┐
│  Agente en monitoreo cada 10s       │
├─────────────────────────────────────┤
│                                     │
│  ¿Cambios en gen_landings.py?      │ ➜ SÍ ➜ EJECUTAR PIPELINE
│  ¿Cambios en carpetas?             │ ➜ SÍ ➜ EJECUTAR PIPELINE
│  ¿Pasaron >1 hora sin ejecutar?    │ ➜ SÍ ➜ EJECUTAR PIPELINE
│                                     │
│  Si NO → Esperar 10s y re-chequear │
└─────────────────────────────────────┘
```

## Uso

### Iniciar el agente

```bash
cd c:\Users\marcelo\Documents\Landings
python watch_and_generate.py
```

### Salida esperada

```
🔍 AGENTE INTELIGENTE DE GENERACIÓN DE LANDINGS
======================================================================
Iniciado: 2026-06-10 14:30:45
Monitorea: gen_landings.py
Directorio base: c:\Users\marcelo\Documents\Landings
Presiona Ctrl+C para detener
======================================================================

[14:30:45] ✏️  Cambio detectado en gen_landings.py

======================================================================
[14:30:46] INICIANDO PIPELINE DE GENERACIÓN
======================================================================

[1/4] Ejecutando gen_landings.py...
✓ gen_landings.py completado

[2/4] Ejecutando gen_pdfs.py...
✓ gen_pdfs.py completado

[3/4] Ejecutando gen_index.py...
✓ gen_index.py completado

[4/4] Sincronizando con GitHub...
✓ Cambios sincronizados con GitHub

======================================================================
[14:35:20] ✓ PIPELINE COMPLETADO EXITOSAMENTE
======================================================================
```

### Detener el agente

Presiona `Ctrl+C` en la terminal.

## Configuración

Parámetros configurables en `watch_and_generate.py`:

```python
check_interval = 10        # Chequear cambios cada 10 segundos
inactivity_timeout = 3600  # Ejecutar al menos cada 1 hora (3600 segundos)
```

## Casos de uso

### ✓ Cuando el agente ejecuta automáticamente:

1. **Modificas `gen_landings.py`** → Agrega/modifica una unidad
2. **Creas nueva carpeta de unidad** → `p14_dram_1-01-02/`
3. **Eliminas una carpeta** → Unidad no disponible
4. **Pasa 1 hora sin cambios** → Ejecución preventiva

### ✗ Cuando el agente NO ejecuta:

- El archivo `gen_landings.py` no cambió
- No se agregaron/eliminaron carpetas de unidades
- Menos de 1 hora desde la última ejecución

## Modo de funcionamiento

### Continuo (Recomendado)

Mantener el agente ejecutándose permanentemente:

```bash
# En una terminal dedicada o tmux/screen
python watch_and_generate.py
```

### Con supervisor (Producción)

Usar herramientas como `supervisor` para que el agente se reinicie automáticamente si falla.

## Logs y debugging

El agente imprime en consola:

- `✏️ Cambio detectado` → Cambio en gen_landings.py
- `📁 Cambio en unidades` → Carpetas agregadas/eliminadas
- `⏱️ Tiempo de inactividad excedido` → Ejecución preventiva
- `✓ PIPELINE COMPLETADO` → Ejecución exitosa
- `❌ Error` → Problema durante la ejecución

## Flujo de datos

```
gen_landings.py (modificas aquí)
    ↓
watch_and_generate.py (detecta cambio)
    ↓
Ejecuta pipeline:
  • gen_landings.py → HTML
  • gen_pdfs.py → PDF
  • gen_index.py → index.html
    ↓
Git commit + push
    ↓
GitHub Pages actualiza automáticamente
```

## Notas

- El agente chequea cambios cada **10 segundos**
- Ejecuta al menos cada **1 hora** (aunque no haya cambios)
- Si el pipeline falla, reintenta en 1 minuto
- Los commits se etiquetan con `[Auto-update landings]`
- Funciona en Windows, macOS y Linux

## Troubleshooting

### El agente no detecta cambios

Verificar:
- `gen_landings.py` está siendo modificado (no solo leído)
- Las nuevas carpetas de unidades siguen el patrón `pXX_*` o `z_*`

### El pipeline falla

Verificar:
- `gen_landings.py`, `gen_pdfs.py`, `gen_index.py` funcionan manualmente
- Credenciales de Git están configuradas
- Hay espacio en disco

### El agente se detiene inesperadamente

Reiniciar:
```bash
python watch_and_generate.py
```

Use supervisor o task scheduler para que se reinicie automáticamente.
