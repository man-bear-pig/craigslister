CREATE USER 'crawler'@'localhost';

CREATE USER 'api'@'localhost';

CREATE DATABASE craigslister
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

GRANT ALL PRIVILEGES ON craigslister.*
    TO 'crawler'@'localhost';

GRANT SELECT ON craigslister.*
    TO 'api'@'localhost';

FLUSH PRIVILEGES;

USE craigslister;

CREATE TABLE `ad` (
  `crawl_date` datetime NOT NULL,
  `crawl_id` int(11) DEFAULT NULL,
  `crawl_event_id` int(11) DEFAULT NULL,
  `post_date` datetime NOT NULL,
  `pid` bigint(15) NOT NULL DEFAULT '0',
  `pid_parent` bigint(15) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `link` varchar(200) DEFAULT NULL,
  `price` decimal(7,2) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `pic` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pid`,`post_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `crawler` (
  `createdate` datetime NOT NULL,
  `crawl_id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(100) DEFAULT NULL,
  `search_term` bigint(15) NOT NULL DEFAULT '0',
  `price_low` decimal(7,2) DEFAULT NULL,
  `price_high` decimal(7,2) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `active` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`crawl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `crawl_event` (
  `crawl_event_id` int(11) NOT NULL AUTO_INCREMENT,
  `crawl_id` int(11) NOT NULL,
  `crawl_date` datetime DEFAULT NULL,
  `recs_loaded` int(11) DEFAULT NULL,
  PRIMARY KEY (`crawl_event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

