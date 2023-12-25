# running the server
```bash
docker build -t asciilograph-api .
docker run -it --rm --volume ./main.py:/usr/src/app/main.py --publish 8000:8000 --name asciilograph-api asciilograph-api
```
