FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 4444
ENTRYPOINT ["python"]
CMD ["main.py"]