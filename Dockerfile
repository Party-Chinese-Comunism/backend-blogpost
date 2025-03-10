# Use a imagem base
FROM python:3.12.2-slim

# Instalar dependências necessárias para o Filebeat
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg

# Adicionar a chave GPG do repositório Elastic
RUN curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

# Adicionar o repositório do Elastic
RUN echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-8.x.list

# Atualizar os repositórios e instalar o Filebeat
RUN apt-get update && apt-get install -y filebeat

# Copiar o arquivo de configuração do Filebeat
COPY filebeat.yml /etc/filebeat/filebeat.yml

# Expor a porta do serviço Filebeat (caso necessário)
EXPOSE 5000

# Configurar o entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Definir o entrypoint
ENTRYPOINT ["/entrypoint.sh"]
