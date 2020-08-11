CREATE TABLE network
(
    bssid VARCHAR(20) PRIMARY KEY NOT NULL,
    essid VARCHAR(50),
    longitude float,
    latitude float,
    handshake VARCHAR(100)
);


insert into network (bssid,essid,longitude,latitude) values(1234,"Freebox",10,20);
insert into network (bssid,essid) values(0908,"Livebox");
