CREATE DATABASE VisionSecurityDB;
GO

USE VisionSecurityDB;
GO

CREATE TABLE BiometricAudit (
    EventID INT IDENTITY(1,1) PRIMARY KEY,
    CaptureTimestamp DATETIME DEFAULT GETDATE(),
    ImageFilename VARCHAR(255) NOT NULL,
    ImagePath VARCHAR(500) NOT NULL,
    DetectionType VARCHAR(50) DEFAULT 'FaceMesh_468_Points'
);
GO

SELECT * FROM BiometricAudit;