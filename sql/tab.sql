CREATE TABLE `T_BALANCE_REPORT` (
  `ID` int(11) DEFAULT NULL COMMENT 'ID；说明：记录唯一ID；样例：1234',
  `ACCOUNT_ID` int(11) DEFAULT NULL COMMENT 'ACCOUNTID；说明：PNC该字段是一个数字，设置为自增的；样例：12345678',
  `CARD_NO` varchar(100) DEFAULT NULL COMMENT '卡号',
  `CARD_NAME` varchar(100) DEFAULT NULL COMMENT '卡名称',
  `CARD_STATUS` varchar(10) DEFAULT NULL COMMENT '卡状态',
  `UPDATE_DATE` datetime DEFAULT NULL COMMENT '更新时间',
  `TRADING_DATE` datetime DEFAULT NULL COMMENT '交易时间',
  `BALANCE` decimal(10,3) DEFAULT NULL COMMENT '余额',
  `INIT_AMOUNT` decimal(10,3) DEFAULT NULL COMMENT '初始金额',
  `INIT_DATE` varchar(20) DEFAULT NULL COMMENT '激活日期',
  `VALID_END_DATE` varchar(20) DEFAULT NULL COMMENT '卡有效期',
  `IS_REPLACE` varchar(10) DEFAULT NULL COMMENT '实体卡换卡标识（Y:换过卡，N:未换卡）',
  `OLD_CARD_NO` varchar(30) DEFAULT NULL COMMENT '旧卡号',
  UNIQUE KEY `INDEX_NAME` (`ACCOUNT_ID`),
  KEY `INDEX_CARD_NO` (`CARD_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='测试表';