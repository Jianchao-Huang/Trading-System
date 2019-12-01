drop table history;

create table history(
	history_id int auto_increment,
    user_id int,
    crypto_name varchar (255),
    volume int,
    unit_price decimal (10,5),
    trading_date date,
    action varchar (255),
    primary key (history_id)
);

insert into history (user_id, crypto_name, volume, unit_price, trading_date, action) values (0110, 'bitcoin', 100, 0.1111000, '2019-11-17', 'buy');

select * from history;asset