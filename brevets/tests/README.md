# Nose tests #

Jump into your container and run `./run_tests.sh`.

```shell
docker-compose exec <your_service> bash 
```

Note that you should not enter the tests directory, `run_tests.sh` will take care of everything. 


For example on project 5 we first build the program in a detatched mode then we:


`docker-compose exec brevets bash`


then:

`./run_tests.sh`

