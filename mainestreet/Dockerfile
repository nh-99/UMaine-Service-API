FROM python:2.7
ADD . /app/
WORKDIR /app/
RUN sh install_phantomjs.sh
RUN easy_install flask
RUN python setup.py install
CMD python app/mainestreet.py
