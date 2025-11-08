# Use uma imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . /app/

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta onde o Streamlit será executado
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]