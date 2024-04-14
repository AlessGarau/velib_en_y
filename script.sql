CREATE TABLE `user`(
    `user_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `firstname` VARCHAR(255) NOT NULL,
    `lastname` VARCHAR(255) NOT NULL,
    `profile_picture` TEXT NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL
);
CREATE TABLE `favorite_station`(
    `station_code` VARCHAR(6) NOT NULL,
    `user_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `picture` TEXT NULL,
    `name_custom` VARCHAR(255) NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    PRIMARY KEY(`station_code`, `user_id`)
);
