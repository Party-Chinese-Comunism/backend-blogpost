

FROM python:3.12.2-slim

# Instalar o Filebeat
RUN apt-get update && apt-get install -y curl apt-transport-https
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.6.3-amd64.deb
RUN dpkg -i filebeat-8.6.3-amd64.deb

# Definir o diretório de trabalho
WORKDIR /app

# Copiar e instalar as dependências do Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do backend
COPY . .

# Expor a porta do Flask
EXPOSE 5000

# Copiar o arquivo de configuração do Filebeat
COPY backbeat.yml /etc/filebeat/filebeat.yml

# Iniciar o Filebeat em segundo plano e o Flask
CMD filebeat -e & flask run --host=0.0.0.0
