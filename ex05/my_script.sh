#!/bin/bash

# Definir variables
LOG_FILE="pip_install.log"
PYTHON_PATH="/usr/bin/python3"
VENV_DIR="django_venv"

# Verificar si el entorno virtual ya existe
if [ -d "$VENV_DIR" ]; then
    echo "El entorno virtual '$VENV_DIR' ya existe."
else
    echo "Creando el entorno virtual '$VENV_DIR'..."
    $PYTHON_PATH -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Error: No se pudo crear el entorno virtual." >&2
        exit 1
    fi
fi

# Activar el entorno virtual
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Activando el entorno virtual..."
    source $VENV_DIR/bin/activate
else
    echo "Error: No se encontró el archivo 'activate' en '$VENV_DIR/bin'." >&2
    exit 1
fi

# Mostrar la versión de pip
echo "Versión de pip:"
pip --version

# Instalar paquetes usando pip
echo "Instalando paquetes desde requirements.txt..."
pip install --log $LOG_FILE --force-reinstall -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: La instalación de paquetes falló." >&2
    exit 1
fi

echo "Instalación completada con éxito. Verifica el archivo de log '$LOG_FILE' para detalles."

