create table IF NOT EXISTS file_content
(
    id     int auto_increment
        primary key,
    data   longblob not null,
    width int not null,
    height int not null,
    aspect int    not null,
    hash   blob     not null
);