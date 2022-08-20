import subprocess
import sys
from xml.etree import ElementTree


class maven_obj:
    def __init__(self, groupId, artifactId, version, parent, dependancy, scope):
        self.groupeId = groupId
        self.artifactId = artifactId
        self.version = version
        self.dependancy = dependancy
        self.parent = parent
        self.scope = scope

    def toString(self, decalage=0):
        s = self.groupeId + ':' + self.artifactId + ':' + self.version
        if self.scope != None:
            s += ':' + self.scope
        for child in self.dependancy:
            s += '\n' + '  ' * (decalage + 1) + child.toString(decalage + 1)
        return s


def listDependancyBasic(pomFile):
    # POM_FILE = "y16ra/test_pom.xml"  # replace your path
    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}

    tree = ElementTree.parse(pomFile)
    root = tree.getroot()

    deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
    for d in deps:
        artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
        version = d.find("xmlns:version", namespaces=namespaces)
        print(artifactId.text + '\t' + version.text)


def dependancyTree(pom):
    cmd = "mvn dependency:tree"
    param = ['cmd', '/C', 'echo', 'More output']
    param = ['cmd', '/C', 'mvn']
    param = ['mvn', '-f', pom, 'dependency:tree']
    res = subprocess.run(param, shell=True, capture_output=True)
    # stdout, stderr = process.communicate()

    # print("stdout:"+stdout)
    # print("stderr:" + stderr)
    print("res:" + str(res))
    print("error:" + str(res.returncode != 0))
    print("output:" + res.stdout.decode('utf-8'))

    lines = res.stdout.decode('utf-8').splitlines()

    project = ''
    dependancy = False
    dependancyList = []

    for line in lines:

        if line.startswith('Downloading from ') or line.startswith('Downloaded from '):
            continue

        if line.startswith('[INFO] '):
            line = line[7:]

        if line.startswith('Building '):
            project = line[8:]
            if project.endswith(']'):
                pos = project.rfind('[')
                if pos >= 0:
                    line = project[:pos - 1]
            project = project.strip()
            print("project:" + project)

        if line.find('--- maven-dependency-plugin') >= 0:
            dependancy = True
            dependancyList = []
            continue
        elif dependancy and line.startswith('---'):
            dependancy = False

        if dependancy:
            dependancyList.append(line)

    depmap = None
    last = None
    lastno = -1
    for line in dependancyList:
        if line.startswith('---'):
            break
        elif line.startswith('+') or line.startswith('|') or line.startswith('\\') or (
                line.startswith(' ') and line.find('- ') >= 0):
            i = line.find('+-')
            if i == -1:
                i = line.find('\\-')
            if i >= 0:
                line = line[i + 2:].strip()
                nb = int(i / 3)
            else:
                nb = 0
            obj = line.split(':')
            scope = ''
            if len(obj) >= 5:
                scope = obj[4]
            depmap2 = maven_obj(obj[0], obj[1], obj[3], None, [], scope)
            if nb == lastno:
                depmap2.parent = last.parent
                last.parent.dependancy.append(depmap2)
            elif nb > lastno:
                depmap2.parent = last
                last.dependancy.append(depmap2)
            elif nb < lastno:
                parent = last.parent
                for i in range(lastno - nb):
                    parent = parent.parent
                depmap2.parent = parent
                parent.dependancy.append(depmap2)
                # depmap2.parent = last.parent
                # for i in range(lastno-nb):
                #    depmap2.parent =depmap2.parent.parent
            lastno = nb
            last = depmap2
        elif depmap == None:
            obj = line.split(':')
            depmap = maven_obj(obj[0], obj[1], obj[3], None, [], None)
            last = depmap
            lastno = -1

    print('project:' + project)
    print('dependancy:' + str(dependancyList))
    print('depmap:' + str(depmap.__dict__))
    print('depmap.toString:' + depmap.toString())


def main(file):
    # listDependancyBasic(file)
    dependancyTree(file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Error: missing file in argument')
        exit(1)
    main(sys.argv[1])
