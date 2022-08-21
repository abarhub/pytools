import unittest

from maven_dependancy import parse_output


def readLine(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


class MavenDendendancyCase(unittest.TestCase):
    def test_parse_output(self):
        lines = []
        lines = readLine('data_test/maven_dependancy_test1.txt')
        res = parse_output(lines)

        self.assertIsNotNone(res)
        self.assertEqual(1, len(res))
        self.assertEqual('org.springframework.samples', res[0].groupeId)
        self.assertEqual('spring-petclinic', res[0].artifactId)
        self.assertEqual('2.7.0-SNAPSHOT', res[0].version)
        self.assertEqual(16, len(res[0].dependancy))

        dep1 = res[0].dependancy[0]
        self.assertEqual('org.springframework.boot', dep1.groupeId)
        self.assertEqual('spring-boot-starter-actuator', dep1.artifactId)
        self.assertEqual('2.7.0', dep1.version)
        self.assertEqual('compile', dep1.scope)
        self.assertEqual(3, len(dep1.dependancy))

        dep1 = res[0].dependancy[0].dependancy[2]
        self.assertEqual('io.micrometer', dep1.groupeId)
        self.assertEqual('micrometer-core', dep1.artifactId)
        self.assertEqual('1.9.0', dep1.version)
        self.assertEqual('compile', dep1.scope)
        self.assertEqual(2, len(dep1.dependancy))

        dep1 = res[0].dependancy[7]
        self.assertEqual('com.h2database', dep1.groupeId)
        self.assertEqual('h2', dep1.artifactId)
        self.assertEqual('2.1.212', dep1.version)
        self.assertEqual('runtime', dep1.scope)
        self.assertEqual(0, len(dep1.dependancy))

        dep1 = res[0].dependancy[15]
        self.assertEqual('org.springframework.boot', dep1.groupeId)
        self.assertEqual('spring-boot-devtools', dep1.artifactId)
        self.assertEqual('2.7.0', dep1.version)
        self.assertEqual('compile', dep1.scope)
        self.assertEqual(2, len(dep1.dependancy))

        dep1 = res[0].dependancy[15].dependancy[0]
        self.assertEqual('org.springframework.boot', dep1.groupeId)
        self.assertEqual('spring-boot', dep1.artifactId)
        self.assertEqual('2.7.0', dep1.version)
        self.assertEqual('compile', dep1.scope)
        self.assertEqual(0, len(dep1.dependancy))

        dep1 = res[0].dependancy[15].dependancy[1]
        self.assertEqual('org.springframework.boot', dep1.groupeId)
        self.assertEqual('spring-boot-autoconfigure', dep1.artifactId)
        self.assertEqual('2.7.0', dep1.version)
        self.assertEqual('compile', dep1.scope)
        self.assertEqual(0, len(dep1.dependancy))



if __name__ == '__main__':
    unittest.main()
