CREATE DATABASE myfirstkick CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'myfirstkick'@'localhost' IDENTIFIED BY 'myfirstkick';
GRANT ALL PRIVILEGES ON myfirstkick.* TO 'myfirstkick'@'localhost' WITH GRANT OPTION;
CREATE USER 'myfirstkick'@'%' IDENTIFIED BY 'myfirstkick';
GRANT ALL PRIVILEGES ON myfirstkick.* TO 'myfirstkick'@'%' WITH GRANT OPTION;
flush privileges;
