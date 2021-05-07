env_vars = $(python3 export_env_vars.py 2>&1)

eb create --scale=1 --database.username=postgres --database.password=password \
    --database.engine=postgres --database.instance=db.t2.micro --envvars $env_vars