#!/usr/bin/python

import argparse
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
    # for model, v in models.items():
    #     print model, v

    return bases, models


def main(args):
    base_featurs, models = get_featurs_and_models(CPU_MAP)

    probe_models = models.keys()
    if args.m:
        probe_models = args.m.split(",")
        probe_models_map = dict([(m.lower(), m) for m in probe_models])
        all_models_map  = dict([(m.lower(), m) for m in models.keys()])

        unsupport_m = set(probe_models_map.keys()) - set(all_models_map.keys())
        if unsupport_m:
            m = [probe_models_map[k] for k in unsupport_m]
            print 'libvirt does not support these models: "%s"' % ",".join(m)
            print 'please choose these models: "%s"' % ",".join(models)
            exit(1)
        probe_models = [all_models_map[m] for m in probe_models_map.keys()]

    for model in probe_models:
        ft = models[model]
        extra = []
        if args.f:
            extra = args.f.split(",")
        f = set(base_featurs + ft + extra).union()
        f = " ".join(f)

        avaliabe = get_model_features(args.b, model, f)
        unavaliabe = list(set(ft) - set(avaliabe))
        if unavaliabe:
            print "\n" + "=" * 80
            print ("These features defined in libvirt for model %s "
                   "are not supported by qemu:" % model)
            print " " * 4 + ", ".join(unavaliabe)
        else:
            if args.m:
                print "\n" + "=" * 80
                print ("All features of model %s defined in libvirt are "
                       "supported by qemu." % model)

        if args.f:
            features = ",".join(avaliabe)
            libvrt_unsupport = set(extra) - set(base_featurs + ft).union()
            qemu_unsupport = set(extra) - set(avaliabe)
            unsupport_msg = "**** %s does not support %s featurs:\n    %s"
            if libvrt_unsupport:
                print unsupport_msg % ("libvirt",  len(libvrt_unsupport),
                                       list(libvrt_unsupport))
            if qemu_unsupport:
                print unsupport_msg % ("qemu",  len(qemu_unsupport),
                                       list(qemu_unsupport))

if __name__ == "__main__":
    QEMU_BINARY = "qemu-system-x86_64"
    parser = argparse.ArgumentParser(
        description="find the intersection features of CPU model")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-m", "--model", type=str, default="", dest="m",
                        help='The models name of cpu, -m "Haswell, ivybridge"')
    parser.add_argument("-f", "--feature", type=str, default="", dest="f",
                        help='The features to be probed, -f "avx,sse"')
    parser.add_argument("-b", "--binary", type=str,
                        default=QEMU_BINARY, dest="b",
                        help='The models name of cpu, -m "Haswell, ivybridge"')
    args = parser.parse_args()

    main(args)
