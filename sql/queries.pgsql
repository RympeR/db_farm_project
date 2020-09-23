4.2  Получить список клиентов, которые потратили наибольшую сумму в каждом виде продукции.

WITH client_costs AS
(SELECT product_id, client_id,
 RANK() OVER (PARTITION BY product_id ORDER BY SUM(supply.product_count * supply.product_price) DESC) AS cost_rank
 FROM product 
 JOIN supply USING(product_id)
 JOIN order_ USING (order_id)
 JOIN client USING(client_id)
 GROUP BY product_id, client_id
)

SELECT p.product_id, product_name,
c.client_id, first_name||' '||last_name as client_name
FROM product P
JOIN client_costs CC ON (P.product_id = CC.product_id)
JOIN client C ON ( C.client_id = CC.client_id)
WHERE CC.cost_rank = 1
ORDER BY p.product_id, c.client_id



4.1 Создать представление, формирующее список продуктов с указанием рейтинга (места) при ранжировании по:
– количеству сотрудников, занятых в соответствующих подразделениях;
– затратам на корма; 
– среднегодовому доходу от их продажи.

CREATE OR REPLACE VIEW product_rating AS 

WITH StaffDivision AS 
(SELECT subdivision_id, COUNT(staff_id)
FROM subdivision
JOIN staff USING(subdivision_id)
GROUP BY subdivision_id),

AvgRevenue AS
(SELECT product_id,
ROUND(SUM(supply.product_count*supply.product_price)
    / count(distinct EXTRACT (YEAR FROM order_.date_)), 2) as avg_revenue
FROM product
JOIN supply USING (product_id)
JOIN order_ USING(order_id)
GROUP BY product_id)

SELECT product_id, product_name, 
SD.count AS staff_count,
DENSE_RANK() OVER (ORDER BY SD.count DESC) AS staff_count_rate,
P.required_feed,
DENSE_RANK() OVER (ORDER BY P.required_feed DESC) AS feed_rate,
AR.avg_revenue,
DENSE_RANK() OVER (ORDER BY AR.avg_revenue DESC) AS avg_rev_rate
FROM product P 
JOIN StaffDivision SD USING(subdivision_id)
JOIN AvgRevenue AR USING(product_id)



-----------------------
create TABLE users(
    login text PRIMARY KEY,
    password text not NULL,
    role text not null
);
--client
SELECT subdivision_id, addres, chief_first_name || ' ' || chief_last_name as chief from subdivision
                        where city = '{city}'


SELECT product_price, quanity_of_produced from product
    JOIN subdivision USING (subdivision_id)
    WHERE product_name = 'Здоровье'

SELECT product_id, product_name, product_type, subdivision_id, product.product_price, quanity_of_produced
from client
    JOIN order_ USING(client_id)
    JOIN supply USING(order_id)
    JOIN product USING(product_id)
    JOIN subdivision USING(subdivision_id)
    WHERE client_id = 1
	and order_.date_ between '2019-10-10' and '2020-12-20';

--staff

--staff
INSERT INTO client(last_name, first_name, mobile_number, adress_of_client)
    values('', '', '' ,'')

UPDATE client
    set
        ....

SELECT product_id, product_name, product_type,
        subdivision_id, product_price
        from product
        JOIN subdivision USING(subdivision_id)
        WHERE product_name='Счастье'

drop view client_info
CREATE OR REPLACE VIEW client_info as
    SELECT client_id, client.first_name, client.last_name,
        client.adress_of_client, product_name, product_type
        from client
        JOIN order_ USING(client_id)
        JOIN supply USING(order_id)
        JOIN product USING(product_id)
    GROUP BY 2, 3, 4, 5, 1, 6

SELECT * from client_info WHERE client_id=1

SELECT product_id, product_name, product_type, subdivision_id, product.product_price,
        quanity_of_produced, sum(product_count) as sold_amount
    from product
    JOIN supply USING(product_id)
    JOIN order_ USING(order_id)
    JOIN subdivision USING(subdivision_id)
    WHERE product_date between '2019-10-10' and '2020-12-20'
	GROUP by 1, 2, 3, 4, 5, 6
    

--director
INSERT INTO Staff(First_name, Last_name, Phone_number, Work_role, Quantity_of_products_produced, Salary, Subdivision_ID, Adress, cheese_equipment, milk_equipment)
 values('Виктор','Муркин','380960403212','2','15','3550','2','Прохоровская, 5','false','true'),

UPDATE staff
    set
        ....

DELETE from staff
    where staff_id = 1;

SELECT staff_id, last_name || ' ' || first_name as fio, chief_first_name || ' ' || chief_last_name as chief_fio, quantity_of_products_produced 
    from staff
    join subdivision using(subdivision_id)
    where staff_id = 1

select chief_first_name || ' ' || chief_last_name as chief_fio, product_type, quanity_of_produced, sum(product_count) as sold_amount
    from subdivision
        join product USING(subdivision_id)
        join supply USING(product_id)
    where addres = 'fontan 1a'
    GROUP by 1,2,3

