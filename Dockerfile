FROM python:3.8.12-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=80
# Copy local code to the container image.
WORKDIR /birb_android
COPY . /birb_android
EXPOSE $PORT
# Install production dependencies.
RUN apt-get update; apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pwd; ls

#CMD exec uvicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 webhook:app
CMD exec uvicorn birb_backend:app --port $PORT --host "0.0.0.0"
