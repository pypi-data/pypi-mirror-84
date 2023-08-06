from localstack.utils.aws import aws_models
oKfdV=super
oKfdH=None
oKfdJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  oKfdV(LambdaLayer,self).__init__(arn)
  self.cwd=oKfdH
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.oKfdJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(RDSDatabase,self).__init__(oKfdJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(RDSCluster,self).__init__(oKfdJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(AppSyncAPI,self).__init__(oKfdJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(AmplifyApp,self).__init__(oKfdJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(ElastiCacheCluster,self).__init__(oKfdJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(TransferServer,self).__init__(oKfdJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(CloudFrontDistribution,self).__init__(oKfdJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,oKfdJ,env=oKfdH):
  oKfdV(CodeCommitRepository,self).__init__(oKfdJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
