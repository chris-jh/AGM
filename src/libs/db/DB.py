import datetime
import sqlite3
from libs.Utils import *

class DB():
    FIND_PLATFORM_BY_NAME = "SELECT * from platform WHERE name=?"
    FIND_ALL_GAMES_BY_PLATFORM = "SELECT * from game WHERE platform_ref=?"
    FIND_RECENTLY_PLAYED_GAMES_BY_PLATFORM = "SELECT * from game WHERE platform_ref=? ORDER BY date_last_played"
    FIND_RECENTLY_ADDED_GAMES_BY_PLATFORM = "SELECT * from game WHERE platform_ref=? ORDER BY date_added"
    def __init__(self, app):
        self.app = app
        self.db = self.app.config["database"]["name"]
        self._init_connection()
    
    def _init_connection(self):
        idb = True
        if (check_file_exists(self.db)):
            idb = False
        self.connection = sqlite3.connect(self.db)
        if (idb):
            self._init_db()
        #self._show_data()
    
    def _init_db(self):
        self.app.update_loading("[INIT DATABASE]")
        c = self.connection.cursor()
        c.executescript("""
            CREATE TABLE platform (
                id INTEGER PRIMARY KEY, 
                name TEXT
            );
            
            CREATE TABLE game (
                id INTEGER PRIMARY KEY, 
                name TEXT,
                platform_ref INTEGER,
                external_id INTEGER,
                overview_text TEXT,
                image_box_art_path TEXT,
                image_screen_shot_path TEXT,
                image_art_path TEXT,
                date_added TEXT,
                date_last_played TEXT,
                play_count INTEGER,
                rating INTEGER,
                FOREIGN KEY(platform_ref) REFERENCES platform(id)
            );
            
            CREATE TABLE game_path (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                game_path TEXT,
                game_ref INTEGER,
                FOREIGN KEY(game_ref) REFERENCES game(id)
            );
            
            CREATE INDEX platformnameindex ON platform(name);
            CREATE INDEX gamenameindex ON game(name);
            CREATE INDEX gamedateaddedindex ON game(date_added);
            CREATE INDEX gamelastplayedindex ON game(date_last_played);
            CREATE INDEX gameplatformdateaddedindex ON game(platform_ref, date_added);
            CREATE INDEX gameplatformlastplayedindex ON game(platform_ref, date_last_played);
            """)
        
        self.connection.commit()
        self._init_dummy_data()
    
    def _init_dummy_data(self):
        c = self.connection.cursor()
        c.executescript("""
            INSERT INTO platform(name) VALUES("Megadrive");
            INSERT INTO game(name, platform_ref, image_box_art_path, image_screen_shot_path, image_art_path, date_added, date_last_played) VALUES("Sonic The Hedgehog", 1, "./../test/img/md/boxart/1.png" ,"./../test/img/md/sshot/1.png", "./../test/img/md/art/1.png", "2014-01-03 01:01:00.000000", "2014-01-04 05:01:00.000000");
            INSERT INTO game(name, platform_ref, image_box_art_path, image_screen_shot_path, image_art_path, date_added, date_last_played) VALUES("Sonic The Hedgehog 2", 1, "./../test/img/md/boxart/2.png" ,"./../test/img/md/sshot/2.png", "./../test/img/md/art/2.png", "2014-01-03 01:02:00.000000", "2014-01-04 05:02:00.000000");
            INSERT INTO game(name, platform_ref, image_box_art_path, image_screen_shot_path, image_art_path, date_added, date_last_played) VALUES("Streets Of Rage 2", 1, "./../test/img/md/boxart/3.png" ,"./../test/img/md/sshot/3.png", "./../test/img/md/art/3.png", "2014-01-03 01:03:00.000000", "2014-01-04 05:03:00.000000");
            INSERT INTO game(name, platform_ref, image_box_art_path, image_screen_shot_path, image_art_path, date_added, date_last_played) VALUES("Street Fighter 2", 1, "./../test/img/md/boxart/4.png" ,"./../test/img/md/sshot/4.png", "./../test/img/md/art/4.png", "2014-01-03 01:04:00.000000", "2014-01-04 05:04:00.000000");
            INSERT INTO game(name, platform_ref, image_box_art_path, image_screen_shot_path, image_art_path, date_added, date_last_played) VALUES("Golden Axe", 1, "./../test/img/md/boxart/5.png" ,"./../test/img/md/sshot/5.png", "./../test/img/md/art/5.png", "2014-01-03 01:05:00.000000", "2014-01-04 05:05:00.000000");    
            INSERT INTO game_path (file_name, game_path, game_ref) VALUES ("sonic.rom","./../test/rom/md/", 1);
            INSERT INTO game_path (file_name, game_path, game_ref) VALUES ("sonic2.rom","./../test/rom/md/", 2);
            INSERT INTO game_path (file_name, game_path, game_ref) VALUES ("sor2.rom","./../test/rom/md/", 3);
            INSERT INTO game_path (file_name, game_path, game_ref) VALUES ("sf2.rom","./../test/rom/md/", 4);
            INSERT INTO game_path (file_name, game_path, game_ref) VALUES ("gaxe.rom","./../test/rom/md/", 5);
        """)
        self.connection.commit()
        
    def _show_data(self):
        c = self.connection.cursor()
        for row in c.execute('SELECT * FROM platform ORDER BY name'):
            print row
        
        for row in c.execute('SELECT * FROM game ORDER BY name'):
            print row
        
        for row in c.execute('SELECT * FROM game_path ORDER BY file_name'):
            print row
    
    def process_sql(self, sql, params, offset=None, limit=None):
        c = self.connection.cursor()
        msql = sql
        
        if (limit):
            msql1 = "%s limit %s" % (msql, limit)
            msql = msql1        
            if (offset):
                msql2 = "%s offset %s" % (msql, offset)
                msql = msql2
        
        #print "PROCESS SQL: %s | [%s]" % (msql, str(params))
        
        try:
            return c.execute(msql, params).fetchall()
        except sqlite3.Error as e:
            print "ERROR: %s" % e
            return None
    
    def find_games_by_platform(self, platform, offset=None, limit=None):
        try:
            row =  self.process_sql(DB.FIND_PLATFORM_BY_NAME, (platform,), 0, 1)
            if (row):
                return self.process_sql(DB.FIND_ALL_GAMES_BY_PLATFORM, (str(row[0][0]),), offset, limit)
        except sqlite3.Error as e:
            return None
    
    def find_recently_played_games_by_platform(self, platform, offset=None, limit=None):
        try:
            row =  self.process_sql(DB.FIND_PLATFORM_BY_NAME, (platform,), 0, 1)
            if (row):
                return self.process_sql(DB.FIND_RECENTLY_PLAYED_GAMES_BY_PLATFORM, (str(row[0][0]),), offset, limit)
        except sqlite3.Error as e:
            return None
    
    def find_recently_added_games_by_platform(self, platform, offset=None, limit=None):
        try:
            row =  self.process_sql(DB.FIND_PLATFORM_BY_NAME, (platform,), 0, 1)
            if (row):
                return self.process_sql(DB.FIND_RECENTLY_ADDED_GAMES_BY_PLATFORM, (str(row[0][0]),), offset, limit)
        except sqlite3.Error as e:
            return None
        
