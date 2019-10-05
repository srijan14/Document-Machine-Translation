FROM pytorch/pytorch:latest
COPY . /app/
WORKDIR /app
RUN pip install -r /app/OpenNMT-py/requirements.txt && python /app/OpenNMT-py/setup.py install
RUN pip install -r /app/requirements.txt && apt-get install tesseract-ocr libtesseract-dev libleptonica-dev
EXPOSE 5000 5001
ENTRYPOINT ["/app/docker_entrypoint.sh"]