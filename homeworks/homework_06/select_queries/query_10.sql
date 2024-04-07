-- 10 Список курсів, які певному студенту читає певний викладач --
select  s."name"  as student, 
		s2."name" as course, 
		t."name" as teacher
from grades g 
join students s on s.id = g.student_id
join subjects s2 on s2.id = g.subject_id
join teachers t on s2.teacher_id = t.id 
where s.id = 46 and t.id = 6
group by s."name" , s2."name" , t."name" 