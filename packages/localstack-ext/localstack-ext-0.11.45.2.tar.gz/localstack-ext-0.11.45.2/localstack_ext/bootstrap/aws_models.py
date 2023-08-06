from localstack.utils.aws import aws_models
wJBDk=super
wJBDr=None
wJBDa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  wJBDk(LambdaLayer,self).__init__(arn)
  self.cwd=wJBDr
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.wJBDa.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(RDSDatabase,self).__init__(wJBDa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(RDSCluster,self).__init__(wJBDa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(AppSyncAPI,self).__init__(wJBDa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(AmplifyApp,self).__init__(wJBDa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(ElastiCacheCluster,self).__init__(wJBDa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(TransferServer,self).__init__(wJBDa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(CloudFrontDistribution,self).__init__(wJBDa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,wJBDa,env=wJBDr):
  wJBDk(CodeCommitRepository,self).__init__(wJBDa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
