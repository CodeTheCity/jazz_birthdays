import re
tests = ["Milt Jackson, vibraphone, piano, guitar, 1923 (d. October 9, 1999)", "Howard Johnson, alto sax, 1908 (d. December 28, 1991)","Sonny Greenwich, guitar, 1936", "Eiichi Hayashi, alto sax, 1960", "Yoshio Ikeda, bass, 1942", "Urs Leimgruber, saxophones, bass clarinet. 1952"]

for test in tests:
    m = re.search ("\(d\.(.*)\)", test)
    if m:
        print(m.groups())
