FROM --platform=linux/amd64 python:3.9
RUN apt-get install wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb                         
ENV PATH=/virtualenvs/venv/bin:$PATH     
RUN python -m venv /virtualenvs/venv/       
RUN python -m pip install -U pip setuptools wheel && python -m pip install --use-pep517 --no-cache-dir 'pandas' 'selenium'
COPY . /app                                        
WORKDIR /app                                       
ENTRYPOINT python linkedinn.py
