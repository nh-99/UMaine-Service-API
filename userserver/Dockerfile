FROM python:2.7
ADD . /app/
WORKDIR /app/
RUN easy_install flask
RUN python setup.py install
CMD python app/pinchange.py
