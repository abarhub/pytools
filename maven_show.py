import subprocess
import sys
import xml.etree.ElementTree as ET


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def execute_maven(pom):
    cmd = "mvn dependency:tree"
    param = ['cmd', '/C', 'echo', 'More output']
    param = ['cmd', '/C', 'mvn']
    param = ['mvn', '-f', pom, 'help:effective-pom']
    res = subprocess.run(param, shell=True, capture_output=True, )
    # stdout, stderr = process.communicate()

    # print("stdout:"+stdout)
    # print("stderr:" + stderr)
    print("res:" + str(res))
    print("error:" + str(res.returncode != 0))
    if res.returncode != 0:
        eprint("output:" + res.stdout.decode('utf-8'))
        eprint("error:" + res.stderr.decode('utf-8'))
        exit(1)
    print("output:" + res.stdout.decode('utf-8'))

    lines = res.stdout.decode('utf-8').splitlines()
    return lines


def parse_output(lines):
    project = ''
    dependancy = False
    dependancyList = []
    projectDependancy=[]
    debut=False
    fin=False
    xmlLine=[]

    for line in lines:

        if line.startswith('Effective POMs, after inheritance, interpolation, and profiles are applied:'):
            debut = True
            continue
        elif debut and line.startswith('[INFO] -------'):
            fin=True
            break

        if debut:
            xmlLine.append(line)

    if len(xmlLine)>0 and xmlLine[0]=='':
        del xmlLine[0]

    return xmlLine


def show_pom(pom):
    lines=execute_maven(pom)
    xmlLines=parse_output(lines)

    print("xml:"+'\n'.join(xmlLines))

    root = ET.fromstring('\n'.join(xmlLines))
    #tree = ET.parse('country_data.xml')
    #root = tree.getroot()
    namespaces = {'ns': 'http://maven.apache.org/POM/4.0.0'}
    tmp=root.find("ns:parent",namespaces)
    print("parent",tmp,root,tmp.text)
    model=root.find('ns:modelVersion',namespaces)
    print("model", model,model.text)
    # print("child", root.find('modelVersion'))
    for child in root:
        print(child.tag, child.attrib)
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
