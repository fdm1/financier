FROM python:3.7.4-stretch

WORKDIR /financier
COPY budget_builder/setup.* budget_builder/
COPY budget_builder/budget_builder budget_builder/budget_builder
RUN pip install -e budget_builder

COPY budgie/setup.* budgie/
COPY budgie/budgie budgie/budgie
RUN pip install -e budgie

COPY financier_flask/setup.* financier_flask/
COPY financier_flask/financier_flask financier_flask/financier_flask
RUN pip install -e financier_flask

CMD ["python", "financier_flask/financier_flask/app.py"]
