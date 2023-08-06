import MySQLdb as sql

#db = sql.connect(host="mysql", user="runner", passwd="Databasepss20/21", db="assignment1")# noqa
db = sql.connect(host="mysql", user="root", passwd="Databasepss20/21", db="assignment1")# noqa
cursor = db.cursor()
create_table = """DROP TABLE IF EXISTS `metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `metadata` (
  `id` int(4) NOT NULL,
  `nome` varchar(20) NOT NULL,
  `estensione` varchar(4) NOT NULL,
  `percorso` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
populate_table = """LOCK TABLES `metadata` WRITE;
/*!40000 ALTER TABLE `metadata` DISABLE KEYS */; INSERT INTO `metadata` 
VALUES (1,'neve','jpg','immagini/neve.jpg'),
(2,'ghepardo','jpg','immagini/ghepardo.jpg'),
(3,'flower','jpg','immagini/flower.jpg'),
(4,'cioccolatino','jpg','immagini/cioccolatino.jpg'),
(5,'arancia','jpg','immagini/arancia.jpg');
/*!40000 ALTER TABLE `metadata` ENABLE KEYS */;
UNLOCK TABLES;"""
cursor.execute(create_table)
cursor.nextset()
cursor.execute(populate_table)
