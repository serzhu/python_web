-- 2 Знайти студента із найвищим середнім балом з певного предмета --
select  s."name" as student, 
		s2."name" as subject, 
		round(avg(g.grade),2) as avg_grade
from grades g 
join students s on s.id = g.student_id  
join subjects s2 on s2.id = g.subject_id
where s2."name"  = 'Physics'
group by s."name", s2."name" 
order by avg_grade desc 
limit 1