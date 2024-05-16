CREATE SCHEMA IF NOT EXISTS dcrb;
USE dcrb;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS directories;
SET foreign_key_checks = 1;

CREATE TABLE directories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_dir INT NOT NULL,
    FOREIGN KEY (parent_dir) REFERENCES directories (id) ON DELETE CASCADE,
    INDEX idx_id_dir (id)
);

DROP TABLE IF EXISTS files;
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    readable BOOLEAN,
    dir INT NOT NULL,
    content MEDIUMTEXT,
    FOREIGN KEY (dir) REFERENCES directories (id) ON DELETE CASCADE,
    INDEX idx_file_name (name),
    FULLTEXT INDEX idx_file_content (content)
);