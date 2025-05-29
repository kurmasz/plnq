FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN pip install .

CMD ["python", "test/run_tests.py"]
