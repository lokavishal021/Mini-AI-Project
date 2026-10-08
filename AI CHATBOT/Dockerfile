FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y tesseract-ocr libespeak1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# Install CPU-only PyTorch first to save gigabytes of space
RUN pip install --no-cache-dir torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main1.py"]
