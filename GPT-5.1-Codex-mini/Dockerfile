FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
CMD ["sh", "run_tests.sh"]
