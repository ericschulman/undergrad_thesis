import requests
import sqlite3
import json


#to start osrm osrm-routed ../maps/new-york-latest.osrm from the directory

def ps_edges(db):
	"""computes edge weights between stores and processors"""
	conn = sqlite3.connect(db)
	c = conn.cursor()

	c.execute("SELECT COUNT(*) FROM stores")
	storenum = c.fetchone()[0]
	c.execute("SELECT COUNT(*) FROM proc")
	procnum = c.fetchone()[0]

	for storeid in range(1,storenum+1):
		for procid in range(1,procnum+1): #may change this depending on RAM constraints
			c.execute("SELECT proc.procid, proc.lat, proc.lon, stores.storeid, stores.lat, stores.lon FROM proc, stores WHERE proc.procid=? AND stores.storeid=?",(procid,storeid,))
			row = c.fetchone()
			duration = routing(row[2],row[1],row[5],row[4])
			c.execute('INSERT INTO ps_edges VALUES (?,?,?,?)', (storeid,procid,0,duration,))
	conn.commit()
	return


def routing(lon0,lat0,lon1,lat1):
	"""wrapper for doing routing with OSRM"""
	req = "http://0.0.0.0:5000/route/v1/table/%s,%s;%s,%s"%(lon0,lat0,lon1,lat1)
	osrm_raw = requests.get(req)
	orsm =json.loads(osrm_raw.text)
	return orsm['routes'][0]['duration']



if __name__ == "__main__":
	ps_edges("db/test.db")
