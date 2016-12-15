import os
from xml.etree import ElementTree
from intersection_features import get_model_features


CPU_MAP = "/usr/share/libvirt/cpu_map.xml"


def get_all_featurs_of_models(x86):
    def recursion_farther(models, model, features=[]):
        sub_models = model.findall("model")
        features = features + [feature.attrib["name"] for
                               feature in model.findall("feature")]
        if sub_models:
            model_name = sub_models[0].attrib["name"]
            sub = models[model_name]
            features = features + recursion_farther(models, sub, features)
        features = list(set(features).union())
        return features

    model_feature_map = {}
    models = dict(
        [(model.attrib["name"], model) for model in x86.findall("model")])
    for model in models.keys():
        model_feature_map[model] = recursion_farther(models, models[model])
    return model_feature_map


def get_featurs_and_models(path):
    bases = []
    models = {}
    if not os.path.isfile(path):
        return bases, models

    root = ElementTree.parse(path)
    x86 = [node for node in root.findall("arch")
           if node.attrib["name"] == "x86" ][0]

    bases = [feature.attrib["name"] for feature in x86.findall("feature")]
    models = get_all_featurs_of_models(x86)
    for model, v in models.items():
        print model, v

    return bases, models


def main():
    QEMU_BINARY = "qemu-system-x86_64  -enable-kvm"

    base_featurs, models = get_featurs_and_models(CPU_MAP)
    for model, ft in models.items():
        f = set(base_featurs + ft).union()
        f = " ".join(f)
        avaliabe = get_model_features(QEMU_BINARY, model, f)
        unavaliabe = list(set(ft) - set(avaliabe))
        if unavaliabe:
            print "\n" + "=" * 80
            print ("These features defined in libvirt for model %s "
                   "are not supported by qemu:" % model)
            print " " * 4 + ", ".join(unavaliabe)
        # else:
        #     print "All features of model %s are supported by qemu" % model

if __name__ == "__main__":
    main()
