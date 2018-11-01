# docker-compose-collection

## Oracle DB (SingleInstance)
!NOTE - integration tested with _*11.2.0.2 XE*_ only!

Intention of this docker-compose is to provide a quick way to startup a local development environment with Oracle DB.

More details at [official Oracle docker collection](https://github.com/oracle/docker-images/tree/master/OracleDatabase/SingleInstance).

### Quick Start
1. Copy the directory _[docker-context/scripts/otn-downloader/](docker-context/scripts/otn-downloader)_ to _[docker-context/oracle/DbSingleInstance/dockerfiles/11.2.0.2/](docker-context/oracle/DbSingleInstance/dockerfiles/11.2.0.2)_
2. Create a copy of [docker-compose.override.tmpl.yml](docker-compose.override.tmpl.yml) - you can name it as you like, _*docker-compose.override.yml*_ for example
    * Open the copied _*docker-compose.override.yml*_ and enter your _*[OTN (Oracle Technology Network)](https://www.oracle.com/technetwork/index.html)*_ credentials
3. Start up Oracle DB service
    ```
    docker-compose -f dcc.oracle.tmpl.yml -f docker-compose.override.yml up
    ```
    Wait until you'll see

    ```
    #########################
    DATABASE IS READY TO USE!
    #########################
	```
	You can do a quick check by opening [APEX](http://localhost:8080/apex/)

## Hana eXpress Edition (HXE)

docker-compose file based on [official documentation](https://www.sap.com/developer/tutorials/hxe-ua-install-using-docker.html) of using Hana XE with docker

### Quick Start
1. You've to be signed in with your _Docker ID_ - if you don't have you can register for free.

    Though Hana XE free of charge the docker image is distributed through the commercial docker hub, that's why you've to be logged in.
2. Start up Hana XE DB service
    ```
    docker-compose -f dcc.hana-xe.tmpl.yml up
    ```
3. The image weights over 3GB and the initialization will take some time, go and get a :coffee:.

    When HXE is ready, check its status
    ```
    docker exec -it dcc_hana-xe_1 'HDB info'
    ```
    If it fails, exec as root and full login shell
    ```
    docker exec -it -u root dcc_hana-xe_1 su - hxeadm -c 'HDB info'
    ```
    The container name _'dcc_hana-xe_1' might_ be different for you, if so check for its ID/name with `docker ps -a`

## Advanced usage

* Start multiple services (Oracle DB, HXE, MS SQL in this example)
    ```
    docker-compose -f dcc.oracle.tmpl.yml -f dcc.hana-xe.tmpl.yml -f dcc.ms-sql.tmpl.yml -f docker-compose.override.yml up
    ```
    Or you can of course assemble a compose file with all the services you need.