-- 11 Середній бал, який певний викладач ставить певному студентові --
select  s."name"  as student, 
		t."name" as teacher,
		round(avg(g.grade),2) as avg_grade
from grades g 
join students s on s.id = g.student_id
join subjects s2 on s2.id = g.subject_id
join teachers t on s2.teacher_id = t.id 
where   s.id = 36 and 
		t.id = 2
group by s."name", t."name" 