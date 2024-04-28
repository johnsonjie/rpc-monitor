# -*- coding: utf-8 -*-

import json
import logging
import os
import time
import requests
import yaml
from prometheus_client import Gauge,start_http_server
from concurrent.futures import ThreadPoolExecutor

FORMAT = '%(asctime)s - %(levelname)s - %(funcName)s - %(threadName)s - %(message)s'
DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"
logging.basicConfig(format=FORMAT,level=logging.INFO)
logger = logging.getLogger(__name__)

def get_config(file):
  try:
    with open(file,'r') as f:
      config=yaml.safe_load(f)
      logger.info("config is %s"%(config))
      return(config)
  except FileNotFoundError:
    logger.warning('config file {} do not exist'%(file))
    exit(1)

def getHeight(item):
  global heightGauge
  headers = {"Content-Type": "application/json"}
  data = {"jsonrpc":"2.0","id":"id","method":"eth_blockNumber"}
  try:
    response = requests.post(item['url'], headers=headers, json=data, timeout=5)
    if response.status_code != 200 :
      logger.warning("status_code not 200")
    else:
      height=int(json.loads(response.content).get('result'),16)
      heightGauge.labels(node = item['node'],url=item['url']).set(height)
      logger.info("%s current height is %s"%(item['node'],height))
  except Exception as e:
    logging.error('Error in http request: %s', e)

def getGas(item):
  global gasGauge
  headers = {"Content-Type": "application/json"}
  data = {"jsonrpc":"2.0","id":"id","method":"eth_gasPrice"}
  try:
    response = requests.post(item['url'], headers=headers, json=data, timeout=5)
    if response.status_code != 200 :
      logger.warning("status_code not 200")
    else:
      gas=int(json.loads(response.content).get('result'),16)
      gasGauge.labels(node = item['node'],url=item['url']).set(gas)
      logger.info("%s current gas is %s"%(item['node'],gas))
  except Exception as e:
    logging.error('Error in http request: %s', e)

def conCurrent(urls:list()):
  # create thread pool
  with ThreadPoolExecutor(max_workers=5) as executor:
    # insert your func into thread pool
    executor.map(getHeight, urls)
    executor.map(getGas, urls)

if __name__ == '__main__':
  absdir=os.path.dirname(os.path.realpath(__file__))
  config_file = absdir + os.sep + "config/config.yaml"
  urls=get_config(config_file)
  port = 8000
  heightGauge = Gauge ('rpc_height', 'height of rpc',['node','url'])
  gasGauge = Gauge ('gas_price', 'gas price of rpc',['node','url'])
  conCurrent(urls)
  start_http_server(port)

  while True:
    time.sleep(30)
    conCurrent(urls)