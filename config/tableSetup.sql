use kaizen;

DROP TABLE if exists kaizen.adlisting, kaizen.users, kaizen.booklibrary,
kaizen.adlistingAttributes, kaizen.feedback, kaizen.transactions, kaizen.session, kaizen.wishlist;

CREATE TABLE `adlisting` (
    `id` int(8) NOT NULL AUTO_INCREMENT,
    `title` varchar(30) DEFAULT NULL,
    `price` float DEFAULT 0.00,
    `sellerId` int(6) DEFAULT NULL,
    `buyerId` int(6) DEFAULT NULL,
    `permLink` varchar(255) DEFAULT NULL,
    `imageLocation` varchar(255) DEFAULT "default.jpg",
    `condition` varchar(20) DEFAULT NULL,
    `description` varchar(512) DEFAULT NULL,
    `author` varchar(512) DEFAULT NULL,
    `year` varchar(30) DEFAULT NULL,
    `publisher` varchar(255) DEFAULT NULL,
    `edition` varchar(255) DEFAULT NULL,
    `ISBN13` varchar(255) DEFAULT NULL,
    `activeFlag` boolean DEFAULT TRUE,
    `txId` int(6) DEFAULT -1,
    `createdDate` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `users` (
    `id` int(6) NOT NULL AUTO_INCREMENT,
    `firstName` varchar(255) DEFAULT NULL,
    `surname` varchar(255) DEFAULT NULL,
    `email` varchar(255) DEFAULT NULL,
    `password` varchar(255) DEFAULT NULL,
    `phoneNumber` varchar(30) DEFAULT NULL,
    `createdDate`	datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `feedback` (
	`id` int(6) NOT NULL AUTO_INCREMENT,
	`giverId` int(6) NOT NULL DEFAULT 000000,
    `receiverId` int(6) NOT NULL DEFAULT 000000,
    `receiverType` varchar(1) DEFAULT 'x',
    `adId` int(8) NOT NULL DEFAULT 00000000,
    `feedback` varchar(512),
    `rating` int(1),
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `transactions` (
    `id` int(6) NOT NULL AUTO_INCREMENT,
    `adId` int(8) NOT NULL,
    `sellerId` int(6) NOT NULL,
    `buyerid` int(6) NOT NULL,
    `txdate` datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `session` (
    `user_id` int(6) NOT NULL DEFAULT -1,
    `session_id` varchar(255) NOT NULL,
    `expired` boolean NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`session_id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `wishlist` (
	`id` int(6) NOT NULL AUTO_INCREMENT,
    `adId` int(8) NOT NULL,
    `userId` int(6) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

ALTER TABLE adlisting AUTO_INCREMENT = 10000001;
ALTER TABLE users AUTO_INCREMENT = 100001;
ALTER TABLE transactions AUTO_INCREMENT = 200001;
ALTER TABLE wishlist AUTO_INCREMENT = 100001;