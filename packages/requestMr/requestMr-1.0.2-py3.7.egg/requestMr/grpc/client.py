# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-10-30 14:22:19
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-10-30 15:21:36


from __future__ import print_function
import grpc
import soa_invoke_pb2
import soa_invoke_pb2_grpc
import sys
import json




def rpc(host, iface, method, requestJson):
    if isinstance(content,dict):
        pass
    elif isinstance(content,str):
        try:
            content = json.loads(content)
        except:
            raise Exception("字符串请求格式不对")
    else:
        raise Exception("非法请求格式")

    try:
        host = content.get("addr")
        iface = content.get("iface")
        method = content.get("method")
        arg0 = content.get("request").get("arg0")
    except:
        raise Exception("解析请求时,发现格式不对")

    requestJson = {"arg0": json.dumps(arg0)}



    channel = grpc.insecure_channel(host)
    stub = soa_invoke_pb2_grpc.SoaInvokerServiceStub(channel)

    soa_params = dict()
    soa_params['reqId'] = '1'
    soa_params['rpcId'] = '1'
    soa_params['iface'] = iface
    soa_params['method'] = method
    soa_params['requestJson'] = requestJson
    request = soa_invoke_pb2.SoaInvokerRequest(**soa_params)

    response = stub.call(request)
    # print(type(response))
    # print(dir(response))
    # print(response.code)
    # print('ge')
    # print(response.msg)
    # print(dir(response.resultJson))
    print(response.resultJson)
    # print(type(response.resultJson))
    print("soa result: " + str(response))

    return (response.code,response.resultJson)
    