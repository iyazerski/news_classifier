docker exec rabbitmq bash -c "rabbitmqctl add_vhost dev && rabbitmqctl add_vhost prod"
docker exec rabbitmq bash -c "rabbitmqctl add_user '$1' '$2'"
docker exec rabbitmq bash -c "rabbitmqctl set_permissions -p 'dev' '$1' '.*' '.*' '.*'"
docker exec rabbitmq bash -c "rabbitmqctl set_permissions -p 'prod' '$1' '.*' '.*' '.*'"
