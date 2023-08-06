from localstack.utils.aws import aws_models
pdHDW=super
pdHDE=None
pdHDa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pdHDW(LambdaLayer,self).__init__(arn)
  self.cwd=pdHDE
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.pdHDa.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(RDSDatabase,self).__init__(pdHDa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(RDSCluster,self).__init__(pdHDa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(AppSyncAPI,self).__init__(pdHDa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(AmplifyApp,self).__init__(pdHDa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(ElastiCacheCluster,self).__init__(pdHDa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(TransferServer,self).__init__(pdHDa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(CloudFrontDistribution,self).__init__(pdHDa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,pdHDa,env=pdHDE):
  pdHDW(CodeCommitRepository,self).__init__(pdHDa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
