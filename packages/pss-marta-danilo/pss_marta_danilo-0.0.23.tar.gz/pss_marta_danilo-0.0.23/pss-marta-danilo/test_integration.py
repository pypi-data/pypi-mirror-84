import MySQLdb as sql
import random
import numpy
import pytest
import matplotlib.pyplot as plt
from main import get_im_from_db

def test_integration():
    image = []
    image2 = []
    try:
        # per far funzionare su gitlab usare questi valori
        # Host: mysql
        # User: runner
        # Password: Databasepss20/21
        # Database: assignment1
        # normalmente la porta è 3306
        #db = sql.connect(host="mysql", user="runner", passwd="Databasepss20/21", db="Assignment1")#noqa
        db=sql.connect(host="mysql", user="runner", passwd="Databasepss20/21", db="assignment1")# noqa
        print("connessione eseguita")
    except:
        pytest.fail("errore durante la connessione al db")
    try:
        cursor = db.cursor()
        indice = random.randint(1, 5)
        image = get_im_from_db(indice, "mysql")
        query = "SELECT percorso FROM metadata WHERE id =" + str(indice)
        cursor.execute(query)
        print("query eseguita")
        # results = cursor.fetchall()
        results = cursor.fetchone()
        image2 = plt.imread(str(results[0]))
        assert len(image) == len(image2)
        numpy.testing.assert_array_equal(image, image2)
    except:
        pytest.fail("errore durante la query di richiesta del percorso di un immagine")
