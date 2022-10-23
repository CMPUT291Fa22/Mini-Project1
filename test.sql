drop table if exists perform;
drop table if exists artists;
drop table if exists plinclude;
drop table if exists playlists;
drop table if exists listen;
drop table if exists sessions;
drop table if exists songs;
drop table if exists users;

PRAGMA foreign_keys = ON;

create table users (
  uid		char(4),
  name		text,
  pwd       text,
  primary key (uid)
);
create table songs (
  sid		int,
  title		text,
  duration	int,
  primary key (sid)
);
create table sessions (
  uid		char(4),
  sno		int,
  start 	date,
  end 		date,
  primary key (uid,sno),
  foreign key (uid) references users
	on delete cascade
);
create table listen (
  uid		char(4),
  sno		int,
  sid		int,
  cnt		real,
  primary key (uid,sno,sid),
  foreign key (uid,sno) references sessions,
  foreign key (sid) references songs
);
create table playlists (
  pid		int,
  title		text,
  uid		char(4),
  primary key (pid),
  foreign key (uid) references users
);
create table plinclude (
  pid		int,
  sid		int,
  sorder	int,
  primary key (pid,sid),
  foreign key (pid) references playlists,
  foreign key (sid) references songs
);
create table artists (
  aid		char(4),
  name		text,
  nationality	text,
  pwd       text,
  primary key (aid)
);
create table perform (
  aid		char(4),
  sid		int,
  primary key (aid,sid),
  foreign key (aid) references artists,
  foreign key (sid) references songs
);

/*
    This is a set of test cases for the login screen.
*/
insert into users values ("admin", "admin", "admin");
insert into users values ("junye", "John Yu", "junye");

insert into songs values (0, "Baby", 2);
insert into songs values (1, "Yummy", 4);
insert into songs values (2, "Love Yourself", 4);
insert into songs values (3, "Peaches", 3);
insert into songs values (4, "Beauty And A Beat", 2);
insert into songs values (5, "Ghost", 3);
insert into songs values (6, "Jimmy Cooks", 3);
insert into songs values (7, "Feel No Ways", 3);
insert into songs values (8, "Knife Talk", 3);
insert into songs values (9, "Way 2 Sexy", 3);
insert into songs values (10, "Chicago Freestyle", 3);
insert into songs values (11, "Toosie Slide", 3);
insert into songs values (12, "Wants and Needs", 3);
insert into songs values (13, "Nonstop", 3);

insert into playlists values (0, "happy", "admin");
insert into playlists values (1, "sad", "admin");
insert into playlists values (2, "mad", "admin");
insert into playlists values (3, "scared", "admin");
insert into playlists values (4, "disgust", "admin");

insert into plinclude values (0, 0, NULL);
insert into plinclude values (0, 1, NULL);
insert into plinclude values (0, 2, NULL);
insert into plinclude values (1, 3, NULL);
insert into plinclude values (1, 4, NULL);
insert into plinclude values (1, 5, NULL);
insert into plinclude values (2, 6, NULL);
insert into plinclude values (2, 7, NULL);
insert into plinclude values (2, 8, NULL);
insert into plinclude values (2, 9, NULL);
insert into plinclude values (2, 10, NULL);
insert into plinclude values (2, 11, NULL);
insert into plinclude values (2, 12, NULL);
insert into plinclude values (2, 13, NULL);

insert into artists values ("a0", "Justin Bieber", "Canadian", "a0");
insert into artists values ("junye", "John Yu", "Canadian", "junye");
insert into artists values ("a1", "Drake", "Canadian", "a1");
insert into artists values ("a2", "Celine Dion", "Canadian", "a2");
insert into artists values ("a3", "Shania Twain", "Canadian", "a3");
insert into artists values ("a4", "Bryan Adams", "Canadian", "a4");
insert into artists values ("a5", "The Weeknd", "Canadian", "a5");
insert into artists values ("a6", "Avril Lavigne", "Canadian", "a6");
insert into artists values ("a7", "Shawn Mendes", "Canadian", "a7");
insert into artists values ("a8", "Taylor Swift", "American", "a8");
insert into artists values ("a9", "Ariana Grande", "American", "a9");
insert into artists values ("a10", "Katy Perry", "American", "a10");
insert into artists values ("a11", "Olivia Rodrigo", "American", "a11");
insert into artists values ("a12", "Billie Eilish", "American", "a12");
insert into artists values ("a13", "Miley Cyrus", "American", "a13");
insert into artists values ("a14", "Rihanna", "Barbadian", "a14");
insert into artists values ("a15", "Lady Gaga", "American", "a15");
insert into artists values ("a16", "Beyonce", "American", "a16");
insert into artists values ("a17", "Demi Lovato", "American", "a17");
insert into artists values ("a18", "Britney Spears", "American", "a18");

insert into perform values ("a0", 0);
insert into perform values ("a0", 1);
insert into perform values ("a0", 2);
insert into perform values ("a0", 3);
insert into perform values ("a0", 4);
insert into perform values ("a0", 5);
insert into perform values ("a1", 6);
insert into perform values ("a1", 7);
insert into perform values ("a1", 8);
insert into perform values ("a1", 9);
insert into perform values ("a1", 10);
insert into perform values ("a1", 11);
insert into perform values ("a1", 12);
insert into perform values ("a1", 13);

/*
    This is a set of test cases for the system functionalities.
*/

/*
    This is a set of test cases for the song actions.
*/

/*
    This is a set of test cases for the artist actions.
*/