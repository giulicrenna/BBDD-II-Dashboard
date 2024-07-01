FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9999

CMD ["streamlit", "run", "main.py"]