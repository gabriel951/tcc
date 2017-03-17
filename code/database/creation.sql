-- SQL SCRIPT TO CREATE THE TABLES
-- DROP PREVIOUS SCHEMA
DROP SCHEMA BD_UNB CASCADE;

-- SCHEMA CREATION
CREATE SCHEMA BD_UNB;

-- STUDENT
CREATE TABLE BD_UNB.STUDENT
(
    COD_MAT         BIGINT                 NOT NULL    UNIQUE,
    SEX             VARCHAR(50)         NOT NULL, 
    AGE             INT, 
    QUOTA           VARCHAR(100),
    SCHOOL_TYPE     VARCHAR(100),
    RACE            VARCHAR(100),
    LOCAL           VARCHAR(100), 
    COURSE          VARCHAR(100),
    YEAR_IN         INT,
    SEMESTER_IN     INT,
    YEAR_END        INT, 
    SEMESTER_END    INT,
    WAY_IN          VARCHAR(100),
    WAY_OUT         VARCHAR(100),
PRIMARY KEY(COD_MAT));

-- SUBJECT
CREATE TABLE BD_UNB.SUBJECT
(
    ID              SERIAL,
    CODE            INT                 NOT NULL    UNIQUE,
    NAME            VARCHAR(100)        NOT NULL, 
    CREDITS         INT                 NOT NULL,
PRIMARY KEY(ID)); 

-- RELANTIONSHIP BETWEEN STUDENT AND SUBJECT
CREATE TABLE BD_UNB.STUDENT_SUBJECT
(
    CODE_STU        BIGINT,
    CODE_SUB        INT, 
    SEMESTER        INT             NOT NULL,
    YEAR            INT             NOT NULL,
    GRADE           VARCHAR(10),
-- the primary key needs to account for the possibility that a student takes a
-- discipline many times
PRIMARY KEY (CODE_STU, CODE_SUB, YEAR, SEMESTER), 
FOREIGN KEY (CODE_STU) REFERENCES BD_UNB.STUDENT (COD_MAT)
    ON DELETE CASCADE, 
FOREIGN KEY (CODE_SUB) REFERENCES BD_UNB.SUBJECT (CODE)
    ON DELETE CASCADE
); 
