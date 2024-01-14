# Cache Service

To build:
```
docker-compose -f docker-compose.yml build
```

To run:
```
docker run -p 80:3030 -t docker-dashcache:latest
```

Or in case of using docker-compose file to run the container:
```
docker-compose -f docker-compose.yml up
```


Send prefetching file
```
curl -X POST 127.0.0.1:30001/prefetching -H 'Content-Type: application/json' -d "@metadata.json"
```

