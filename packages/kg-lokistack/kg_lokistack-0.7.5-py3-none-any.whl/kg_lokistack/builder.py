from typing import Optional, Sequence

from kg_grafana import GrafanaBuilder, GrafanaOptions
from kubragen import KubraGen
from kubragen.builder import Builder
from kubragen.configfile import ConfigFileRenderMulti, ConfigFileRender_Yaml, ConfigFileRender_RawStr
from kubragen.data import ValueData
from kubragen.exception import InvalidParamError, InvalidNameError, OptionError
from kubragen.helper import LiteralStr, QuotedStr
from kubragen.kdatahelper import KDataHelper_Volume
from kubragen.object import ObjectItem, Object
from kubragen.types import TBuild, TBuildItem

from .lokiconfigfile import LokiConfigFile
from .option import LokiStackOptions
from .promtailconfigfile import PromtailConfigFile, PromtailConfigFileExt_Kubernetes


class LokiStackBuilder(Builder):
    """
    Loki Stack builder.

    Based on `Install Loki with Helm <https://grafana.com/docs/loki/latest/installation/helm/>`_.

    .. list-table::
        :header-rows: 1

        * - build
          - description
        * - BUILD_ACCESSCONTROL
          - creates service account, roles, and roles bindings
        * - BUILD_CONFIG
          - creates ConfigMap and Secret
        * - BUILD_SERVICE
          - creates deployments and services

    .. list-table::
        :header-rows: 1

        * - build item
          - description
        * - BUILDITEM_CONFIG
          - ConfigMap
        * - BUILDITEM_CONFIG_SECRET
          - Secret
        * - BUILDITEM_SERVICE_ACCOUNT
          - ServiceAccount
        * - BUILDITEM_PROMTAIL_CLUSTER_ROLE
          - Promtail ClusterRole
        * - BUILDITEM_PROMTAIL_CLUSTER_ROLE_BINDING
          - Promtail ClusterRoleBinding
        * - BUILDITEM_PROMTAIL_DAEMONSET
          - Promtail Daemonset
        * - BUILDITEM_LOKI_SERVICE_HEADLESS
          - Loki Service Headless
        * - BUILDITEM_LOKI_SERVICE
          - Loki Service
        * - BUILDITEM_LOKI_STATEFULSET
          - Loki StatefulSet
        * - BUILDITEM_GRAFANA_DEPLOYMENT
          - Grafana Deployment
        * - BUILDITEM_GRAFANA_SERVICE
          - Grafana Service

    .. list-table::
        :header-rows: 1

        * - object name
          - description
          - default value
        * - config
          - ConfigMap
          - ```<basename>-config```
        * - config-secret
          - Secret
          - ```<basename>-config-secret```
        * - service-account
          - ServiceAccount
          - ```<basename>```
        * - promtail-cluster-role
          - Promtail cluster role
          - ```<basename>-promtail```
        * - promtail-cluster-role-binding
          - Promtail cluster role binding
          - ```<basename>-promtail```
        * - promtail-daemonset
          - Promtail DaemonSet
          - ```<basename>-promtail```
        * - promtail-pod-label-app
          - Promtail label *app* to be used by selection
          - ```<basename>-promtail```
        * - loki-service-headless
          - Loki Service headless
          - ```<basename>-loki-headless```
        * - loki-service
          - Loki Service
          - ```<basename>-loki```
        * - loki-statefulset
          - Loki StatefulSet
          - ```<basename>-loki```
        * - loki-pod-label-app
          - Loki label *app* to be used by selection
          - ```<basename>-loki```
        * - grafana-service
          - Grafana Service
          - ```<basename>-grafana```
        * - grafana-deployment
          - Grafana Deployment
          - ```<basename>-grafana```
    """
    options: LokiStackOptions
    lokiconfigfile: Optional[str]
    promtailconfigfile: Optional[str]
    _namespace: str

    granana_config: Optional[GrafanaBuilder]

    SOURCE_NAME = 'kg_lokistack'

    BUILD_ACCESSCONTROL: TBuild = 'accesscontrol'
    BUILD_CONFIG: TBuild = 'config'
    BUILD_SERVICE: TBuild = 'service'

    BUILDITEM_CONFIG: TBuildItem = 'config'
    BUILDITEM_CONFIG_SECRET: TBuildItem = 'config-secret'
    BUILDITEM_SERVICE_ACCOUNT: TBuildItem = 'service-account'
    BUILDITEM_PROMTAIL_CLUSTER_ROLE: TBuildItem = 'promtail-cluster-role'
    BUILDITEM_PROMTAIL_CLUSTER_ROLE_BINDING: TBuildItem = 'promtail-cluster-role-binding'
    BUILDITEM_PROMTAIL_DAEMONSET: TBuildItem = 'promtail-daemonset'
    BUILDITEM_LOKI_SERVICE_HEADLESS: TBuildItem = 'loki-service-headless'
    BUILDITEM_LOKI_SERVICE: TBuildItem = 'loki-service'
    BUILDITEM_LOKI_STATEFULSET: TBuildItem = 'loki-statefulset'
    BUILDITEM_GRAFANA_DEPLOYMENT: TBuildItem = 'grafana-deployment'
    BUILDITEM_GRAFANA_SERVICE: TBuildItem = 'grafana-service'

    def __init__(self, kubragen: KubraGen, options: Optional[LokiStackOptions] = None):
        super().__init__(kubragen)
        if options is None:
            options = LokiStackOptions()
        self.options = options
        self.lokiconfigfile = None
        self.promtailconfigfile = None

        self._namespace = self.option_get('namespace')

        if self.option_get('config.authorization.serviceaccount_create') is not False:
            serviceaccount_name = self.basename()
        else:
            serviceaccount_name = self.option_get('config.authorization.serviceaccount_use')
            if serviceaccount_name == '':
                serviceaccount_name = None

        if self.option_get('config.authorization.roles_bind') is not False:
            if serviceaccount_name is None:
                raise InvalidParamError('To bind roles a service account is required')

        if self.option_get('enable.grafana') is not False:
            try:
                self.granana_config = GrafanaBuilder(kubragen=kubragen, options=GrafanaOptions({
                    'basename': self.basename('-grafana'),
                    'namespace': self.namespace(),
                    'config': {
                        'install_plugins': self.option_get('config.grafana_install_plugins'),
                        'service_port': self.option_get('config.grafana_service_port'),
                        'provisioning': {
                            'datasources': self.option_get('config.grafana_provisioning.datasources'),
                            'plugins': self.option_get('config.grafana_provisioning.plugins'),
                            'dashboards': self.option_get('config.grafana_provisioning.dashboards'),
                        },
                    },
                    'kubernetes': {
                        'volumes': {
                            'data': self.option_get('kubernetes.volumes.grafana-data'),
                        },
                        'resources': {
                            'deployment': self.option_get('kubernetes.resources.grafana-deployment'),
                        },
                    },
                }))
            except OptionError as e:
                raise OptionError('Grafana option error: {}'.format(str(e))) from e
            except TypeError as e:
                raise OptionError('Grafana type error: {}'.format(str(e))) from e
        else:
            self.granana_config = None

        self.object_names_update({
            'config': self.basename('-config'),
            'config-secret': self.basename('-config-secret'),
            'service-account': serviceaccount_name,
            'promtail-cluster-role': self.basename('-promtail'),
            'promtail-cluster-role-binding': self.basename('-promtail'),
            'promtail-daemonset': self.basename('-promtail'),
            'promtail-pod-label-app': self.basename('-promtail'),
            'loki-service-headless': self.basename('-loki-headless'),
            'loki-service': self.basename('-loki'),
            'loki-statefulset': self.basename('-loki'),
            'loki-pod-label-app': self.basename('-loki'),
        })

        if self.option_get('enable.grafana') is not False:
            self.object_names_update({
                'grafana-deployment': self.granana_config.object_name('deployment'),
                'grafana-service': self.granana_config.object_name('service'),
            })

    def option_get(self, name: str):
        return self.kubragen.option_root_get(self.options, name)

    def basename(self, suffix: str = ''):
        return '{}{}'.format(self.option_get('basename'), suffix)

    def namespace(self):
        return self._namespace

    def build_names(self) -> Sequence[TBuild]:
        return [self.BUILD_ACCESSCONTROL, self.BUILD_CONFIG, self.BUILD_SERVICE]

    def build_names_required(self) -> Sequence[TBuild]:
        ret = [self.BUILD_CONFIG, self.BUILD_SERVICE]
        if self.option_get('config.authorization.serviceaccount_create') is not False or \
                self.option_get('config.authorization.roles_create') is not False:
            ret.append(self.BUILD_ACCESSCONTROL)
        return ret

    def builditem_names(self) -> Sequence[TBuildItem]:
        return [
            self.BUILDITEM_CONFIG,
            self.BUILDITEM_CONFIG_SECRET,
            self.BUILDITEM_SERVICE_ACCOUNT,
            self.BUILDITEM_PROMTAIL_CLUSTER_ROLE,
            self.BUILDITEM_PROMTAIL_CLUSTER_ROLE_BINDING,
            self.BUILDITEM_PROMTAIL_DAEMONSET,
            self.BUILDITEM_LOKI_SERVICE_HEADLESS,
            self.BUILDITEM_LOKI_SERVICE,
            self.BUILDITEM_LOKI_STATEFULSET,
            self.BUILDITEM_GRAFANA_DEPLOYMENT,
            self.BUILDITEM_GRAFANA_SERVICE,
        ]

    def internal_build(self, buildname: TBuild) -> Sequence[ObjectItem]:
        if buildname == self.BUILD_ACCESSCONTROL:
            return self.internal_build_accesscontrol()
        elif buildname == self.BUILD_CONFIG:
            return self.internal_build_config()
        elif buildname == self.BUILD_SERVICE:
            return self.internal_build_service()
        else:
            raise InvalidNameError('Invalid build name: "{}"'.format(buildname))

    def internal_build_accesscontrol(self) -> Sequence[ObjectItem]:
        ret = []

        if self.option_get('config.authorization.serviceaccount_create') is not False:
            ret.extend([
                Object({
                    'apiVersion': 'v1',
                    'kind': 'ServiceAccount',
                    'metadata': {
                        'name': self.object_name('service-account'),
                        'namespace': self.namespace(),
                    }
                }, name=self.BUILDITEM_SERVICE_ACCOUNT, source=self.SOURCE_NAME, instance=self.basename()),
            ])

        if self.option_get('config.authorization.roles_create') is not False:
            ret.extend([
                Object({
                    'kind': 'ClusterRole',
                    'apiVersion': 'rbac.authorization.k8s.io/v1',
                    'metadata': {
                        'name': self.object_name('promtail-cluster-role'),
                    },
                    'rules': [{
                        'apiGroups': [''],
                        'resources': ['nodes',
                                      'nodes/proxy',
                                      'services',
                                      'endpoints',
                                      'pods'],
                        'verbs': ['get', 'watch', 'list']
                    }]
                }, name=self.BUILDITEM_PROMTAIL_CLUSTER_ROLE, source=self.SOURCE_NAME, instance=self.basename()),
            ])

        if self.option_get('config.authorization.roles_bind') is not False:
            ret.extend([
                Object({
                    'kind': 'ClusterRoleBinding',
                    'apiVersion': 'rbac.authorization.k8s.io/v1beta1',
                    'metadata': {
                        'name': self.object_name('promtail-cluster-role-binding'),
                    },
                    'subjects': [{
                        'kind': 'ServiceAccount',
                        'name': self.object_name('service-account'),
                        'namespace': self.namespace(),
                    }],
                    'roleRef': {
                        'apiGroup': 'rbac.authorization.k8s.io',
                        'kind': 'ClusterRole',
                        'name': self.object_name('promtail-cluster-role'),
                    }
                }, name=self.BUILDITEM_PROMTAIL_CLUSTER_ROLE_BINDING, source=self.SOURCE_NAME, instance=self.basename())
            ])

        return ret

    def internal_build_config(self) -> Sequence[ObjectItem]:
        ret = []

        ret.append(Object({
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': self.object_name('config'),
                'namespace': self.namespace(),
            },
            'data': {
                'promtail.yaml': LiteralStr(self.promtail_configfile_get()),
            }
        }, name=self.BUILDITEM_CONFIG, source=self.SOURCE_NAME, instance=self.basename()))

        ret.append(Object({
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {
                'name': self.object_name('config-secret'),
                'namespace': self.namespace(),
            },
            'type': 'Opaque',
            'data': {
                'loki.yaml': self.kubragen.secret_data_encode(self.loki_configfile_get()),
            }
        }, name=self.BUILDITEM_CONFIG_SECRET, source=self.SOURCE_NAME, instance=self.basename()))

        return ret

    def internal_build_service(self) -> Sequence[ObjectItem]:
        ret = []

        ret.extend([
            Object({
                'apiVersion': 'v1',
                'kind': 'Service',
                'metadata': {
                    'name': self.object_name('loki-service-headless'),
                    'namespace': self.namespace(),
                    'labels': {
                        'app': self.object_name('loki-pod-label-app'),
                    }
                },
                'spec': {
                    'clusterIP': 'None',
                    'ports': [{
                        'port': self.option_get('config.loki_service_port'),
                        'protocol': 'TCP',
                        'name': 'http-metrics',
                        'targetPort': 'http-metrics'
                    }],
                    'selector': {
                        'app': self.object_name('loki-pod-label-app'),
                    }
                }
            }, name=self.BUILDITEM_LOKI_SERVICE_HEADLESS, source=self.SOURCE_NAME, instance=self.basename()),
            Object({
                'apiVersion': 'v1',
                'kind': 'Service',
                'metadata': {
                    'name': self.object_name('loki-service'),
                    'namespace': self.namespace(),
                    'labels': {
                        'app': self.object_name('loki-pod-label-app'),
                    },
                },
                'spec': {
                    'type': 'ClusterIP',
                    'ports': [{
                        'port': self.option_get('config.loki_service_port'),
                        'protocol': 'TCP',
                        'name': 'http-metrics',
                        'targetPort': 'http-metrics'
                    }],
                    'selector': {
                        'app': self.object_name('loki-pod-label-app'),
                    },
                }
            }, name=self.BUILDITEM_LOKI_SERVICE, source=self.SOURCE_NAME, instance=self.basename()),
            Object({
                'apiVersion': 'apps/v1',
                'kind': 'DaemonSet',
                'metadata': {
                    'name': self.object_name('promtail-daemonset'),
                    'namespace': self.namespace(),
                    'labels': {
                        'app': self.object_name('promtail-pod-label-app'),
                    },
                },
                'spec': {
                    'selector': {
                        'matchLabels': {
                            'app': self.object_name('promtail-pod-label-app'),
                        }
                    },
                    'template': {
                        'metadata': {
                            'labels': {
                                'app': self.object_name('promtail-pod-label-app'),
                            },
                            'annotations': ValueData({
                                'prometheus.io/scrape': QuotedStr('true'),
                                'prometheus.io/port': QuotedStr('http-metrics'),
                            }, enabled=self.option_get('config.prometheus_annotation') is not False),
                        },
                        'spec': {
                            'serviceAccountName': self.object_name('service-account'),
                            'containers': [{
                                'name': 'promtail',
                                'image': self.option_get('container.promtail'),
                                'args': [
                                    '-config.file=/etc/promtail/promtail.yaml',
                                    '-client.url=http://{}:{}/loki/api/v1/push'.format(
                                        self.object_name('loki-service'), self.option_get('config.loki_service_port'))
                                ],
                                'volumeMounts': [{
                                    'name': 'config',
                                    'mountPath': '/etc/promtail'
                                },
                                {
                                    'name': 'run',
                                    'mountPath': '/run/promtail'
                                },
                                {
                                    'mountPath': '/var/lib/docker/containers',
                                    'name': 'docker',
                                    'readOnly': True
                                },
                                {
                                    'mountPath': '/var/log/pods',
                                    'name': 'pods',
                                    'readOnly': True
                                }],
                                'env': [{
                                    'name': 'HOSTNAME',
                                    'valueFrom': {
                                        'fieldRef': {
                                            'fieldPath': 'spec.nodeName'
                                        }
                                    },
                                }],
                                'ports': [{
                                    'containerPort': 3101,
                                    'name': 'http-metrics'
                                }],
                                'securityContext': {
                                    'readOnlyRootFilesystem': True,
                                    'runAsGroup': 0,
                                    'runAsUser': 0
                                },
                                'readinessProbe': {
                                    'failureThreshold': 5,
                                    'httpGet': {
                                        'path': '/ready',
                                        'port': 'http-metrics'
                                    },
                                    'initialDelaySeconds': 10,
                                    'periodSeconds': 10,
                                    'successThreshold': 1,
                                    'timeoutSeconds': 1
                                },
                                'resources': ValueData(
                                    value=self.option_get('kubernetes.resources.promtail-daemonset'),
                                    disabled_if_none=True),
                            }],
                            'tolerations': [{
                                'effect': 'NoSchedule',
                                'key': 'node-role.kubernetes.io/master',
                                'operator': 'Exists'
                            }],
                            'volumes': [{
                                'name': 'config',
                                'configMap': {
                                    'name': self.object_name('config'),
                                    'items': [{
                                        'key': 'promtail.yaml',
                                        'path': 'promtail.yaml',
                                    }]
                                }
                            },
                            {
                                'name': 'run',
                                'hostPath': {
                                    'path': '/run/promtail'
                                }
                            },
                            {
                                'hostPath': {
                                    'path': '/var/lib/docker/containers'
                                },
                                'name': 'docker'
                            },
                            {
                                'hostPath': {
                                    'path': '/var/log/pods'
                                },
                                'name': 'pods'
                            }]
                        }
                    }
                }
            }, name=self.BUILDITEM_PROMTAIL_DAEMONSET, source=self.SOURCE_NAME, instance=self.basename()),
            Object({
                'apiVersion': 'apps/v1',
                'kind': 'StatefulSet',
                'metadata': {
                    'name': self.object_name('loki-statefulset'),
                    'namespace': self.namespace(),
                    'labels': {
                        'app': self.object_name('loki-pod-label-app'),
                    },
                },
                'spec': {
                    'podManagementPolicy': 'OrderedReady',
                    'replicas': 1,
                    'selector': {
                        'matchLabels': {
                            'app': self.object_name('loki-pod-label-app'),
                        }
                    },
                    'serviceName': self.object_name('loki-service-headless'),
                    'updateStrategy': {
                        'type': 'RollingUpdate'
                    },
                    'template': {
                        'metadata': {
                            'labels': {
                                'app': self.object_name('loki-pod-label-app'),
                            },
                            'annotations': ValueData({
                                'prometheus.io/scrape': QuotedStr('true'),
                                'prometheus.io/port': QuotedStr('http-metrics'),
                            }, enabled=self.option_get('config.prometheus_annotation') is not False),
                        },
                        'spec': {
                            'serviceAccountName': self.object_name('service-account'),
                            'securityContext': {
                                'fsGroup': 10001,
                                'runAsGroup': 10001,
                                'runAsNonRoot': True,
                                'runAsUser': 10001
                            },
                            'containers': [{
                                'name': 'loki',
                                'image': self.option_get('container.loki'),
                                'args': [
                                    '-config.file=/etc/loki/loki.yaml'
                                ],
                                'volumeMounts': [{
                                    'name': 'config',
                                    'mountPath': '/etc/loki'
                                },
                                {
                                    'name': 'storage',
                                    'mountPath': '/data',
                                    'subPath': None
                                }],
                                'ports': [{
                                    'name': 'http-metrics',
                                    'containerPort': 3100,
                                    'protocol': 'TCP'
                                }],
                                'livenessProbe': {
                                    'httpGet': {
                                        'path': '/ready',
                                        'port': 'http-metrics'
                                    },
                                    'initialDelaySeconds': 45
                                },
                                'readinessProbe': {
                                    'httpGet': {
                                        'path': '/ready',
                                        'port': 'http-metrics'
                                    },
                                    'initialDelaySeconds': 45
                                },
                                'securityContext': {
                                    'readOnlyRootFilesystem': True
                                },
                                'resources': ValueData(value=self.option_get('kubernetes.resources.loki-statefulset'),
                                                       disabled_if_none=True),
                            }],
                            'terminationGracePeriodSeconds': 4800,
                            'volumes': [{
                                'name': 'config',
                                'secret': {
                                    'secretName': self.object_name('config-secret'),
                                    'items': [{
                                        'key': 'loki.yaml',
                                        'path': 'loki.yaml',
                                    }]
                                }
                            },
                            KDataHelper_Volume.info(base_value={
                                'name': 'storage',
                            }, value=self.option_get('kubernetes.volumes.loki-data'))]
                        }
                    }
                }
            }, name=self.BUILDITEM_LOKI_STATEFULSET, source=self.SOURCE_NAME, instance=self.basename()),
        ])

        if self.option_get('enable.grafana') is not False:
            ret.extend(self._build_result_change(
                self.granana_config.build(self.granana_config.BUILD_SERVICE), 'grafana'))

        return ret

    def _build_result_change(self, items: Sequence[ObjectItem], name_prefix: str) -> Sequence[ObjectItem]:
        for o in items:
            if isinstance(o, Object):
                o.name = '{}-{}'.format(name_prefix, o.name)
                o.source = self.SOURCE_NAME
                o.instance = self.basename()
        return items

    def loki_configfile_get(self) -> str:
        if self.lokiconfigfile is None:
            configfile = self.option_get('config.loki_config')
            if configfile is None:
                configfile = LokiConfigFile()
            if isinstance(configfile, str):
                self.lokiconfigfile = configfile
            else:
                configfilerender = ConfigFileRenderMulti([
                    ConfigFileRender_Yaml(),
                    ConfigFileRender_RawStr()
                ])
                self.lokiconfigfile = configfilerender.render(configfile.get_value(self))
        return self.lokiconfigfile

    def promtail_configfile_get(self) -> str:
        if self.promtailconfigfile is None:
            configfile = self.option_get('config.promtail_config')
            if configfile is None:
                configfile = PromtailConfigFile(extensions=[
                    PromtailConfigFileExt_Kubernetes(),
                ])
            if isinstance(configfile, str):
                self.promtailconfigfile = configfile
            else:
                configfilerender = ConfigFileRenderMulti([
                    ConfigFileRender_Yaml(),
                    ConfigFileRender_RawStr()
                ])
                self.promtailconfigfile = configfilerender.render(configfile.get_value(self))
        return self.promtailconfigfile
