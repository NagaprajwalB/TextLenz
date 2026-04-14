FROM python:3.11.15-trixie
WORKDIR /app
COPY ./src /app
RUN pip install flask
CMD python app.py
EXPOSE 8000