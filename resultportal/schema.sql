-- Database admin and its tables
CREATE DATABASE IF NOT EXISTS nilekrator$admin;
use nilekrator$admin;

-- feedback table
CREATE TABLE IF NOT EXISTS feedback (roll varchar(30), problem text);

-- users table
CREATE TABLE IF NOT EXISTS users (
  roll varchar(20) PRIMARY KEY,
  student_name varchar(70),
  image_id varchar(10) DEFAULT NULL,
  google_image_id varchar(50) DEFAULT NULL,
  image_link text DEFAULT NULL,
  -- position is equivalent to student rank
  -- position keyword is used because rank is a reserved keyword in mysql
  position int DEFAULT 0
);

--subjects table
CREATE TABLE IF NOT EXISTS subjects (
  subject_code varchar(20) PRIMARY KEY,
  subject_name text,
  credits int(1)
)

-- All the database suffixed as 2015, 2016, etc are year wise student database
-- these database are created on the basis of a json file submitted after scraping
-- of data from the original website
-- below is a sample of such database
CREATE DATABASE IF NOT EXISTS nilekrator$2015;
use nilekrator$2015;

-- metadata table
CREATE TABLE IF NOT EXISTS metadata (
  branch_name varchar(20) PRIMARY KEY,
  session_date varchar(15),
  publish_date varchar(10),
  semesters varchar(10),
  scheme varchar(10),
  degree varchar(15)
);

-- semester student status
CREATE TABLE IF NOT EXISTS nilekrator$2015_ug_cs_5 (
  roll varchar(20) PRIMARY KEY,
  cgpa float(5, 2),
  sgpa float(5, 2),
  google_pdf_id varchar(50) DEFAULT NULL,
  pdf_link text DEFAULT NULL,
  result_status enum(1,0),
  FOREIGN KEY (roll) REFERENCES nilekrator$admin.users (roll) ON DELETE CASCADE
);

-- semester student result
CREATE TABLE IF NOT EXISTS nilekrator$2015.result_ug_cs_5 (
  roll varchar(20),
  subject_code varchar(10),
  end_sem float(5, 2),
  test_1 float(5, 2),
  test_2 float(5, 2),
  grade varchar(7),
  total float(5, 2),
  assignment float(5, 2),
  quiz_avg float(5, 2),
  FOREIGN KEY (roll) REFERENCES nilekrator$admin.users (roll) ON DELETE CASCADE
);