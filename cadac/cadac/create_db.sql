-- Table for storing simple nodes,
-- without attributes or children.

CREATE TABLE nodes ( 
       uuid  varchar(36), 
       name  varchar(256), 
       value TEXT );

CREATE TABLE linktypes ( 
       uuid  varchar(36), 
       name  varchar(256),
       value varchar(256), 
       url   varchar(512) );

CREATE TABLE parameters (
       uuid   varchar(36),
       name  varchar(256),
       value varchar(512),
       url   varchar(1024));

CREATE TABLE tags (
       uuid  varchar(36),
       tag   varchar(64),
       user  varchar(64));

CREATE TABLE userfields (
       uuid   varchar(36),
       name  varchar(256),
       value varchar(512));

CREATE TABLE runs (
       uuid varchar(36));

CREATE TABLE programs (
       uuid   varchar(36),
       name  varchar(256),
       version varchar(512),
       url   varchar(512));

CREATE TABLE members (
       username  varchar(256),
       name varchar(512),
       url   varchar(512));
