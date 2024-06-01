FROM python:3.12.3-bullseye
WORKDIR /develop

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV SERVER_URL=http://server:5000
ENV TRANSACTION_PATH=/transactions

CMD ["streamlit", "run", "main.py"]
