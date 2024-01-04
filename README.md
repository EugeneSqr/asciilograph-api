# start the server
```bash
docker build -t asciilograph-api .
docker run -it --rm --volume ./app:/usr/src/app --publish 8000:8000 --name asciilograph-api asciilograph-api
```

# run lint checks
```bash
docker exec -it asciilograph-api ./run_lint
```

# convert to ascii
```bash
curl -X POST 'http://localhost:8000/ascii_arts' --data-binary '@/home/eugenesqr/Downloads/test.jpg'
```
