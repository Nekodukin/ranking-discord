FROM gorialis/discord.py:3.9.7-alpine-minimal

WORKDIR /app

COPY . .

CMD ["python", "ranking.py"]
