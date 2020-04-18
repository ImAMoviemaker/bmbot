import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

data = None

def findVersionInVersionList(list, version):
  result = None
  for release in list: 
    if release['version'] == version: 
      result = release 
      break
  return result

# reload data
def reloadData():
  global data
  data = json.loads(os.popen('node ' + dir_path + '/fetch-fusion-versions').read())

# list EVERY version of a software
def allFusionVersionNames():
  return list(map(lambda release: release['version'], data['fusion']))
def allResolveVersionNames():
  return list(map(lambda release: release['version'], data['resolve']))

# list VISIBLE (last two major releases) versions of a software
def allVisibleFusionVersionNames():
  return list(map(lambda release: release['version'], filter(lambda release: release['visible'], data['fusion'])))
def allVisibleResolveVersionNames():
  return list(map(lambda release: release['version'], filter(lambda release: release['visible'], data['resolve'])))

# get version data for a specific one
def getFusionVersionData(version):
  return findVersionInVersionList(data['fusion'], version)
def getResolveVersionData(version):
  return findVersionInVersionList(data['resolve'], version)

# get latest version data for a specific one
def getFusionLatestData():
  return getFusionVersionData(data['latestFusion'])
def getResolveLatestData():
  return getResolveVersionData(data['latestResolve'])

reloadData()
