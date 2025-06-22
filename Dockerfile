FROM python:3.11-slim
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip --timeout 100 \
 && pip install -r requirements.txt --timeout 100
CMD [ "python", "main.py" ]
