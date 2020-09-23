CREATE USER farm_developer WITH LOGIN CREATEROLE PASSWORD 'developer';
CREATE USER farm_director WITH LOGIN CREATEROLE PASSWORD 'director';
CREATE USER farm_staff WITH LOGIN  PASSWORD 'staff';
CREATE USER farm_client WITH LOGIN  PASSWORD 'client';
CREATE USER farm_guest WITH LOGIN  PASSWORD 'guest';


REVOKE ALL on DATABASE farm FROM farm_developer;
REVOKE ALL ON SCHEMA public FROM farm_developer;

REVOKE CREATE ON SCHEMA public FROM public;
REVOKE ALL ON DATABASE farm FROM public;

grant all PRIVILEGES on schema public to farm_developer;
grant all PRIVILEGES on schema public to farm_director;


GRANT CREATE ON SCHEMA public to farm_developer;

GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, TRIGGER ON ALL TABLES IN SCHEMA public
TO farm_developer;
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, TRIGGER ON ALL TABLES IN SCHEMA public
TO farm_director;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO farm_director;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO farm_developer;

GRANT CONNECT ON DATABASE farm to farm_director;
GRANT CONNECT ON DATABASE farm to farm_developer;
GRANT CONNECT ON DATABASE farm to farm_staff;
GRANT CONNECT ON DATABASE farm to farm_client;
GRANT CONNECT ON DATABASE farm to farm_guest;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE staff
TO farm_guest;

grant select on client_info to farm_staff;

GRANT SELECT ON TABLE client
TO farm_guest;

GRANT SELECT, REFERENCES ON TABLE
	public.subdivision, 
	public.client,
	public.order_,
	public.supply,
	public.product
	TO farm_client;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE 
	public.client,
	public.order_,
	public.supply,
	public.product,
	TO farm_staff;

GRANT SELECT ON TABLE
	public.subdivision, 
	public.order_resource,
	public.staff
	TO farm_staff; 

