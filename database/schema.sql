create schema if not exists tmdb collate utf8mb4_0900_ai_ci;

create table if not exists collections
(
	collection_id int not null,
	id int null,
	collection_name varchar(100) null
);

create table if not exists movie_credits_cast
(
	movie_id int not null,
	cast_id int not null,
	credit_id varchar(100) not null,
	`character` varchar(1000) not null,
	`order` int not null
);

create index movie_credits_cast_movie_id_IDX
	on movie_credits_cast (movie_id);

create table if not exists movie_details
(
	org_title varchar(500) null,
	org_language varchar(10) null,
	movie_id int not null,
	overview varchar(1000) null,
	title varchar(500) null,
	tagline varchar(500) null
);

create index movie_details_movie_id_IDX
	on movie_details (movie_id);

create table if not exists movie_external_id
(
	movie_id int not null,
	imdb_id varchar(100) null,
	faceboook_id varchar(100) null,
	instagram_id varchar(100) null,
	twitter_id varchar(100) null
);

create table if not exists movie_genres
(
	movie_id int not null,
	genre_id int not null
);

create index movie_genres_movie_id_IDX
	on movie_genres (movie_id);

create table if not exists movie_keywords
(
	movie_id int not null,
	keyword varchar(100) null
);

create table if not exists movie_title
(
	movie_id int not null,
	title varchar(100) not null,
	language varchar(100) not null,
	type varchar(100) not null
);

create index movie_title_movie_id_IDX
	on movie_title (movie_id);

create table if not exists people_information
(
	id int not null,
	full_name varchar(100) null,
	gender varchar(100) null
);

create table if not exists posters
(
	movie_id int not null,
	poster_url varchar(100) null
);

create index movie_poster_idx
	on posters (movie_id);

create table if not exists spotify_tracks
(
	id varchar(200) not null,
	title varchar(5000) null,
	artist varchar(5000) null
);

create table if not exists movie_soundtrack
(
	movie_id int null,
	sp_track_id varchar(100) null,
	constraint movie_soundtrack_movie_details__fk
		foreign key (movie_id) references movie_details (movie_id),
	constraint movie_soundtrack_spotify_tracks__fk
		foreign key (sp_track_id) references spotify_tracks (id)
);

create index mv_st_mid_idx
	on movie_soundtrack (movie_id);

create index mv_st_sid_idx
	on movie_soundtrack (sp_track_id);

create table if not exists spotify_track_analysis
(
	id varchar(200) not null,
	track_href varchar(200) null,
	analysis_url varchar(200) null,
	duration_ms int null,
	time_signature int null,
	tempo int null,
	valence int null,
	instrumentalness int null,
	acousticness int null,
	speechiness int null,
	mode int null,
	loudness int null,
	`key` int null,
	energy int null,
	danceability int null,
	constraint spotify_track_analysis_spotify_tracks__fk
		foreign key (id) references spotify_tracks (id)
);

create index spot_track_ana
	on spotify_track_analysis (id);

create index spot_track
	on spotify_tracks (id);

create table if not exists tmdb_genre
(
	genre_id varchar(100) not null,
	genre_name varchar(100) not null
);

create index tmdb_genre_genre_id_IDX
	on tmdb_genre (genre_id);

