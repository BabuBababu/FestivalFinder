from xml.dom.minidom import parseString
import urllib.request
from xml.etree import ElementTree

locations = ['서울특별시', '인천광역시', '대전광역시', '대구광역시', '울산광역시', '부산광역시', '광주광역시', '세종특별자치시',
             '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도']

chargingStations=[set() for i in range(len(locations))]

class Data:
    def __init__(self, address, stationID, stationName, lat, lng, useTime, type, stat):
        self.address = address
        self.stationID = stationID
        self.stationName = stationName
        self.lat = lat
        self.lng = lng
        self.useTime = useTime
        self.type = type  # 충전기 타입
        # (01:DC 차데모,
        # 03: DC 차데모+AC 3상,
        # 06: DC 차데모+AC 3상
        # +DC 콤보)
        self.stat = stat  # 충전기
        # 1. 통신이상
        # 2. 충전대기
        # 3. 충전중
        # 4. 운영중지
        # 5. 점검중

    def printData(self):
        print("지역:{0}\t충전소 이름:{1},\t충전소 ID:{2}\t경도:{3}\t위도:{4}\t사용가능시간:{5}".format(self.address, self.stationName,
                                                                                    self.stationID,
                                                                                    self.lng, self.lat, self.useTime))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.address == other.address and self.stationID == other.stationID and self.stationName == other.stationName

    def __hash__(self):
        return hash((self.address, self.stationID, self.stationName))

    # 위 두 함수는 셋에서 중복제거에 필요한 정보를 제공해줍니다.


xmlDocument = None

url = "http://open.ev.or.kr:8080/openapi/services/rest/EvChargerService?serviceKey=s%2F5nW%2BMXFPVjfdX5Mg0Z4Uo3OOmT0coY0%2BqBfxFYBQjNX%2FoVB0AmdMf1HOwQjTTybjApkg6F3V0vzqIzomndFQ%3D%3D"


def createXmlDoc():
    global xmlDocument
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    responseBody = resp.read()
    xmlDocument = parseString(responseBody.decode('utf-8'))


def parseStationInfo():
    global xmlDocument
    tree = ElementTree.fromstring(xmlDocument.toxml())
    items = tree.getiterator("item")

    for i in range(len(locations)):
        for item in items:
            address = item.find("addrDoro")
            if locations[i] in address.text:  # 여기에 원하는 지역을 입력하면 해당 지역의 충전소를 셋에 집어넣습니다.
                stationID = item.find("statId")  # 셋에 집어넣는 이유는 중복된 데이터가 다수 존재하기 때문입니다.
                stationName = item.find("statNm")  # 충전기 타입과 충전기상태는 제외했지만 언제든지 추가 가능합니다.
                lat = item.find("lat")  # chgerType: 충전기타입, stat: 충전기 상태
                lng = item.find("lng")
                useTime = item.find("useTime")
                chgerType = item.find("chgerType")
                stat = item.find("stat")
                chargingStations[i].add(Data(address.text, stationID.text, stationName.text, lng.text, lat.text, useTime.text,
                         chgerType.text, stat.text))
    print("complete")

def printSeoulData():
    for i in chargingStations[0]:
        i.printData()

def deleteDoc():
    global xmlDocument
    del xmlDocument
