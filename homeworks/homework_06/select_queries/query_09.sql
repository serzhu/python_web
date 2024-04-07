-- 9 Знайти список курсів, які відвідує студент --
select  s."name"  as student,
		s2."name" as course
from grades g 
join students s on s.id = g.student_id
join subjects s2 on s2.id = g.subject_id
where s.id = 55
group by s."name" , s2."name" 