# For å bygge XMJOS-imaget: docker build -t xmjos .


FROM python:latest


WORKDIR /installasjon
# Installasjon av MariaDB Connector/C 
# [https://mariadb.com/docs/skysql/connect/programming-languages/c/install/]
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-11.2.2"
RUN apt install libmariadb3 libmariadb-dev -y
# ----------------


WORKDIR /xmjos
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt
CMD [ "bash","-c","echo -e '\n\n' >> LOGS/error.log; echo --  NY KJØRING $(date +'%d/%m-%Y %H:%M:%S')  -- >> LOGS/error.log; python SKRIPT/main.py 2>>LOGS/error.log"]

