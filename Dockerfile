FROM python:3.12

# Configurar variables de entorno
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/odoodjango

# Establecer directorio de trabajo
WORKDIR /app

# Copiar y instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . /app/

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "--chdir", "/app/odoodjango", "odoodjango.odoodjango.wsgi:application", "--bind", "0.0.0.0:8000"]

