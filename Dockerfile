FROM python:3.12.1-bookworm

RUN mkdir -p /home/app
RUN cd /home/app

COPY algebra.py /home/app 
COPY rest_api_server.py /home/app 
COPY farm_animals/ /home/app/farm_animals/
 
RUN pip3 install bottle

CMD ["python3", "/home/app/rest_api_server.py"]
