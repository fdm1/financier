FROM python:3.6.2-alpine

COPY budget_builder/setup.* /financier/budget_builder/
COPY budget_builder/budget_builder /financier/budget_builder/budget_builder
WORKDIR /financier/budget_builder
RUN pip install -e .

COPY financier_flask/setup.* /financier/financier_flask/
COPY financier_flask/financier_flask /financier/financier_flask/financier_flask
WORKDIR /financier/financier_flask
RUN pip install -e .

WORKDIR /financier
CMD ["python", "financier_flask/financier_flask/app.py"]
