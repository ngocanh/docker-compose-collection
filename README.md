# docker-compose-collection

## Oracle DB (SingleInstance)
!NOTE - integration tested with _*11.2.0.2 XE*_ only!

Intention of this docker-compose is to provide a quick way to startup a local development environment with Oracle DB.

More details at [official Oracle docker collection](https://github.com/oracle/docker-images/tree/master/OracleDatabase/SingleInstance).

### Quick Start
1. Copy the directory _'[docker-context/scripts/otn-downloader/](docker-context/scripts/otn-downloader)'_ to _'[docker-context/oracle/DbSingleInstance/dockerfiles/11.2.0.2/](docker-context/oracle/DbSingleInstance/dockerfiles/11.2.0.2)'_
2. Create a copy of [docker-compose.override.tmpl.yml](docker-compose.override.tmpl.yml) - you can name it as you like, _*docker-compose.override.yml*_ for example
    * Open the copied _*docker-compose.override.yml*_ and enter your _*OTN*_ [Oracle Technology Network](https://www.oracle.com/technetwork/index.html) credentials
3. Start up the service(s)
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