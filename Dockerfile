FROM python:3.15-rc-slim

# Create a virtual environment
RUN python -m venv /opt/venv

# Ensure the virtual environment is used by updating the PATH
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

ENTRYPOINT ["python", "main.py"]