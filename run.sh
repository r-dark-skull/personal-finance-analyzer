#! /bin/bash

# docker container rm mera_financial_analyst
# docker image rm personal-finance-analyzer:beta

# docker image build -t personal-finance-analyzer:beta .
# docker run  --name mera_financial_analyst -d -p 8000:8000 personal-finance-analyzer:beta

docker-compose up -d
docker image prune
