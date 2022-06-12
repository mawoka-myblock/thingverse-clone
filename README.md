# Thingverse-Clone
Pretty much what you guess it'd be, BUT it's far from finished. If you want to work on it, fork it and make me smile by forking it.

As far as I know, user-management is done, among the upload and search of models. The main problem is that this is build with MongoDB, which was the worst decision (for this project).
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

