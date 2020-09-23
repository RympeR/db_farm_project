CREATE TABLE Subdivision(
 Subdivision_ID SERIAL PRIMARY KEY,
 Chief_first_name VARCHAR(50) NOT NULL,
 Chief_last_name VARCHAR(50) NOT NULL,
 Street VARCHAR(100) NOT NULL,
 Quanity_of_produced NUMERIC(10)
);
CREATE TABLE Proffesion(
 Proffesion_ID SERIAL PRIMARY KEY,
 Name_of_prof VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE Client(
 Client_ID SERIAL PRIMARY KEY ,
 Last_name VARCHAR(50) NOT NULL,
 First_name VARCHAR(50) NOT NULL,
 Mobile_number CHAR(12) UNIQUE,
 Adress_of_Client VARCHAR(50) NOT NULL 
);
CREATE TABLE Staff(
 Staff_ID SERIAL PRIMARY KEY,
 Last_name VARCHAR(50) NOT NULL,
 First_name VARCHAR(50) NOT NULL,
 Phone_number CHAR(12) UNIQUE,
 Work_role INT NOT NULL references Proffesion(Proffesion_ID) ,
 Salary NUMERIC(7,2) NOT NULL,
 Quantity_of_products_produced NUMERIC(10),
 Subdivision_ID INT NOT NULL references Subdivision(Subdivision_ID),
 Adress VARCHAR(50) NOT NULL,
  cheese_equipment boolean not null,
  milk_equipment boolean not null
);
CREATE TABLE Product(
 Product_ID SERIAL PRIMARY KEY,
 Product_Kind VARCHAR(50) NOT NULL CHECK(Product_Kind IN('Стерилизованное','Не стерилизованное','Твердый','Мягкий','Плавленный')),
 Product_Name VARCHAR(50) NOT NULL,
 Product_Price NUMERIC(10,2) NOT NULL,
 Product_Type VARCHAR(50) NOT NULL CHECK(Product_Type IN('Молоко','Сыр')),
 Subdivision_ID INT NOT NULL references Subdivision(Subdivision_ID),
 description varchar (100) not null,
  product_date date not null,
  required_feed numeric(10) not null,
  required_fuel numeric (10) not null,
  required_med numeric (10) not null
);

CREATE TABLE Order_(
 Order_ID SERIAL CHECK(Order_ID>0) PRIMARY KEY,
 Date_ DATE NOT NULL,
 Client_ID INT NOT NULL references Client(Client_ID)
);
CREATE TABLE Supply(
 Order_ID SERIAL references Order_(Order_ID),
 Product_ID INT references Product(Product_ID),
 Product_Price NUMERIC(10,2) NOT NULL,
 Product_Count NUMERIC(10) NOT NULL,
 PRIMARY KEY(Order_ID, Product_ID)
);


INSERT INTO Proffesion(Name_of_prof)
 values('Сыровар'),('Доярка'),('Молочник'),('Кладовщик');

INSERT INTO Subdivision(Street, Chief_first_name,Chief_last_name, Quanity_of_produced)
 values('Левитана 51', 'Андрей','Краснопольский','100'),
 ('Пенная 32', 'Николай', 'Харитонов','150'),
 ('Пенная 1', 'Олег', 'Полеев','120');
 
INSERT INTO Client(First_name, Last_name, Mobile_number, Adress_of_Client)
 values('Инна','Попова','380503319782','Дерибасовская, 32'),
 ('Михаил','Копиевский','380933328282','Успенская, 32'),
 ('Екатерина','Стоичкова','380503317654','Успенская, 32'),
 ('Ваган','Авагян','380509876543','Фонтанская дорога, 58'),
 ('Роман','Чермаш','380991234567','Балковская, 1'),
 ('Иван','Петров','380991996934','Балковская, 1');
 

INSERT INTO Staff(First_name, Last_name, Phone_number, Work_role, Quantity_of_products_produced, Salary, Subdivision_ID, Adress, cheese_equipment, milk_equipment)
 values('Виктор','Муркин','380960403212','2','15','3550','2','Прохоровская, 5','false','true'),
 ('Григорий','Академов','380502405122','1','49','5200','3','Красная, 10','true','true'),
 ('Максим','Малеев','380934953674','3','72','7800','1','Общажная, 101','true','true'),
 ('Мария','Тройкина','380631136390','4',NULL,'3000','1','Общажная, 101','true','false'),
 ('Степан','Тройкин','380632236390','4',NULL,'3000','2','Балковская, 1','true','false'),
 ('Павел','Стюс','380992236390','4',NULL,'3000','3','Мечникова, 13','false','true'),
 ('Николай','Харитонов',NULL,'2','25','5000','2','Южная, 11','false','false'),
 ('Николай','Мохов','380995253599','3','51','6200','1','Посмитного, 21','true','true'),
 ('Андрей','Краснопольский','380503364191','3','25','8000','1','Проспект мира, 11','true','false'),
 ('Михаил','Михеев','380505253550','3','39','5200','1','Проспект мира, 11','true','false'),
 ('Александр','Неискрений','380935333599','2','23','4200','2','Канатная, 43','false','false'),
 ('Александра','Голец','380502405331','1','29','3800','3','Сочная, 23','false','true'),
 ('Олег','Полеев','380502401122','1','34','6000','3','Бригадная, 87','false','true');

INSERT INTO Product(Product_Name, Product_Type, Product_Kind, Product_Price, Subdivision_ID, description, product_date, required_feed, required_fuel, required_med)
 values('Здоровье','Молоко','Стерилизованное','27.10','1','Молоко стерилизованное 3% жирности', '2019-12-05','40','10','20'),
 ('Счастье','Молоко','Не стерилизованное','22.00','1', 'Молоко нестерилизованное 5% жирности','2019-12-07','40','0','20'),
 ('Пармезан','Сыр','Твердый','47.00','3','Сыр пармезан высшего качества','2019-10-01','50','20','40'),
 ('Фета','Сыр','Мягкий','41.50','3','Сыр фета высшего качества','2019-11-29','30','30','30'),
 ('Дружба','Сыр','Плавленный','50.00','3', 'сырок дружба плавленный хороший :)','2019-12-20', '40','15','30');
 
 
  

INSERT INTO Order_(Date_,Client_ID)
 values('2019-7-17','1'),
 ('2019-11-23','1'),
 ('2019-9-17','2'),
 ('2019-9-20','5'),
 ('2019-10-1','3'),
 ('2019-8-15','2'),
 ('2019-10-1','4'),
 ('2018-1-27','1'),
 ('2018-9-29','2'),
 ('2018-11-17','3'),
 ('2018-12-7','2'),
 ('2019-6-30','1'),
 ('2018-11-11','1');

INSERT INTO Supply(Order_ID, Product_ID, Product_Count , Product_Price)
 values('1','1','23','27.10'),
 ('2','4','20','41.50'),
 ('3','5','15','50.00'),
 ('4','3','30','47.00'),
 ('5','5','8','50.00'),
 ('6','1','15','27.10'),
 ('7','1','23','27.10'),
 ('8','2','20','22.00'),
 ('9','5','15','50.00'),
 ('10','3','30','47.00'),
 ('11','5','8','50.00'),
 ('12','3','18','47.00'),
 ('13','5','15','50.00');
 
 
 
 
 
 create table order_resource (
   order_resource_id serial primary key,
   resource_type varchar(50) not null check (resource_type in ('корм', 'медикаменты', 'топливо')), 
   resource_price numeric (10,2) not null,
   resource_count numeric (10) not null,
   subdivision_id int not null references Subdivision (Subdivision_ID)
 );

 
 
 insert into order_resource (resource_type, resource_price, subdivision_id, resource_count) 
 values ('корм','100','3','50'), 
 ('топливо','28','1','100'),
 ('медикаменты', '17','1','25'),
('корм','100','2','30'), 
 ('топливо','28','2','200'),
 ('медикаменты', '17','2','250'),
 ('корм','100','2','70'), 
 ('топливо','28','3','200'),
 ('медикаменты', '17','3','250'),
 ('корм','100','3','70');
=======
CREATE TABLE product_mm_product_order(
    product_order_id bigint,
    product_id int,
    product_price int,
    PRIMARY key(product_order_id, product_id)
);

