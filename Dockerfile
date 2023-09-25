# Dockerfile, Image, Container
FROM python:3.10

ADD main.py .
RUN pip install pip install discord.py
RUN pip install selenium
RUN pip install beautifulsoup4

CMD ["python", "./main.py"]