FROM gcr.io/google-appengine/python
RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y firefox
LABEL python_version=python
RUN virtualenv --no-download /env -p python3
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
RUN pip install -r requirements.txt
RUN apt-get install -y x11-utils
ADD . /app/
# Consider if default --timeout 30 is sufficient
CMD exec gunicorn -b :$PORT main:app
