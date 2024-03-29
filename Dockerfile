FROM python:3.11-buster AS builder


COPY requirements.txt /requirements.txt
RUN pip install --user -r requirements.txt


FROM python:3.11-slim

ENV MPLBACKEND=Agg

COPY --from=builder /root/.local /root/.local


COPY . .

CMD [ "python", "./bot.py" ]