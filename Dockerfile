FROM jjanzic/docker-python3-opencv:latest
RUN ["pip", "install", "web.py"]
RUN ["apt", "update"]
RUN ["apt", "install", "python3-opencv", "-y"]
COPY . ./app/
WORKDIR /app/
EXPOSE 8080
# CMD ["python", "Start.py", "-f './Data/IMG_20201216_185903.jpg'"]
CMD ["python", "./Server.py"]