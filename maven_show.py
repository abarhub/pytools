import subprocess
import sys
import xml.etree.ElementTree as ET


class MavenDependancy:

    def __init__(self, groupId, artifactId, version, scope):
        self.groupeId = groupId
        self.artifactId = artifactId
        self.version = version
        self.scope = scope

    def toString(self):
        s = self.groupeId + ':' + self.artifactId + ':' + self.version
        if self.scope != None:
            s += ':' + self.scope
        return s


class MavenPom:

    def __init__(self, id: MavenDependancy, parent: MavenDependancy | None, dependancy: list[MavenDependancy]):
        self.id = id
        self.dependancy = dependancy
        self.parent = parent

    def toString(self) -> str:
        s = self.id.toString()
        if self.parent is not None:
            s += ' (' + self.parent.toString() + ')'
        if self.dependancy is not None and len(self.dependancy) > 0:
            for dep in self.dependancy:
                s += '\n' + dep.toString()
        return s


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def execute_maven(pom) -> list[str]:
    param = ['mvn', '-f', pom, 'help:effective-pom']
    res = subprocess.run(param, shell=True, capture_output=True, )

    print("res:" + str(res))
    print("error:" + str(res.returncode != 0))
    if res.returncode != 0:
        eprint("output:" + res.stdout.decode('utf-8'))
        eprint("error:" + res.stderr.decode('utf-8'))
        exit(1)
    print("output:" + res.stdout.decode('utf-8'))

    lines = res.stdout.decode('utf-8').splitlines()
    return lines


def parse_output(lines: list[str]):
    debut = False
    xmlLine = []

    for line in lines:

        if line.startswith('Downloading from ') or line.startswith('Downloaded from '):
            continue

        if line.startswith('Effective POMs, after inheritance, interpolation, and profiles are applied:'):
            debut = True
            continue
        elif debut and line.startswith('[INFO] -------'):
            break

        if debut:
            xmlLine.append(line)

    if len(xmlLine) > 0 and xmlLine[0] == '':
        del xmlLine[0]

    return xmlLine


def getText(elt: ET.Element | None) -> str | None:
    if elt is None:
        return None
    else:
        return elt.text


def parseXmlEffectivePom(xmlLines: list[str]) -> MavenPom:
    root = ET.fromstring('\n'.join(xmlLines))
    namespaces = {'ns': 'http://maven.apache.org/POM/4.0.0'}
    parent = root.find("ns:parent", namespaces)
    if parent is not None:
        parentPom = MavenDependancy(getText(parent.find('ns:groupId', namespaces)),
                                    getText(parent.find('ns:artifactId', namespaces)),
                                    getText(parent.find('ns:version', namespaces)), None)
    else:
        parentPom = None

    id = MavenDependancy(getText(root.find('ns:groupId', namespaces)), getText(root.find('ns:artifactId', namespaces)),
                         getText(root.find('ns:version', namespaces)), None)

    depList = []
    dep = root.find("ns:dependencies", namespaces)
    if dep is not None:
        for dep2 in dep.findall('ns:dependency', namespaces):
            depends = MavenDependancy(getText(dep2.find('ns:groupId', namespaces)),
                                      getText(dep2.find('ns:artifactId', namespaces)),
                                      getText(dep2.find('ns:version', namespaces)),
                                      getText(dep2.find('ns:scope', namespaces)))
            depList.append(depends)

    pom = MavenPom(id, parentPom, depList)

    return pom


def getInfoPom(pom: str) -> MavenPom:
    lines = execute_maven(pom)
    xmlLines = parse_output(lines)

    # print("xml:" + '\n'.join(xmlLines))

    pom = parseXmlEffectivePom(xmlLines)
    return pom


def show_pom(pom: str):
    pom = getInfoPom(pom)

    print("pom", pom.toString())

    # print("parent", parent, root, parent.text)
    # model = root.find('ns:modelVersion', namespaces)
    # print("model", model, model.text)
    # print("child", root.find('modelVersion'))
    # for child in root:
    #     print(child.tag, child.attrib)
    # tree = etree.parse("data.xml")
    # for user in tree.xpath("/users/user/nom"):
    #     print(user.text)


def main(file):
    # listDependancyBasic(file)
    show_pom(file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        eprint('Error: missing file in argument')
        exit(1)
    main(sys.argv[1])
