# capstione-project-intern
This is a project in which the skills learned at intership as a DevOps engineer are reflected. It contains a FastAPI web application, with a nginx web server for the python backend and a postgres database for data persistence.

To run it locally it is needed to start in the following order:

### 1. Run DB
1. Start minikube service by typing:
    ```bash
    bash minikube start
    ```
2. Mapping into [interns-db](https://github.com/jnavarro447/capstione-project-intern/tree/main/interns-db) folder. 
   Then, mount on the data directory from this same repo. <br/>
    ```bash
    cd data
    DIR=$(pwd)
    minikube mount $DIR:$DIR
    ```
3. Deploy kubernetes services and deployment.
    ```bash
    kubectl apply -f .
    ```
    
### 2. Run backend API
4. Mapping into [interns-backend-api](https://github.com/jnavarro447/capstione-project-intern/tree/main/interns-backend-api) folder.
5. Build a local iamge with the backend api code.
    ```bash
    minikube image build -t internes-backend-container .
    ```
6. Deploy kubernetes services and deployment.
    ```bash
    kubectl apply -f .
    ```

### 3. Run webserver
7. Mapping into [interns-webserver](https://github.com/jnavarro447/capstione-project-intern/tree/main/interns-webserver) folder.
8. Deploy kubernetes services and deployment.
    ```bash
    kubectl apply f .
    ```
9. Run a port forward to expose a port on your local
    ```bash
    kubectl port-forward service/nginx 8080:80
    ```


