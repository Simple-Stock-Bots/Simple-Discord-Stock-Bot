FROM python:3.9-buster AS builder


COPY requirements.txt /requirements.txt
RUN pip install --user -r requirements.txt


FROM python:3.9-slim

ENV MPLBACKEND=Agg

COPY --from=builder /root/.local /root/.local

# Formatting
RUN pip install --no-cache-dir black
# Jupyter Notebooks
RUN pip install --no-cache-dir ipykernel

ENV DISCORD=TOKEN
ENV IEX=TOKEN

COPY . .

# CMD [ "python", "./bot.py" ]
