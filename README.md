# Thingverse-Clone


To-Do's are on the Vikunja-Board below:
https://tasks.mawoka.eu.org/share/vorLlamODyqrtoBcxydxMNEjslRQzarIjnPjqHjU/auth
## Setup
### Requirements
- Redis
- pnpm
- Minio
- (Caddy)

### Configuration
Set the reqiured environment variables found in `example.env` and place them in your `.env` file.

### Start the stack

#### Minio
`docker run -p 9002:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"`
#### TypseSense
`docker run -p 8108:8108 -v/tmp/typesense-data:/data typesense/typesense:0.22.1 --data-dir /data --api-key=1`
#### MongoDB -> TypseSense
`python3 bg.py`
#### Redis
`redis-server`
#### Uvicorn
`uvicorn main:app`

