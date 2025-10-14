FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8050
CMD ["python", "umt_dashboard.py"]