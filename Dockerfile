FROM python:3.12.2-slim

# Evita cache de bytecode e garante logs imediatos (boa prática para containers)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py  # Ajuste para o nome correto do seu app principal (ex: app.py ou wsgi.py)
ENV FLASK_ENV=production

WORKDIR /app

# Copia só o requirements primeiro (aproveita cache)
COPY requirements.txt ./

# Instala dependências do Python
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
