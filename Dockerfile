FROM python:3.7-slim
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-utils \
    firefox-esr \
 && apt autoremove # Reduce image size
LABEL python_version=python
RUN python3 -m venv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app/
# Consider if default --timeout 30 is sufficient
CMD exec gunicorn -b :$PORT main:app
