-- 1 Знайти 5 студентів із найбільшим середнім балом з усіх предметів --
select  s."name" as student, 
		round(avg(g.grade),2) as avg_grade 
from students as s
join grades as g on g.student_id = s.id
group by s.id 
order by avg_grade desc  
limit 5