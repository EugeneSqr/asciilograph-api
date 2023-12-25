# running the server
```bash
docker build -t asciilograph-api .
docker run -it --rm --volume ./app:/usr/src/app --publish 8000:8000 --name asciilograph-api asciilograph-api
```
