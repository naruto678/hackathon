
create table if not exists projects (
	id integer primary key,
	name text not null,
    description text not null, 
    project_link text null, 
    business_tags text not null
);

-- delim 
create table if not exists users(
    id integer primary key, 
    name text not null, 
    email text not null unique,  
    hashed_password text not null,  
    is_logged_in integer default 0
); 



