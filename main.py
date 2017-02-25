import sqlite3
from farms import *
from edges import *
from stores import *


#to start osrm osrm-routed ../maps/new-york-latest.osrm

def create_db(db):
	"""run the sql file to create the db"""
	f = open('db_create.sql','r')
	sql = f.read()
	con = sqlite3.connect(db) #create the db
	cur = con.cursor()
	cur.executescript(sql)
	con.commit()


def main(db,farms,procs,stores):
	create_db(db)
	
	#import data
	print('Loading Bands into the DB...')
	import_bands(db)
	print('Loading Census Data into the DB...')
	import_tractvalues(db, 'input/ACS_10_SF4_B25077/ACS_10_SF4_B25077_with_ann.csv')
	
	print('Loading Processors into the DB...')
	import_proc(db,procs)
	print('Loading Stores into the DB...')
	import_store(db,stores)
	print('Loading Farms into the DB...')
	import_farms(db, farms,68,20)
	#import_farms(db, farms,36,10)

	#calculate edges
	print('Building Store Edges...')
	proc_edges(db)
	print('Building Farm Edges...')
	proc_edges(db, farms = True )
	print('DB Complete!')
	return


if __name__ == "__main__":
	#main('db/ag_networks.db','input/NASSnyc2010.036.tif.8033/cdl_tm_r_ny_2010_utm18.tif','input/Farm_Product_Dealer_Licenses_Currently_Issued.csv','input/Retail_Food_Stores.csv')
	main('db/test.db', 'input/test.tif', 'input/ptest.csv', 'input/stest.csv' )