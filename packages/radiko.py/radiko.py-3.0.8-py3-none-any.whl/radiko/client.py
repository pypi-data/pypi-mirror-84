import base64
import datetime
import time
import threading
import xml.etree.ElementTree as ET

import m3u8
import requests


class AuthError(Exception):
    """認証失敗を知らせる例外クラス
    """
    pass


class CannotGetError(Exception):
    """HTTPリクエストに失敗したことを知らせる例外クラス
    """
    pass


class NotSelectedError(Exception):
    """局が選択されていないことを知らせる例外クラス
    """
    pass


_authKey = b'bcd151073c03b352e1ef2fd66c32209da9ca0afa'

_URL_AUTH1 = 'https://radiko.jp/v2/api/auth1'
_URL_AUTH2 = 'https://radiko.jp/v2/api/auth2'
_URL_PROGRAM = 'https://radiko.jp/v3/program/date/{date}/{area}.xml'
_URL_GET_LIST = 'http://f-radiko.smartstream.ne.jp/{st}/_definst_/' \
                + 'simul-stream.stream/playlist.m3u8'


def get_partial_key(r):
    offset = int(r.headers["X-Radiko-KeyOffset"])
    length = int(r.headers["X-Radiko-KeyLength"])
    return base64.b64encode(_authKey[offset: offset + length])


def get_date(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    if dt.hour < 5:
        dt -= datetime.timedelta(days=1)
    return dt.strftime("%Y%m%d")


class Client:
    """RadikoAPIにアクセスするためのクライアントクラス
    """

    def auto_reload(self):
        t = threading.currentThread()
        while self.auto_reloading:
            start = datetime.datetime.now()
            target = datetime.datetime(year=start.year, month=start.month, day=start.day, hour=5, minute=0)
            if start >= target:
                target += datetime.timedelta(days=1)
            duration = target - start
            time.sleep(duration.total_seconds())
            self.get_stations()

    def __init__(self):
        """
        
        Raise:
            AuthError:　認証に失敗した場合に発生
        """
        self.area = None
        self.headers = {
            'x-radiko-app': 'pc_html5',
            'x-radiko-app-version': '0.0.1',
            'x-radiko-user': 'dummy_user',
            'x-radiko-device': 'pc',
            'x-radiko-authtoken': '',
            'x-radiko-partialkey': '',
        }
        self.stations = []
        self.select = None

        r = requests.get(_URL_AUTH1, headers=self.headers)
        if r.status_code != 200:
            raise AuthError("認証1に失敗")
        self.headers["x-radiko-authtoken"] = r.headers["X-RADIKO-AUTHTOKEN"]
        self.headers["x-radiko-partialkey"] = get_partial_key(r)

        r = requests.get(_URL_AUTH2, headers=self.headers)
        if r.status_code != 200:
            print(r.content)
            raise AuthError("認証2に失敗")
        self.area = r.content.decode().split(',')[0]
        self.auto_reloading = True
        self.get_stations()
        self.thread = []
        t = threading.Thread(name="auto_reload", target=self.auto_reload)
        t.setDaemon(True)
        t.start()

    def get_stations(self):
        """受信可能な局一覧を取得する関数
        
        Raises:
            CannotGetError: リクエストに失敗した場合に発生

        Returns:
            List: 受信可能な局のリスト
        """
        r = requests.get(_URL_PROGRAM.format(date=get_date(), area=self.area), headers=self.headers)
        if r.status_code != 200:
            raise CannotGetError("取得に失敗しました")
        x_program = ET.fromstring(r.content.decode())
        x_stations = x_program.find("stations").findall("station")
        for x_station in x_stations:
            station = Station(x_station)
            for i in range(len(self.stations)):
                if self.stations[i].id == station.id:
                    self.stations[i] = station
                    break
            else:
                self.stations.append(station)
        return self.stations[:]
    
    def get_stream(self, identifier=None):
        """放送のストリームURLを取得する関数

        identifierを指定しない場合はすでに選択されている局のストリームを返す

        Args:
            identifier (:obj:str, optional): 局のidまたはidxまたは名前
        
        Raises:
            NotSelectedError: 局が選択されていない場合に発生
            CannotGetError: リクエストに失敗した場合に発生

        Returns:
            str: ストリームURL
        """
        if identifier != None:
            self.select_station(identifier)
        if self.select == None:
            raise NotSelectedError("局が選択されていません")
        r = requests.get(_URL_GET_LIST.format(st=self.select.id), headers=self.headers)
        if r.status_code != 200:
            raise CannotGetError("取得に失敗しました")
        m3u8_obj = m3u8.loads(r.content.decode())
        return m3u8_obj.playlists[0].uri

    def select_station(self, identifier=None):
        """局を選択する関数

        Args:
            identifier (str): 局のidまたはidxまたは名前
        
        Returns:
            Station: 現在選択されている局
        """
        if type(identifier) == str:
            if identifier.isdecimal():
                identifier = int(identifier)
        if type(identifier) == int:
            idx = identifier
            if 0 <= idx < len(self.stations):
                self.select = self.stations[idx]
                return self.select
        elif type(identifier) == Station:
            self.select == identifier
            return
        elif type(identifier) == str:
            for station in self.stations:
                if identifier == station.id:
                    self.select = station
                    return
                elif identifier == station.name:
                    self.select = station
                    return self.select
        return self.select


class Station:
    """局を表すクラス
    """

    def __init__(self, x_station):
        self.progs = []
        self.id = x_station.attrib["id"]
        self.name = x_station.find("name").text
        self.load_programs(x_station.find("progs"))

    def load_programs(self, x_progs):
        for x_prog in x_progs.findall("prog"):
            self.progs.append(Prog(x_prog))

    def get_on_air(self, dt=None):
        """放送中の番組を返す関数

        指定したdatetimeで放送中の番組を返す.
        指定しない場合は現在時刻が指定される.

        Args:
            dt (:obj:`datetime.datetime`, optional): 日時

        Return:
            Prog: 放送中の番組

        Note:
            翌日の動作について保証しない
        """
        if dt is None:
            dt = datetime.datetime.now()
        for prg in self.progs:
            if prg.is_on_air(dt):
                return prg
        return None


class Prog:
    """番組を表すクラス
    """

    def __init__(self, x_prg):
        self.id = x_prg.attrib["id"]
        self.master_id = x_prg.attrib["master_id"]
        self.ft = datetime.datetime.strptime(x_prg.attrib["ft"][0:12], "%Y%m%d%H%M")
        self.to = datetime.datetime.strptime(x_prg.attrib["to"][0:12], "%Y%m%d%H%M")
        self.title = x_prg.find("title").text
        self.url = x_prg.find("url").text
        self.pfm = x_prg.find("pfm").text
        self.img = x_prg.find("img").text

    def is_on_air(self, dt=None):
        """番組が放送中かどうかを返す関数

        指定したdatetimeで放送中の番組を返す.
        指定しない場合は現在時刻が指定される.

        Args:
            dt (:obj:`datetime.datetime`, optional): 日時

        Returns:
            bool: Trueなら放送中
        """
        if dt is None:
            dt = datetime.datetime.now()
        return self.ft <= dt < self.to

if __name__ == "__main__":
    client = Client()
    print(client.get_stream(0))
    input()
