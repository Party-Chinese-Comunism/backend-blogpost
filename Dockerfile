# Use a imagem base do Python
FROM python:3.12.2-slim

# Diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar o Filebeat
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.6.2-amd64.deb && \
    dpkg -i filebeat-8.6.2-amd64.deb && \
    rm -f filebeat-8.6.2-amd64.deb

# Copie o código do aplicativo Flask para o contêiner
COPY . .

# Exponha a porta 5000
EXPOSE 5000

# Comando para rodar o Flask e o Filebeat
CMD ["sh", "-c", "filebeat -e -d '*' & flask run --host=0.0.0.0"]
