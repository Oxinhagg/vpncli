import argparse
import logging
import sys

from vpncli.connectivity import wait_for_connection, wait_until_unreachable
from vpncli.cisco_any_connect import CiscoAnyConnect
from vpncli.configuration import get_config, get_path_cisco

def connect(config):
  name = config.get('name')
  test_ip = config.get(site, 'test_ip')
  logging.info(f"Connect to {name}")
  client = create_client(config)
  client.connect()
  if wait_for_connection(test_ip) == 0:
      logging.info("Connection established.")
  else:
      raise Exception(f"Could not establish connection to {name}")


def disconnect():
  logging.info("Disconnect")
  client = create_client()
  client.disconnect()
  if wait_until_unreachable(config.get(site, 'testAddress')) == 0:
      logging.info("Disconnected successfully")
  else:
      raise Exception("Could not disconnect")


def switch(config):
  name = config.get('name')
  logging.info(f"Switching to {name}")
  disconnect()
  connect(config)
  logging.info(f"Switched successfully to {name}")


def create_client(config={}):
  return CiscoAnyConnect(get_path_cisco(),
                          config.get('host_name'),
                          config.get('login'),
                          config.get('password'))


def main():
  logging.basicConfig(format=logging.BASIC_FORMAT, stream=sys.stdout, level=logging.DEBUG)
  
  parser = argparse.ArgumentParser(description='Generic VPN client command line')
  parser.add_argument('-c', dest='connect', metavar='name', help='Connect to VPN by name')
  parser.add_argument('-d', dest='disconnect', action="store_true", help='Disconnect from VPN')
  parser.add_argument('-s', dest='switch', metavar='name', help='Switch between VPN')
  
  args = parser.parse_args()
  if args.connect:
    config = get_config(args.connect)
    connect(config)
  elif args.disconnect:
    disconnect()
  elif args.switch:
    config = get_config(args.switch)
    switch(config)

if __name__ == '__main__':
  main()