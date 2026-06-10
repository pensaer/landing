"""
Agente Inteligente de Generacion - Servicio para Windows 11

Descripcion:
  Monitorea cambios en gen_landings.py y carpetas de unidades.
  Ejecuta automáticamente el pipeline de generación.
  Se ejecuta como servicio de Windows con logs y control de errores.

Instalacion:
  python server/scripts/agent_service.py install

Uso:
  net start PensaerLandingsAgent
  net stop PensaerLandingsAgent
"""

import os
import sys
import json
import time
import hashlib
import logging
import logging.handlers
import subprocess
from datetime import datetime
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'


class Config:
    """Carga configuracion desde config.json"""

    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get(self, key, default=None):
        """Obtiene valor de configuracion con soporte para claves anidadas"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default


class Logger:
    """Sistema de logging con rotacion automatica"""

    def __init__(self, config):
        log_dir = Path(config.get('paths.log_directory'))
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"agent_service.log"

        # Crear logger
        self.logger = logging.getLogger('PensaerAgent')
        self.logger.setLevel(logging.INFO)

        # Handler con rotacion
        handler = logging.handlers.RotatingFileHandler(
            str(log_file),
            maxBytes=config.get('logging.max_file_size_mb', 10) * 1024 * 1024,
            backupCount=config.get('logging.backup_count', 5),
            encoding='utf-8'
        )

        formatter = logging.Formatter(config.get('logging.format', '[%(asctime)s] [%(levelname)s] %(message)s'))
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        # También imprimir en consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)


class Agent:
    """Agente inteligente de generacion"""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.base_dir = Path(config.get('paths.base_directory'))
        self.watch_file = self.base_dir / config.get('paths.watch_file')

    def get_file_hash(self, filepath):
        """Obtiene hash MD5 de un archivo"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error al leer {filepath}: {e}")
            return None

    def count_unit_folders(self):
        """Cuenta carpetas de unidades"""
        count = 0
        prefixes = ["p14_", "p15_", "p16_", "p17_", "p18_", "p20_", "p7_", "z_"]
        for item in self.base_dir.iterdir():
            if item.is_dir() and any(item.name.startswith(p) for p in prefixes):
                count += 1
        return count

    def run_pipeline(self):
        """Ejecuta el pipeline completo"""
        self.logger.info("="*70)
        self.logger.info("INICIANDO PIPELINE DE GENERACION")
        self.logger.info("="*70)

        scripts = self.config.get('pipeline.scripts', [])
        os.chdir(str(self.base_dir))

        try:
            for idx, script_config in enumerate(scripts, 1):
                name = script_config['name']
                desc = script_config['description']
                timeout = script_config.get('timeout_seconds', 300)

                self.logger.info(f"[{idx}/{len(scripts)}] Ejecutando {name}...")
                self.logger.info(f"  Descripcion: {desc}")

                try:
                    result = subprocess.run(
                        ["python", name],
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        encoding='utf-8',
                        errors='replace'
                    )

                    if result.returncode != 0:
                        self.logger.error(f"  [ERROR] {name} fallo")
                        if result.stderr:
                            self.logger.error(f"  Stderr: {result.stderr[:500]}")
                        return False

                    self.logger.info(f"  [OK] {name} completado")

                except subprocess.TimeoutExpired:
                    self.logger.error(f"  [TIMEOUT] {name} excedio {timeout}s")
                    return False

            # Git commit y push
            if self.config.get('pipeline.git_auto_commit', True):
                self.logger.info("[4/4] Sincronizando con GitHub...")

                # Chequear cambios
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.stdout.strip():
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    subprocess.run(["git", "add", "-A"], check=True, timeout=30)
                    subprocess.run(
                        ["git", "commit", "-m", f"Auto-update [{timestamp}]"],
                        check=True,
                        timeout=30
                    )

                    if self.config.get('pipeline.git_auto_push', True):
                        subprocess.run(
                            ["git", "push", "origin", "main"],
                            check=True,
                            timeout=60
                        )

                    self.logger.info("  [OK] Cambios sincronizados")
                else:
                    self.logger.info("  [INFO] No hay cambios para commitear")

            self.logger.info("="*70)
            self.logger.info("[OK] PIPELINE COMPLETADO EXITOSAMENTE")
            self.logger.info("="*70)
            return True

        except Exception as e:
            self.logger.error(f"[ERROR] Error durante pipeline: {e}")
            return False

    def monitor(self):
        """Monitorea cambios y ejecuta pipeline"""
        self.logger.info("")
        self.logger.info("[AGENTE INTELIGENTE DE GENERACION]")
        self.logger.info("="*70)
        self.logger.info(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Monitorea: {self.config.get('paths.watch_file')}")
        self.logger.info(f"Directorio: {self.base_dir}")
        self.logger.info(f"Intervalo chequeo: {self.config.get('monitoring.check_interval_seconds')}s")
        self.logger.info(f"Timeout inactividad: {self.config.get('monitoring.inactivity_timeout_seconds')}s")
        self.logger.info("="*70)

        last_hash = self.get_file_hash(self.watch_file)
        last_unit_count = self.count_unit_folders()
        check_interval = self.config.get('monitoring.check_interval_seconds', 10)
        inactivity_timeout = self.config.get('monitoring.inactivity_timeout_seconds', 3600)
        last_run = time.time()

        while True:
            try:
                time.sleep(check_interval)

                current_hash = self.get_file_hash(self.watch_file)
                current_unit_count = self.count_unit_folders()
                changes_detected = False

                if current_hash and current_hash != last_hash:
                    self.logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] [CAMBIO] Detectado en {self.config.get('paths.watch_file')}")
                    changes_detected = True
                    last_hash = current_hash

                if current_unit_count != last_unit_count:
                    diff = current_unit_count - last_unit_count
                    self.logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] [CARPETAS] Cambio: {diff:+d} (total: {current_unit_count})")
                    changes_detected = True
                    last_unit_count = current_unit_count

                time_since_last_run = time.time() - last_run
                if time_since_last_run > inactivity_timeout:
                    self.logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] [TIMEOUT] Inactividad {int(time_since_last_run/60)}m. Generacion preventiva...")
                    changes_detected = True

                if changes_detected:
                    if self.run_pipeline():
                        last_run = time.time()
                    else:
                        self.logger.warning("[AVISO] Pipeline fallo. Reintentando en 1 minuto...")
                        time.sleep(60)

            except Exception as e:
                self.logger.error(f"[ERROR] Error en monitor: {e}")
                time.sleep(60)


def main():
    """Punto de entrada principal"""

    # Obtener rutas
    script_dir = Path(__file__).parent
    config_dir = script_dir.parent / 'config'
    config_file = config_dir / 'config.json'

    if not config_file.exists():
        print(f"ERROR: config.json no encontrado en {config_file}")
        sys.exit(1)

    # Cargar configuracion
    config = Config(str(config_file))
    logger = Logger(config)
    agent = Agent(config, logger)

    try:
        agent.monitor()
    except KeyboardInterrupt:
        logger.info("")
        logger.info("[DETENIDO] Agente interrumpido")
        logger.info(f"Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        logger.error(f"[ERROR] Error fatal: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
