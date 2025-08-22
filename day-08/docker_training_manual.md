# Docker Training Manual

This manual provides a structured and practical introduction to
**Docker**. It covers installation, container lifecycle, image
management, Dockerfiles, building images, and working with real-world
applications using **Node.js** and **Redis**. Each section includes
explanations, notes, and exercises to reinforce learning.

------------------------------------------------------------------------

## 1. Installation of Docker

-   Visit: <https://www.docker.com/get-started/>

-   Follow the instructions based on your operating system (Windows,
    macOS, Linux).

-   Verify installation:

    ``` bash
    docker --version
    docker info
    ```

------------------------------------------------------------------------

## 2. The `docker run` Command

### Part 1: First Run

-   Run your first container:

    ``` bash
    docker run hello-world
    ```

-   Analyze the console output:

    -   Docker checks for the image locally.
    -   If not found, it pulls from Docker Hub.
    -   Executes and prints a message.

Useful commands: - `docker run --help` → Get help on `run` options. -
`docker images -a` → List all downloaded images.

### Part 2: Override Features

-   Examples:

    ``` bash
    docker run busybox echo "hi there!"
    docker run busybox ls -l
    docker run busybox whoami
    docker run busybox top
    ```

-   Each `run` creates a **new container**.

**Question:** Will this work?

``` bash
docker run hello-world echo hi there!
docker run hello-world ls
```

**Answer:** No. The `hello-world` image is built only to print a welcome
message, not to execute custom commands.

------------------------------------------------------------------------

## 3. Listing Running Containers

-   `docker ps` → Show running containers.

-   Example:

    ``` bash
    docker run busybox echo hello
    docker ps   # won’t show it (exited immediately)
    docker run busybox ping google.com
    docker ps   # shows it running
    docker ps -a # shows all containers (running + stopped)
    docker info # system-wide details
    ```

------------------------------------------------------------------------

## 4. Container Lifecycle

-   Create container without starting:

    ``` bash
    docker create hello-world
    ```

-   Start container:

    ``` bash
    docker start -a <id>
    ```

    -   `-a` → attach to console
    -   `-i` → interactive mode

------------------------------------------------------------------------

## 5. Restarting Stopped Containers

-   Example:

    ``` bash
    docker run busybox echo hi there
    docker ps -a
    docker start -a <id>
    ```

-   Container runs again with **original command**.

-   You **cannot override commands** during restart.

Try:

``` bash
docker start -a <id> echo newcommand
```

Will **not** work.

------------------------------------------------------------------------

## 6. Stopping & Removing Containers

-   Clean up system:

    ``` bash
    docker system prune
    ```

-   Removes stopped containers, not images.

------------------------------------------------------------------------

## 7. Logging Outputs

-   Example:

    ``` bash
    docker create busybox echo hi there
    docker start <id>
    docker logs <id>
    ```

-   `docker logs` lets you see output without restarting the container.

------------------------------------------------------------------------

## 8. Stopping Containers

-   Example:

    ``` bash
    docker run busybox ping google.com
    docker ps
    docker stop <id>   # gives 10s grace before stopping
    docker kill <id>   # force stop immediately
    ```

------------------------------------------------------------------------

## 9. Multi-command Containers

-   Run Redis server:

    ``` bash
    docker run redis
    ```

-   In a separate terminal:

    ``` bash
    docker ps
    docker exec -it <id> redis-cli
    ```

-   Test with Redis commands:

        ping
        set key 78
        get key

------------------------------------------------------------------------

## 10. Starting with a Shell

-   Start container with shell access:

    ``` bash
    docker run -it busybox sh
    ```

------------------------------------------------------------------------

## 11. Container Isolation

-   Open two terminals:

    ``` bash
    docker run -it busybox sh
    ```

-   Create a file in each container.

-   Notice: Containers are **isolated**.

------------------------------------------------------------------------

## 12. Inspecting Images

-   Example:

    ``` bash
    docker image inspect redis
    ```

-   Provides JSON with metadata (layers, config, etc.).

------------------------------------------------------------------------

## 13. Removing Images & Containers

-   Remove container:

    ``` bash
    docker rm <container_id>
    ```

-   Remove image:

    ``` bash
    docker rmi -f <image_name>
    ```

------------------------------------------------------------------------

## 14. Docker Images -- Building Custom Images

### Part 1: Building a Redis Image

``` dockerfile
FROM alpine
RUN apk add --update redis
CMD ["redis-server"]
```

-   Build image:

    ``` bash
    docker build .
    docker run <id>
    ```

### Part 2: Build Process

-   Observe temporary layers created during build.

### Part 3: Rebuilds & Caching

-   Adding new steps affects cache.
-   Reordering `RUN` commands changes rebuild efficiency.

### Part 4: Tagging Images

``` bash
docker build -t <your_docker_id>/redis:latest .
```

### Part 5: Docker Commit (manual customization)

-   Not recommended for production.

-   Example:

    ``` bash
    docker run -it alpine sh
    apk add --update redis
    docker commit -c 'CMD "redis-server"' <container_id>
    docker run <new_id>
    ```

------------------------------------------------------------------------

## 15. Practice Project: Simple Web App

### Step 1: App Setup

**package.json**

``` json
{
  "dependencies": { "express": "*"},
  "scripts": { "start": "node index.js"}
}
```

**index.js**

``` js
const express = require("express");
const app = express();

app.get('/', (req, res) => {
    res.send("Hello There");
});

app.listen(8080, () => {
    console.log("Listening on port 8080");
});
```

**Initial Dockerfile** (fails -- alpine has no npm)

``` dockerfile
FROM alpine
RUN npm install
CMD ["npm", "start"]
```

### Step 2: Fixing the Error

-   Use Node base image:

``` dockerfile
FROM node:alpine
WORKDIR /usr/app
COPY ./ ./
RUN npm install
CMD ["npm", "start"]
```

### Step 3: Port Mapping

``` bash
docker build -t simpleweb .
docker run -p 8080:8080 simpleweb
```

-   Access at: <http://localhost:8080>

### Step 4: Rebuilds & Cache Optimization

-   Place `COPY` after dependency installation for faster rebuilds.

------------------------------------------------------------------------

## 16. Docker Compose: Node + Redis

Create `docker-compose.yml`:

``` yaml
version: '3'
services:
  redis-server:
    image: 'redis'
  node-app:
    build: .
    ports:
      - '4040:8081'
```

-   Run with:

    ``` bash
    docker-compose up
    ```

------------------------------------------------------------------------

# ✅ Summary

This manual covered: - Docker basics (`run`, `ps`, lifecycle) - Managing
containers and images - Building custom images with Dockerfile - Running
multi-service applications using **Docker Compose** - A real-world
**Node.js + Redis app** example

------------------------------------------------------------------------

# 🔧 Exercises

1.  Run a `nginx` container and map it to port 8080. Access it via
    browser.
2.  Create a Dockerfile for a Python Flask app and run it.
3.  Modify the Node.js app to serve a JSON API and rebuild.
4.  Use Docker Compose to add a MongoDB service with Node.js.

------------------------------------------------------------------------

End of Docker Training Manual 🚀
