FROM python:3.11-slim
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]
