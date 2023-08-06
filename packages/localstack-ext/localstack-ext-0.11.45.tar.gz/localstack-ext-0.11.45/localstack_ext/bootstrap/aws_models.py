from localstack.utils.aws import aws_models
RGCiW=super
RGCiE=None
RGCiH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RGCiW(LambdaLayer,self).__init__(arn)
  self.cwd=RGCiE
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.RGCiH.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(RDSDatabase,self).__init__(RGCiH,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(RDSCluster,self).__init__(RGCiH,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(AppSyncAPI,self).__init__(RGCiH,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(AmplifyApp,self).__init__(RGCiH,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(ElastiCacheCluster,self).__init__(RGCiH,env=env)
class TransferServer(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(TransferServer,self).__init__(RGCiH,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(CloudFrontDistribution,self).__init__(RGCiH,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,RGCiH,env=RGCiE):
  RGCiW(CodeCommitRepository,self).__init__(RGCiH,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
