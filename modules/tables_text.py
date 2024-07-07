create_tables_text = [
    """
CREATE TABLE `titles` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`id_kinopoisk` INT(10) NOT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `id_kinopoisk` (`id_kinopoisk`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;
""",
    """
CREATE TABLE `titles_history` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`user_id` INT(10) NOT NULL,
	`title_id` INT(10) NOT NULL,
	`status` TEXT NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`status_change` DATETIME NOT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `user_id` (`user_id`) USING BTREE,
	INDEX `title_id` (`title_id`) USING BTREE,
	CONSTRAINT `title_id` FOREIGN KEY (`title_id`) REFERENCES `titles` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;
""",
    """
CREATE TABLE `users` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`telegram_id` BIGINT(19) NOT NULL,
	`datetime_create` DATETIME NOT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `telegram_id` (`telegram_id`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;
""",
]
