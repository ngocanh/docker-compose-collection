# docker-compose-collection

A set of compose files I collected through the time.

`*.yml` files are in [.gitignore](.gitignore) if you have to customize compose files to your needs, copy the desired templates and remove the `tmpl` part or create a `override.yml` file and override the values there - such as user/pass etc. the _override.yml_ is automatically picked up by `docker-compose` when you're in the root of this repo.

NOTE: non of these services are any close to _production-ready_!

## Compose Files
* [Oracle B](#oracle-db-singleinstance)
* [Hana eXpress Edition](#hana-express-edition-hxe)
* [MS SQL Server](#ms-sql-server-2017)
* [PHP Apache Dev Stack](#php-apache-dev-stack)

## Oracle DB (SingleInstance)
!NOTE - integration tested with `11.2.0.2 XE` only!

Intention of this docker-compose is to provide a quick way to startup a local development environment with Oracle DB. The need of downloading the binaries and create an image with a separate script is not convenient from my point of view.

More details at [official Oracle docker collection](https://github.com/oracle/docker-images/tree/master/OracleDatabase/SingleInstance).

### Quick Start
1. Copy the directory _[docker-context/scripts/otn-downloader/](docker-context/scripts/otn-downloader)_ to _[docker-context/oracle/DbSingleInstance/dockerfiles/11.2.0.2/](docker-context/oracle/DbSingleInstance/dockerfiles/11.2.0.2)_
2. Create a copy of [docker-compose.override.tmpl.yml](docker-compose.override.tmpl.yml) - you can name it as you like, `override.yml` for example
    * Open the copied _*override.yml*_ and enter your _*[OTN (Oracle Technology Network)](https://www.oracle.com/technetwork/index.html)*_ credentials
3. Start up Oracle DB service
    ```
    docker-compose -f dcc.oracle.tmpl.yml -f override.yml up
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
1. You've to be signed in with your _Docker ID_ (`docker login` or the _whale_ icon) - if you don't have one you can register for free.

    Though Hana XE is free of charge the docker image is distributed through the commercial docker hub, that's why you've to be logged in.
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

## MS SQL Server 2017

Compose file based on https://hub.docker.com/r/microsoft/mssql-server/

### Quick Start
1. Pretty straight forward
    ```
    docker-compose -f dcc.ms-sql.tmpl.yml up
    ```

## PHP Apache Dev Stack

A stack for a quick development setup for PHP

### Quick Start
1. Add `php-dev-stack.loc` to your `/etc/hosts` file and point it to `127.0.0.1`
2. Start up the stack
    ```
    docker-compose -f dcc.php-dev-stack.tmpl.yml up
    ```
3. Open [php-dev-stack.loc](http://php-dev-stack.loc) in your browser to see the result of `phpinfo()`

### Details

The configurations underneath [docker-context/php-dev-stack](docker-context/php-dev-stack) are mounted into the service containers

* Apache and site config
* MySQL / MariaDB [my.cnf](docker-context/php-dev-stack/mysql/my.cnf)
* [php.ini](docker-context/php-dev-stack/php/php.ini)
* [index.php](docker-context/php-dev-stack/html_dir/index.php) used as demonstration and it's printing the PHP settings

This way the configs can be easily changed on the host system.

What you probably wanna do is mounting your source code into the `php-apache` container, by default the Apache in this container serves from `/var/www/html`. To do so open your compose file, navigate to the `php-apache` service and look for the `volume` section

```yaml
    ...
    volumes:
      ...
      # mount your source code to /var/www or /var/www/html
      # NOTE: if your host is not a linux machine the FS performance is really bad if the amount of files is high!
      - ./docker-context/php-dev-stack/html_dir:/var/www/html
      ...
```

and replace `./docker-context/php-dev-stack/html_dir` with the path of your source code.

To use

## Advanced usage

* Start multiple services (Oracle DB, HXE, MS SQL in this example)
    ```
    docker-compose -f dcc.oracle.tmpl.yml -f dcc.hana-xe.tmpl.yml -f dcc.ms-sql.tmpl.yml -f override.yml up
    ```
    Or you can of course assemble a compose file with all the services you need (like [dcc.php-dev-stack.tmpl.yml](dcc.php-dev-stack.tmpl.yml)).