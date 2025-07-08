# my-python-app
docker run -d   -p 0.0.0.0:5000:5000   --restart=always   --name registry   registry:2
docker build -t localhost:5000/my-python-app:latest .
docker push localhost:5000/my-python-app:latest
