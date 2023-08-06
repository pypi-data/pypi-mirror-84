# Cort Python Client

A client for communicating with backend (provider).

## installation

```bash
pip install cort_client
```

## usage

```python
from cort_client import CortClient
from loguru import logger
import time


FILE_SERVER = "http://localhost:20428"

cli = CortClient(
    host="localhost",
    port=20426,
    serial_no="123456F"
)

# refresh a session?
session_id = "YOUR_SESSION_ID"

while True:
    job_id = cli.sync_session(session_id)
    resp = cli.wait_job_until_done(job_id)
    logger.info(resp)
    time.sleep(2)
```

all the apis were designed as same as backend so you can check the backend docs for further details.

```python
job_id = cli.new_session(
    product_name="YOUR_PRODUCT",
    package_name="com.ac.ef",
    version_name="1.0.0",
    hash_name="123456F",
    token="williamfzc",
)
resp = cli.wait_job_until_done(job_id)
```

and use it to upload files:

```python
receiver_cli = CortClient(HOST, RECEIVER_PORT)
data = {
    "productName": PROJECT_NAME,
    "packageName": PACKAGE_NAME,
    "versionName": VERSION_NAME,
    "hashName": HASH_NAME,
    "fileType": "compiled_files",
    "artifactType": "coverage",
}
receiver_cli.upload_artifact(file_path=compiled_zip, **data)
time.sleep(1)

# and .coverage file
# upload cov
data = {
    "productName": PROJECT_NAME,
    "packageName": PACKAGE_NAME,
    "versionName": VERSION_NAME,
    "hashName": HASH_NAME,
    "artifactType": "coverage",
    "userName": "williamfzc",
    "serialNo": "123456F",
}
receiver_cli.upload_cov(file_path=".coverage", **data)
time.sleep(1)
```

## license

MIT
