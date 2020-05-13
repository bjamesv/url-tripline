FROM python:3.7-slim
RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y firefox-esr
LABEL python_version=python
RUN python3 -m venv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN apt-get install -y x11-utils
RUN apt autoremove
RUN apt clean
ADD . /app/
WORKDIR /app
# Consider if default --timeout 30 is sufficient
CMD exec gunicorn -b :$PORT main:app
