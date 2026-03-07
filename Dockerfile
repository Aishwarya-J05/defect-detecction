FROM python:3.10

WORKDIR /app

COPY requirements.txt .

# Install system libraries required by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Prevent YOLO from trying to download anything at runtime
ENV YOLO_CONFIG_DIR=/app/.yolo
ENV ULTRALYTICS_CONFIG_DIR=/app/.yolo
ENV YOLO_OFFLINE=1

EXPOSE 7860

CMD ["gunicorn", "flask_app:app", "--bind", "0.0.0.0:7860", "--timeout", "120"]