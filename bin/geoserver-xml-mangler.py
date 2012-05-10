#!/usr/bin/python
import sys
sys.path.append('/var/lib/geonode/src/GeoNodePy')
sys.path.append('/var/lib/geonode/src/GeoNodePy/geonode')

import local_settings
from lxml import etree

def usage(name, ret):
    print "USAGE:"
    print "  %s <install|template> <file> [<file2> ...]" % name
    sys.exit(ret)

if __name__ == '__main__':
    if len(sys.argv) < 3:
	usage(sys.argv[0], 3)

    if sys.argv[1] == 'install':
        db_passwd = local_settings.DATABASE_PASSWORD
    elif sys.argv[1] == 'template':
        db_passwd = 'DATABASE_PASSWORD'
    else:
        usage(sys.argv[0],3)

    for fid in range(2,len(sys.argv)):
        fname = sys.argv[fid]
        print "Processing [%s]" % fname
        doc = etree.parse(fname)
        if doc == None:
            print "an error occur during [%s] xml parsing" % fname
		
        matcs = doc.xpath("//dataStore/connectionParameters/entry[@key='passwd']");

        if len(matcs) > 1:
            print "wrong number of passwd tags into [%s] file" % fname
            sys.exit(1)
    
        elif len(matcs) == 1:
            matc = matcs[0] 
            matc.text = db_passwd
    
        else:
            matcs = doc.xpath("//dataStore/connectionParameters");
            if len(matcs) != 1:
                print "wrong number of connectionParameters tags into [%s] file" % fname
                sys.exit(1)
            matc = matcs[0] 
            newel = etree.SubElement(matc, "entry", key="passwd")
            newel.text = db_passwd
                
        try:
            f = file(fname, 'w')
        except:
            print "file [%s] not found" % fname
            sys.exit(1)

        f.write(etree.tostring(doc))
        f.close()
 
        del doc

    sys.exit(0)

