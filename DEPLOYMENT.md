# Deployment a Windows 11 Server

Guía de qué archivos copiar al servidor de producción.

---

## 📋 Archivos NECESARIOS (Copia TODO esto)

### Carpeta `server/` - COMPLETA
```
server/
├── bin/
│   ├── install.bat          ✅ COPIA
│   ├── start.bat            ✅ COPIA
│   ├── stop.bat             ✅ COPIA
│   ├── status.bat           ✅ COPIA
│   ├── logs.bat             ✅ COPIA
│   └── uninstall.bat        ✅ COPIA
│
├── config/
│   └── config.json          ✅ COPIA
│
└── scripts/
    └── agent_service.py     ✅ COPIA
```

### Scripts Generadores
```
✅ gen_landings.py           (necesario - genera landings)
✅ gen_pdfs.py               (necesario - genera PDFs)
✅ gen_index.py              (necesario - regenera index)
✅ export_data.py            (opcional - solo si usas exportación)
```

### Carpetas de Assets Públicos
```
✅ p14_dram_*                (todas las carpetas de unidades)
✅ p15_elyol_*
✅ p15_elysj_*
✅ p16_eryn_*
✅ p17_nythu_*
✅ p18_dynha_*
✅ p20_elsj_*
✅ p7_oficina_*
✅ z_italia1165_*
✅ z_rosas930_*

✅ plantas_pNN/              (plantas de las unidades)
✅ renders_pNN/              (renders de proyectos, EXCEPTO insert*.pdf)
```

### Archivos Públicos Raíz
```
✅ index.html                (página principal)
✅ pensaer-logo.png          (logo)
✅ politica-privacidad.html  (página de privacidad)
```

### Configuración de Git
```
✅ .git/                     (todo el directorio git)
✅ .gitignore                (archivo de ignorados)
```

### Documentación en Servidor
```
✅ server/README.md          (guía rápida)
✅ server/INSTALACION.md     (guía de instalación)
✅ server/requirements.txt   (dependencias)
```

---

## ❌ Archivos NO NECESARIOS (NO copiar)

### Privados / Configuración Local
```
❌ CLAUDE.md                 (instrucciones de Claude, locales)
❌ .claude/                  (configuración de Claude Code)
❌ INSTALACION.md            (documentación privada original)
❌ SETUP.md                  (setup local)
❌ DEVELOPMENT.md            (desarrollo local)
```

### Herramientas de Desarrollo
```
❌ watch_and_generate.py     (versión antigua, usa agent_service.py)
❌ __pycache__/              (caché de Python)
❌ *.pyc                     (bytecode compilado)
```

### Datos Sensibles/Generados
```
❌ data/                     (JSON/CSV exportados - se regeneran)
❌ renders_*/insert*.pdf     (inserts privados - no públicos)
❌ renders_*/insert_pages/   (inspección privada)
❌ renders_*/check/          (archivos de chequeo)
❌ renders_p*/cam_*.jpg      (cámaras privadas)
❌ renders_p*/render_*.jpg   (renders privados)
```

### Marcas Privadas
```
❌ p7_oficina_sl/Venta oficina SanLo/  (carpeta privada)
❌ manual/                              (brand guidelines privado)
```

---

## 📊 Resumen de Tamaño

Aproximadamente:

```
server/                      ~100 KB  (scripts + config)
Landing pages HTML/PDF       ~200-300 MB (depende de cuántas unidades)
Assets públicos              ~500 MB  (renders + plantas)

TOTAL APROXIMADO:           ~700-800 MB
```

---

## 🚀 Método de Copia Recomendado

### Opción 1: Copia Manual (más seguro)

```bash
# En el servidor Windows 11:

# 1. Crea carpeta base
mkdir C:\Landings
cd C:\Landings

# 2. Desde tu PC, copia via Windows Explorer o:
# - Comprime C:\Users\marcelo\Documents\Landings
# - Copia el ZIP al servidor
# - Extrae en C:\Landings

# 3. Verifica la estructura:
dir /s
```

