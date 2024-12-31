FROM python:3.11
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]
