FROM python:3.7.4-stretch

WORKDIR /financier

COPY ./budgie/requirements.txt ./budgie/requirements.txt
COPY ./budget_builder/requirements.txt ./budget_builder/requirements.txt
COPY ./financier_flask/requirements.txt ./financier_flask/requirements.txt
RUN pip install -r ./budgie/requirements.txt
RUN pip install -r ./budget_builder/requirements.txt
RUN pip install -r ./financier_flask/requirements.txt

COPY ./ ./
RUN pip install -e budget_builder
RUN pip install -e budgie
RUN pip install -e financier_flask

CMD ["python", "financier_flask/financier_flask/app.py"]
