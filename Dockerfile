FROM python:3.12.3-bullseye
WORKDIR /develop

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "app.py"]
