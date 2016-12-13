import os
from xml.etree import ElementTree
from intersection_features import get_model_features


CPU_MAP = "/usr/share/libvirt/cpu_map.xml"


def get_featurs_and_models(path):
    bases = []
    models = {}
    if not os.path.isfile(path):
        return bases, models

    root = ElementTree.parse(path)
    x86 = [node for node in root.findall("arch")
           if node.attrib["name"] == "x86" ][0]

    bases = [feature.attrib["name"] for feature in x86.findall("feature")]
    models = dict([(model.attrib["name"],
                    [feature.attrib["name"]
                     for feature in model.findall("feature")])
                   for model in x86.findall("model")])

    return bases, models


def main():
    QEMU_BINARY = "qemu-system-x86_64  -enable-kvm"

    base_featurs, models = get_featurs_and_models(CPU_MAP)
    for model, ft in models.items():
        f = " ".join(base_featurs + ft)
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
