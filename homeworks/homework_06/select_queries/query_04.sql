-- 4 Знайти середній бал на потоці (по всій таблиці оцінок) --
select round(avg(grade),2) as global_avg_grade
from grades