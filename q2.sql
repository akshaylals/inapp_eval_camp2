CREATE DATABASE camp2_eval_q2;
GO
USE camp2_eval_q2;
GO

CREATE TABLE patients(
    patientId INT IDENTITY NOT NULL PRIMARY KEY,
    patientName VARCHAR(20) NOT NULL,
    gender CHAR(1) NOT NULL,
    age INT NOT NULL,
    bloodGroup CHAR(3) NOT NULL
);
GO