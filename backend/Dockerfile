FROM python:3.12.3-bullseye

WORKDIR /develop
COPY . .

RUN apt-get update
RUN apt-get install -y cron
RUN chmod +x jobs/setup.sh

# setting env variables
ENV MONGO_URL_TEMPLATE=mongodb://{username}:{password}@{address}/?authMechanism=DEFAULT&retryWrites=true&w=majority
ENV MONGO_USERNAME=root
ENV MONGO_PASSWORD=toor
ENV MONGO_SOCKET_ADDRESS=mongo_db:27017
ENV MONGO_DATABASE=personal_finance_analyzer
ENV TRANSACTION_COLLECTION=transactions
ENV MAIL_COLLECTION=raw_emails
ENV CATEGORY_COLLECTION=category_db


RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
