wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=<project_name>:asia-east1:<connection_name>=tcp:localhost:<port> -credential_file=./gcloud-sql-admin.json

