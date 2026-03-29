FROM python:3.11-slim
WORKDIR /app
RUN pip install flask --no-cache-dir
COPY app.py .
EXPOSE 9000
CMD ["python", "app.py"]
