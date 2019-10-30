#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8aaf07086c282571016c514350111a9d'

#���ʺ�Token
accountToken= 'eb52d0dc58ea41008631c1af85ef24b3'

#Ӧ��Id
appId='8aaf07086c282571016c514350691aa4'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

class CCP(object):
    instance = None

    def __new__(cls):
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance

    def send_templatesms(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        status_code = result.get("status_code")
        if status_code == "000000":
            return 1
        else:
            return -1


#sendTemplateSMS(�ֻ�����,��������,ģ��Id)
if __name__ == "__main__":
    ccp = CCP()
    ccp.send_templatesms("18850149389", ["1234", "1"], 1)