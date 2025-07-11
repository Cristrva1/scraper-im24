FROM selenium/standalone-chrome:123.0
USER root
COPY requirements.txt /tmp/req.txt
RUN pip install --no-cache-dir -r /tmp/req.txt
COPY src/ /src/
WORKDIR /src
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "runner.py"]
1~FROM selenium/standalone-chrome:123.0
USER root
COPY requirements.txt /tmp/req.txt
RUN pip install --no-cache-dir -r /tmp/req.txt
COPY src/ /src/
WORKDIR /src
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "runner.py"]
