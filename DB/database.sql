DROP DATABASE ProjectM;
DROP USER 'ProjectMServer'@'localhost';

CREATE DATABASE ProjectM CHARACTER SET 'utf8';
USE ProjectM;

CREATE USER 'ProjectMServer'@'localhost' IDENTIFIED BY 'Pr0j3c7M';
GRANT SELECT, UPDATE, INSERT, DELETE, EXECUTE
ON ProjectM.* TO 'ProjectMServer'@'localhost' IDENTIFIED BY 'Pr0j3c7M';

CREATE TABLE Users(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	username VARCHAR(50) NOT NULL UNIQUE,
	salt VARCHAR(50) NOT NULL UNIQUE,
	password VARCHAR(100) NOT NULL,
	email VARCHAR(50) NOT NULL UNIQUE,
	PRIMARY KEY(id)
)
ENGINE=INNODB;

DELIMITER |
CREATE PROCEDURE add_user (IN username VARCHAR(50), IN salt VARCHAR(50), IN password VARCHAR(100), IN email VARCHAR(50))
SQL SECURITY INVOKER
BEGIN
	INSERT INTO Users (username, salt, password, email)
	VALUES (username, salt, password, email);
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE del_user (IN to_del VARCHAR(50))
SQL SECURITY INVOKER
BEGIN
	DELETE FROM Users
	WHERE username = to_del;
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE update_username (IN old_username VARCHAR(50), IN new_username VARCHAR(50))
SQL SECURITY INVOKER
BEGIN
	UPDATE Users
	SET username = new_username
	WHERE username = old_username;
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE update_password (IN to_update VARCHAR(50), IN new_salt VARCHAR(50), IN new_password VARCHAR(100))
SQL SECURITY INVOKER
BEGIN
	UPDATE Users
	SET password = new_password, salt = new_salt
	WHERE username = to_update;
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE update_email (IN to_update VARCHAR(50), IN new_mail VARCHAR(50))
SQL SECURITY INVOKER
BEGIN
	UPDATE Users
	SET email = new_mail
	WHERE username = to_update;
END |
DELIMITER ;