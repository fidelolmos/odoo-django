FROM python:3.12

# Configurar variables de entorno
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/odoodjango

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt en /app/
COPY requirements.txt /app/requirements.txt

# Instalar dependencias antes de copiar el código
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar todo el código de la aplicación
COPY . /app/

# Cambiar al directorio correcto donde está manage.py
WORKDIR /app/odoodjango

# Exponer el puerto 8000 para Gunicorn
EXPOSE 8000

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "--chdir", "/app/odoodjango", "odoodjango.wsgi:application", "--bind", "0.0.0.0:8000"]
