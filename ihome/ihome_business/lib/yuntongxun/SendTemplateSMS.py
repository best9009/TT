#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome_business.lib.yuntongxun.CCPRestSDK import REST

#主帐号
accountSid= '8aaf07086a25761e016a3a6277930e72';

#主帐号Token
accountToken= '110ad5ee6f5044a6b53aab2cf5be2e4b';

#应用Id
appId='8aaf07086a25761e016a3a6277dd0e78';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort= '8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

def sendTemplateSMS(to,datas,tempId):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.sendTemplateSMS(to,datas,tempId)
    for k,v in result.items():
        
        if k=='templateSMS' :
                for k,s in v.items():
                    print ('%s:%s' % (k, s))
        else:
            print ('%s:%s' % (k, v))
    
   
#sendTemplateSMS(手机号码,内容数据,模板Id)
if __name__ == '__main__':
    sendTemplateSMS('15501079251', {'12','34'}, 1)