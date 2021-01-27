FROM python:3.6-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit","run"]
CMD dashboard.py --server.port $PORT