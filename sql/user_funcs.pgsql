--5.2 Составить триггер для блокирования продажи отсутствующей продукции.

CREATE OR REPLACE FUNCTION Check_Amount() RETURNS TRIGGER AS $$
DECLARE
  produced_amount NUMERIC:=0;
  sold_amount NUMERIC:=0;
  SubdivisionId subdivision.subdivision_id%TYPE;
BEGIN
  SELECT subdivision_id INTO SubdivisionId
  FROM product
  WHERE product_id = NEW.product_id;

  SELECT quanity_of_produced INTO produced_amount
  FROM subdivision
  WHERE subdivision_id = SubdivisionId;
  
  SELECT SUM(product_count) INTO sold_amount
  FROM product
  JOIN supply USING(product_id)
  WHERE subdivision_id = SubdivisionId;
  
  IF(produced_amount < sold_amount + NEW.product_count)
    THEN RAISE EXCEPTION 'Недостаточное количество продукции';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER NewSupply
BEFORE INSERT OR UPDATE ON supply
FOR EACH ROW EXECUTE PROCEDURE Check_Amount();



-- 5.1 Создать хранимую процедуру для формирования предварительного заказа на корма для конкретной продукции
-- на следующий год (как прогноз на основании прошлогоднего и перспективного соотношения «объём кормов» / «объём проданной продукции»).
-- Название продукции передавать, как параметр.

CREATE OR REPLACE FUNCTION Create_Res_Order(ProductName product.product_name%TYPE) RETURNS VOID AS $$
DECLARE
  RequiredFeed  product.required_feed%TYPE:=0;
  SoldAmount NUMERIC:=0;
  SubdivisionID subdivision.subdivision_id%TYPE;
  AvgPrice order_resource.resource_price%TYPE;
BEGIN
  SELECT required_feed, subdivision_id
  INTO RequiredFeed,SubdivisionID
  FROM product
  WHERE product_name = ProductName;
  
  SELECT AVG(resource_price) INTO AvgPrice
  FROM order_resource 
  WHERE subdivision_id = SubdivisionID
  AND resource_type = 'корм';
  
  SELECT SUM(product_count) 
  INTO SoldAmount
  FROM supply
  JOIN product USING(product_id)
  JOIN order_ USING (order_id)
  WHERE product_name = ProductName
  AND order_.date_ BETWEEN CURRENT_DATE - INTERVAL '1 year' AND CURRENT_DATE;
  
  INSERT INTO order_resource (resource_type, resource_price, subdivision_id, resource_count) 
   VALUES ('корм',AvgPrice,SubdivisionID,SoldAmount*RequiredFeed*1.1); 
  
END;
$$ LANGUAGE plpgsql;


-----------USER STORY------------------------------
--1.Сотрудник
--добавление клиента в базу
DROP FUNCTION insert_new_client;
CREATE OR REPLACE FUNCTION insert_new_client(last_name_client varchar, first_name_client varchar,
   mobile_number_client varchar, adress_of_client_client varchar, login_client varchar, passw_client varchar) RETURNS INT AS $$
  
  INSERT INTO client(last_name, first_name, mobile_number, adress_of_client, login, passw) VALUES
      (last_name_client, first_name_client, mobile_number_client, adress_of_client_client, login_client, passw_client);
  SELECT max(client_id)  FROM client;
$$LANGUAGE sql;
--редактирование клиента в базе
DROP FUNCTION update_client;
CREATE OR REPLACE FUNCTION update_client(last_name_client varchar, first_name_client varchar,
   mobile_number_client varchar, adress_of_client_client varchar) RETURNS VOID AS $$
  UPDATE client
    set 
      client.first_name = first_name_client,
      client.last_name = last_name_client,
      client.mobile_number = mobile_number_client,
      client.adress_of_client = adress_of_client_client
    WHERE
      client.first_name = first_name_client AND
      client.last_name = last_name_client
$$ LANGUAGE sql;

--просмотр клиента
SELECT * from client_info WHERE last_name = '' and first_name = '';

--
drop FUNCTION check_product;
CREATE OR REPLACE FUNCTION check_product(name_product text) RETURNS
  TABLE (product_id int, product_name varchar, product_type varchar,
        subdivision_id int, product_price numeric)
