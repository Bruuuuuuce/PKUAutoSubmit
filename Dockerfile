FROM ubuntu:latest

RUN apt-get -qq update && apt-get -qq -y install curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && apt-get -qq -y remove curl bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes

ENV PATH /opt/conda/bin:$PATH

WORKDIR /workspace

ADD main.py /workspace/main.py
ADD entrypoint.sh /workspace/entrypoint.sh
ADD phantomjs/phantomjs-linux-x86_64 /workspace/phantomjs/phantomjs-linux-x86_64
RUN conda create -n workenv python selenium -c conda-forge --yes
# RUN conda create -n workenv python selenium firefox geckodriver -c conda-forge --yes

ENTRYPOINT [ "/workspace/entrypoint.sh" ]
