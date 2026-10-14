-- Create Database for Ki System
CREATE DATABASE IF NOT EXISTS ki_attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ki_attendance_db;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    is_theoretical BOOLEAN DEFAULT TRUE
);

-- Insert Official Curriculum Subjects
INSERT INTO subjects (subject_name, is_theoretical) VALUES 
('Basic of Anesthesia (1)', TRUE),
('Basic of Anesthesia Equipments (1)', TRUE),
('Basic of Surgery (1)', TRUE),
('Basic of Medicine (1)', TRUE),
('Applied Physiology (1)', TRUE),
('Pharmacology (1)', TRUE),
('Computer & Artificial Intelligence (AI)', TRUE),
('جرائم البعث', TRUE);

CREATE TABLE IF NOT EXISTS attendance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    lecture_type ENUM('theory', 'group1', 'group2') DEFAULT 'theory',
    week_1 TINYINT DEFAULT 1,
    week_2 TINYINT DEFAULT 1,
    week_3 TINYINT DEFAULT 1,
    week_4 TINYINT DEFAULT 1,
    week_5 TINYINT DEFAULT 1,
    week_6 TINYINT DEFAULT 1,
    week_7 TINYINT DEFAULT 1,
    week_8 TINYINT DEFAULT 1,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);