### Opción 2: Git Clone (más automático)

```bash
# En el servidor:
cd C:\
git clone https://github.com/pensaer/landing.git Landings
cd Landings
```

**Ventajas:**
- ✅ Descarga automáticamente los archivos públicos
- ✅ Mantiene la historia de git
- ✅ Fácil de actualizar: `git pull`

**Nota:** Los archivos en .gitignore NO se descargarán (es lo esperado)

### Opción 3: Script de Sincronización

```bash
# Crear sync.bat en el servidor para actualizar:
@echo off
cd C:\Landings
git pull origin main
echo.
echo [OK] Landing pages actualizadas
pause
```

---

## ✅ Checklist de Instalación

Después de copiar, verifica:

```bash
# 1. Estructura correcta
C:\Landings\
├── server\
├── gen_landings.py
├── gen_pdfs.py
├── gen_index.py
├── index.html
├── p14_dram_*/
└── .git/

# 2. Instala el servicio
cd C:\Landings\server\bin
install.bat

# 3. Inicia el servicio
start.bat

# 4. Verifica logs
status.bat

# 5. Prueba un cambio
(Modifica gen_landings.py)
# Espera 10 segundos
status.bat  # Debe mostrar cambio detectado
```

---

## 🔄 Actualizar Landings en Servidor

Opción 1: Automático (el agente hace todo)
```bash
# 1. Modifica gen_landings.py en el servidor
# 2. El agente detecta en <10s
# 3. Ejecuta automáticamente todo
```

Opción 2: Manual
```bash
cd C:\Landings
python gen_landings.py
python gen_pdfs.py
python gen_index.py
git add -A
git commit -m "Update"
git push
```

Opción 3: Desde tu PC, usar agente inteligente
```bash
# Tu PC continúa ejecutando el agente
python watch_and_generate.py
# Los cambios se synchonizan via git push
# El servidor ejecuta: git pull
```

---

## 🛡️ Requisitos en Servidor

```
✅ Python 3.8+ instalado y en PATH
✅ Git instalado y en PATH
✅ Git autenticado (SSH key o token)
✅ Acceso de administrador (para instalar servicio)
✅ ~800 MB de espacio disco libre
```

---

## 📦 Estructura Esperada en Servidor

```
C:\Landings\                        (raíz)
├── server\                          (servicio de Windows)
│   ├── bin\
│   ├── config\
│   ├── scripts\
│   └── logs\                        (se crea automáticamente)
│
├── gen_landings.py                  (generador)
├── gen_pdfs.py
├── gen_index.py
├── export_data.py
│
├── index.html                       (público)
├── politica-privacidad.html
├── pensaer-logo.png
│
├── p14_dram_*/                      (unidades)
├── p15_elyol_*/
├── p16_eryn_*/
├── ... (resto de unidades)
│
├── plantas_pNN/                     (assets)
├── renders_pNN/
│
├── .git/                            (historial git)
└── .gitignore
```

---

## 🚀 Resumen Quick

### Copia SOLO ESTO:

```
✅ server/              (scripts + config)
✅ gen_*.py             (generadores)
✅ p*_*/                (unidades HTML/PDF)
✅ plantas_*/           (plantas)
✅ renders_pNN/         (SOLO *.jpg, NO inserts)
✅ index.html
✅ politica-privacidad.html
✅ .git/
```

### NO copies ESTO:

```
❌ .claude/
❌ CLAUDE.md
❌ data/
❌ manual/
❌ watch_and_generate.py
❌ insert*.pdf
❌ __pycache__/
```

---

## 💡 Tip Final

Para verificar que copiaste bien:

```bash
# En el servidor, ejecuta:
server\bin\install.bat

# Si todo está bien:
# [OK] Servicio instalado
# [OK] Directorio base: C:\Landings

# Si algo falta:
# [ERROR] Python no encontrado
# [ERROR] gen_landings.py no existe
```

---

**¿Necesitas un script de copia automatizada?** Pregunta por `deployment-script.bat`
