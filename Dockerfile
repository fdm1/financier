FROM fdm1/base_python_dev:python3
ADD . /financier
WORKDIR /financier
# RUN pip3 install -r requirements.txt
ARG config_yaml
ADD tmp/$config_yaml /config/
RUN echo $config_yaml
CMD bash
