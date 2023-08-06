import re
import sys
import yaml


def gen_manifest(pod_name, version):
    manifest = {
        'apiVersion': 'serving.knative.dev/v1',
        'kind': 'Service',
        'metadata': {
            'name': pod_name,
            'namespace': 'default',
        },
        'spec': {
            'template': {
                'spec': {
                    'containers': [
                        {
                            'image': 'gcr.io/apt-phenomenon-243802/{}:{}'.format(pod_name, version),
                            'ports': [
                                {
                                    'containerPort': 5000,
                                },
                            ],
                            'livenessProbe': {
                                'httpGet': {
                                    'path': '/healthz',
                                },
                                'initialDelaySeconds': 3,
                                'periodSeconds': 5,
                            },
                            'readinessProbe': {
                                'httpGet': {
                                    'path': '/healthz',
                                },
                                'initialDelaySeconds': 3,
                                'periodSeconds': 5,
                                'failureThreshold': 3,
                                'timeoutSeconds': 60,
                            },
                        },
                    ],
                },
            },
        },
    }
    return yaml.dump(manifest)


def camel_to_kebab(name):
    out = re.sub(r'([a-z0-9]|(?=[A-Z]))([A-Z])', r'\1-\2', name)
    out = out.lower()
    if out[0] == '-':
        out = out[1:]
    return out


if __name__ == '__main__':
    bento = str(sys.argv[1])
    name, version = bento.split(':')
    pod_name = camel_to_kebab(name)
    print(gen_manifest(pod_name, version))
