FROM python:3.11-buster AS builder


COPY requirements.txt /requirements.txt
COPY dev-reqs.txt /dev-reqs.txt
RUN pip install --user -r dev-reqs.txt


FROM python:3.11-slim


COPY --from=builder /root/.local /root/.local


ENV MPLBACKEND=Agg

ENV DISCORD=NTMyMDQ1MjAwODIzMDI1NjY2.XDQftA.Px-arL5wDMB4XKcoPOS1r4gCGmA
ENV MARKETDATA=a01mVUZ4cW1sUUFOVWlEZ3NNTHFNeHYzS2diUUhTUVJZbzNxVVEwTUxVMD0

COPY . .

# CMD [ "python", "./bot.py" ]
