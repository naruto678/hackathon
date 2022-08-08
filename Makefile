

create_db:
	python manager.py create-db 
start_server: 
	python app.py start-server 4000
clean_db: 
	python app.py clean-db 
drop_db: 
	python app.py drop-db
stop_server:
	python app.py stop-server 

build-dep: 
	echo "To be done later"
