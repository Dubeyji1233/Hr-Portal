create database hr_portal;
use hr_portal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    azure_oid VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    role ENUM('hr', 'interviewer', 'manager', 'admin', 'hr lead') NOT NULL,
    department VARCHAR(100),
    is_external BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

select * from users;
truncate table users;
INSERT INTO users (name, email,password_hash, role, department, is_external, is_active)
VALUES
('Deepa', 'deepa@orientindia.net','Deepa@123', 'hr', 'Human Resources', FALSE, TRUE);

INSERT INTO users (name, email,password_hash, role, department, is_external, is_active)
VALUES
('Shubham', 'shubhambhoite@orientindia.net','shubham@123', 'hr', 'Human Resources', FALSE, TRUE);

UPDATE users
SET role = 'hr'
WHERE id = 1;


DELETE FROM users
where id = 1;


CREATE TABLE interview_hierarchy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requisition_id INT,
    level INT, -- 1 to 5
    interviewer_name VARCHAR(255),
    interviewer_email VARCHAR(255),
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
);

select * from interview_hierarchy;
drop table interview_hierarchy;
truncate table interview_hierarchy;

CREATE TABLE requisitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255),
    department VARCHAR(255),
    number_of_openings INT,
    skills_required TEXT,
    location VARCHAR(255),
    hiring_type ENUM('Replacement', 'New'),
    budget DECIMAL(10,2),
    job_description TEXT,
    created_by VARCHAR(255),
    assigned_to VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from requisitions;
truncate table requisitions;
drop table requisitions;
ALTER TABLE requisitions ADD COLUMN status ENUM('Open', 'Closed') DEFAULT 'Open';
ALTER TABLE requisitions ADD COLUMN openings_filled INT DEFAULT 0;
alter table requisitions add column comments text;
ALTER TABLE requisitions ADD COLUMN comments_updated_at DATETIME;

SELECT department, SUM(number_of_openings) AS openings, SUM(openings_filled) AS filled
FROM requisitions
GROUP BY department;





CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    skills text,
    resume BLOB,
    requisition_id INT,
    submitted_by varchar(100),
    shortlisted_by INT,
    shortlisted_on DATETIME,
    is_shortlisted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id),
    FOREIGN KEY (submitted_by) REFERENCES users(email),
    FOREIGN KEY (shortlisted_by) REFERENCES users(id)
);

select * from candidates;
drop table candidates;
truncate table candidates;
ALTER TABLE candidates
ADD COLUMN selection_status ENUM('In Process', 'Rejected', 'Selected') DEFAULT 'In Process';
ALTER TABLE candidates
  ADD COLUMN final_ctc DECIMAL(10,2)     NULL,
  ADD COLUMN planned_joining_date DATE   NULL,
  ADD COLUMN actual_joining_date DATE    NULL ;

ALTER TABLE candidates
  ADD COLUMN offer_letter LONGBLOB NULL;
  
ALTER TABLE candidates
MODIFY COLUMN resume LONGBLOB;

alter table candidates
add column total_exp VARCHAR(150) NOT NULL,
add column current_loc VARCHAR(150) NOT NULL,
add column current_ctc VARCHAR(150) NOT NULL,
add column exp_ctc VARCHAR(150) NOT NULL,
add column source VARCHAR(150) NOT NULL;




CREATE TABLE interview_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    level INT,
    interview_datetime DATETIME,
    interviewer_name VARCHAR(255),
    interviewer_email VARCHAR(255),
    status ENUM('pending', 'completed') DEFAULT 'pending',
    UNIQUE(candidate_id, level),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
);


select * from interview_schedule;
drop table interview_schedule;


CREATE TABLE ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    requisition_id INT,
    interviewer_id INT,
    communication_skills INT CHECK (communication_skills BETWEEN 1 AND 5),
    technical_skills INT CHECK (technical_skills BETWEEN 1 AND 5),
    learning_ability INT CHECK (learning_ability BETWEEN 1 AND 5),
    problem_solving INT CHECK (problem_solving BETWEEN 1 AND 5),
    cultural_fitment INT CHECK (cultural_fitment BETWEEN 1 AND 5),
    remarks TEXT,
    status ENUM('pending', 'submitted') DEFAULT 'pending',
    submitted_on DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (candidate_id) REFERENCES candidates(id),
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id),
    FOREIGN KEY (interviewer_id) REFERENCES interview_hierarchy(id),
    UNIQUE(candidate_id, requisition_id, interviewer_id)
);

select * from ratings;

CREATE TABLE job_profile ( 
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    name VARCHAR(100) NOT NULL,
    email_id VARCHAR(150) UNIQUE NOT NULL,
    contact_number VARCHAR(150) UNIQUE NOT NULL,
    total_exp VARCHAR(150) NOT NULL,
    current_loc VARCHAR(150) NOT NULL,
    skills TEXT NOT NULL,
    current_ctc VARCHAR(150) NOT NULL,
    exp_ctc VARCHAR(150) NOT NULL,
    source VARCHAR(150) NOT NULL,
    cv LONGBLOB
);  

select * from job_profile;

ALTER TABLE job_profile
ADD COLUMN dynamic_exp INT GENERATED ALWAYS AS (TIMESTAMPDIFF(YEAR, date, CURDATE()) + total_exp) STORED;






