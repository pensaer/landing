# Pensaer Landings Auto-Generation Service

Servicio Windows automatizado que monitorea cambios en landing pages y ejecuta el pipeline completo de generación.

## ⚡ Quick Start

```bash
# 1. Abre CMD como ADMINISTRADOR
cd server\bin

# 2. Instala
install.bat

# 3. Inicia
start.bat

# ¡Listo! El servicio está activo
```

## 📚 Documentación Completa

Ver **[INSTALACION.md](INSTALACION.md)** para:
- Instalación paso a paso
- Configuración
- Comandos de control
- Troubleshooting
- Seguridad

## 🎮 Comandos Rápidos

| Comando | Descripción |
|---------|------------|
| `bin\install.bat` | Instala el servicio |
| `bin\start.bat` | Inicia el servicio |
| `bin\stop.bat` | Detiene el servicio |
| `bin\status.bat` | Ver estado y logs |
| `bin\logs.bat` | Ver logs en tiempo real |
| `bin\uninstall.bat` | Desinstala el servicio |

## 📂 Estructura

```
server/
├── bin/              Scripts de control (install, start, stop, etc.)
├── config/           Archivo config.json
├── scripts/          agent_service.py (proceso principal)
├── logs/             Archivos de log (automático)
└── README.md         Este archivo
```

## 🔄 Qué hace el servicio

```
Monitorea cada 10 segundos:
  ✓ Cambios en gen_landings.py
  ✓ Cambios en carpetas de unidades
  ✓ Timeout de inactividad (1 hora)

Si detecta cambios → Ejecuta:
  1. python gen_landings.py
  2. python gen_pdfs.py
  3. python gen_index.py
  4. git commit + git push

Logs en: server/logs/agent_service.log
```

## ⚙️ Configuración

Edita `config/config.json` para:
- Intervalo de chequeo
- Timeout de inactividad
- Niveles de log
- Auto-commit/push de Git

## 🆘 Soporte

**Ver logs:**
```bash
bin\logs.bat
```

**Ver estado:**
```bash
bin\status.bat
```

**Reinstalar:**
```bash
bin\uninstall.bat
bin\install.bat
bin\start.bat
```

---

Para documentación detallada: [INSTALACION.md](INSTALACION.md)
