CREATE TABLE `user` (
  `userid` varchar(28) NOT NULL,
  `username` varchar(255) NOT NULL,
  PRIMARY KEY (`userid`)
);

CREATE TABLE `category` (
  `categoryid` int(11) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  PRIMARY KEY (`categoryid`)
);

CREATE TABLE `review` (
  `reviewid` varchar(18) NOT NULL,
  `review` varchar(255) NOT NULL,
  PRIMARY KEY (`reviewid`)
);

CREATE TABLE `product` (
  `productid` varchar(10) NOT NULL,
  `product_name` mediumtext NOT NULL,
  `actual_price` float NOT NULL,
  `discount_percentage` float NOT NULL,
  `product_desc` longtext NOT NULL,
  `img_link` mediumtext NOT NULL,
  `product_link` mediumtext NOT NULL,
  `rating_count` int(11) NOT NULL,
  `rating` float NOT NULL,
  PRIMARY KEY (`productid`)
);

CREATE TABLE `is_category` (
  `productid` varchar(10) NOT NULL,
  `categoryid` int(11) NOT NULL,
  PRIMARY KEY (`productid`,`categoryid`),
  KEY `categoryid` (`categoryid`),
  CONSTRAINT `is_category_ibfk_1` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`),
  CONSTRAINT `is_category_ibfk_2` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`)
);

CREATE TABLE `has_review` (
  `productid` varchar(10) NOT NULL,
  `reviewid` varchar(18) NOT NULL,
  PRIMARY KEY (`productid`,`reviewid`),
  KEY `reviewid` (`reviewid`),
  CONSTRAINT `has_review_ibfk_1` FOREIGN KEY (`productid`) REFERENCES `product` (`productid`),
  CONSTRAINT `has_review_ibfk_2` FOREIGN KEY (`reviewid`) REFERENCES `review` (`reviewid`)
);

CREATE TABLE `written_by` (
  `userid` varchar(28) NOT NULL,
  `reviewid` varchar(18) NOT NULL,
  PRIMARY KEY (`userid`,`reviewid`),
  KEY `reviewid` (`reviewid`),
  CONSTRAINT `written_by_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`),
  CONSTRAINT `written_by_ibfk_2` FOREIGN KEY (`reviewid`) REFERENCES `review` (`reviewid`)
);
