# -*- coding: utf-8 -*-
"""
    cwb_weather.models

    Taiwan Central Weather Bureau opendata

    Author: hwkao
"""
import xml.etree.ElementTree as ET
import re

class WeatherBase(object):

    _TW_TRANS = {'TEMP': '溫度',
                'LAT': '緯度',
                'LON': '經度',
                'STID': '測站 ID',
                'STNM': '測站編號',
                'TIME': '未使用',
                'ELEV': '高度，單位 公尺',
                'WDIR': '風向，單位 度，一般風向 0 表示無風',
                'WDSD': '風速，單位 公尺/秒',
                'TEMP': '溫度，單位 攝氏',
                'HUMD': '相對濕度，單位 百分比率，此處以實數 0-1.0 記錄',
                'PRES': '測站氣壓，單位 百帕',
                '24R': '日累積雨量，單位 毫米',
                'H_FX': '小時瞬間最大陣風風速，單位 公尺/秒',
                'H_XD': '小時瞬間最大陣風風向，單位 度',
                'H_FXT': '小時瞬間最大陣風時間，hhmm (小時分鐘)',
                'H_F10': '本時最大 10 分鐘平均風速，單位 公尺/秒',
                'H_10D': '本時最大 10 分鐘平均風向，單位 度',
                'H_F10T': '本時最大 10分鐘平均風速發生時間，hhmm (小時分鐘)',
                'CITY': '縣市',
                'CITY_SN': '縣市編號',
                'TOWN': '鄉鎮',
                'TOWN_SN': '鄉鎮編號'}
    _EN_TRANS = {'TEMP': 'Temperature'}
    _TRANS = {'EN': _EN_TRANS, 'TW': _TW_TRANS}

    def __init__(self, report_name, xml='./weather.xml'):
        self._data = dict()
        self._report_name = report_name
        self._xml = xml

    def insert_data(self, key, value):
        self._data.setdefault(key, value)

    def get_all_data_by_country(self, country):
        """
            Return all data of a country
        """
        if country not in self.show_avail_country():
            return None

        return self._data[country]

    def get_column_data_by_country(self, country, column):
        """
            Return specific data of a country
        """
        if country not in self.show_avail_country() or column not in self.show_avail_column(country):
            return None

        return self._data[country][column]

    def show_avail_country(self):
        """
            Return a list of avaliable country.
        """
        return self._data.keys()

    def show_avail_column(self, country):
        """
            Return a list of avaliable column.
        """
        return self._data[country].keys()

    def trans_column(self, lang, column):
        """
            Return the translation of column name in specific language.
        """
        if lang not in self._TRANS.keys():
            return None

        return self._TRANS[lang][column]

    @property
    def report_name(self):
        return self._report_name

    @property
    def refresh_time(self):
        return self._refresh_time

    def __repr__(self):
        return "WeatherBase (report_name = %s)" % (self._report_name)

class WeatherObservation(WeatherBase):
    """
    局屬氣象站-現在天氣觀測報告

    Source: 氣象資料開放平台 [http://opendata.cwb.gov.tw/]
    """

    _REPORT_NAME = 'A0003-001'

    def __init__(self, lang=None):
        WeatherBase.__init__(self, self._REPORT_NAME)
        self._lang = lang
        self.refresh()

    def refresh(self):
        """ Refresh data from latest xml file"""
        self._data.clear()
        tree = ET.parse(self._xml)
        root = tree.getroot()

        prefix = re.findall("{.*}", root.tag)[0]
        self._refresh_time = root.find(prefix + 'sent').text

        for child in root.findall(prefix + 'location'):
            loc_data = dict()
            for item in child.findall(prefix + 'weatherElement'):
                column = item.find(prefix + 'elementName').text
                value = item.find(prefix + 'elementValue').find(prefix + 'value').text
                try:
                        loc_data.setdefault(column, value)
                except Exception as e:
                    raise e
            self._data.setdefault(child.find(prefix + 'locationName').text, loc_data)

    def __repr__(self):
        return self._REPORT_NAME + " 局屬氣象站-現在天氣觀測報告"
