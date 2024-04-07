-- 8 Знайти середній бал, який ставить певний викладач зі своїх предметів --
select  s."name" as subject, 
		t."name"as teacher, 
		round(avg(g.grade),2) as avg_grade 
from subjects s
join teachers t  on t.id = s.teacher_id
join grades g on g.subject_id  = s.id 
where t.id  = 3
group by s."name" , t."name" 