aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 099104132944.dkr.ecr.us-west-2.amazonaws.com




docker build . --build-arg entity=guadalajara -t guadalajara:latest
docker tag guadalajara:latest 099104132944.dkr.ecr.us-west-2.amazonaws.com/guadalajara:latest
docker push 099104132944.dkr.ecr.us-west-2.amazonaws.com/guadalajara:latest
