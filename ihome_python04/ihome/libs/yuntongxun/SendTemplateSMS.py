#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8aaf07086c282571016c514350111a9d'

#主帐号Token
accountToken= 'eb52d0dc58ea41008631c1af85ef24b3'

#应用Id
appId='8aaf07086c282571016c514350691aa4'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

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


#sendTemplateSMS(手机号码,内容数据,模板Id)
if __name__ == "__main__":
    ccp = CCP()
    ccp.send_templatesms("18850149389", ["1234", "1"], 1)