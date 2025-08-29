# 🐳 Docker Compose YAML Tutorial & Cheat Sheet

Docker Compose allows you to define and manage **multi-container Docker
applications** using a simple YAML configuration file
(`docker-compose.yml`).\
This tutorial explains the structure, key specifications, and serves as
a cheat sheet.

------------------------------------------------------------------------

## 📌 What is Docker Compose?

-   A tool to define and run multi-container Docker applications.
-   Configuration is stored in `docker-compose.yml`.
-   One command (`docker-compose up`) starts the entire application
    stack.

------------------------------------------------------------------------

## 📂 Basic Structure of `docker-compose.yml`

``` yaml
version: "3.9"  # Docker Compose file format version

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
```

------------------------------------------------------------------------

## 🏗️ Key Sections in Docker Compose YAML

### 1. **version**

Specifies the Docker Compose file format. - Common versions: `"2"`,
`"3"`, `"3.8"`, `"3.9"`.

### 2. **services**

Defines the containers (services) that make up your app.

Example:

``` yaml
services:
  app:
    image: myapp:latest
```

### 3. **build**

Used to build an image from a Dockerfile.

``` yaml
services:
  app:
    build: ./app
```

### 4. **image**

Specifies the image to use for the container.

``` yaml
image: nginx:alpine
```

### 5. **ports**

Maps container ports to host ports.

``` yaml
ports:
  - "8080:80"
```

### 6. **volumes**

Mounts directories or named volumes.

``` yaml
volumes:
  - ./data:/var/lib/mysql
```

### 7. **environment**

Sets environment variables inside the container.

``` yaml
environment:
  MYSQL_ROOT_PASSWORD: rootpass
  MYSQL_DATABASE: mydb
```

### 8. **depends_on**

Defines service dependencies (startup order).

``` yaml
depends_on:
  - db
```

### 9. **networks**

Defines custom networks for services.

``` yaml
networks:
  mynetwork:
    driver: bridge
```

### 10. **restart**

Specifies restart policy.

``` yaml
restart: always
```

------------------------------------------------------------------------

## 📝 Example: Multi-Service Application

``` yaml
version: "3.9"

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    depends_on:
      - app

  app:
    build: ./app
    volumes:
      - .:/usr/src/app
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - dbdata:/var/lib/postgresql/data

volumes:
  dbdata:
```

------------------------------------------------------------------------

## ⚡ Cheat Sheet

  Key             Description                   Example
  --------------- ----------------------------- -----------------------------
  `version`       File format version           `version: "3.9"`
  `services`      Define containers             `services: web, db`
  `build`         Build image from Dockerfile   `build: ./app`
  `image`         Use prebuilt image            `image: nginx:alpine`
  `ports`         Port mapping                  `"8080:80"`
  `volumes`       Data persistence              `./data:/var/lib/mysql`
  `environment`   Environment variables         `MYSQL_ROOT_PASSWORD: pass`
  `depends_on`    Service dependencies          `depends_on: - db`
  `networks`      Custom networks               `driver: bridge`
  `restart`       Restart policy                `always`, `unless-stopped`

------------------------------------------------------------------------

## 🚀 Running Docker Compose

1.  Start containers:

    ``` bash
    docker-compose up
    ```

2.  Start in detached mode:

    ``` bash
    docker-compose up -d
    ```

3.  Stop containers:

    ``` bash
    docker-compose down
    ```

4.  View logs:

    ``` bash
    docker-compose logs -f
    ```

------------------------------------------------------------------------

✅ With this guide, you can now **create, configure, and manage
multi-container apps** using Docker Compose!
