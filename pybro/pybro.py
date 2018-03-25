import sqlite3, os
from sys import platform as PLATFORM 
from datetime import datetime
from getpass import getuser

class Browser:
    __slots__ = ['name', 'cursor']

    supported_br = {"chrome" : {"win32" : [
                                            os.path.join("C:",os.sep,"Users",getuser(), "AppData","Local","Google","Chrome","User Data","ChromeDefaultData","History"),
                                            os.path.join("C:",os.sep,"Users",getuser(),"Chromium","User Data","History"),
                                            os.path.join("C:",os.sep,"Users",getuser(),"Google","Chrome SxS","User Data","History")
                                        ],
                                "darwin" : [
                                            os.path.join("Users",getuser(),"Library","Application Support","Google","Chrome","History"),
                                            os.path.join("Users",getuser(),"Library","Application Support","Google","Chrome Canary","History"),
                                            os.path.join("Users",getuser(),"Library","Application Support","Google","Chromium","History")
                                            ],
                                "linux" :  [
                                            os.path.join(os.sep, "home",getuser(),".config","google-chrome","History"),
                                            os.path.join(os.sep, "home",getuser(),".config","google-chrome-beta","History"),
                                            os.path.join(os.sep, "home",getuser(),".config","google-chrome-unstable","History"),
                                            os.path.join(os.sep, "home",getuser(),".config","chromium","History")
                                            ]
                                },
                    "firefox" : {"win32" : [
                                            os.path.join("C:",os.sep,"Users",getuser(), "AppData","Roaming","Mozilla","Firefox","Profiles")
                                            ],
                                 "darwin" : [
                                            os.path.join("Users",getuser(),"Library","Application Support","Firefox","Profiles"),
                                            os.path.join("Users",getuser(),"Library","Mozilla","Firefox","Profiles")
                                            ],
                                 "linux" : [
                                            os.path.join(os.sep, "home",getuser(),".mozilla","firefox")
                                            ]

                                }
                    } 
    
    def __init__(self, **argv):
        """
            Finds the path of browser's database file and open sqlite connection.

            Takes a keyword argument "name" to specify the browser's name to use.
            Currently supportes only "firefox" and "chrome".
            
        """
        br_name = argv.get("name", "")
        db_file = self.get_browser_hist(br_name)

        cnx = sqlite3.connect(db_file)
        self.cursor = cnx.cursor()

    def get_autoFill(self, **argv):
        """ 
            Return a list of autofill strings used in the browser.

            Takes keyword argument "max" to specify the number of results to return.
            If it's omitted or used "max=all" then, all strings will be returned.

            It supportes only chrome/chromium at the moment, other browsers will return empty list [].

        """
        limit = argv.get("max", "all")
        limit = str(limit)

        if self.name == "chrome":
            tmp_db_loc = os.path.dirname(Browser.supported_br[self.name])
            tmp_cnx = sqlite3.connect(os.path.join(tmp_db_loc, "Web Data"))
            tmp_cursor = tmp_cnx.cursor()
            sql = "select value, date_last_used from autofill limit ?"
            if limit == "all" :
                sql = "select value, date_last_used from autofill"
                tmp_cursor.execute(sql)
            else:
                tmp_cursor.execute(sql, (limit,))

            values = tmp_cursor.fetchall()
            to_return = list()
            for i in values:
                item = dict()
                item["value"] = i[0]
                item["date_last_used"] = "{}".format(datetime.fromtimestamp(i[1]).strftime('%Y-%m-%d %H:%M:%S'))
                to_return.append(item)
            tmp_cnx.close()
            return to_return
        elif self.name == "firefox":
            return []

    def get_bookmarks(self, **argv) :
        """ 
            Return a list of saved bookmarks used in the browser.

            Takes keyword argument "max" to specify the number of results to return.
            If it's omitted or used "max=all" then, all strings will be returned.

            It supportes only firefox at the moment, other browsers will return empty list [].

        """
        limit = argv.get("max", "all")
        limit = str(limit)

        if self.name == "firefox" :
            sql = "select moz_bookmarks.title, moz_places.url from moz_bookmarks join moz_places where moz_bookmarks.fk = moz_places.id limit ?"
            if limit == "all":
                sql =  "select moz_bookmarks.title, moz_places.url from moz_bookmarks join moz_places where moz_bookmarks.fk = moz_places.id "
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, (limit,))

            b_marks = self.cursor.fetchall()
            to_return = list()
            for i in b_marks :
                item = dict()
                item["title"] = i[0]
                item["url"]   = i[1]
                to_return.append(item)

            return to_return
        elif self.name == "chrome" :
            return []

    def get_keyword_search(self, **argv):
        """ 
            Return a list of keyword_search strings used in the browser.

            Takes keyword argument "max" to specify the number of results to return.
            If it's omitted or used "max=all" then, all strings will be returned.

        """
        limit = argv.get("max", "all")
        limit = str(limit)

        if self.name == "chrome" :
            sql = "select lower_term from keyword_search_terms limit ?"
            if limit == "all":
                sql =  "select lower_term from keyword_search_terms"
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, (limit,))

            keywords = self.cursor.fetchall()
            terms = list()
            for i in keywords :
                terms.append(i[0])
            return terms
        
        elif self.name == "firefox":
            sql = "select input from moz_inputhistory limit ?"
            if limit == "all":
                sql =  "select input from moz_inputhistory"
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, (limit,))

            keywords = self.cursor.fetchall()
            terms = []
            for i in keywords :
                terms.append(i[0])
            return terms

    def get_downloads(self, **argv):
        """ 
            Return a list of dict downloads of the browser.

            Takes keyword argument "max" to specify the number of results to return.
            If it's omitted or used "max=all" then, all strings will be returned.

            The dict keys are : file_name, file_type, file_size, site_url, full_url, start_time
            state (cancled, completed..), received_bytes, danger .

            It supportes only chrome/chromium at the moment, other browsers will return empty list [].

        """
        limit = argv.get("max", "all")
        limit = str(limit)

        if self.name == "chrome" :
            sql = "select target_path, start_time, end_time, received_bytes, total_bytes, state, danger_type,\
               tab_url, site_url, original_mime_type from downloads limit ?"
            if limit == "all" :
                sql = "select target_path, start_time, end_time, received_bytes, total_bytes, state, danger_type,\
               tab_url, site_url, original_mime_type from downloads"
                self.cursor.execute()
            else:
                self.cursor.execute(sql, (limit,))

            history = self.cursor.fetchall()
            downloads = list()
            for i in history :
                item = dict()
                item["file_name"]  = i[0]
                item["file_type"]  = i[9]
                item["file_size"]  = i[4]
                item["site_url"]   = i[8]
                item["full_url"]   = i[7]
                item["start_time"] = "{}".format(datetime.fromtimestamp(i[1]/1e6 - 11644473600).strftime('%Y-%m-%d %H:%M:%S'))
                
                state = i[5]
                if state == 0 :
                    item["state"] = "IN_PROGRESS"
                elif state == 1 :
                    item["state"] = "COMPLETED"
                    item["received_bytes"] = i[4] 
                    #in {} s".format((i[2]-i[1])/1e6))
                elif state == 2:
                    item["state"] = "CONCLED"
                    item["received_bytes"] = i[3]
                elif state == 4 :
                    item["state"] = "INTERRUPTED"
                    item["received_bytes"] = i[3]

                danger = ["NotDangerous", "DangerousFile", "DangerousUrl", "DangerousContent", "MaybeDangerousContent", \
                    "UncommonContent", "UserValidated", "DangerousHost", "PotentiallyUnwanted"]
                
                item["danger"] = danger[i[6]]
                downloads.append(item)

            return downloads
        
        elif self.name == "firefox":
            return []

    def get_visited_ws(self, **argv):
        """ 
            Return a list of dict of visited web sites stored in the browser.

            Takes keyword argument "max" to specify the number of results to return.
            If it's omitted or used "max=all" then, all strings will be returned.

            The dict keys are :  url, last_visit_time, nb_visits.
            
            It supportes only chrome/chromium at the moment, other browsers will return empty list [].

        """
        limit = argv.get("max", "all")
        limit = str(limit)

        if self.name == "chrome" :
            sql = "select url, visit_count, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', \
                                'localtime') from urls order by visit_count desc limit ?"
            if limit == "all" :
                sql = "select url, visit_count, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', \
                                'localtime') from urls order by visit_count desc"
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, (limit,))

            mst_visit = self.cursor.fetchall()
            to_return = list()
            for i in mst_visit :
                item = dict()
                item["url"] = i[0]
                item["last_visit_time"] = i[2]
                item["nb_visits"] = i[1]
                
                to_return.append(item)
            return to_return

        elif self.name == "firefox" :
            sql = "select host, frecency from moz_hosts order by frecency desc limit ?"
            if limit == "all" :
                sql = "select host, frecency from moz_hosts order by frecency desc"
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, (limit,))

            mst_visit = self.cursor.fetchall()
            to_return = []
            for i in mst_visit :
                item = dict()
                item["url"] = i[0]
                item["last_visit_time"] = ""
                item["nb_visits"] = i[1]
                
                to_return.append(item)
            return to_return

    def get_moz_profile(self, path):
        """ 
            Return a default profile name of mozilla firefox browser.

            Takes string as a path of where firefox stores profiles.

        """
        p = os.listdir(path)
        for i in p:
            if "default" in i:
                return i
        return p[0]

    def get_browser_hist(self, br_name):
        """ 
            Return a string of browser's database file's path.
            If browser is not supported, a ValueError exception will be raised.
            If browser database file is not found, a FileNotFoundError exception will be raised.

            Takes browser's name, if the browser name is not supported a ValueError exception will be raised.

        """
        # check if browser is supported
        if br_name.lower() not in list(Browser.supported_br.keys()) :
            raise ValueError("Not Supported Browser")
        self.name = br_name

        # look for db file for requested browser
        db_locs = Browser.supported_br[br_name][PLATFORM]
        for loc in db_locs :
            if os.path.exists(loc):
                if br_name == "firefox":
                    # add db file to full location for firefox
                    return os.path.join(loc, self.get_moz_profile(loc), "places.sqlite")
                else:
                    return loc
        # raise exception if db file is not found
        raise FileNotFoundError(br_name + " 's db file Not Found")

    @staticmethod
    def get_supported_brs():
        """
        Return a list of supported browsers.
        """
        return list(Browser.supported_br.keys())
    

if __name__ == "__main__" :

    
    br = Browser(name="chrome")
    #k = br.get_keyword_search(max=10)
    #for i in k :
    #    print(i)

    #d = br.get_downloads(max=5)
    #for item in d :
    #    print(item["file_name"])  
    #    print(item["file_type"] ) 
    #    print(item["file_size"] )
    #    print(item["site_url"]  )
    #    print(item["full_url"]   )
    #    print(item["start_time"] )
    #    print(item["state"]     )
    #    print(item["received_bytes"])  
    #    print(item["danger"])

    v = br.get_visited_ws(max=5)
    for i in v :
       print("[->] URL : " + i["url"])
       print("[->] Last Visit Time : " + i["last_visit_time"])
       print("[->] Visited {} times".format(i["nb_visits"]))
       print("=======")

    # bk = br.get_bookmarks(max=7)
    # for i in bk:
    #     print(i["title"] + " : " + i["url"])
    #     print("=====")

    # af = br.get_autoFill(max=10)
    # for i in af:
    #     print(i["value"] + " : " + i["date_last_used"])
    #     print("====")