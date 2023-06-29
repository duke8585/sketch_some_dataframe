-- +++++ SQL values table definition
with base as (
select * from (
values
 ('2022-02-01', 'max', '1', null),
('2022-02-02', 'max', '2', null),
('2022-02-03', 'max', '3', null),
('2022-02-04', 'max', '4', null),
('2022-02-01', 'john', '3', null),
('2022-02-02', 'john', '4', null),
('2022-02-03', 'john', '5', null),
('2022-02-04', 'john', '3', null),
('2022-02-05', 'john', '4', null),
('2022-02-06', 'john', '5', null),
('2022-02-07', 'john', '6', null),
('2022-02-04', 'liz', '2', null),
('2022-02-05', 'liz', '3', null),
('2022-02-06', 'liz', '4', null),
('2022-02-07', 'liz', '5', null),
('2022-02-08', 'liz', '5', null),
('2022-02-09', 'liz', '8', null),
('2022-02-10', 'liz', '9', null),
('2022-02-03', 'liz', null, 'null_allowed'),
('2022-02-04', 'liz', null, 'null_allowed'),
('2022-02-05', 'liz', null, 'null_allowed')
 ) AS t(date, name, debt, remark))
select * from base