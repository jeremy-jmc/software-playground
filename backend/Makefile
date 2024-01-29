include Makefile.variable

build:
	sudo chmod 666 /var/run/docker.sock
	docker build -t $(IMAGE_NAME) -f ./Dockerfile .
up:
# emulate a e2-highcpu-2 machine (2 vCPUs, 2 GB memory)
# emulate a e2-micro machine (2 vCPUs, 1 GB memory)
	docker run -it --cpus=2 --memory=2g -p 8000:$(TO_PORT) $(IMAGE_NAME)
down:
	docker stop $(IMAGE_NAME)
	docker rm $(IMAGE_NAME)
stress:
# https://www.inmotionhosting.com/support/edu/wordpress/performance/stress-test-with-apachebench/
	sudo apt install apache2-utils -y
	ab -n 10000 -c 100 -g test.txt http://localhost:$(TO_PORT)/
clean:
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name 'node_modules' -type d -exec rm -rf {} +
	find . -name '.next' -type d -exec rm -rf {} +
# find . -name 'venv' -type d -exec rm -rf {} +
	rm -f *.pyc
	rm -f *.pyo
	rm -f *~
	docker ps -a --format "{{.Names}}" | grep "healer-" | xargs docker stop | xargs docker rm || true
	docker ps -a --filter "ancestor=$$(docker images -f "dangling=true" -q)" -q | xargs docker rm || true
	docker rmi $$(docker images --filter "dangling=true" -q) || true
	docker images
	docker system prune -a