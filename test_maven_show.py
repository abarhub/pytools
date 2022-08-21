import unittest
from unittest import TestCase

from maven_show import parse_output, parseXmlEffectivePom


def readLine(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


class Test(TestCase):

    def test_parse_output(self):
        lines = []
        lines = readLine('data_test/maven_show_test1.txt')

        xmlLines = parse_output(lines)

        self.assertIsNotNone(xmlLines)
        self.assertEqual(7078, len(xmlLines))

        self.assertEqual('<?xml version="1.0" encoding="Cp1252"?>', xmlLines[0])
        self.assertEqual('<!-- ====================================================================== -->', xmlLines[1])

        self.assertEqual('  </profiles>', xmlLines[7074])
        self.assertEqual('</project>', xmlLines[7075])
        self.assertEqual('', xmlLines[7076])
        self.assertEqual('', xmlLines[7077])

    def test_parse_xml_effective_pom(self):
        lines = readLine('data_test/maven_show_test1.txt')
        xmlLines = parse_output(lines)

        pom = parseXmlEffectivePom(xmlLines)

        self.assertIsNotNone(pom)
        self.assertIsNotNone(pom.id)
        self.assertEqual('org.springframework.samples', pom.id.groupeId)
        self.assertEqual('spring-petclinic', pom.id.artifactId)
        self.assertEqual('2.7.0-SNAPSHOT', pom.id.version)
        self.assertIsNotNone(pom.parent)
        self.assertEqual('org.springframework.boot', pom.parent.groupeId)
        self.assertEqual('spring-boot-starter-parent', pom.parent.artifactId)
        self.assertEqual('2.7.0', pom.parent.version)

        self.assertIsNotNone(pom.dependancy)
        self.assertEqual(16, len(pom.dependancy))

        dep = pom.dependancy[0]
        self.assertEqual('org.springframework.boot', dep.groupeId)
        self.assertEqual('spring-boot-starter-actuator', dep.artifactId)
        self.assertEqual('2.7.0', dep.version)
        self.assertEqual('compile', dep.scope)

        dep = pom.dependancy[7]
        self.assertEqual('com.h2database', dep.groupeId)
        self.assertEqual('h2', dep.artifactId)
        self.assertEqual('2.1.212', dep.version)
        self.assertEqual('runtime', dep.scope)

        dep = pom.dependancy[15]
        self.assertEqual('org.springframework.boot', dep.groupeId)
        self.assertEqual('spring-boot-devtools', dep.artifactId)
        self.assertEqual('2.7.0', dep.version)
        self.assertEqual('compile', dep.scope)


if __name__ == '__main__':
    unittest.main()
