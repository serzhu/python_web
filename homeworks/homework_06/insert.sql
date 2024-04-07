    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL, 
        group_id INTEGER REFERENCES groups(id)
  	        on delete cascade
    );

    CREATE TABLE IF NOT EXISTS teachers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        teacher_id INTEGER REFERENCES teachers(id)
  	        on delete cascade
    );

    CREATE TABLE IF NOT EXISTS grades (
        id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES students(id)
  	        on delete cascade,
        subject_id INTEGER REFERENCES subjects(id)
  	        on delete cascade,
        grade INTEGER CHECK (grade >= 0 AND grade <= 100),
        grade_date DATE NOT NULL
    );
