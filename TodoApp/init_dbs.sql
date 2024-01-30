DROP TABLE IF exists users;
CREATE TABLE users (
	id serial, 
	email VARCHAR NOT NULL, 
	username VARCHAR NOT NULL, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR NOT NULL, 
	hashed_pwd VARCHAR NOT NULL, 
	is_active BOOLEAN, 
	role VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (username)
);
CREATE INDEX ix_users_id ON users (id);
DROP TABLE IF exists todos;
CREATE TABLE todos (
	id serial, 
	title VARCHAR NOT NULL, 
	description VARCHAR, 
	priority INTEGER NOT NULL, 
	complete BOOLEAN, 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
CREATE INDEX ix_todos_id ON todos (id);
