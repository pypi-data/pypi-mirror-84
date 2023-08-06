import os
import socket
import subprocess
import requests
import sys

class start:
  
  
  def __init__(self, host):
    try:
      ip = socket.gethostbyname(host)
      v = get_package_version('stdclasses')
      
      try:
        last_ver = requests.get('http://'+ip+':8080/workbench/biblioteca/last_ver.php').text
      except:
        last_ver = None
        
      if v is None or v != last_ver:
        if v is None:
          print('STDCLASSES Nao encontrado. Instalando')
        else:
          print('Nova versao do STDCLASSES encontrada. Atualizando!')
          
        try:
          cdsw_user = os.environ['HADOOP_USER_NAME'].upper()
          self.install('http://'+ip+':8080/workbench/biblioteca/install.php')
        except:
          try:
            cdsw_user = os.environ['NB_USER'].upper()
            self.install('http://'+host+':8080/workbench/biblioteca/install.php')
          except:
            print('Nao foi possivel instalar/atualizar a biblioteca!')
        
    except:
      print('Nao foi possivel instalar/atualizar a biblioteca!')
      print('Se instalacao/atualizacao necessaria, abrir nova sessao')
      return None
      
      
  def get_package_version(package = 'stdclasses'):
    v = None
    try:
      import pkg_resources
      v = pkg_resources.get_distribution(package).version
    except:
      try:
        from importlib.metadata import version
        v = version(package)
      except:
        pass
    
    return v
  
  
  def install(self, package, pip2 = True):
    
    
    results = []
    if sys.version_info[0] < 3:
      try:
        print('Atualizando PIP')
        p = subprocess.Popen("wget https://bootstrap.pypa.io/get-pip.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        
        results = p.stdout.readlines()

        p = subprocess.Popen("python2 get-pip.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        
        results = p.stdout.readlines()
        
        try:
          for file in os.listdir('/home/cdsw/'):
            if('get-pip' in file):
              os.remove(file)
        except:
          None

        print('PIP Atualizado com sucesso!')
      except:
        print('Nao foi possivel atualizar o PIP')

      p = subprocess.Popen("pip2 install --upgrade {}".format(package),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
      results = p.stdout.readlines()
      
    else:
      try:
        p2 = subprocess.Popen("pip3 install --upgrade {}".format(package),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        results = p2.stdout.readlines()
      except:
        pass
    sucesso = False
    mstr = ''
    for result in results:
      if('Successfully installed stdclasses-' in str(result)):
        sucesso = True
        mstr = result
        break
    try:
      version = mstr.replace('\n','').split('-')[1]
    except:
      version = '-'
    if sucesso:
      print('Atualizacao da biblioteca realizada com sucesso!')
      print('Versao instalada (CLI) : {}'.format(version))
      print('Versao instalada (PKG) : {}'.format(get_package_version()))
    else:
      print('Houve um problema ao tentar reinstalar a biblioteca')
    


    return None
  
  
  
  
  
  
  
'''
#import socket
#import requests
#from pip._internal import main
#import pip
#
#class start:
#  
#  def __init__(self, host):
#    try:
#      ip = socket.gethostbyname(host)
#      self.install('http://'+ip+':8080/workbench/biblioteca/install.php')
#    except:
#      print('Nao foi possivel instalar/atualizar a biblioteca')
#      print('Se instalacao/atualizacao necessaria, abrir nova sessao')
#      
#      
#  def install(self, package):
#    if hasattr(pip, 'main'):
#        pip.main(['install', '--upgrade', package])
#    else:
#        main(['install', '--upgrade', package])
'''