as $$
SELECT product_id, product_name, product_type,
        subdivision_id, product_price
        from product
        JOIN subdivision USING(subdivision_id)
        WHERE product_name=name_product;
$$ language sql;

select * from check_product('Счастье');

drop FUNCTION if EXISTS sold_product;
CREATE OR REPLACE FUNCTION sold_product(begin_date date, end_date date) 
RETURNS TABLE
    (product_id int, product_name varchar, product_type varchar, subdivision_id int, product_price numeric,
        quanity_of_produced numeric, sold_amount numeric)
AS $$
  SELECT product_id, product_name, product_type, subdivision_id, product.product_price,
        quanity_of_produced, sum(product_count) as sold_amount
    from product
    JOIN supply USING(product_id)
    JOIN order_ USING(order_id)
    JOIN subdivision USING(subdivision_id)
    WHERE product_date between begin_date and end_date
	GROUP by 1, 2, 3, 4, 5, 6

$$ LANGUAGE SQL;

select * from sold_product('2019-10-10', '2020-12-20');

--client

drop FUNCTION if EXISTS client_bought_product;
CREATE OR REPLACE FUNCTION client_bought_product(begin_date date, end_date date, c_login varchar) 
RETURNS TABLE
    (product_id int, product_name varchar, product_type varchar, subdivision_id int, product_price numeric,
        product_count numeric)
AS $$
  SELECT product.product_id, product.product_name, product.product_type, subdivision.subdivision_id, product.product_price, supply.product_count
  from client
      JOIN order_ USING(client_id)
      JOIN supply USING(order_id)
      JOIN product USING(product_id)
      JOIN subdivision USING(subdivision_id)
      WHERE client.first_name=(select first_name from client where login=c_login) and client.last_name=(select last_name from client where login=c_login)
    and order_.date_ between begin_date and end_date;
$$ LANGUAGE sql;

select * from client_bought_product('2019-10-10', '2020-12-20', 'c1');

SELECT subdivision_id, addres, chief_first_name || ' ' || chief_last_name as chief from subdivision
                        where city = '{city}'


SELECT product_price, quanity_of_produced from product
    JOIN subdivision USING (subdivision_id)
    WHERE product_name = 'Здоровье'

--director


--добавление сотрудника в базу
INSERT INTO Staff(First_name, Last_name, Phone_number, Work_role, Quantity_of_products_produced, Salary, Subdivision_ID, Adress, cheese_equipment, milk_equipment, login, passw, role_)
 values('','','','','','','','','','', '', '', '');

--редактирование сотрудника в базе
UPDATE staff
  set
    First_name = {},
    Last_name = {},
    Phone_number = {},
    Work_role = {},
    Quantity_of_products_produced = {},
    Salary = {},
    Subdivision_ID = {},
    Adress = {},
    cheese_equipment = {},
    milk_equipment= {},
    login = {},
    passw = {},
    role_ = {}
  where staff_id = {id}
--удаление сотрудника
DELETE from staff
    where staff_id = 1;
--активность сотрудника
SELECT staff_id, last_name || ' ' || first_name as fio, chief_first_name || ' ' || chief_last_name as chief_fio, quantity_of_products_produced 
    from staff
    join subdivision using(subdivision_id)
    where staff_id = 1
--активность подразделения
select chief_first_name || ' ' || chief_last_name as chief_fio, product_type, quanity_of_produced, sum(product_count) as sold_amount
    from subdivision
        join product USING(subdivision_id)
        join supply USING(product_id)
    where addres = 'fontan 1a'
    GROUP by 1,2,3
--редактирование зарплаты
UPDATE staff
  set salary = {salary}
  WHERE staff_id = {id};
--добавление подразделения
INSERT INTO subdivision(chief_first_name, chief_last_name,city, quanity_of_produced, addres) 
  VALUES('', '', '', 123, '')
--обновление подразделения
UPDATE subdivision
  SET
    chief_first_name = {},
    chief_last_name = {},
    city = {},
    quanity_of_produced = {},
    addres = {}
WHERE subdivision_id = {id};
--удаление подразделения
delete from subdivision
  where subdivision_id = {id};