CREATE DATABASE hr_portal;
USE hr_portal;

-- USERS TABLE
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
DELETE FROM users
where id = 6;

INSERT INTO users (name, email,password_hash, role, department, is_external, is_active)
VALUES
('Deepa', 'deepa@orientindia.net','Deepa@123', 'hr', 'Human Resources', FALSE, TRUE);

INSERT INTO users (name, email,password_hash, role, department, is_external, is_active)
VALUES
('Aastha', 'astha@orientindia.net','astha@123', 'hr', 'Human Resources', FALSE, TRUE);

UPDATE users
SET role = 'admin'
WHERE id = 4;

-- REQUISITIONS TABLE
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
    status ENUM('Open', 'Closed') DEFAULT 'Open',
    openings_filled INT DEFAULT 0,
    comments TEXT,
    comments_updated_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from requisitions; 
truncate table requisitions;
alter table requisitions add column customer_name varchar(255);
delete from requisitions
where id = 1;

ALTER TABLE requisitions
MODIFY status ENUM('Open', 'Closed', 'On Hold', 'Lost from Customer') DEFAULT 'Open';

ALTER TABLE requisitions ADD COLUMN closed_at DATETIME DEFAULT NULL;

CREATE TABLE requisition_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requisition_id INT NOT NULL,
    assigned_to_email VARCHAR(255) NOT NULL,
    assigned_by_email VARCHAR(255),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id),
    FOREIGN KEY (assigned_to_email) REFERENCES users(email),
    FOREIGN KEY (assigned_by_email) REFERENCES users(email)
);

-- INTERVIEW HIERARCHY TABLE
CREATE TABLE interview_hierarchy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requisition_id INT,
    level INT,
    interviewer_name VARCHAR(255),
    interviewer_email VARCHAR(255),
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
);

select * from interview_hierarchy;
truncate table interview_hierarchy;
drop table interview_hierarchy;
delete from interview_hierarchy
where id = 1;

CREATE TABLE department_utilization (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requisition_id INT,
    department_name VARCHAR(255),
    utilization DECIMAL(5,2),
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id)
);
select * from department_utilization;
drop table department_utilization;
delete from department_utilization
where id = 1;



-- CANDIDATES TABLE
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    skills TEXT,
    resume LONGBLOB,
    requisition_id INT,
    submitted_by VARCHAR(100),
    shortlisted_by INT,
    shortlisted_on DATETIME,
    is_shortlisted BOOLEAN DEFAULT FALSE,
    selection_status ENUM('In Process', 'Rejected', 'Selected') DEFAULT 'In Process',
    final_ctc DECIMAL(10,2),
    planned_joining_date DATE,
    actual_joining_date DATE,
    offer_letter LONGBLOB NULL,
    total_exp VARCHAR(150) NOT NULL,
    current_loc VARCHAR(150) NOT NULL,
    current_ctc VARCHAR(150) NOT NULL,
    exp_ctc VARCHAR(150) NOT NULL,
    source VARCHAR(150) NOT NULL,
    FOREIGN KEY (requisition_id) REFERENCES requisitions(id),
    FOREIGN KEY (submitted_by) REFERENCES users(email),
    FOREIGN KEY (shortlisted_by) REFERENCES users(id)
);

select * from candidates;
truncate table candidates;
drop table candidates;

ALTER TABLE candidates
ADD COLUMN designation VARCHAR(100) NOT NULL,
ADD COLUMN notice_period INT NOT NULL,
ADD COLUMN reason_for_change TEXT NOT NULL;
ALTER TABLE candidates
ADD COLUMN offer_letter_date datetime;

-- INTERVIEW SCHEDULE TABLE
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
truncate table interview_schedule;
drop table interview_schedule;

ALTER TABLE interview_schedule ADD COLUMN teams_event_id VARCHAR(255);

-- RATINGS TABLE
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
truncate table ratings;
drop table ratings;

-- JOB PROFILE TABLE
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
truncate table job_profile;
