from localstack.utils.aws import aws_models
CcOzf=super
CcOzP=None
CcOzB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CcOzf(LambdaLayer,self).__init__(arn)
  self.cwd=CcOzP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CcOzB.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(RDSDatabase,self).__init__(CcOzB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(RDSCluster,self).__init__(CcOzB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(AppSyncAPI,self).__init__(CcOzB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(AmplifyApp,self).__init__(CcOzB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(ElastiCacheCluster,self).__init__(CcOzB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(TransferServer,self).__init__(CcOzB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(CloudFrontDistribution,self).__init__(CcOzB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CcOzB,env=CcOzP):
  CcOzf(CodeCommitRepository,self).__init__(CcOzB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
