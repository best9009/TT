#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome_business.lib.yuntongxun.CCPRestSDK import REST

#���ʺ�
accountSid= '8aaf07086a25761e016a3a6277930e72';

#���ʺ�Token
accountToken= '110ad5ee6f5044a6b53aab2cf5be2e4b';

#Ӧ��Id
appId='8aaf07086a25761e016a3a6277dd0e78';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort= '8883';

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

def sendTemplateSMS(to,datas,tempId):

    
    #��ʼ��REST SDK
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
    
   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)
if __name__ == '__main__':
    sendTemplateSMS('15501079251', {'12','34'}, 1)